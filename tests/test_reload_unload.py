"""Tests for Homekeep reload/unload behavior with local Home Assistant fakes."""

from __future__ import annotations

import unittest
from types import SimpleNamespace

from custom_components.homekeep import async_unload_entry
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
        self.calendar_unsub = self._calendar_unsub

    def _calendar_unsub(self) -> None:
        self.unsub_count += 1


class ReloadUnloadTest(unittest.IsolatedAsyncioTestCase):
    async def test_unload_removes_entry_storage_and_calendar_listener(self) -> None:
        entry = SimpleNamespace(entry_id="entry-1")
        storage = FakeStorage()
        hass = SimpleNamespace(
            data={DOMAIN: {entry.entry_id: storage}},
            config_entries=FakeConfigEntries(unload_ok=True),
        )

        unloaded = await async_unload_entry(hass, entry)

        self.assertTrue(unloaded)
        self.assertEqual(storage.unsub_count, 1)
        self.assertEqual(hass.config_entries.calls, [(entry, PLATFORMS)])
        self.assertNotIn(DOMAIN, hass.data)

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


if __name__ == "__main__":
    unittest.main()
