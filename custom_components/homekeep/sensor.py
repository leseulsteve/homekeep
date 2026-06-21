"""Homekeep sensor entities."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from .const import DOMAIN
from .health import home_health

try:
    from homeassistant.components.sensor import SensorEntity
except ModuleNotFoundError:
    class SensorEntity:  # type: ignore[no-redef]
        """Fallback base class for tests without Home Assistant installed."""


async def async_setup_entry(hass: Any, entry: Any, async_add_entities: Any) -> None:
    """Set up Homekeep sensors for one config entry."""

    storage = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            HomekeepHomeHealthSensor(storage),
            HomekeepDueChoreCountSensor(storage),
            HomekeepBestNextChoreSensor(storage),
            HomekeepNextCalendarContextSensor(storage),
        ]
    )


class HomekeepSensorBase(SensorEntity):
    """Base class for simple Homekeep sensors."""

    _attr_has_entity_name = True

    def __init__(self, storage: Any, key: str, name: str) -> None:
        self.storage = storage
        self._attr_unique_id = f"homekeep_{key}"
        self._attr_name = name


class HomekeepHomeHealthSensor(HomekeepSensorBase):
    """Derived whole-home health sensor."""

    def __init__(self, storage: Any) -> None:
        super().__init__(storage, "home_health", "Home Health")

    @property
    def native_value(self) -> float:
        store = self.storage.store
        return round(home_health(store.chores, store.states, _now()), 1)


class HomekeepDueChoreCountSensor(HomekeepSensorBase):
    """Count chores due now."""

    def __init__(self, storage: Any) -> None:
        super().__init__(storage, "due_chore_count", "Due Chore Count")

    @property
    def native_value(self) -> int:
        now = _now()
        count = 0
        for chore_id, chore in self.storage.store.chores.items():
            state = self.storage.store.states.get(chore_id)
            if chore.enabled and state and state.next_due_at and state.next_due_at <= now:
                count += 1
        return count


class HomekeepBestNextChoreSensor(HomekeepSensorBase):
    """Expose the best current recommendation title."""

    def __init__(self, storage: Any) -> None:
        super().__init__(storage, "best_next_chore", "Best Next Chore")

    @property
    def native_value(self) -> Optional[str]:
        snapshot = _latest_snapshot(self.storage.store.recommendations)
        if not snapshot:
            return None
        result = snapshot.get("result", {})
        rec = result.get("best_single_chore") or result.get("best_bundle")
        return rec.get("title") if rec else None


class HomekeepNextCalendarContextSensor(HomekeepSensorBase):
    """Expose minimized calendar context freshness."""

    def __init__(self, storage: Any) -> None:
        super().__init__(storage, "next_calendar_context", "Next Calendar Context")

    @property
    def native_value(self) -> str:
        context = self.storage.store.calendar_context
        if not context:
            return "unknown"
        if context.get("invalidated_at"):
            return "stale"
        if context.get("has_guests_soon"):
            return "guests"
        if context.get("busy_evening"):
            return "busy"
        return "clear"


def _latest_snapshot(snapshots: dict[str, Any]) -> Optional[dict[str, Any]]:
    if not snapshots:
        return None
    return max(snapshots.values(), key=lambda item: item.get("created_at", ""))


def _now() -> datetime:
    return datetime.now(timezone.utc)
