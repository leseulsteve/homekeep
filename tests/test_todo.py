"""Tests for Homekeep To-do projections."""

from __future__ import annotations

import unittest
import json
from dataclasses import dataclass

from custom_components.homekeep.models import ChoreDefinition, ChoreState
from custom_components.homekeep.sessions import SessionEngine
from custom_components.homekeep.storage import HomekeepStore
from custom_components.homekeep.todo import (
    HomekeepActiveSessionTodoEntity,
    HomekeepRecommendationsTodoEntity,
    HomekeepTodoMutationError,
    TodoItem,
    TodoItemStatus,
)


def chore_data(name: str) -> dict:
    return {
        "name": name,
        "area_id": "kitchen",
        "group_id": "default",
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
            "empty_compost": chore_data("Empty compost"),
            "wipe_counters": chore_data("Wipe counters"),
        }.items()
    }
    states = {
        chore_id: ChoreState.new_for_chore(chore)
        for chore_id, chore in chores.items()
    }
    return HomekeepStore(chores=chores, states=states)


@dataclass
class FakeStorage:
    store: HomekeepStore
    save_count: int = 0

    async def async_save(self) -> None:
        self.save_count += 1


class TestableActiveSessionTodo(HomekeepActiveSessionTodoEntity):
    def __init__(self, storage: FakeStorage) -> None:
        super().__init__(storage)
        self.write_count = 0

    def async_write_ha_state(self) -> None:
        self.write_count += 1


class TestableRecommendationsTodo(HomekeepRecommendationsTodoEntity):
    def __init__(self, storage: FakeStorage) -> None:
        super().__init__(storage)
        self.write_count = 0

    def async_write_ha_state(self) -> None:
        self.write_count += 1


class HomekeepTodoProjectionTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.storage = FakeStorage(make_store())
        self.session = SessionEngine(self.storage.store).start_session(
            ["empty_compost"]
        )
        self.entity = TestableActiveSessionTodo(self.storage)

    async def test_todo_projection_names_include_homekeep_prefix(self) -> None:
        recommendations = TestableRecommendationsTodo(self.storage)

        self.assertEqual(self.entity._attr_name, "Homekeep Active Session")
        self.assertEqual(self.entity._attr_unique_id, "homekeep_active_session")
        self.assertEqual(self.entity._attr_entity_id, "todo.homekeep_active_session")
        self.assertEqual(recommendations._attr_name, "Homekeep Recommendations")
        self.assertEqual(recommendations._attr_unique_id, "homekeep_recommendations")
        self.assertEqual(
            recommendations._attr_entity_id, "todo.homekeep_recommendations"
        )

    async def test_active_session_projection_completes_valid_item(self) -> None:
        item = self.entity.todo_items[0]
        completed = TodoItem(
            uid=item.uid,
            summary="Changed by Home Assistant",
            status=TodoItemStatus.COMPLETED,
        )

        await self.entity.async_update_todo_item(completed)

        self.assertEqual(len(self.storage.store.completions), 1)
        self.assertEqual(self.storage.store.completions[0].source, "todo")
        self.assertEqual(self.storage.save_count, 1)
        self.assertEqual(self.entity.write_count, 1)

    async def test_completion_without_valid_projection_metadata_is_rejected(self) -> None:
        with self.assertRaisesRegex(HomekeepTodoMutationError, "unknown"):
            await self.entity.async_update_todo_item(
                TodoItem(
                    uid="external-item",
                    summary="External item",
                    status=TodoItemStatus.COMPLETED,
                )
            )

        self.assertEqual(len(self.storage.store.completions), 0)

    async def test_create_delete_edit_and_reorder_are_rejected_and_refreshed(self) -> None:
        item = self.entity.todo_items[0]

        with self.assertRaisesRegex(HomekeepTodoMutationError, "create"):
            await self.entity.async_create_todo_item(item)
        with self.assertRaisesRegex(HomekeepTodoMutationError, "delete"):
            await self.entity.async_delete_todo_items([item.uid])
        with self.assertRaisesRegex(HomekeepTodoMutationError, "update"):
            await self.entity.async_update_todo_item(
                TodoItem(uid=item.uid, summary="Renamed", status=TodoItemStatus.NEEDS_ACTION)
            )
        with self.assertRaisesRegex(HomekeepTodoMutationError, "move"):
            await self.entity.async_move_todo_item(item.uid)

        self.assertEqual(self.entity.write_count, 4)
        self.assertEqual(len(self.storage.store.completions), 0)
        self.assertIn(self.session["session_id"], self.storage.store.sessions)

    async def test_recommendation_projection_cannot_complete_without_session(self) -> None:
        snapshot_id = "snapshot-1"
        self.storage.store.recommendations[snapshot_id] = {
            "snapshot_id": snapshot_id,
            "created_at": "2026-06-21T09:00:00+00:00",
            "selected_recommendations": [
                {
                    "recommendation_id": "rec-1",
                    "chore_items": [
                        {"chore_id": "wipe_counters", "variant": "normal"}
                    ],
                }
            ],
        }
        entity = TestableRecommendationsTodo(self.storage)
        item = entity.todo_items[0]

        with self.assertRaisesRegex(HomekeepTodoMutationError, "active session"):
            await entity.async_update_todo_item(
                TodoItem(uid=item.uid, summary=item.summary, status=TodoItemStatus.COMPLETED)
            )

        self.assertEqual(len(self.storage.store.completions), 0)

    async def test_recommendation_projection_completion_uses_matching_active_session(self) -> None:
        snapshot_id = "snapshot-1"
        self.storage.store.recommendations[snapshot_id] = {
            "snapshot_id": snapshot_id,
            "created_at": "2026-06-21T09:00:00+00:00",
            "selected_recommendations": [
                {
                    "recommendation_id": "rec-1",
                    "chore_items": [
                        {"chore_id": "empty_compost", "variant": "normal"}
                    ],
                }
            ],
        }
        entity = TestableRecommendationsTodo(self.storage)
        item = entity.todo_items[0]
        description = json.loads(item.description or "{}")

        self.assertEqual(description["projection_kind"], "active_session")
        self.assertEqual(description["session_id"], self.session["session_id"])
        self.assertEqual(
            description["session_item_id"],
            self.session["items"][0]["session_item_id"],
        )

        await entity.async_update_todo_item(
            TodoItem(
                uid=item.uid,
                summary=item.summary,
                status=TodoItemStatus.COMPLETED,
            )
        )

        session_item = self.storage.store.sessions[self.session["session_id"]]["items"][0]
        self.assertEqual(session_item["status"], "done")
        self.assertEqual(len(self.storage.store.completions), 1)
        self.assertEqual(self.storage.store.completions[0].source, "todo")
        self.assertEqual(self.storage.save_count, 1)


if __name__ == "__main__":
    unittest.main()
