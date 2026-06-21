"""Tests for Homekeep storage and sample loading."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone
from pathlib import Path

from custom_components.homekeep.const import CURRENT_STORAGE_VERSION
from custom_components.homekeep.storage import (
    UnsupportedStorageVersionError,
    dump_store_dict,
    empty_store_dict,
    load_sample_chores,
    load_store_dict,
    migrate_store_dict,
)


ROOT = Path(__file__).resolve().parents[1]


def chore_data() -> dict:
    return {
        "name": "Empty compost",
        "area_id": "kitchen",
        "group_id": "trash",
        "base_interval_days": 2,
        "min_interval_days": 1,
        "max_interval_days": 4,
        "estimated_minutes": 2,
        "energy": "low",
        "visibility": "medium",
        "health_weight": 1.4,
        "variants": {"normal": {"label": "Empty compost", "credit": 1.0}},
        "pairs_with": [],
        "enabled": True,
    }


class StorageTest(unittest.TestCase):
    def test_empty_storage_initializes(self) -> None:
        store = load_store_dict(None)

        self.assertEqual(store.version, CURRENT_STORAGE_VERSION)
        self.assertEqual(store.chores, {})

    def test_v1_store_migrates_chore_state_to_v2(self) -> None:
        raw = {
            "version": 1,
            "chores": {"empty_compost": chore_data()},
            "states": {
                "empty_compost": {
                    "chore_id": "empty_compost",
                    "last_completed_at": "2026-01-01T12:00:00+00:00",
                    "adaptive_interval_days": 99,
                    "next_due_at": "2026-01-03T12:00:00+00:00",
                    "recent_dismissals": 4,
                    "recent_snoozes": 2,
                }
            },
            "completions": [],
        }

        migrated = migrate_store_dict(raw)
        migrated_state = migrated["states"]["empty_compost"]

        self.assertEqual(migrated["version"], CURRENT_STORAGE_VERSION)
        self.assertNotIn("recent_dismissals", migrated_state)
        self.assertNotIn("recent_snoozes", migrated_state)
        self.assertIsNone(migrated_state["snoozed_until"])
        self.assertEqual(migrated_state["dismissal_events"], [])
        self.assertEqual(migrated_state["snooze_events"], [])
        self.assertIsNone(migrated_state["last_dismissed_at"])
        self.assertIsNone(migrated_state["last_snoozed_at"])
        self.assertEqual(
            migrated_state["last_completed_at"], "2026-01-01T12:00:00+00:00"
        )
        self.assertEqual(migrated_state["next_due_at"], "2026-01-03T12:00:00+00:00")

        store = load_store_dict(raw)
        self.assertEqual(store.states["empty_compost"].adaptive_interval_days, 4)

    def test_future_storage_version_is_rejected(self) -> None:
        raw = empty_store_dict()
        raw["version"] = CURRENT_STORAGE_VERSION + 1

        with self.assertRaisesRegex(UnsupportedStorageVersionError, "unsupported"):
            load_store_dict(raw)

    def test_storage_round_trip_preserves_definitions_state_and_history(self) -> None:
        raw = empty_store_dict()
        raw["chores"] = {"empty_compost": chore_data()}
        raw["states"] = {
            "empty_compost": {
                "chore_id": "empty_compost",
                "last_completed_at": "2026-01-01T12:00:00+00:00",
                "adaptive_interval_days": 2,
                "next_due_at": "2026-01-03T12:00:00+00:00",
                "snoozed_until": None,
                "dismissal_events": ["2026-01-02T12:00:00+00:00"],
                "snooze_events": ["2026-01-02T13:00:00+00:00"],
                "last_dismissed_at": "2026-01-02T12:00:00+00:00",
                "last_snoozed_at": "2026-01-02T13:00:00+00:00",
            }
        }
        raw["completions"] = [
            {
                "completion_id": "completion-1",
                "chore_id": "empty_compost",
                "session_id": None,
                "completed_at": "2026-01-01T12:00:00+00:00",
                "completed_by": None,
                "variant": "normal",
                "credit": 1.0,
                "source": "service",
            }
        ]

        store = load_store_dict(raw, now=datetime(2026, 1, 3, tzinfo=timezone.utc))
        round_tripped = dump_store_dict(store)

        self.assertEqual(
            round_tripped["chores"]["empty_compost"]["name"], "Empty compost"
        )
        self.assertEqual(
            round_tripped["chores"]["empty_compost"]["variants"]["normal"]["credit"],
            1.0,
        )
        self.assertEqual(
            round_tripped["states"]["empty_compost"]["dismissal_events"],
            ["2026-01-02T12:00:00+00:00"],
        )
        self.assertEqual(round_tripped["completions"], raw["completions"])

    def test_sample_chores_load_for_tests(self) -> None:
        chores = load_sample_chores(ROOT / "examples" / "sample_chores.yaml")

        self.assertIn("empty_compost", chores)
        self.assertIn("wipe_kitchen_counters", chores)
        self.assertIn("normal", chores["empty_compost"].variants)


if __name__ == "__main__":
    unittest.main()
