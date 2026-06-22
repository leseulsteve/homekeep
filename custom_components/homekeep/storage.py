"""Versioned Homekeep storage helpers."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Mapping, Optional

from .const import CURRENT_STORAGE_VERSION, STORAGE_KEY
from .models import (
    ChoreCompletion,
    ChoreDefinition,
    ChoreState,
    HomekeepValidationError,
)


class UnsupportedStorageVersionError(HomekeepValidationError):
    """Raised when a store was written by a newer unsupported Homekeep version."""


def empty_store_dict() -> Dict[str, Any]:
    """Return the canonical empty versioned store shape."""

    return {
        "version": CURRENT_STORAGE_VERSION,
        "chores": {},
        "states": {},
        "completions": [],
        "sessions": {},
        "recommendations": {},
        "calendar_context": {},
        "user_preference_stats": {},
        "idempotency_records": {},
    }


@dataclass(frozen=True)
class HomekeepStore:
    """Validated in-memory Homekeep store."""

    version: int = CURRENT_STORAGE_VERSION
    chores: Dict[str, ChoreDefinition] = field(default_factory=dict)
    states: Dict[str, ChoreState] = field(default_factory=dict)
    completions: list[ChoreCompletion] = field(default_factory=list)
    sessions: Dict[str, Any] = field(default_factory=dict)
    recommendations: Dict[str, Any] = field(default_factory=dict)
    calendar_context: Dict[str, Any] = field(default_factory=dict)
    user_preference_stats: Dict[str, Any] = field(default_factory=dict)
    idempotency_records: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(
        cls, data: Mapping[str, Any], now: Optional[datetime] = None
    ) -> "HomekeepStore":
        """Build and validate a store from migrated raw data."""

        chores_raw = data.get("chores", {})
        if not isinstance(chores_raw, Mapping):
            raise HomekeepValidationError("chores must be a mapping")

        chores = {
            chore_id: ChoreDefinition.from_dict(chore_id, chore_data)
            for chore_id, chore_data in chores_raw.items()
        }

        states_raw = data.get("states", {})
        if not isinstance(states_raw, Mapping):
            raise HomekeepValidationError("states must be a mapping")

        states: Dict[str, ChoreState] = {}
        for chore_id, state_data in states_raw.items():
            chore = chores.get(chore_id)
            if chore is None:
                continue
            states[chore_id] = ChoreState.from_dict(
                chore_id, state_data, chore, now=now
            )

        for chore_id, chore in chores.items():
            states.setdefault(chore_id, ChoreState.new_for_chore(chore))

        completions_raw = data.get("completions", [])
        if not isinstance(completions_raw, list):
            raise HomekeepValidationError("completions must be a list")
        completions = [
            ChoreCompletion.from_dict(completion) for completion in completions_raw
        ]

        return cls(
            version=CURRENT_STORAGE_VERSION,
            chores=chores,
            states=states,
            completions=completions,
            sessions=_dict_field(data, "sessions"),
            recommendations=_dict_field(data, "recommendations"),
            calendar_context=_dict_field(data, "calendar_context"),
            user_preference_stats=_dict_field(data, "user_preference_stats"),
            idempotency_records=_dict_field(data, "idempotency_records"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize this store to JSON-safe data."""

        return {
            "version": self.version,
            "chores": {
                chore_id: chore.to_dict() for chore_id, chore in self.chores.items()
            },
            "states": {
                chore_id: state.to_dict() for chore_id, state in self.states.items()
            },
            "completions": [
                completion.to_dict() for completion in self.completions
            ],
            "sessions": copy.deepcopy(self.sessions),
            "recommendations": copy.deepcopy(self.recommendations),
            "calendar_context": copy.deepcopy(self.calendar_context),
            "user_preference_stats": copy.deepcopy(self.user_preference_stats),
            "idempotency_records": copy.deepcopy(self.idempotency_records),
        }


def _dict_field(data: Mapping[str, Any], field_name: str) -> Dict[str, Any]:
    value = data.get(field_name, {})
    if not isinstance(value, Mapping):
        raise HomekeepValidationError(f"{field_name} must be a mapping")
    return copy.deepcopy(dict(value))


def migrate_store_dict(data: Mapping[str, Any]) -> Dict[str, Any]:
    """Run explicit storage migrations and return a current-version store dict."""

    migrated = copy.deepcopy(dict(data))
    version = migrated.get("version")
    if version is None:
        if "states" not in migrated:
            raise HomekeepValidationError("storage version is missing")
        version = 1

    if not isinstance(version, int):
        raise HomekeepValidationError("storage version must be an integer")
    if version > CURRENT_STORAGE_VERSION:
        raise UnsupportedStorageVersionError(
            f"unsupported Homekeep storage version {version}"
        )

    while version < CURRENT_STORAGE_VERSION:
        if version == 1:
            migrated = _migrate_v1_to_v2(migrated)
            version = 2
            migrated["version"] = version
        elif version == 2:
            migrated = _migrate_v2_to_v3(migrated)
            version = 3
            migrated["version"] = version
        else:
            raise UnsupportedStorageVersionError(
                f"unsupported Homekeep storage version {version}"
            )

    for key, value in empty_store_dict().items():
        migrated.setdefault(key, copy.deepcopy(value))
    _normalize_legacy_completion_sources(migrated)
    migrated["version"] = CURRENT_STORAGE_VERSION
    return migrated


def _migrate_v1_to_v2(data: Mapping[str, Any]) -> Dict[str, Any]:
    """Migrate early ChoreState counters to bounded timestamp-list fields."""

    migrated = copy.deepcopy(dict(data))
    states = migrated.setdefault("states", {})
    if not isinstance(states, Mapping):
        raise HomekeepValidationError("states must be a mapping")

    for state in states.values():
        if not isinstance(state, dict):
            continue
        state.setdefault("snoozed_until", None)
        state.setdefault("dismissal_events", [])
        state.setdefault("snooze_events", [])
        state.setdefault("last_dismissed_at", None)
        state.setdefault("last_snoozed_at", None)
        state.pop("recent_dismissals", None)
        state.pop("recent_snoozes", None)

    return migrated


def _migrate_v2_to_v3(data: Mapping[str, Any]) -> Dict[str, Any]:
    """Add bounded learned duration samples to ChoreState."""

    migrated = copy.deepcopy(dict(data))
    states = migrated.setdefault("states", {})
    if not isinstance(states, Mapping):
        raise HomekeepValidationError("states must be a mapping")

    for state in states.values():
        if not isinstance(state, dict):
            continue
        state.setdefault("duration_samples_minutes", [])

    return migrated


def _normalize_legacy_completion_sources(data: Dict[str, Any]) -> None:
    """Normalize former UI source labels in durable completion history."""

    completions = data.get("completions", [])
    if not isinstance(completions, list):
        return
    for completion in completions:
        if isinstance(completion, dict) and completion.get("source") == "bubble_card":
            completion["source"] = "dashboard"


def load_store_dict(
    data: Optional[Mapping[str, Any]], now: Optional[datetime] = None
) -> HomekeepStore:
    """Migrate and validate raw storage data."""

    if data is None:
        data = empty_store_dict()
    migrated = migrate_store_dict(data)
    return HomekeepStore.from_dict(migrated, now=now)


def dump_store_dict(store: HomekeepStore) -> Dict[str, Any]:
    """Serialize a validated store."""

    return store.to_dict()


class HomekeepStorage:
    """Home Assistant storage adapter for the validated Homekeep store."""

    def __init__(self, hass: Any, entry: Any) -> None:
        from homeassistant.helpers.storage import Store

        self.hass = hass
        self.entry = entry
        self.calendar_unsub = None
        self._store = Store(
            hass,
            CURRENT_STORAGE_VERSION,
            f"{STORAGE_KEY}.{entry.entry_id}",
        )
        self.store = load_store_dict(None)
        self.data = dump_store_dict(self.store)

    async def async_load(self) -> HomekeepStore:
        """Load, migrate, validate, and repair Homekeep storage."""

        raw = await self._store.async_load()
        self.store = load_store_dict(raw)
        self.data = dump_store_dict(self.store)

        if raw != self.data:
            await self.async_save()
        return self.store

    async def async_save(self) -> None:
        """Persist the current Homekeep store."""

        self.data = dump_store_dict(self.store)
        await self._store.async_save(self.data)
