"""Tests for deterministic Recommendation Engine V1."""

from __future__ import annotations

import unittest
from datetime import timedelta

from custom_components.homekeep.health import apply_completion_to_state, utc_datetime
from custom_components.homekeep.history import context_bucket, history_fit_score
from custom_components.homekeep.models import ChoreDefinition, ChoreState
from custom_components.homekeep.recommendations import (
    RecommendationEngine,
    RecommendationError,
    _calendar_context_score,
    context_fingerprint,
)
from custom_components.homekeep.storage import HomekeepStore


def chore_data(
    name: str,
    *,
    area_id: str = "kitchen",
    minutes: int = 5,
    energy: str = "normal",
    weight: float = 1.0,
) -> dict:
    return {
        "name": name,
        "area_id": area_id,
        "group_id": "default",
        "base_interval_days": 7,
        "min_interval_days": 3,
        "max_interval_days": 14,
        "estimated_minutes": minutes,
        "energy": energy,
        "visibility": "high",
        "health_weight": weight,
        "variants": {"normal": {"label": name, "credit": 1.0}},
        "pairs_with": [],
        "enabled": True,
    }


def make_store() -> HomekeepStore:
    chores = {
        chore_id: ChoreDefinition.from_dict(chore_id, data)
        for chore_id, data in {
            "empty_compost": chore_data("Empty compost", minutes=2, energy="low"),
            "wipe_counters": chore_data("Wipe counters", minutes=5),
            "clean_sink": chore_data("Clean sink", area_id="bathroom", minutes=6),
            "vacuum_hall": chore_data("Vacuum hall", area_id="hall", minutes=12, energy="high"),
        }.items()
    }
    now = utc_datetime(2026, 6, 21, 9)
    states = {
        chore_id: apply_completion_to_state(
            chore,
            ChoreState.new_for_chore(chore),
            now - timedelta(days=20 if chore_id != "vacuum_hall" else 3),
            "normal",
        )
        for chore_id, chore in chores.items()
    }
    return HomekeepStore(chores=chores, states=states)


class RecommendationEngineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.now = utc_datetime(2026, 6, 21, 9)
        self.store = make_store()
        self.engine = RecommendationEngine(self.store)

    def test_payload_shape_and_stable_recommendation_ids(self) -> None:
        result = self.engine.generate_smart_chore_list(
            now=self.now,
            time_budget_minutes=10,
            energy_level="normal",
            goal="quick_wins",
            area_id="kitchen",
        )
        again = self.engine.generate_smart_chore_list(
            now=self.now,
            time_budget_minutes=10,
            energy_level="normal",
            goal="quick_wins",
            area_id="kitchen",
        )

        self.assertEqual(result["snapshot_id"], again["snapshot_id"])
        self.assertEqual(
            result["best_single_chore"]["recommendation_id"],
            again["best_single_chore"]["recommendation_id"],
        )
        self.assertEqual(result["recommendation_mode"], "ready_now")
        self.assertIsNotNone(result["best_bundle"])
        self.assertIsNotNone(result["best_single_chore"])
        self.assertIsNotNone(result["easiest_chore"])
        self.assertLessEqual(len(result["alternates"]), 3)

        recommendation = result["best_single_chore"]
        self.assertEqual(
            set(recommendation),
            {
                "recommendation_id",
                "kind",
                "title",
                "estimated_minutes",
                "chore_items",
                "projected_impact",
                "reason",
                "score",
                "source_snapshot_id",
                "expires_at",
            },
        )
        self.assertIsNone(recommendation["chore_items"][0]["session_item_id"])
        self.assertTrue(recommendation["reason"].startswith("Reason: "))
        self.assertGreaterEqual(recommendation["score"], 0)
        self.assertLessEqual(recommendation["score"], 100)

        snapshot = self.store.recommendations[result["snapshot_id"]]
        self.assertEqual(snapshot["materialized_session_id"], None)
        self.assertEqual(snapshot["context_fingerprint"][:7], "ctx:v1:")
        self.assertTrue(snapshot["context_bucket"].startswith("mode=ready_now|"))

    def test_context_fingerprint_normalizes_lists_and_ignores_volatile_fields(self) -> None:
        payload = {
            "schema_version": 1,
            "recommendation_mode": "ready_now",
            "target_time_window": None,
            "time_budget_minutes": 10,
            "energy_level": "normal",
            "goal": "quick_wins",
            "area_id": "kitchen",
            "mood": None,
            "calendar_context_id": None,
            "calendar_context_version": None,
            "chore_definition_version": "v1",
            "enabled_chore_ids": ["b", "a"],
            "home_assistant_area_ids": ["kitchen", "bathroom"],
            "user_id": None,
            "created_at": "ignored",
        }
        reordered = dict(payload)
        reordered["enabled_chore_ids"] = ["a", "b"]
        reordered["created_at"] = "also ignored"

        self.assertEqual(context_fingerprint(payload), context_fingerprint(reordered))
        changed = dict(payload)
        changed["energy_level"] = "low"
        self.assertNotEqual(context_fingerprint(payload), context_fingerprint(changed))

    def test_sparse_history_falls_back_to_neutral_then_broader_bucket(self) -> None:
        bucket = context_bucket(
            recommendation_mode="ready_now",
            when=self.now,
            energy_level="normal",
            goal="quick_wins",
            area_id="kitchen",
            mood="unknown",
        )
        self.assertEqual(
            history_fit_score([], bucket=bucket, chore_id="empty_compost", area_id="kitchen"),
            50.0,
        )

        broad_bucket = bucket.replace("area=selected:kitchen", "area=any")
        stats = [
            {
                "user_id": None,
                "context_bucket": broad_bucket,
                "chore_id": "empty_compost",
                "area_id": "kitchen",
                "accepted_count": 2,
                "completed_count": 2,
                "skipped_count": 0,
                "snoozed_count": 0,
            }
        ]

        self.assertEqual(
            history_fit_score(
                stats, bucket=bucket, chore_id="empty_compost", area_id="kitchen"
            ),
            100.0,
        )

    def test_expired_snapshot_cannot_start_recommendation(self) -> None:
        result = self.engine.generate_smart_chore_list(now=self.now)
        recommendation_id = result["best_single_chore"]["recommendation_id"]

        with self.assertRaisesRegex(RecommendationError, "expired"):
            self.engine.start_recommendation(
                result["snapshot_id"],
                recommendation_id,
                now=self.now + timedelta(minutes=31),
            )
        self.assertEqual(len(self.store.sessions), 0)

    def test_fresh_snapshot_materializes_and_copies_fingerprint(self) -> None:
        result = self.engine.generate_smart_chore_list(now=self.now)
        snapshot = self.store.recommendations[result["snapshot_id"]]
        recommendation_id = result["best_single_chore"]["recommendation_id"]

        session = self.engine.start_recommendation(
            result["snapshot_id"],
            recommendation_id,
            user_id="person.steve",
            now=self.now + timedelta(minutes=1),
        )

        stored_session = self.store.sessions[session["session_id"]]
        self.assertEqual(snapshot["materialized_session_id"], session["session_id"])
        self.assertEqual(
            stored_session["context_fingerprint"],
            snapshot["context_fingerprint"],
        )
        self.assertIsNotNone(session["items"][0]["session_item_id"])

    def test_materialized_session_infers_missing_setup_fields(self) -> None:
        result = self.engine.generate_smart_chore_list(now=self.now)
        recommendation = result["easiest_chore"]

        session = self.engine.start_recommendation(
            result["snapshot_id"],
            recommendation["recommendation_id"],
            now=self.now + timedelta(minutes=1),
        )

        stored_session = self.store.sessions[session["session_id"]]
        self.assertEqual(stored_session["mode"], "quick_wins")
        self.assertEqual(
            stored_session["time_budget_minutes"],
            recommendation["estimated_minutes"],
        )
        self.assertEqual(
            stored_session["energy_level"],
            self.store.chores[recommendation["chore_items"][0]["chore_id"]].energy,
        )

    def test_recommendations_use_learned_duration_samples(self) -> None:
        self.store.states["empty_compost"] = ChoreState(
            chore_id="empty_compost",
            last_completed_at=self.store.states["empty_compost"].last_completed_at,
            adaptive_interval_days=self.store.states[
                "empty_compost"
            ].adaptive_interval_days,
            next_due_at=self.store.states["empty_compost"].next_due_at,
            duration_samples_minutes=[9, 11, 10],
        )

        result = self.engine.generate_smart_chore_list(
            now=self.now,
            time_budget_minutes=10,
            include_alternates=True,
        )
        compost_item = next(
            item
            for rec in [
                result["best_bundle"],
                result["best_single_chore"],
                result["easiest_chore"],
                *result["alternates"],
            ]
            if rec
            for item in rec["chore_items"]
            if item["chore_id"] == "empty_compost"
        )

        self.assertEqual(compost_item["estimated_minutes"], 10)

    def test_recommendations_shorten_learned_duration_for_low_mood(self) -> None:
        self.store.states["empty_compost"] = ChoreState(
            chore_id="empty_compost",
            last_completed_at=self.store.states["empty_compost"].last_completed_at,
            adaptive_interval_days=self.store.states[
                "empty_compost"
            ].adaptive_interval_days,
            next_due_at=self.store.states["empty_compost"].next_due_at,
            duration_samples_minutes=[9, 11, 10],
        )

        result = self.engine.generate_smart_chore_list(
            now=self.now,
            time_budget_minutes=10,
            mood="low",
            include_alternates=True,
        )
        compost_item = next(
            item
            for rec in [
                result["best_bundle"],
                result["best_single_chore"],
                result["easiest_chore"],
                *result["alternates"],
            ]
            if rec
            for item in rec["chore_items"]
            if item["chore_id"] == "empty_compost"
        )

        self.assertEqual(compost_item["estimated_minutes"], 8)

    def test_recommendations_can_expand_learned_duration_for_high_readiness(self) -> None:
        self.store.states["empty_compost"] = ChoreState(
            chore_id="empty_compost",
            last_completed_at=self.store.states["empty_compost"].last_completed_at,
            adaptive_interval_days=self.store.states[
                "empty_compost"
            ].adaptive_interval_days,
            next_due_at=self.store.states["empty_compost"].next_due_at,
            duration_samples_minutes=[9, 11, 10],
        )

        result = self.engine.generate_smart_chore_list(
            now=self.now,
            time_budget_minutes=15,
            energy_level="high",
            include_alternates=True,
        )
        compost_item = next(
            item
            for rec in [
                result["best_bundle"],
                result["best_single_chore"],
                result["easiest_chore"],
                *result["alternates"],
            ]
            if rec
            for item in rec["chore_items"]
            if item["chore_id"] == "empty_compost"
        )

        self.assertEqual(compost_item["estimated_minutes"], 12)

    def test_calendar_context_string_guesses_include_french_chore_terms(self) -> None:
        calendar_context = {
            "has_guests_soon": True,
            "trash_day_tomorrow": True,
        }
        guest_prep = ChoreDefinition.from_dict(
            "salle_de_bain",
            chore_data("Nettoyer la salle de bain", area_id="salle_de_bain"),
        )
        trash = ChoreDefinition.from_dict(
            "poubelles",
            chore_data("Sortir les poubelles et le recyclage", area_id="garage"),
        )

        self.assertEqual(_calendar_context_score(guest_prep, calendar_context), 80.0)
        self.assertEqual(_calendar_context_score(trash, calendar_context), 85.0)


if __name__ == "__main__":
    unittest.main()
