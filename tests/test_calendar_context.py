"""Tests for Calendar Context snapshots and invalidation."""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping

from custom_components.homekeep.calendar_context import (
    CalendarContextEngine,
    calendar_event_fingerprint,
    calendar_context_version,
    derive_calendar_signals,
    invalidate_calendar_context_for_entity,
    is_calendar_context_fresh,
)
from custom_components.homekeep.const import (
    ATTR_CALENDAR_ENTITY_IDS,
    ATTR_RECOMMENDATION_MODE,
    ATTR_TARGET_TIME_WINDOW,
    SERVICE_GENERATE_SMART_CHORE_LIST,
    SERVICE_REFRESH_CALENDAR_CONTEXT,
)
from custom_components.homekeep.health import apply_completion_to_state, utc_datetime
from custom_components.homekeep.models import ChoreDefinition, ChoreState
from custom_components.homekeep.runtime import HomekeepServiceRuntime
from custom_components.homekeep.storage import HomekeepStore


NOW = utc_datetime(2026, 6, 21, 9)


def chore_data(name: str, *, area_id: str = "kitchen", group_id: str = "default") -> dict:
    return {
        "name": name,
        "area_id": area_id,
        "group_id": group_id,
        "base_interval_days": 7,
        "min_interval_days": 3,
        "max_interval_days": 14,
        "estimated_minutes": 5,
        "energy": "normal",
        "visibility": "high",
        "health_weight": 1.0,
        "variants": {"normal": {"label": name, "credit": 1.0}},
        "pairs_with": [],
        "enabled": True,
    }


def make_store() -> HomekeepStore:
    chores = {
        chore_id: ChoreDefinition.from_dict(chore_id, data)
        for chore_id, data in {
            "wipe_counters": chore_data(
                "Wipe kitchen counters", group_id="surfaces"
            ),
            "empty_compost": chore_data(
                "Empty compost", group_id="trash"
            ),
        }.items()
    }
    states = {
        chore_id: apply_completion_to_state(
            chore,
            ChoreState.new_for_chore(chore),
            NOW - timedelta(days=20),
            "normal",
        )
        for chore_id, chore in chores.items()
    }
    return HomekeepStore(chores=chores, states=states)


@dataclass
class FakeStorage:
    store: HomekeepStore
    entry: Any = None
    save_count: int = 0

    async def async_save(self) -> None:
        self.save_count += 1


class FakeEntry:
    def __init__(self, options: dict[str, Any]) -> None:
        self.options = options


class CalendarContextTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.store = make_store()
        self.events_by_entity = {
            "calendar.family": [
                {
                    "start": (NOW + timedelta(hours=3)).isoformat(),
                    "end": (NOW + timedelta(hours=4)).isoformat(),
                    "summary": "Guests arrive",
                    "description": "Private details should not be stored",
                    "location": "Private place",
                },
                {
                    "start": (NOW + timedelta(days=1)).isoformat(),
                    "end": (NOW + timedelta(days=1, hours=1)).isoformat(),
                    "summary": "Trash pickup",
                },
            ]
        }
        self.versions = {
            "calendar.family": {
                "state": "off",
                "last_changed": NOW.isoformat(),
                "last_updated": NOW.isoformat(),
            }
        }

    async def test_refresh_stores_derived_snapshot_without_raw_calendar_details(self) -> None:
        engine = CalendarContextEngine(
            self.store,
            event_provider=self._event_provider,
            state_provider=lambda entity_ids: self.versions,
        )

        snapshot = await engine.async_refresh(
            entity_ids=["calendar.family"],
            recommendation_mode="ready_now",
            now=NOW,
        )

        self.assertTrue(snapshot["has_guests_soon"])
        self.assertTrue(snapshot["trash_day_tomorrow"])
        self.assertEqual(snapshot["event_count"], 2)
        encoded = repr(snapshot)
        self.assertNotIn("Guests arrive", encoded)
        self.assertNotIn("Private details", encoded)
        self.assertNotIn("Private place", encoded)
        self.assertFalse(snapshot["diagnostics"]["raw_event_details_stored"])
        self.assertTrue(
            snapshot["source_calendar_event_fingerprint"].startswith("calevt:")
        )
        self.assertEqual(self.store.calendar_context, snapshot)

    async def test_max_age_target_and_version_changes_make_snapshot_stale(self) -> None:
        engine = CalendarContextEngine(
            self.store,
            event_provider=self._event_provider,
            state_provider=lambda entity_ids: self.versions,
        )
        snapshot = await engine.async_refresh(
            entity_ids=["calendar.family"],
            target_time_window=None,
            recommendation_mode="ready_now",
            now=NOW,
        )

        self.assertTrue(
            is_calendar_context_fresh(
                snapshot,
                entity_ids=["calendar.family"],
                current_versions=self.versions,
                target_time_window=None,
                recommendation_mode="ready_now",
                now=NOW + timedelta(minutes=14),
            )
        )
        self.assertFalse(
            is_calendar_context_fresh(
                snapshot,
                entity_ids=["calendar.family"],
                current_versions=self.versions,
                target_time_window=None,
                recommendation_mode="ready_now",
                now=NOW + timedelta(minutes=16),
            )
        )
        changed_versions = {
            "calendar.family": {
                **self.versions["calendar.family"],
                "last_updated": (NOW + timedelta(minutes=1)).isoformat(),
            }
        }
        self.assertFalse(
            is_calendar_context_fresh(
                snapshot,
                entity_ids=["calendar.family"],
                current_versions=changed_versions,
                target_time_window=None,
                recommendation_mode="ready_now",
                now=NOW + timedelta(minutes=1),
            )
        )
        self.assertFalse(
            is_calendar_context_fresh(
                snapshot,
                entity_ids=["calendar.family"],
                current_versions=self.versions,
                target_time_window=f"{NOW.isoformat()}/{(NOW + timedelta(hours=2)).isoformat()}",
                recommendation_mode="ready_now",
                now=NOW + timedelta(minutes=1),
            )
        )

    async def test_calendar_change_invalidates_context_and_dependent_recommendations(self) -> None:
        engine = CalendarContextEngine(
            self.store,
            event_provider=self._event_provider,
            state_provider=lambda entity_ids: self.versions,
        )
        snapshot = await engine.async_refresh(
            entity_ids=["calendar.family"],
            now=NOW,
        )
        self.store.recommendations["snapshot-1"] = {
            "snapshot_id": "snapshot-1",
            "calendar_context_id": snapshot["snapshot_id"],
            "invalidated_at": None,
            "invalidation_reason": None,
        }

        changed = invalidate_calendar_context_for_entity(
            self.store,
            "calendar.family",
            now=NOW + timedelta(minutes=1),
        )

        self.assertTrue(changed)
        self.assertEqual(
            self.store.calendar_context["invalidation_reason"],
            "calendar_entity_changed",
        )
        self.assertEqual(
            self.store.recommendations["snapshot-1"]["invalidation_reason"],
            "calendar_entity_changed",
        )

    async def test_added_event_makes_context_stale_without_state_change(self) -> None:
        events_by_entity = {"calendar.family": []}
        engine = CalendarContextEngine(
            self.store,
            event_provider=lambda entity_ids, start, end: self._events_from(
                events_by_entity,
                entity_ids,
            ),
            state_provider=lambda entity_ids: self.versions,
        )
        snapshot = await engine.async_refresh(
            entity_ids=["calendar.family"],
            now=NOW,
        )
        self.store.recommendations["snapshot-1"] = {
            "snapshot_id": "snapshot-1",
            "calendar_context_id": snapshot["snapshot_id"],
            "invalidated_at": None,
            "invalidation_reason": None,
        }

        self.assertTrue(
            await engine.async_is_fresh(
                entity_ids=["calendar.family"],
                now=NOW + timedelta(minutes=1),
            )
        )

        events_by_entity["calendar.family"] = [
            {
                "start": (NOW + timedelta(hours=2)).isoformat(),
                "end": (NOW + timedelta(hours=3)).isoformat(),
                "summary": "Synthetic calendar hold",
            }
        ]

        self.assertFalse(
            await engine.async_is_fresh(
                entity_ids=["calendar.family"],
                now=NOW + timedelta(minutes=1),
            )
        )
        refreshed = await engine.async_refresh(
            entity_ids=["calendar.family"],
            now=NOW + timedelta(minutes=1),
        )
        self.assertNotEqual(refreshed["snapshot_id"], snapshot["snapshot_id"])
        self.assertEqual(
            self.store.recommendations["snapshot-1"]["invalidation_reason"],
            "calendar_context_refreshed",
        )

    async def test_modified_event_signal_changes_event_fingerprint(self) -> None:
        original = {
            "calendar.family": [
                {
                    "start": (NOW + timedelta(hours=2)).isoformat(),
                    "end": (NOW + timedelta(hours=3)).isoformat(),
                    "summary": "Synthetic calendar hold",
                }
            ]
        }
        modified = {
            "calendar.family": [
                {
                    "start": (NOW + timedelta(hours=2)).isoformat(),
                    "end": (NOW + timedelta(hours=3)).isoformat(),
                    "summary": "Guest visit",
                }
            ]
        }

        self.assertNotEqual(
            calendar_event_fingerprint(original, now=NOW),
            calendar_event_fingerprint(modified, now=NOW),
        )

    def test_french_calendar_keywords_set_derived_signals(self) -> None:
        events_by_entity = {
            "calendar.family": [
                {
                    "start": (NOW + timedelta(hours=2)).isoformat(),
                    "end": (NOW + timedelta(hours=3)).isoformat(),
                    "summary": "Visite d'invités pour souper",
                },
                {
                    "start": (NOW + timedelta(hours=4)).isoformat(),
                    "end": (NOW + timedelta(hours=5)).isoformat(),
                    "summary": "Départ vers l'aéroport",
                },
                {
                    "start": (NOW + timedelta(days=1)).isoformat(),
                    "end": (NOW + timedelta(days=1, hours=1)).isoformat(),
                    "summary": "Sortir les poubelles et le recyclage",
                },
            ]
        }

        derived = derive_calendar_signals(events_by_entity, now=NOW)

        self.assertTrue(derived["has_guests_soon"])
        self.assertTrue(derived["leaving_home_soon"])
        self.assertTrue(derived["trash_day_tomorrow"])

    async def test_runtime_refresh_and_recommendation_uses_selected_calendar_context(self) -> None:
        storage = FakeStorage(
            make_store(),
            entry=FakeEntry({"calendar_entity_ids": ["calendar.family"]}),
        )
        runtime = HomekeepServiceRuntime(storage)

        refreshed = await runtime.async_handle(
            SERVICE_REFRESH_CALENDAR_CONTEXT,
            {
                ATTR_CALENDAR_ENTITY_IDS: ["calendar.family"],
                ATTR_RECOMMENDATION_MODE: "ready_now",
            },
        )
        assert refreshed is not None
        recommendation = await runtime.async_handle(
            SERVICE_GENERATE_SMART_CHORE_LIST,
            {},
        )

        assert recommendation is not None
        snapshot = storage.store.recommendations[recommendation["snapshot_id"]]
        self.assertEqual(
            snapshot["calendar_context_id"],
            storage.store.calendar_context["snapshot_id"],
        )
        self.assertEqual(storage.save_count, 2)

    def test_calendar_context_version_excludes_raw_event_text(self) -> None:
        derived = derive_calendar_signals(self.events_by_entity, now=NOW)
        version = calendar_context_version(self.versions, {"derived": derived})

        self.assertTrue(version.startswith("cal:"))
        self.assertNotIn("Guests arrive", version)
        self.assertNotIn("Private details", version)

    async def _event_provider(
        self, entity_ids: list[str], start: datetime, end: datetime
    ) -> Mapping[str, list[Any]]:
        return {
            entity_id: self.events_by_entity.get(entity_id, [])
            for entity_id in entity_ids
        }

    async def _events_from(
        self,
        events_by_entity: Mapping[str, list[Any]],
        entity_ids: list[str],
    ) -> Mapping[str, list[Any]]:
        return {
            entity_id: events_by_entity.get(entity_id, [])
            for entity_id in entity_ids
        }


if __name__ == "__main__":
    unittest.main()
