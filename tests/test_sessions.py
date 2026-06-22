"""Tests for Chore Session lifecycle behavior."""

from __future__ import annotations

import unittest
from datetime import timedelta

from custom_components.homekeep.health import utc_datetime
from custom_components.homekeep.models import ChoreDefinition, ChoreState
from custom_components.homekeep.sessions import SessionEngine, SessionLifecycleError
from custom_components.homekeep.storage import HomekeepStore


def chore_data(name: str, area_id: str = "kitchen") -> dict:
    return {
        "name": name,
        "area_id": area_id,
        "group_id": "surfaces",
        "base_interval_days": 7,
        "min_interval_days": 3,
        "max_interval_days": 14,
        "estimated_minutes": 5,
        "energy": "normal",
        "visibility": "high",
        "health_weight": 1.0,
        "variants": {
            "tiny": {"label": f"Tiny {name}", "credit": 0.5},
            "normal": {"label": name, "credit": 1.0},
            "deep": {"label": f"Deep {name}", "credit": 1.5},
        },
        "pairs_with": [],
        "enabled": True,
    }


def make_store() -> HomekeepStore:
    chores = {
        chore_id: ChoreDefinition.from_dict(chore_id, data)
        for chore_id, data in {
            "wipe_counters": chore_data("Wipe counters"),
            "empty_compost": chore_data("Empty compost"),
            "bonus_sink": chore_data("Clean sink", "bathroom"),
        }.items()
    }
    states = {
        chore_id: ChoreState.new_for_chore(chore)
        for chore_id, chore in chores.items()
    }
    return HomekeepStore(chores=chores, states=states)


class DeterministicIds:
    def __init__(self) -> None:
        self.counts: dict[str, int] = {}

    def __call__(self, prefix: str) -> str:
        self.counts[prefix] = self.counts.get(prefix, 0) + 1
        return f"{prefix}_{self.counts[prefix]}"


class SessionLifecycleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.store = make_store()
        self.engine = SessionEngine(self.store, id_factory=DeterministicIds())
        self.now = utc_datetime(2026, 6, 21, 9)

    def start_two_item_session(self) -> dict:
        return self.engine.start_session(
            ["wipe_counters", "empty_compost"],
            started_at=self.now,
            started_by="person.steve",
            participants=["person.steve", "person.alex"],
        )

    def test_start_pause_and_disallowed_terminal_transition(self) -> None:
        session = self.start_two_item_session()

        paused = self.engine.pause_session(session["session_id"])
        self.assertEqual(paused["status"], "paused")

        ended = self.engine.end_session(
            session["session_id"],
            status="cancelled",
            now=self.now + timedelta(minutes=5),
        )
        self.assertEqual(ended["status"], "cancelled")

        with self.assertRaisesRegex(SessionLifecycleError, "only active"):
            self.engine.pause_session(session["session_id"])

    def test_complete_validates_participants_and_defaults_started_by(self) -> None:
        session = self.start_two_item_session()
        item = session["items"][0]

        with self.assertRaisesRegex(SessionLifecycleError, "participant"):
            self.engine.complete_chore(
                item["chore_id"],
                session_id=session["session_id"],
                session_item_id=item["session_item_id"],
                completed_by="person.someone_else",
                completed_at=self.now,
            )

        result = self.engine.complete_chore(
            item["chore_id"],
            session_id=session["session_id"],
            session_item_id=item["session_item_id"],
            completed_at=self.now,
        )

        stored_item = self.store.sessions[session["session_id"]]["items"][0]
        self.assertEqual(result["completed_by"], "person.steve")
        self.assertEqual(stored_item["completed_by"], "person.steve")
        self.assertEqual(self.store.completions[0].completed_by, "person.steve")

    def test_duplicate_complete_same_item_creates_one_completion(self) -> None:
        session = self.start_two_item_session()
        item = session["items"][0]

        first = self.engine.complete_chore(
            item["chore_id"],
            session_id=session["session_id"],
            session_item_id=item["session_item_id"],
            completed_at=self.now,
        )
        second = self.engine.complete_chore(
            item["chore_id"],
            session_id=session["session_id"],
            session_item_id=item["session_item_id"],
            completed_at=self.now + timedelta(seconds=1),
        )

        self.assertEqual(first["completion_id"], "completion_1")
        self.assertEqual(second["completion_id"], "completion_1")
        self.assertTrue(second["duplicate"])
        self.assertEqual(len(self.store.completions), 1)

    def test_session_item_duration_trains_learned_estimate(self) -> None:
        session = self.start_two_item_session()
        first = session["items"][0]
        second = session["items"][1]

        self.engine.complete_chore(
            first["chore_id"],
            session_id=session["session_id"],
            session_item_id=first["session_item_id"],
            completed_at=self.now + timedelta(minutes=8),
        )

        stored_session = self.store.sessions[session["session_id"]]
        self.assertEqual(
            self.store.states[first["chore_id"]].duration_samples_minutes,
            [8],
        )
        self.assertEqual(stored_session["items"][1]["status"], "active")
        self.assertEqual(
            stored_session["items"][1]["started_at"],
            (self.now + timedelta(minutes=8)).isoformat(),
        )

        self.engine.complete_chore(
            second["chore_id"],
            session_id=session["session_id"],
            session_item_id=second["session_item_id"],
            completed_at=self.now + timedelta(minutes=13),
        )

        self.assertEqual(
            self.store.states[second["chore_id"]].duration_samples_minutes,
            [5],
        )
        self.assertIsNone(stored_session["current_chore"])

    def test_request_id_idempotency_returns_stored_result(self) -> None:
        first = self.engine.start_session(
            ["wipe_counters"],
            started_at=self.now,
            request_id="abc",
        )
        second = self.engine.start_session(
            ["empty_compost"],
            started_at=self.now + timedelta(minutes=1),
            request_id="abc",
        )

        self.assertEqual(first, second)
        self.assertEqual(len(self.store.sessions), 1)

        paused = self.engine.pause_session(
            first["session_id"],
            now=self.now + timedelta(minutes=2),
            request_id="same-id",
        )
        self.assertEqual(paused["status"], "paused")
        self.assertEqual(len(self.store.idempotency_records), 2)

    def test_skip_then_complete_same_item_is_rejected(self) -> None:
        session = self.start_two_item_session()
        item = session["items"][0]

        skipped = self.engine.skip_chore(
            item["chore_id"],
            session_id=session["session_id"],
            session_item_id=item["session_item_id"],
        )

        self.assertEqual(skipped["status"], "skipped")
        with self.assertRaisesRegex(SessionLifecycleError, "no longer completable"):
            self.engine.complete_chore(
                item["chore_id"],
                session_id=session["session_id"],
                session_item_id=item["session_item_id"],
            )

    def test_snooze_and_dismiss_do_not_create_completions(self) -> None:
        session = self.start_two_item_session()
        snooze_item = session["items"][0]
        dismiss_item = session["items"][1]

        snoozed = self.engine.snooze_chore(
            snooze_item["chore_id"],
            session_id=session["session_id"],
            session_item_id=snooze_item["session_item_id"],
            snooze_minutes=15,
            now=self.now,
        )
        dismissed = self.engine.dismiss_chore(
            dismiss_item["chore_id"],
            session_id=session["session_id"],
            session_item_id=dismiss_item["session_item_id"],
            now=self.now,
            request_id="dismiss-1",
        )
        duplicate_dismiss = self.engine.dismiss_chore(
            dismiss_item["chore_id"],
            session_id=session["session_id"],
            session_item_id=dismiss_item["session_item_id"],
            now=self.now + timedelta(minutes=1),
            request_id="dismiss-1",
        )

        self.assertEqual(snoozed["status"], "snoozed")
        self.assertEqual(dismissed, duplicate_dismiss)
        self.assertEqual(len(self.store.completions), 0)
        self.assertEqual(
            self.store.states[snooze_item["chore_id"]].snoozed_until,
            self.now + timedelta(minutes=15),
        )
        self.assertEqual(
            len(self.store.states[dismiss_item["chore_id"]].dismissal_events),
            1,
        )

        with self.assertRaisesRegex(SessionLifecycleError, "between 5 and 1440"):
            self.engine.snooze_chore(
                "wipe_counters",
                snooze_minutes=4,
                now=self.now,
            )

    def test_bonus_chore_lifecycle(self) -> None:
        session = self.start_two_item_session()
        for item in session["items"]:
            self.engine.complete_chore(
                item["chore_id"],
                session_id=session["session_id"],
                session_item_id=item["session_item_id"],
                completed_at=self.now,
            )

        pending = self.engine.end_session(
            session["session_id"],
            status="completed",
            offer_bonus_chore=True,
            bonus_chore_id="bonus_sink",
            now=self.now,
        )
        self.assertEqual(pending["status"], "bonus_pending")
        self.assertEqual(
            pending["bonus_chore_expires_at"],
            (self.now + timedelta(minutes=15)).isoformat(),
        )

        accepted = self.engine.accept_bonus_chore(
            session["session_id"],
            "bonus_sink",
            now=self.now + timedelta(minutes=1),
        )
        self.assertEqual(accepted["status"], "bonus_active")
        self.assertEqual(accepted["chore_id"], "bonus_sink")
        self.assertEqual(accepted["session_item_id"], "item_3")

        with self.assertRaisesRegex(SessionLifecycleError, "only accepts"):
            self.engine.complete_chore(
                "wipe_counters",
                session_id=session["session_id"],
                completed_at=self.now,
            )

        bonus_item = self.store.sessions[session["session_id"]]["items"][-1]
        completed = self.engine.complete_chore(
            "bonus_sink",
            session_id=session["session_id"],
            session_item_id=bonus_item["session_item_id"],
            completed_at=self.now + timedelta(minutes=5),
        )
        self.assertEqual(completed["status"], "done")
        self.assertEqual(self.store.sessions[session["session_id"]]["status"], "completed")

    def test_expired_bonus_pending_completes_and_rejects_accept(self) -> None:
        session = self.start_two_item_session()
        for item in session["items"]:
            self.engine.complete_chore(
                item["chore_id"],
                session_id=session["session_id"],
                session_item_id=item["session_item_id"],
                completed_at=self.now,
            )
        self.engine.end_session(
            session["session_id"],
            status="completed",
            offer_bonus_chore=True,
            bonus_chore_id="bonus_sink",
            now=self.now,
        )

        with self.assertRaisesRegex(SessionLifecycleError, "bonus_chore_expired"):
            self.engine.accept_bonus_chore(
                session["session_id"],
                "bonus_sink",
                now=self.now + timedelta(minutes=16),
            )
        self.assertEqual(self.store.sessions[session["session_id"]]["status"], "completed")

    def test_paused_complete_session_can_offer_bonus(self) -> None:
        session = self.start_two_item_session()
        for item in session["items"]:
            self.engine.complete_chore(
                item["chore_id"],
                session_id=session["session_id"],
                session_item_id=item["session_item_id"],
                completed_at=self.now,
            )
        self.engine.pause_session(session["session_id"])

        pending = self.engine.end_session(
            session["session_id"],
            status="completed",
            offer_bonus_chore=True,
            bonus_chore_id="bonus_sink",
            now=self.now,
        )

        self.assertEqual(pending["status"], "bonus_pending")

    def test_incomplete_session_cannot_offer_bonus(self) -> None:
        session = self.start_two_item_session()

        with self.assertRaisesRegex(SessionLifecycleError, "planned session items"):
            self.engine.end_session(
                session["session_id"],
                status="completed",
                offer_bonus_chore=True,
                bonus_chore_id="bonus_sink",
                now=self.now,
            )


if __name__ == "__main__":
    unittest.main()
