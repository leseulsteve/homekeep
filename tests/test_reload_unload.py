"""Tests for Homekeep reload/unload behavior with local Home Assistant fakes."""

from __future__ import annotations

import unittest
from pathlib import Path
from types import SimpleNamespace

from custom_components.homekeep import (
    _async_seed_sample_chores_for_dev_mode,
    _dev_mode_enabled,
    async_unload_entry,
)
from custom_components.homekeep.const import DOMAIN, OPTION_DEV_MODE, PLATFORMS
from custom_components.homekeep.models import ChoreDefinition, ChoreState
from custom_components.homekeep.sensor import HomekeepDueChoreCountSensor
from custom_components.homekeep.binary_sensor import HomekeepChoreDueBinarySensor
from custom_components.homekeep.storage import HomekeepStore, load_sample_chores


ROOT = Path(__file__).resolve().parents[1]


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

    async def test_dev_mode_defaults_enabled_from_entry_data(self) -> None:
        self.assertTrue(_dev_mode_enabled(SimpleNamespace(data={}, options={})))
        self.assertTrue(
            _dev_mode_enabled(
                SimpleNamespace(data={OPTION_DEV_MODE: True}, options={})
            )
        )
        self.assertFalse(
            _dev_mode_enabled(
                SimpleNamespace(
                    data={OPTION_DEV_MODE: True},
                    options={OPTION_DEV_MODE: False},
                )
            )
        )

    async def test_dev_mode_seed_loads_bundled_samples_when_store_is_empty(self) -> None:
        entry = SimpleNamespace(data={OPTION_DEV_MODE: True}, options={})
        storage = FakeStorage()

        await _async_seed_sample_chores_for_dev_mode(storage, entry)

        self.assertGreaterEqual(len(storage.store.chores), 20)
        self.assertIn("empty_compost", storage.store.chores)
        self.assertEqual(set(storage.store.chores), set(storage.store.states))
        self.assertGreater(HomekeepDueChoreCountSensor(storage).native_value, 0)
        self.assertTrue(
            HomekeepChoreDueBinarySensor(storage, "empty_compost").is_on
        )
        self.assertEqual(storage.save_count, 1)

    async def test_dev_mode_seed_does_not_replace_existing_chores(self) -> None:
        entry = SimpleNamespace(data={OPTION_DEV_MODE: True}, options={})
        storage = FakeStorage()
        chore = ChoreDefinition.from_dict("existing_chore", chore_data())
        storage.store.chores["existing_chore"] = chore
        storage.store.states["existing_chore"] = ChoreState.new_for_chore(chore)

        await _async_seed_sample_chores_for_dev_mode(storage, entry)

        self.assertEqual(set(storage.store.chores), {"existing_chore"})
        self.assertEqual(storage.save_count, 0)

    async def test_dev_mode_repairs_existing_unstarted_sample_chores(self) -> None:
        entry = SimpleNamespace(data={OPTION_DEV_MODE: True}, options={})
        storage = FakeStorage()
        sample_chores = load_sample_chores(
            ROOT / "custom_components" / "homekeep" / "sample_chores.yaml"
        )
        storage.store.chores.update(sample_chores)
        storage.store.states.update(
            {
                chore_id: ChoreState.new_for_chore(chore)
                for chore_id, chore in sample_chores.items()
            }
        )

        await _async_seed_sample_chores_for_dev_mode(storage, entry)

        self.assertGreater(HomekeepDueChoreCountSensor(storage).native_value, 0)
        self.assertTrue(
            HomekeepChoreDueBinarySensor(storage, "empty_compost").is_on
        )
        self.assertEqual(storage.save_count, 1)

    async def test_dev_mode_seed_can_be_disabled(self) -> None:
        entry = SimpleNamespace(data={OPTION_DEV_MODE: False}, options={})
        storage = FakeStorage()

        await _async_seed_sample_chores_for_dev_mode(storage, entry)

        self.assertEqual(storage.store.chores, {})
        self.assertEqual(storage.save_count, 0)


if __name__ == "__main__":
    unittest.main()
