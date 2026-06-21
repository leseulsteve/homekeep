"""Tests for Homekeep Home Assistant service facade behavior."""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from datetime import timedelta

from custom_components.homekeep.const import (
    ATTR_BASE_INTERVAL_DAYS,
    ATTR_CHORE_ID,
    ATTR_ENERGY_LEVEL,
    ATTR_ESTIMATED_MINUTES,
    ATTR_RECOMMENDATION_ID,
    ATTR_RECOMMENDATION_SNAPSHOT_ID,
    ATTR_REQUEST_ID,
    ATTR_SESSION_ID,
    ATTR_SESSION_ITEM_ID,
    ATTR_SNOOZE_MINUTES,
    ATTR_STATUS,
    SERVICE_COMPLETE_CHORE,
    SERVICE_CREATE_CHORE,
    SERVICE_END_SESSION,
    SERVICE_GENERATE_SMART_CHORE_LIST,
    SERVICE_PAUSE_SESSION,
    SERVICE_SKIP_CHORE,
    SERVICE_SNOOZE_CHORE,
    SERVICE_START_RECOMMENDATION,
)
from custom_components.homekeep.health import apply_completion_to_state, utc_datetime
from custom_components.homekeep.models import (
    ChoreDefinition,
    ChoreState,
    HomekeepValidationError,
)
from custom_components.homekeep.runtime import HomekeepServiceRuntime
from custom_components.homekeep.sessions import SessionEngine
from custom_components.homekeep.storage import HomekeepStore


def chore_data(name: str, *, area_id: str = "kitchen", minutes: int = 5) -> dict:
    return {
        "name": name,
        "area_id": area_id,
        "group_id": "default",
        "base_interval_days": 7,
        "min_interval_days": 3,
        "max_interval_days": 14,
        "estimated_minutes": minutes,
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
            "empty_compost": chore_data("Empty compost", minutes=2),
            "wipe_counters": chore_data("Wipe counters", minutes=5),
        }.items()
    }
    now = utc_datetime(2026, 6, 21, 9)
    states = {
        chore_id: apply_completion_to_state(
            chore,
            ChoreState.new_for_chore(chore),
            now - timedelta(days=20),
            "normal",
        )
        for chore_id, chore in chores.items()
    }
    return HomekeepStore(chores=chores, states=states)


@dataclass
class FakeStorage:
    store: HomekeepStore
    save_count: int = 0

    async def async_save(self) -> None:
        self.save_count += 1


class FakeHass:
    def __init__(self) -> None:
        self.executor_jobs: list[str] = []

    async def async_add_executor_job(self, func, *args):
        self.executor_jobs.append(func.__name__)
        return func(*args)


class HomekeepServiceRuntimeTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.storage = FakeStorage(make_store())
        self.runtime = HomekeepServiceRuntime(self.storage)

    async def test_generate_and_start_recommendation_service(self) -> None:
        recommendation = await self.runtime.async_handle(
            SERVICE_GENERATE_SMART_CHORE_LIST,
            {"time_budget_minutes": 10},
        )
        assert recommendation is not None
        started = await self.runtime.async_handle(
            SERVICE_START_RECOMMENDATION,
            {
                ATTR_RECOMMENDATION_SNAPSHOT_ID: recommendation["snapshot_id"],
                ATTR_RECOMMENDATION_ID: recommendation["best_single_chore"][
                    "recommendation_id"
                ],
                ATTR_REQUEST_ID: "start-1",
            },
        )

        assert started is not None
        self.assertIn(started["session_id"], self.storage.store.sessions)
        self.assertEqual(self.storage.save_count, 2)

    async def test_create_chore_adds_definition_and_initial_state(self) -> None:
        result = await self.runtime.async_handle(
            SERVICE_CREATE_CHORE,
            {
                "name": "Water the basil",
                "area_id": "kitchen",
                "group_id": "plants",
                ATTR_BASE_INTERVAL_DAYS: 3,
                ATTR_ESTIMATED_MINUTES: 2,
                ATTR_ENERGY_LEVEL: "low",
                ATTR_REQUEST_ID: "create-basil",
            },
        )

        assert result is not None
        self.assertEqual(result["status"], "created")
        self.assertEqual(result["chore_id"], "water_the_basil")
        self.assertIn("water_the_basil", self.storage.store.chores)
        self.assertIn("water_the_basil", self.storage.store.states)
        self.assertEqual(
            self.storage.store.chores["water_the_basil"].name, "Water the basil"
        )
        self.assertEqual(self.storage.save_count, 1)

        retried = await self.runtime.async_handle(
            SERVICE_CREATE_CHORE,
            {
                "name": "Water the basil",
                ATTR_REQUEST_ID: "create-basil",
            },
        )

        self.assertEqual(retried, result)
        self.assertEqual(len(self.storage.store.chores), 3)
        self.assertEqual(self.storage.save_count, 2)

    async def test_create_chore_rejects_duplicate_chore_id(self) -> None:
        with self.assertRaisesRegex(HomekeepValidationError, "already exists"):
            await self.runtime.async_handle(
                SERVICE_CREATE_CHORE,
                {
                    ATTR_CHORE_ID: "empty_compost",
                    "name": "Empty compost again",
                },
            )

        self.assertEqual(self.storage.save_count, 0)

    async def test_malformed_payload_is_rejected_without_save(self) -> None:
        with self.assertRaisesRegex(HomekeepValidationError, "snooze_minutes"):
            await self.runtime.async_handle(
                SERVICE_SNOOZE_CHORE,
                {
                    ATTR_CHORE_ID: "empty_compost",
                    ATTR_SNOOZE_MINUTES: 4,
                },
            )

        self.assertEqual(self.storage.save_count, 0)
        self.assertEqual(len(self.storage.store.completions), 0)

    async def test_missing_required_service_fields_raise_validation_errors(self) -> None:
        cases = [
            (SERVICE_COMPLETE_CHORE, {}, "chore_id"),
            (
                SERVICE_SNOOZE_CHORE,
                {ATTR_CHORE_ID: "empty_compost"},
                "snooze_minutes",
            ),
            (
                SERVICE_START_RECOMMENDATION,
                {ATTR_RECOMMENDATION_ID: "rec"},
                "recommendation_snapshot_id",
            ),
            (SERVICE_PAUSE_SESSION, {}, "session_id"),
            (SERVICE_END_SESSION, {ATTR_SESSION_ID: "session-1"}, "status"),
        ]

        for service_name, payload, message in cases:
            with self.subTest(service_name=service_name):
                with self.assertRaisesRegex(HomekeepValidationError, message):
                    await self.runtime.async_handle(service_name, payload)

        self.assertEqual(self.storage.save_count, 0)

    async def test_unknown_chore_id_is_rejected_without_crashing(self) -> None:
        with self.assertRaisesRegex(HomekeepValidationError, "unknown chore_id"):
            await self.runtime.async_handle(
                SERVICE_COMPLETE_CHORE,
                {ATTR_CHORE_ID: "missing"},
            )

        self.assertEqual(self.storage.save_count, 0)

    async def test_session_service_idempotency_returns_same_result(self) -> None:
        session = SessionEngine(self.storage.store).start_session(["empty_compost"])
        item = session["items"][0]

        first = await self.runtime.async_handle(
            SERVICE_COMPLETE_CHORE,
            {
                ATTR_CHORE_ID: item["chore_id"],
                ATTR_SESSION_ID: session["session_id"],
                ATTR_SESSION_ITEM_ID: item["session_item_id"],
                ATTR_REQUEST_ID: "complete-once",
            },
        )
        second = await self.runtime.async_handle(
            SERVICE_COMPLETE_CHORE,
            {
                ATTR_CHORE_ID: item["chore_id"],
                ATTR_SESSION_ID: session["session_id"],
                ATTR_SESSION_ITEM_ID: item["session_item_id"],
                ATTR_REQUEST_ID: "complete-once",
            },
        )

        self.assertEqual(first, second)
        self.assertEqual(len(self.storage.store.completions), 1)
        self.assertEqual(self.storage.save_count, 2)

    async def test_skip_requires_session_metadata(self) -> None:
        with self.assertRaisesRegex(HomekeepValidationError, "session_id"):
            await self.runtime.async_handle(
                SERVICE_SKIP_CHORE,
                {ATTR_CHORE_ID: "empty_compost"},
            )

    async def test_end_session_unknown_id_is_rejected(self) -> None:
        with self.assertRaisesRegex(HomekeepValidationError, "unknown session_id"):
            await self.runtime.async_handle(
                "end_session",
                {ATTR_SESSION_ID: "missing", ATTR_STATUS: "completed"},
            )

    async def test_stale_session_response_after_cancel_does_not_mutate(self) -> None:
        session = SessionEngine(self.storage.store).start_session(["empty_compost"])
        item = session["items"][0]
        await self.runtime.async_handle(
            SERVICE_END_SESSION,
            {
                ATTR_SESSION_ID: session["session_id"],
                ATTR_STATUS: "cancelled",
            },
        )

        with self.assertRaisesRegex(HomekeepValidationError, "cannot accept completions"):
            await self.runtime.async_handle(
                SERVICE_COMPLETE_CHORE,
                {
                    ATTR_CHORE_ID: item["chore_id"],
                    ATTR_SESSION_ID: session["session_id"],
                    ATTR_SESSION_ITEM_ID: item["session_item_id"],
                },
            )

        self.assertEqual(len(self.storage.store.completions), 0)
        self.assertEqual(
            self.storage.store.sessions[session["session_id"]]["status"],
            "cancelled",
        )


if __name__ == "__main__":
    unittest.main()
