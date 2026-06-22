"""Tests for Homekeep reload/unload behavior with local Home Assistant fakes."""

from __future__ import annotations

import unittest
import sys
import types
from types import SimpleNamespace
from unittest.mock import patch

from custom_components.homekeep import (
    async_unload_entry,
)
from custom_components.homekeep.const import DOMAIN, PLATFORMS
from custom_components.homekeep.storage import HomekeepStore


class FakeConfigEntries:
    def __init__(self, unload_ok: bool = True) -> None:
        self.unload_ok = unload_ok
        self.calls: list[tuple[object, list[str]]] = []

    async def async_unload_platforms(self, entry: object, platforms: list[str]) -> bool:
        self.calls.append((entry, platforms))
        return self.unload_ok


class FakeStorage:
    def __init__(self) -> None:
        self.store = HomekeepStore()
        self.unsub_count = 0
        self.save_count = 0
        self.calendar_unsub = self._calendar_unsub

    def _calendar_unsub(self) -> None:
        self.unsub_count += 1

    async def async_save(self) -> None:
        self.save_count += 1


def chore_data(name: str = "Existing chore") -> dict:
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


class ReloadUnloadTest(unittest.IsolatedAsyncioTestCase):
    async def test_unload_removes_entry_storage_and_calendar_listener(self) -> None:
        entry = SimpleNamespace(entry_id="entry-1")
        storage = FakeStorage()
        hass = SimpleNamespace(
            data={DOMAIN: {entry.entry_id: storage}},
            config_entries=FakeConfigEntries(unload_ok=True),
        )

        with patch.dict("sys.modules", self._frontend_modules()):
            unloaded = await async_unload_entry(hass, entry)

        self.assertTrue(unloaded)
        self.assertEqual(storage.unsub_count, 1)
        self.assertEqual(hass.config_entries.calls, [(entry, PLATFORMS)])
        self.assertNotIn(DOMAIN, hass.data)
        self.assertEqual(hass.removed_panel, "homekeep")

    async def test_failed_platform_unload_preserves_storage_and_listener(self) -> None:
        entry = SimpleNamespace(entry_id="entry-1")
        storage = FakeStorage()
        hass = SimpleNamespace(
            data={DOMAIN: {entry.entry_id: storage}},
            config_entries=FakeConfigEntries(unload_ok=False),
        )

        unloaded = await async_unload_entry(hass, entry)

        self.assertFalse(unloaded)
        self.assertEqual(storage.unsub_count, 0)
        self.assertIn(entry.entry_id, hass.data[DOMAIN])

    def _frontend_modules(self) -> dict[str, types.ModuleType]:
        fake_frontend = types.ModuleType("homeassistant.components.frontend")
        fake_frontend.async_remove_panel = (
            lambda hass, path, **kwargs: setattr(hass, "removed_panel", path)
        )
        homeassistant = types.ModuleType("homeassistant")
        components = types.ModuleType("homeassistant.components")
        components.frontend = fake_frontend
        return {
            "homeassistant": homeassistant,
            "homeassistant.components": components,
            "homeassistant.components.frontend": fake_frontend,
        }


if __name__ == "__main__":
    unittest.main()
