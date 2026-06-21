"""Homekeep service runtime used by Home Assistant handlers and tests."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Protocol

from .const import (
    ATTR_AREA_ID,
    ATTR_BUNDLE_ID,
    ATTR_CALENDAR_ENTITY_IDS,
    ATTR_CHORE_ID,
    ATTR_COMPLETED_BY,
    ATTR_ENERGY_LEVEL,
    ATTR_GOAL,
    ATTR_INCLUDE_ALTERNATES,
    ATTR_INFER_MOOD,
    ATTR_MOOD,
    ATTR_OFFER_BONUS_CHORE,
    ATTR_RECOMMENDATION_ID,
    ATTR_RECOMMENDATION_MODE,
    ATTR_RECOMMENDATION_SNAPSHOT_ID,
    ATTR_REPLACE_EXISTING,
    ATTR_REQUEST_ID,
    ATTR_SESSION_ID,
    ATTR_SESSION_ITEM_ID,
    ATTR_SNOOZE_MINUTES,
    ATTR_SOURCE,
    ATTR_STATUS,
    ATTR_TARGET_TIME_WINDOW,
    ATTR_TIME_BUDGET_MINUTES,
    ATTR_USER_ID,
    ATTR_VARIANT,
    SERVICE_ACCEPT_BONUS_CHORE,
    SERVICE_COMPLETE_CHORE,
    SERVICE_DISMISS_CHORE,
    SERVICE_END_SESSION,
    SERVICE_GENERATE_SMART_CHORE_LIST,
    SERVICE_LOAD_SAMPLE_CHORES,
    SERVICE_PAUSE_SESSION,
    SERVICE_REFRESH_CALENDAR_CONTEXT,
    SERVICE_SKIP_CHORE,
    SERVICE_SNOOZE_CHORE,
    SERVICE_START_CHORE_BUNDLE,
    SERVICE_START_RECOMMENDATION,
)
from .calendar_context import (
    CalendarContextEngine,
    calendar_entity_versions_from_hass,
    fetch_calendar_events_from_hass,
    selected_calendar_entity_ids,
)
from .models import ChoreState, HomekeepValidationError
from .recommendations import RecommendationEngine
from .sessions import SessionEngine
from .storage import HomekeepStore, load_sample_chores


class SupportsSave(Protocol):
    """Storage protocol used by the service runtime."""

    store: HomekeepStore

    async def async_save(self) -> None:
        """Persist the current store."""


class HomekeepServiceRuntime:
    """Thin async service facade over the synchronous Homekeep engines."""

    def __init__(self, storage: SupportsSave, hass: Any | None = None) -> None:
        self.storage = storage
        self.hass = hass

    @property
    def store(self) -> HomekeepStore:
        """Return the active in-memory store."""

        return self.storage.store

    async def async_handle(
        self, service_name: str, data: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Handle one validated Home Assistant service call."""

        if service_name == SERVICE_GENERATE_SMART_CHORE_LIST:
            await self._ensure_calendar_context(data)
            result = self._recommendations().generate_smart_chore_list(
                recommendation_mode=data.get(ATTR_RECOMMENDATION_MODE, "ready_now"),
                target_time_window=data.get(ATTR_TARGET_TIME_WINDOW),
                time_budget_minutes=data.get(ATTR_TIME_BUDGET_MINUTES),
                energy_level=data.get(ATTR_ENERGY_LEVEL),
                goal=data.get(ATTR_GOAL),
                area_id=data.get(ATTR_AREA_ID),
                mood=(
                    data.get(ATTR_MOOD)
                    if data.get(ATTR_INFER_MOOD, True)
                    else data.get(ATTR_MOOD)
                ),
                user_id=data.get(ATTR_USER_ID),
                include_alternates=data.get(ATTR_INCLUDE_ALTERNATES, True),
            )
            await self.storage.async_save()
            return result

        if service_name in {
            SERVICE_START_RECOMMENDATION,
            SERVICE_START_CHORE_BUNDLE,
        }:
            recommendation_id = data.get(ATTR_RECOMMENDATION_ID) or data.get(
                ATTR_BUNDLE_ID
            )
            if not recommendation_id:
                raise HomekeepValidationError("recommendation_id is required")
            result = self._recommendations().start_recommendation(
                _required(data, ATTR_RECOMMENDATION_SNAPSHOT_ID),
                recommendation_id,
                user_id=data.get(ATTR_USER_ID),
                request_id=data.get(ATTR_REQUEST_ID),
            )
            await self.storage.async_save()
            return result

        if service_name == SERVICE_COMPLETE_CHORE:
            result = self._sessions().complete_chore(
                _required(data, ATTR_CHORE_ID),
                session_id=data.get(ATTR_SESSION_ID),
                session_item_id=data.get(ATTR_SESSION_ITEM_ID),
                variant=data.get(ATTR_VARIANT, "normal"),
                completed_by=data.get(ATTR_COMPLETED_BY),
                source=data.get(ATTR_SOURCE, "service"),
                request_id=data.get(ATTR_REQUEST_ID),
            )
            await self.storage.async_save()
            return result

        if service_name == SERVICE_SKIP_CHORE:
            session_id = _required(data, ATTR_SESSION_ID)
            session_item_id = _required(data, ATTR_SESSION_ITEM_ID)
            result = self._sessions().skip_chore(
                _required(data, ATTR_CHORE_ID),
                session_id=session_id,
                session_item_id=session_item_id,
                request_id=data.get(ATTR_REQUEST_ID),
            )
            await self.storage.async_save()
            return result

        if service_name == SERVICE_SNOOZE_CHORE:
            result = self._sessions().snooze_chore(
                _required(data, ATTR_CHORE_ID),
                snooze_minutes=_required_int(data, ATTR_SNOOZE_MINUTES),
                session_id=data.get(ATTR_SESSION_ID),
                session_item_id=data.get(ATTR_SESSION_ITEM_ID),
                request_id=data.get(ATTR_REQUEST_ID),
            )
            await self.storage.async_save()
            return result

        if service_name == SERVICE_DISMISS_CHORE:
            result = self._sessions().dismiss_chore(
                _required(data, ATTR_CHORE_ID),
                session_id=data.get(ATTR_SESSION_ID),
                session_item_id=data.get(ATTR_SESSION_ITEM_ID),
                request_id=data.get(ATTR_REQUEST_ID),
            )
            await self.storage.async_save()
            return result

        if service_name == SERVICE_PAUSE_SESSION:
            result = self._sessions().pause_session(
                _required(data, ATTR_SESSION_ID),
                request_id=data.get(ATTR_REQUEST_ID),
            )
            await self.storage.async_save()
            return result

        if service_name == SERVICE_ACCEPT_BONUS_CHORE:
            result = self._sessions().accept_bonus_chore(
                _required(data, ATTR_SESSION_ID),
                _required(data, ATTR_CHORE_ID),
                request_id=data.get(ATTR_REQUEST_ID),
            )
            await self.storage.async_save()
            return result

        if service_name == SERVICE_END_SESSION:
            session_id = _required(data, ATTR_SESSION_ID)
            result = self._sessions().end_session(
                session_id,
                status=_required(data, ATTR_STATUS),
                offer_bonus_chore=data.get(ATTR_OFFER_BONUS_CHORE, False),
                bonus_chore_id=self._bonus_chore_for_session(session_id),
                request_id=data.get(ATTR_REQUEST_ID),
            )
            await self.storage.async_save()
            return result

        if service_name == SERVICE_REFRESH_CALENDAR_CONTEXT:
            result = await self._refresh_calendar_context(data)
            await self.storage.async_save()
            return result

        if service_name == SERVICE_LOAD_SAMPLE_CHORES:
            result = self._load_sample_chores(data)
            await self.storage.async_save()
            return result

        raise HomekeepValidationError(f"unknown Homekeep service: {service_name}")

    def _sessions(self) -> SessionEngine:
        return SessionEngine(self.store)

    def _recommendations(self) -> RecommendationEngine:
        return RecommendationEngine(self.store, self._sessions())

    def _bonus_chore_for_session(self, session_id: str) -> Optional[str]:
        session = self.store.sessions.get(session_id)
        if not session:
            return None
        selected = set(session.get("selected_chores", []))
        for chore_id, chore in sorted(self.store.chores.items()):
            if chore.enabled and chore_id not in selected:
                return chore_id
        return None

    async def _ensure_calendar_context(self, data: dict[str, Any]) -> None:
        entity_ids = self._calendar_entity_ids(data)
        if not entity_ids:
            return
        engine = self._calendar_context_engine()
        if engine.is_fresh(
            entity_ids=entity_ids,
            target_time_window=data.get(ATTR_TARGET_TIME_WINDOW),
            recommendation_mode=data.get(ATTR_RECOMMENDATION_MODE, "ready_now"),
        ):
            return
        await engine.async_refresh(
            entity_ids=entity_ids,
            target_time_window=data.get(ATTR_TARGET_TIME_WINDOW),
            recommendation_mode=data.get(ATTR_RECOMMENDATION_MODE, "ready_now"),
        )

    async def _refresh_calendar_context(self, data: dict[str, Any]) -> dict[str, Any]:
        entity_ids = self._calendar_entity_ids(data)
        context = await self._calendar_context_engine().async_refresh(
            entity_ids=entity_ids,
            target_time_window=data.get(ATTR_TARGET_TIME_WINDOW),
            recommendation_mode=data.get(ATTR_RECOMMENDATION_MODE, "ready_now"),
        )
        return {"status": "refreshed", "calendar_context": context}

    def _calendar_entity_ids(self, data: dict[str, Any]) -> list[str]:
        if ATTR_CALENDAR_ENTITY_IDS in data and data.get(ATTR_CALENDAR_ENTITY_IDS) is not None:
            return list(data.get(ATTR_CALENDAR_ENTITY_IDS) or [])
        entry = getattr(self.storage, "entry", None)
        return selected_calendar_entity_ids(entry)

    def _calendar_context_engine(self) -> CalendarContextEngine:
        if self.hass is None:
            return CalendarContextEngine(self.store)
        return CalendarContextEngine(
            self.store,
            event_provider=lambda entity_ids, start, end: fetch_calendar_events_from_hass(
                self.hass, entity_ids, start, end
            ),
            state_provider=lambda entity_ids: calendar_entity_versions_from_hass(
                self.hass, entity_ids
            ),
        )

    def _load_sample_chores(self, data: dict[str, Any]) -> dict[str, Any]:
        replace_existing = bool(data.get(ATTR_REPLACE_EXISTING, False))
        if self.store.chores and not replace_existing:
            raise HomekeepValidationError(
                "sample chores already loaded; set replace_existing to true to reset"
            )

        chores = load_sample_chores(Path(__file__).with_name("sample_chores.yaml"))
        if replace_existing:
            self.store.chores.clear()
            self.store.states.clear()
            self.store.completions.clear()
            self.store.sessions.clear()
            self.store.recommendations.clear()
            self.store.user_preference_stats.clear()
            self.store.idempotency_records.clear()

        self.store.chores.update(chores)
        for chore_id, chore in chores.items():
            self.store.states.setdefault(chore_id, ChoreState.new_for_chore(chore))

        return {
            "status": "loaded",
            "chore_count": len(chores),
            "chore_ids": sorted(chores),
            "replace_existing": replace_existing,
        }


def _required(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise HomekeepValidationError(f"{key} is required")
    return value


def _required_int(data: dict[str, Any], key: str) -> int:
    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise HomekeepValidationError(f"{key} is required")
    return value
