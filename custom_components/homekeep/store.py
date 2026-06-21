"""Versioned storage helper for Homekeep."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import DOMAIN, STORAGE_VERSION


def empty_store() -> dict[str, Any]:
    """Return the empty Homekeep storage shape."""
    return {
        "recommendations": {},
        "dismissed_recommendations": {},
        "last_refresh": None,
    }


class HomekeepStorage:
    """Load and save Homekeep's local storage."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self._store: Store[dict[str, Any]] = Store(
            hass,
            STORAGE_VERSION,
            f"{DOMAIN}.{entry.entry_id}",
        )
        self.data = empty_store()

    async def async_load(self) -> None:
        """Load Homekeep data, normalizing the empty Phase 0 schema."""
        stored = await self._store.async_load()
        if isinstance(stored, dict):
            self.data = stored

        changed = self._ensure_schema()
        if changed:
            await self.async_save()

    async def async_save(self) -> None:
        """Persist Homekeep data."""
        await self._store.async_save(self.data)

    def _ensure_schema(self) -> bool:
        """Ensure stored data has all Phase 0 keys."""
        changed = False
        for key, default in empty_store().items():
            if key not in self.data:
                self.data[key] = deepcopy(default)
                changed = True
        return changed
