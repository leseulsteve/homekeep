"""Tests for derived health and adaptive interval helpers."""

from __future__ import annotations

import unittest
from datetime import timedelta

from custom_components.homekeep.health import (
    adaptive_interval_after_non_completion_action,
    apply_completion_to_state,
    area_health,
    home_health,
    priority_staleness,
    projected_impact,
    should_fire_area_health_changed,
    update_adaptive_interval,
    utc_datetime,
)
from custom_components.homekeep.models import ChoreDefinition, ChoreState
from custom_components.homekeep.storage import (
    dump_store_dict,
    load_store_dict,
)


def chore_data(**overrides: object) -> dict:
    data = {
        "name": "Test chore",
        "area_id": "kitchen",
        "group_id": "surfaces",
        "base_interval_days": 10,
        "min_interval_days": 3,
        "max_interval_days": 14,
        "estimated_minutes": 5,
        "energy": "normal",
        "visibility": "high",
        "health_weight": 1.0,
        "variants": {
            "tiny": {"label": "Tiny", "credit": 0.5},
            "normal": {"label": "Normal", "credit": 1.0},
            "deep": {"label": "Deep", "credit": 1.5},
        },
        "pairs_with": [],
        "enabled": True,
    }
    data.update(overrides)
    return data


class HealthTest(unittest.TestCase):
    def test_health_recomputes_from_durable_state_after_cache_loss(self) -> None:
        chores = {
            "empty_compost": ChoreDefinition.from_dict(
                "empty_compost",
                chore_data(
                    name="Empty compost",
                    group_id="trash",
                    base_interval_days=2,
                    min_interval_days=1,
                    max_interval_days=4,
                    estimated_minutes=2,
                    health_weight=1.4,
                ),
            ),
            "wipe_kitchen_counters": ChoreDefinition.from_dict(
                "wipe_kitchen_counters",
                chore_data(name="Wipe kitchen counters", health_weight=1.1),
            ),
        }
        now = utc_datetime(2026, 6, 21)
        raw = {
            "version": 2,
            "chores": {chore_id: chore.to_dict() for chore_id, chore in chores.items()},
            "states": {
                chore_id: ChoreState.new_for_chore(chore).to_dict()
                for chore_id, chore in chores.items()
            },
            "completions": [],
            "sessions": {},
            "recommendations": {},
            "calendar_context": {},
            "user_preference_stats": {},
            "idempotency_records": {},
        }
        raw["states"]["empty_compost"]["last_completed_at"] = "2026-06-17T00:00:00+00:00"
        raw["states"]["empty_compost"]["adaptive_interval_days"] = 2
        raw["states"]["empty_compost"]["next_due_at"] = "2026-06-19T00:00:00+00:00"
        raw["states"]["empty_compost"]["cached_staleness_score"] = 0

        store = load_store_dict(raw, now=now)
        before_dump = dump_store_dict(store)
        recomputed = home_health(store.chores, store.states, now)
        restarted = load_store_dict(before_dump, now=now)

        self.assertEqual(
            home_health(restarted.chores, restarted.states, now),
            recomputed,
        )
        self.assertNotIn(
            "cached_staleness_score", before_dump["states"]["empty_compost"]
        )

    def test_completion_then_restart_recomputes_home_and_area_health(self) -> None:
        chore = ChoreDefinition.from_dict("test_chore", chore_data())
        initial = ChoreState(
            chore_id=chore.id,
            last_completed_at=utc_datetime(2026, 5, 1),
            adaptive_interval_days=10,
            next_due_at=utc_datetime(2026, 5, 11),
        )
        now = utc_datetime(2026, 6, 21)
        completed = apply_completion_to_state(chore, initial, now, "normal")
        raw = {
            "version": 2,
            "chores": {chore.id: chore.to_dict()},
            "states": {chore.id: completed.to_dict()},
            "completions": [],
            "sessions": {},
            "recommendations": {},
            "calendar_context": {},
            "user_preference_stats": {},
            "idempotency_records": {},
        }

        restarted = load_store_dict(raw, now=now)

        self.assertEqual(home_health(restarted.chores, restarted.states, now), 100.0)
        self.assertEqual(
            area_health(restarted.chores, restarted.states, now, "kitchen"), 100.0
        )

    def test_adaptive_interval_clamps_to_min_after_frequent_completions(self) -> None:
        chore = ChoreDefinition.from_dict("test_chore", chore_data())
        state = ChoreState(
            chore_id=chore.id,
            last_completed_at=utc_datetime(2026, 6, 20),
            adaptive_interval_days=3,
            next_due_at=None,
        )

        updated = update_adaptive_interval(
            chore, state, utc_datetime(2026, 6, 21), train=True
        )

        self.assertEqual(updated, 3)

    def test_adaptive_interval_clamps_to_max_after_late_completion(self) -> None:
        chore = ChoreDefinition.from_dict("test_chore", chore_data())
        state = ChoreState(
            chore_id=chore.id,
            last_completed_at=utc_datetime(2026, 1, 1),
            adaptive_interval_days=14,
            next_due_at=None,
        )

        updated = update_adaptive_interval(
            chore, state, utc_datetime(2026, 6, 21), train=True
        )

        self.assertEqual(updated, 14)

    def test_first_completion_uses_definition_base_interval(self) -> None:
        chore = ChoreDefinition.from_dict("test_chore", chore_data())
        state = ChoreState.new_for_chore(chore)

        self.assertEqual(
            update_adaptive_interval(chore, state, utc_datetime(2026, 6, 21)),
            10,
        )

    def test_skip_snooze_dismiss_and_cancel_do_not_train_interval(self) -> None:
        chore = ChoreDefinition.from_dict("test_chore", chore_data())
        state = ChoreState(
            chore_id=chore.id,
            last_completed_at=utc_datetime(2026, 6, 1),
            adaptive_interval_days=8,
            next_due_at=None,
        )

        for action in ("skip", "snooze", "dismiss", "cancel"):
            self.assertEqual(
                adaptive_interval_after_non_completion_action(state, action),
                8,
            )
        self.assertEqual(
            update_adaptive_interval(
                chore, state, utc_datetime(2026, 6, 21), train=False
            ),
            8,
        )

    def test_tiny_completion_sets_next_due_but_does_not_train_interval(self) -> None:
        chore = ChoreDefinition.from_dict("test_chore", chore_data())
        completed_at = utc_datetime(2026, 6, 21)
        state = ChoreState(
            chore_id=chore.id,
            last_completed_at=utc_datetime(2026, 6, 1),
            adaptive_interval_days=8,
            next_due_at=None,
            snoozed_until=completed_at + timedelta(hours=1),
        )

        updated = apply_completion_to_state(chore, state, completed_at, "tiny")

        self.assertEqual(updated.adaptive_interval_days, 8)
        self.assertEqual(updated.next_due_at, completed_at + timedelta(days=4))
        self.assertIsNone(updated.snoozed_until)

    def test_normal_and_deep_completion_train_interval_and_set_next_due(self) -> None:
        chore = ChoreDefinition.from_dict("test_chore", chore_data())
        completed_at = utc_datetime(2026, 6, 21)
        state = ChoreState(
            chore_id=chore.id,
            last_completed_at=utc_datetime(2026, 6, 11),
            adaptive_interval_days=8,
            next_due_at=None,
        )

        normal = apply_completion_to_state(chore, state, completed_at, "normal")
        deep = apply_completion_to_state(chore, state, completed_at, "deep")

        self.assertEqual(normal.adaptive_interval_days, 8.6)
        self.assertEqual(normal.next_due_at, completed_at + timedelta(days=8.6))
        self.assertEqual(deep.adaptive_interval_days, 8.6)
        self.assertEqual(deep.next_due_at, completed_at + timedelta(days=12.9))

    def test_priority_staleness_projected_impact_and_event_thresholds(self) -> None:
        chore = ChoreDefinition.from_dict("test_chore", chore_data())
        now = utc_datetime(2026, 6, 21)
        state = ChoreState(
            chore_id=chore.id,
            last_completed_at=utc_datetime(2026, 5, 1),
            adaptive_interval_days=10,
            next_due_at=utc_datetime(2026, 5, 11),
        )

        self.assertGreater(priority_staleness(chore, state, now), 100)
        self.assertEqual(projected_impact(chore, state, now), 100)
        self.assertTrue(should_fire_area_health_changed(75, 82))
        self.assertTrue(should_fire_area_health_changed(82, 70))
        self.assertFalse(should_fire_area_health_changed(82, 85))
        self.assertFalse(
            should_fire_area_health_changed(82, 70, startup_or_rebuild=True)
        )
        self.assertFalse(should_fire_area_health_changed(None, 70))


if __name__ == "__main__":
    unittest.main()
