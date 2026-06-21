"""Calendar Context snapshot derivation and freshness helpers."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Awaitable, Callable, Iterable, Mapping
from datetime import date, datetime, time, timedelta, timezone
from typing import Any, Optional

from .models import HomekeepValidationError, parse_datetime
from .storage import HomekeepStore
from .text_signals import (
    CALENDAR_GUEST_KEYWORDS,
    CALENDAR_TRAVEL_KEYWORDS,
    TRASH_KEYWORDS,
    has_any_keyword,
    normalize_guess_text,
)


OPTION_CALENDAR_ENTITY_IDS = "calendar_entity_ids"
READY_NOW_MAX_AGE = timedelta(minutes=15)
SCHEDULED_MAX_AGE = timedelta(minutes=60)
READY_NOW_LOOKAHEAD = timedelta(hours=24)
SCHEDULED_LOOKAHEAD = timedelta(days=7)
CalendarEventProvider = Callable[
    [list[str], datetime, datetime], Awaitable[Mapping[str, list[Any]]]
]
CalendarStateProvider = Callable[[list[str]], Mapping[str, Mapping[str, Any]]]


class CalendarContextError(HomekeepValidationError):
    """Raised when Calendar Context refresh or validation fails."""


class CalendarContextEngine:
    """Build and invalidate minimized Calendar Context snapshots."""

    def __init__(
        self,
        store: HomekeepStore,
        *,
        event_provider: Optional[CalendarEventProvider] = None,
        state_provider: Optional[CalendarStateProvider] = None,
    ) -> None:
        self.store = store
        self._event_provider = event_provider or _empty_event_provider
        self._state_provider = state_provider or _empty_state_provider

    async def async_refresh(
        self,
        *,
        entity_ids: Iterable[str],
        target_time_window: Optional[str] = None,
        recommendation_mode: str = "ready_now",
        now: Optional[datetime] = None,
    ) -> dict[str, Any]:
        """Refresh and store a minimized Calendar Context snapshot."""

        snapshot_time = now or _now()
        selected = normalize_calendar_entity_ids(entity_ids)
        start, end = _event_window(
            snapshot_time,
            target_time_window=target_time_window,
            recommendation_mode=recommendation_mode,
        )
        versions = {
            entity_id: dict(version)
            for entity_id, version in self._state_provider(selected).items()
        }
        events_by_entity = await self._event_provider(selected, start, end)
        derived = derive_calendar_signals(events_by_entity, now=snapshot_time)
        event_fingerprint = calendar_event_fingerprint(
            events_by_entity,
            now=snapshot_time,
        )
        expires_at = _expires_at(
            snapshot_time,
            recommendation_mode=recommendation_mode,
            derived=derived,
        )
        context_version = calendar_context_version(
            versions,
            {
                "target_time_window": target_time_window,
                "recommendation_mode": recommendation_mode,
                "source_calendar_event_fingerprint": event_fingerprint,
                "derived": {
                    key: derived[key]
                    for key in (
                        "has_guests_soon",
                        "free_window_minutes",
                        "leaving_home_soon",
                        "trash_day_tomorrow",
                        "busy_evening",
                    )
                },
            },
        )
        snapshot_id = f"calendar_{context_version[4:20]}"
        snapshot = {
            "snapshot_id": snapshot_id,
            "calendar_context_id": snapshot_id,
            "calendar_context_version": context_version,
            "created_at": snapshot_time.isoformat(),
            "expires_at": expires_at.isoformat(),
            "target_time_window": target_time_window,
            "recommendation_mode": recommendation_mode,
            "has_guests_soon": derived["has_guests_soon"],
            "free_window_minutes": derived["free_window_minutes"],
            "leaving_home_soon": derived["leaving_home_soon"],
            "trash_day_tomorrow": derived["trash_day_tomorrow"],
            "busy_evening": derived["busy_evening"],
            "event_count": derived["event_count"],
            "source_calendar_entities": selected,
            "source_calendar_versions": versions,
            "source_calendar_event_fingerprint": event_fingerprint,
            "invalidated_at": None,
            "invalidation_reason": None,
            "diagnostics": {
                "raw_event_details_stored": False,
                "calendar_entity_count": len(selected),
            },
        }
        old_snapshot_id = self.store.calendar_context.get("snapshot_id")
        old_version = self.store.calendar_context.get("calendar_context_version")
        if (
            old_snapshot_id
            and old_version
            and old_version != context_version
            and not self.store.calendar_context.get("invalidated_at")
        ):
            invalidate_recommendations_for_calendar_context(
                self.store,
                old_snapshot_id,
                "calendar_context_refreshed",
            )
        self.store.calendar_context.clear()
        self.store.calendar_context.update(snapshot)
        return snapshot

    async def async_is_fresh(
        self,
        *,
        entity_ids: Iterable[str],
        target_time_window: Optional[str] = None,
        recommendation_mode: str = "ready_now",
        now: Optional[datetime] = None,
    ) -> bool:
        """Return whether the stored Calendar Context can be reused.

        This checks both Home Assistant calendar entity state metadata and a
        minimized event fingerprint, because calendar event edits may not
        change the entity state when the calendar remains off.
        """

        snapshot_time = now or _now()
        selected = normalize_calendar_entity_ids(entity_ids)
        if not self.is_fresh(
            entity_ids=selected,
            target_time_window=target_time_window,
            recommendation_mode=recommendation_mode,
            now=snapshot_time,
        ):
            return False
        fingerprint = self.store.calendar_context.get(
            "source_calendar_event_fingerprint"
        )
        if not fingerprint:
            return False
        created_at = parse_datetime(
            self.store.calendar_context.get("created_at"),
            "created_at",
        )
        if created_at is None:
            return False
        start, end = _event_window(
            created_at,
            target_time_window=target_time_window,
            recommendation_mode=recommendation_mode,
        )
        events_by_entity = await self._event_provider(selected, start, end)
        return (
            calendar_event_fingerprint(events_by_entity, now=created_at)
            == fingerprint
        )

    def is_fresh(
        self,
        *,
        entity_ids: Iterable[str],
        target_time_window: Optional[str] = None,
        recommendation_mode: str = "ready_now",
        now: Optional[datetime] = None,
    ) -> bool:
        """Return whether the current stored Calendar Context can be reused."""

        snapshot = self.store.calendar_context
        if not snapshot:
            return False
        return is_calendar_context_fresh(
            snapshot,
            entity_ids=normalize_calendar_entity_ids(entity_ids),
            current_versions=self._state_provider(
                normalize_calendar_entity_ids(entity_ids)
            ),
            target_time_window=target_time_window,
            recommendation_mode=recommendation_mode,
            now=now or _now(),
        )


def selected_calendar_entity_ids(entry: Any) -> list[str]:
    """Return selected calendar entity ids from a Home Assistant config entry."""

    options = getattr(entry, "options", {}) or {}
    return normalize_calendar_entity_ids(options.get(OPTION_CALENDAR_ENTITY_IDS, []))


def normalize_calendar_entity_ids(entity_ids: Iterable[str] | None) -> list[str]:
    """Normalize selected calendar entity ids."""

    if not entity_ids:
        return []
    normalized = []
    for entity_id in entity_ids:
        if not isinstance(entity_id, str) or not entity_id:
            raise CalendarContextError("calendar_entity_ids must contain strings")
        normalized.append(entity_id.lower())
    return sorted(dict.fromkeys(normalized))


def calendar_entity_versions_from_hass(hass: Any, entity_ids: list[str]) -> dict[str, Any]:
    """Read minimal source calendar versions from Home Assistant state metadata."""

    versions: dict[str, Any] = {}
    for entity_id in entity_ids:
        state = hass.states.get(entity_id)
        if state is None:
            versions[entity_id] = {
                "state": None,
                "last_changed": None,
                "last_updated": None,
            }
            continue
        versions[entity_id] = calendar_entity_version_from_state(state)
    return versions


def calendar_entity_version_from_state(state: Any) -> dict[str, Any]:
    """Return the state metadata needed to detect calendar changes."""

    return {
        "state": getattr(state, "state", None),
        "last_changed": _iso(getattr(state, "last_changed", None)),
        "last_updated": _iso(getattr(state, "last_updated", None)),
    }


async def fetch_calendar_events_from_hass(
    hass: Any, entity_ids: list[str], start: datetime, end: datetime
) -> Mapping[str, list[Any]]:
    """Fetch calendar events through Home Assistant's calendar service."""

    if not entity_ids:
        return {}
    response = await hass.services.async_call(
        "calendar",
        "get_events",
        {
            "entity_id": entity_ids,
            "start_date_time": start.isoformat(),
            "end_date_time": end.isoformat(),
        },
        blocking=True,
        return_response=True,
    )
    events: dict[str, list[Any]] = {}
    if not isinstance(response, Mapping):
        return events
    for entity_id in entity_ids:
        payload = response.get(entity_id, {})
        if isinstance(payload, Mapping):
            raw_events = payload.get("events", [])
            events[entity_id] = list(raw_events) if isinstance(raw_events, list) else []
    return events


def is_calendar_context_fresh(
    snapshot: Mapping[str, Any],
    *,
    entity_ids: Iterable[str],
    current_versions: Mapping[str, Mapping[str, Any]],
    target_time_window: Optional[str],
    recommendation_mode: str,
    now: datetime,
) -> bool:
    """Return whether a Calendar Context snapshot is reusable."""

    if snapshot.get("invalidated_at"):
        return False
    expires_at = parse_datetime(snapshot.get("expires_at"), "expires_at")
    if expires_at is None or now >= expires_at:
        return False
    if snapshot.get("target_time_window") != target_time_window:
        return False
    if snapshot.get("recommendation_mode", "ready_now") != recommendation_mode:
        return False
    if list(snapshot.get("source_calendar_entities", [])) != list(entity_ids):
        return False
    return dict(snapshot.get("source_calendar_versions", {})) == {
        key: dict(value) for key, value in current_versions.items()
    }


def invalidate_calendar_context_for_entity(
    store: HomekeepStore,
    entity_id: str,
    *,
    now: Optional[datetime] = None,
    reason: str = "calendar_entity_changed",
) -> bool:
    """Invalidate the current Calendar Context if it depends on an entity."""

    snapshot = store.calendar_context
    normalized = entity_id.lower()
    if not snapshot or normalized not in snapshot.get("source_calendar_entities", []):
        return False
    if snapshot.get("invalidated_at"):
        return False
    snapshot["invalidated_at"] = (now or _now()).isoformat()
    snapshot["invalidation_reason"] = reason
    invalidate_recommendations_for_calendar_context(store, snapshot["snapshot_id"], reason)
    return True


def invalidate_recommendations_for_calendar_context(
    store: HomekeepStore, calendar_context_id: str, reason: str
) -> None:
    """Invalidate RecommendationSnapshots that used a Calendar Context."""

    for snapshot in store.recommendations.values():
        if snapshot.get("invalidated_at"):
            continue
        if snapshot.get("calendar_context_id") == calendar_context_id:
            snapshot["invalidated_at"] = _now().isoformat()
            snapshot["invalidation_reason"] = reason


def derive_calendar_signals(
    events_by_entity: Mapping[str, list[Any]], *, now: datetime
) -> dict[str, Any]:
    """Convert raw calendar events into minimized derived signals."""

    has_guests = False
    leaving_home = False
    trash_day_tomorrow = False
    busy_evening = False
    relevant_boundaries: list[datetime] = []
    event_ranges: list[tuple[datetime, datetime]] = []
    event_count = 0

    for events in events_by_entity.values():
        for event in events:
            event_count += 1
            start = _event_datetime(event, "start")
            end = _event_datetime(event, "end")
            if start and end:
                event_ranges.append((start, end))
            text = _event_text(event)
            is_guest = has_any_keyword(text, CALENDAR_GUEST_KEYWORDS)
            is_travel = has_any_keyword(text, CALENDAR_TRAVEL_KEYWORDS)
            is_trash = has_any_keyword(text, TRASH_KEYWORDS)
            if is_guest:
                has_guests = True
            if is_travel:
                leaving_home = True
            if is_trash and start and 0 <= (start.date() - now.date()).days <= 1:
                trash_day_tomorrow = True
            if start and _is_evening(start):
                busy_evening = True
            if start and (is_guest or is_travel or is_trash):
                relevant_boundaries.append(start)

    free_window_minutes = _largest_free_window_minutes(now, event_ranges)
    return {
        "has_guests_soon": has_guests,
        "free_window_minutes": free_window_minutes,
        "leaving_home_soon": leaving_home,
        "trash_day_tomorrow": trash_day_tomorrow,
        "busy_evening": busy_evening,
        "event_count": event_count,
        "next_relevant_boundary": min(relevant_boundaries).isoformat()
        if relevant_boundaries
        else None,
    }


def calendar_context_version(
    versions: Mapping[str, Any], derived_fingerprint: Mapping[str, Any]
) -> str:
    """Return a stable version hash for non-raw Calendar Context facts."""

    payload = json.dumps(
        {"versions": versions, "derived": derived_fingerprint},
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return f"cal:{hashlib.sha256(payload.encode()).hexdigest()[:16]}"


def calendar_event_fingerprint(
    events_by_entity: Mapping[str, list[Any]], *, now: datetime
) -> str:
    """Hash minimized event facts without storing raw event text."""

    event_facts: dict[str, list[dict[str, Any]]] = {}
    for entity_id, events in events_by_entity.items():
        facts = []
        for event in events:
            start = _event_datetime(event, "start")
            end = _event_datetime(event, "end")
            text = _event_text(event)
            facts.append(
                {
                    "start": start.isoformat() if start else None,
                    "end": end.isoformat() if end else None,
                    "guest": has_any_keyword(text, CALENDAR_GUEST_KEYWORDS),
                    "travel": has_any_keyword(text, CALENDAR_TRAVEL_KEYWORDS),
                    "trash": has_any_keyword(text, TRASH_KEYWORDS),
                    "evening": bool(start and _is_evening(start)),
                }
            )
        event_facts[entity_id] = sorted(
            facts,
            key=lambda item: (
                item["start"] or "",
                item["end"] or "",
                str(item["guest"]),
                str(item["travel"]),
                str(item["trash"]),
                str(item["evening"]),
            ),
        )

    derived = derive_calendar_signals(events_by_entity, now=now)
    payload = json.dumps(
        {
            "events": event_facts,
            "derived": {
                "has_guests_soon": derived["has_guests_soon"],
                "leaving_home_soon": derived["leaving_home_soon"],
                "trash_day_tomorrow": derived["trash_day_tomorrow"],
                "busy_evening": derived["busy_evening"],
                "event_count": derived["event_count"],
            },
        },
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return f"calevt:{hashlib.sha256(payload.encode()).hexdigest()[:16]}"


def _event_window(
    now: datetime,
    *,
    target_time_window: Optional[str],
    recommendation_mode: str,
) -> tuple[datetime, datetime]:
    if target_time_window:
        parsed = _parse_target_time_window(target_time_window)
        if parsed:
            return parsed
    lookahead = (
        SCHEDULED_LOOKAHEAD
        if recommendation_mode == "scheduled_suggestion"
        else READY_NOW_LOOKAHEAD
    )
    return now, now + lookahead


def _parse_target_time_window(value: str) -> Optional[tuple[datetime, datetime]]:
    start_raw, separator, end_raw = value.partition("/")
    if not separator:
        return None
    start = parse_datetime(start_raw, "target_time_window.start")
    end = parse_datetime(end_raw, "target_time_window.end")
    if start is None or end is None or end <= start:
        return None
    return start, end


def _expires_at(
    now: datetime, *, recommendation_mode: str, derived: Mapping[str, Any]
) -> datetime:
    max_age = (
        SCHEDULED_MAX_AGE
        if recommendation_mode == "scheduled_suggestion"
        else READY_NOW_MAX_AGE
    )
    expires = now + max_age
    boundary = parse_datetime(derived.get("next_relevant_boundary"), "boundary")
    if boundary and now < boundary < expires:
        return boundary
    return expires


def _event_text(event: Any) -> str:
    parts = []
    for field in ("summary", "message", "description", "location"):
        value = _event_value(event, field)
        if value:
            parts.append(str(value))
    return normalize_guess_text(" ".join(parts))


def _event_datetime(event: Any, field: str) -> Optional[datetime]:
    value = _event_value(event, field)
    if isinstance(value, date) and not isinstance(value, datetime):
        return datetime.combine(value, time.min, tzinfo=timezone.utc)
    return parse_datetime(value, field) if value is not None else None


def _event_value(event: Any, field: str) -> Any:
    if isinstance(event, Mapping):
        return event.get(field)
    return getattr(event, field, None)


def _is_evening(value: datetime) -> bool:
    return 17 <= value.hour < 22


def _largest_free_window_minutes(
    now: datetime, event_ranges: list[tuple[datetime, datetime]]
) -> Optional[int]:
    if not event_ranges:
        return None
    ordered = sorted(event_ranges)
    largest = 0
    cursor = now
    for start, end in ordered:
        if start > cursor:
            largest = max(largest, int((start - cursor).total_seconds() // 60))
        if end > cursor:
            cursor = end
    return largest


async def _empty_event_provider(
    entity_ids: list[str], start: datetime, end: datetime
) -> Mapping[str, list[Any]]:
    return {entity_id: [] for entity_id in entity_ids}


def _empty_state_provider(entity_ids: list[str]) -> Mapping[str, Mapping[str, Any]]:
    return {
        entity_id: {"state": None, "last_changed": None, "last_updated": None}
        for entity_id in entity_ids
    }


def _iso(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def _now() -> datetime:
    return datetime.now(timezone.utc)
