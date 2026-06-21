"""Homekeep binary sensor entities."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .const import DOMAIN

try:
    from homeassistant.components.binary_sensor import BinarySensorEntity
except ModuleNotFoundError:
    class BinarySensorEntity:  # type: ignore[no-redef]
        """Fallback base class for tests without Home Assistant installed."""


async def async_setup_entry(hass: Any, entry: Any, async_add_entities: Any) -> None:
    """Set up one due binary sensor per known Chore."""

    storage = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            HomekeepChoreDueBinarySensor(storage, chore_id)
            for chore_id in sorted(storage.store.chores)
        ]
    )


class HomekeepChoreDueBinarySensor(BinarySensorEntity):
    """Binary sensor that is on when a Chore is currently due."""

    _attr_has_entity_name = True

    def __init__(self, storage: Any, chore_id: str) -> None:
        self.storage = storage
        self.chore_id = chore_id
        self._attr_unique_id = f"homekeep_chore_due_{chore_id}"
        self._attr_name = f"{storage.store.chores[chore_id].name} Due"

    @property
    def is_on(self) -> bool:
        chore = self.storage.store.chores.get(self.chore_id)
        state = self.storage.store.states.get(self.chore_id)
        return bool(
            chore
            and chore.enabled
            and state
            and state.next_due_at
            and state.next_due_at <= datetime.now(timezone.utc)
        )
