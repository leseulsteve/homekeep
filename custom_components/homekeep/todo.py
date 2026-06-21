"""Homekeep To-do projection entities."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Optional

from .const import DOMAIN
from .models import HomekeepValidationError
from .runtime import HomekeepServiceRuntime

try:
    from homeassistant.components.todo import (
        TodoItem,
        TodoItemStatus,
        TodoListEntity,
        TodoListEntityFeature,
    )
except ModuleNotFoundError:
    class TodoListEntity:  # type: ignore[no-redef]
        """Fallback base class for tests without Home Assistant installed."""

    class TodoItemStatus:  # type: ignore[no-redef]
        """Fallback To-do status values."""

        NEEDS_ACTION = "needs_action"
        COMPLETED = "completed"

    class TodoListEntityFeature:  # type: ignore[no-redef]
        """Fallback To-do feature flags."""

        UPDATE_TODO_ITEM = 4

    @dataclass
    class TodoItem:  # type: ignore[no-redef]
        """Fallback To-do item used by tests."""

        uid: str
        summary: str
        status: str
        description: Optional[str] = None


class HomekeepTodoMutationError(HomekeepValidationError):
    """Raised when Home Assistant tries to mutate a projection directly."""


@dataclass(frozen=True)
class ProjectionMetadata:
    """Metadata that allows projected To-do completion to write through."""

    projection_kind: str
    chore_id: str
    session_id: Optional[str] = None
    session_item_id: Optional[str] = None
    recommendation_snapshot_id: Optional[str] = None
    variant: str = "normal"


async def async_setup_entry(hass: Any, entry: Any, async_add_entities: Any) -> None:
    """Set up Homekeep To-do projection entities."""

    storage = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            HomekeepRecommendationsTodoEntity(storage),
            HomekeepActiveSessionTodoEntity(storage),
        ]
    )


class HomekeepTodoProjectionEntity(TodoListEntity):
    """Base entity for read-only Homekeep To-do projections."""

    _attr_has_entity_name = True
    _attr_supported_features = TodoListEntityFeature.UPDATE_TODO_ITEM

    def __init__(self, storage: Any, key: str, name: str) -> None:
        self.storage = storage
        self._attr_unique_id = f"homekeep_{key}"
        self._attr_name = name
        self._metadata_by_uid: dict[str, ProjectionMetadata] = {}

    @property
    def todo_items(self) -> list[TodoItem]:
        items = self._project_items()
        self._metadata_by_uid = {uid: metadata for uid, _item, metadata in items}
        return [item for _uid, item, _metadata in items]

    async def async_create_todo_item(self, item: TodoItem) -> None:
        await self._reject_unsupported_mutation("create")

    async def async_delete_todo_items(self, uids: list[str]) -> None:
        await self._reject_unsupported_mutation("delete")

    async def async_update_todo_item(self, item: TodoItem) -> None:
        if _is_completed_status(item.status):
            await self.async_complete_projected_item(item.uid)
            return
        await self._reject_unsupported_mutation("update")

    async def async_move_todo_item(
        self, uid: str, previous_uid: str | None = None
    ) -> None:
        await self._reject_unsupported_mutation("move")

    async def async_complete_projected_item(self, uid: str) -> dict[str, Any]:
        self.todo_items
        metadata = self._metadata_by_uid.get(uid)
        if metadata is None:
            raise HomekeepTodoMutationError("unknown Homekeep projection item")
        if not metadata.session_id or not metadata.session_item_id:
            raise HomekeepTodoMutationError(
                "projected item is not attached to an active session"
            )
        result = await HomekeepServiceRuntime(self.storage).async_handle(
            "complete_chore",
            {
                "chore_id": metadata.chore_id,
                "session_id": metadata.session_id,
                "session_item_id": metadata.session_item_id,
                "variant": metadata.variant,
                "source": "todo",
                "request_id": f"todo:{uid}:complete",
            },
        )
        self._write_ha_state()
        return result or {}

    async def _reject_unsupported_mutation(self, mutation: str) -> None:
        self._write_ha_state()
        raise HomekeepTodoMutationError(
            f"Homekeep To-do projections do not support {mutation}"
        )

    def _write_ha_state(self) -> None:
        writer = getattr(self, "async_write_ha_state", None)
        if writer:
            writer()

    def _project_items(self) -> list[tuple[str, TodoItem, ProjectionMetadata]]:
        raise NotImplementedError


class HomekeepActiveSessionTodoEntity(HomekeepTodoProjectionEntity):
    """Projection of active Chore Session items."""

    def __init__(self, storage: Any) -> None:
        super().__init__(storage, "active_session_todo", "Active Session")

    def _project_items(self) -> list[tuple[str, TodoItem, ProjectionMetadata]]:
        projected: list[tuple[str, TodoItem, ProjectionMetadata]] = []
        for session in self.storage.store.sessions.values():
            if session.get("status") not in {"active", "paused", "bonus_active"}:
                continue
            for item in session.get("items", []):
                if item.get("status") not in {"pending", "active"}:
                    continue
                chore = self.storage.store.chores.get(item["chore_id"])
                if chore is None:
                    continue
                metadata = ProjectionMetadata(
                    projection_kind="active_session",
                    chore_id=item["chore_id"],
                    session_id=session["session_id"],
                    session_item_id=item["session_item_id"],
                    variant=item.get("variant", "normal"),
                )
                uid = _uid(metadata)
                projected.append((uid, _todo_item(uid, chore.name, metadata), metadata))
        return projected


class HomekeepRecommendationsTodoEntity(HomekeepTodoProjectionEntity):
    """Projection of the latest Smart Chore List recommendations."""

    def __init__(self, storage: Any) -> None:
        super().__init__(storage, "recommendations_todo", "Recommendations")

    def _project_items(self) -> list[tuple[str, TodoItem, ProjectionMetadata]]:
        snapshot = _latest_snapshot(self.storage.store.recommendations)
        if not snapshot:
            return []
        projected: list[tuple[str, TodoItem, ProjectionMetadata]] = []
        for recommendation in snapshot.get("selected_recommendations", []):
            for item in recommendation.get("chore_items", []):
                chore = self.storage.store.chores.get(item["chore_id"])
                if chore is None:
                    continue
                metadata = ProjectionMetadata(
                    projection_kind="recommendation",
                    chore_id=item["chore_id"],
                    recommendation_snapshot_id=snapshot["snapshot_id"],
                    variant=item.get("variant", "normal"),
                )
                uid = _uid(metadata)
                projected.append((uid, _todo_item(uid, chore.name, metadata), metadata))
        return projected


def _todo_item(uid: str, summary: str, metadata: ProjectionMetadata) -> TodoItem:
    return TodoItem(
        uid=uid,
        summary=summary,
        status=TodoItemStatus.NEEDS_ACTION,
        description=json.dumps(
            {
                "homekeep_projection_id": uid,
                "chore_id": metadata.chore_id,
                "session_item_id": metadata.session_item_id,
                "session_id": metadata.session_id,
                "recommendation_snapshot_id": metadata.recommendation_snapshot_id,
                "variant": metadata.variant,
                "projection_kind": metadata.projection_kind,
            },
            sort_keys=True,
        ),
    )


def _uid(metadata: ProjectionMetadata) -> str:
    parts = [
        "homekeep",
        metadata.projection_kind,
        metadata.session_id or metadata.recommendation_snapshot_id or "none",
        metadata.session_item_id or metadata.chore_id,
        metadata.chore_id,
    ]
    return ":".join(parts)


def _is_completed_status(status: Any) -> bool:
    return status == TodoItemStatus.COMPLETED or str(status).lower().endswith("completed")


def _latest_snapshot(snapshots: dict[str, Any]) -> Optional[dict[str, Any]]:
    if not snapshots:
        return None
    return max(snapshots.values(), key=lambda item: item.get("created_at", ""))
