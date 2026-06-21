"""Chore Session lifecycle helpers."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from threading import RLock
from typing import Any, Callable, Iterable, Optional
from uuid import uuid4

from .health import apply_completion_to_state
from .models import (
    ChoreCompletion,
    HomekeepValidationError,
    prune_event_timestamps,
    resolve_completed_by,
)
from .storage import HomekeepStore


IDEMPOTENCY_TTL_HOURS = 24
MAX_IDEMPOTENCY_RECORDS = 1000
BONUS_CHORE_TTL_MINUTES = 15
TERMINAL_SESSION_STATUSES = {"completed", "cancelled"}
MUTABLE_SESSION_STATUSES = {"active", "paused", "bonus_pending", "bonus_active"}
PLANNED_ITEM_STATUSES = {"pending", "active"}


class SessionLifecycleError(HomekeepValidationError):
    """Raised when a Chore Session mutation is invalid."""


class SessionEngine:
    """Small synchronous mutation engine for Chore Sessions."""

    def __init__(
        self,
        store: HomekeepStore,
        *,
        id_factory: Optional[Callable[[str], str]] = None,
    ) -> None:
        self.store = store
        self._lock = RLock()
        self._id_factory = id_factory or _default_id_factory

    def start_session(
        self,
        chore_ids: Iterable[str],
        *,
        started_at: Optional[datetime] = None,
        started_by: Optional[str] = None,
        participants: Optional[list[str]] = None,
        variants: Optional[dict[str, str]] = None,
        source_recommendation_snapshot_id: Optional[str] = None,
        mode: str = "quick_wins",
        recommendation_mode: str = "ready_now",
        time_budget_minutes: int = 15,
        energy_level: str = "normal",
        request_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Start a Chore Session with materialized Session Items."""

        with self._lock:
            now = started_at or _now()
            return self._idempotent(
                "start_session",
                request_id,
                now,
                lambda: self._start_session(
                    list(chore_ids),
                    now=now,
                    started_by=started_by,
                    participants=participants or [],
                    variants=variants or {},
                    source_recommendation_snapshot_id=source_recommendation_snapshot_id,
                    mode=mode,
                    recommendation_mode=recommendation_mode,
                    time_budget_minutes=time_budget_minutes,
                    energy_level=energy_level,
                ),
            )

    def pause_session(
        self,
        session_id: str,
        *,
        now: Optional[datetime] = None,
        request_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Pause an active Chore Session."""

        with self._lock:
            mutation_time = now or _now()
            return self._idempotent(
                "pause_session",
                request_id,
                mutation_time,
                lambda: self._pause_session(session_id),
            )

    def complete_chore(
        self,
        chore_id: str,
        *,
        session_id: Optional[str] = None,
        session_item_id: Optional[str] = None,
        variant: str = "normal",
        completed_by: Optional[str] = None,
        source: str = "service",
        completed_at: Optional[datetime] = None,
        request_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Complete a Chore, optionally through a materialized session item."""

        with self._lock:
            now = completed_at or _now()
            return self._idempotent(
                "complete_chore",
                request_id,
                now,
                lambda: self._complete_chore(
                    chore_id,
                    session_id=session_id,
                    session_item_id=session_item_id,
                    variant=variant,
                    completed_by=completed_by,
                    source=source,
                    completed_at=now,
                ),
            )

    def skip_chore(
        self,
        chore_id: str,
        *,
        session_id: str,
        session_item_id: str,
        now: Optional[datetime] = None,
        request_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Mark a materialized Session Item skipped."""

        with self._lock:
            mutation_time = now or _now()
            return self._idempotent(
                "skip_chore",
                request_id,
                mutation_time,
                lambda: self._set_item_terminal_status(
                    chore_id, session_id, session_item_id, "skipped"
                ),
            )

    def snooze_chore(
        self,
        chore_id: str,
        *,
        snooze_minutes: int,
        session_id: Optional[str] = None,
        session_item_id: Optional[str] = None,
        now: Optional[datetime] = None,
        request_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Snooze a Chore and optionally mark a Session Item skipped."""

        with self._lock:
            mutation_time = now or _now()
            return self._idempotent(
                "snooze_chore",
                request_id,
                mutation_time,
                lambda: self._snooze_chore(
                    chore_id,
                    snooze_minutes=snooze_minutes,
                    session_id=session_id,
                    session_item_id=session_item_id,
                    now=mutation_time,
                ),
            )

    def dismiss_chore(
        self,
        chore_id: str,
        *,
        session_id: Optional[str] = None,
        session_item_id: Optional[str] = None,
        now: Optional[datetime] = None,
        request_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Dismiss a Chore and optionally mark a Session Item skipped."""

        with self._lock:
            mutation_time = now or _now()
            return self._idempotent(
                "dismiss_chore",
                request_id,
                mutation_time,
                lambda: self._dismiss_chore(
                    chore_id,
                    session_id=session_id,
                    session_item_id=session_item_id,
                    now=mutation_time,
                ),
            )

    def end_session(
        self,
        session_id: str,
        *,
        status: str,
        offer_bonus_chore: bool = False,
        bonus_chore_id: Optional[str] = None,
        now: Optional[datetime] = None,
        request_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """End, cancel, or move a session to bonus_pending."""

        with self._lock:
            mutation_time = now or _now()
            return self._idempotent(
                "end_session",
                request_id,
                mutation_time,
                lambda: self._end_session(
                    session_id,
                    status=status,
                    offer_bonus_chore=offer_bonus_chore,
                    bonus_chore_id=bonus_chore_id,
                    now=mutation_time,
                ),
            )

    def accept_bonus_chore(
        self,
        session_id: str,
        chore_id: str,
        *,
        now: Optional[datetime] = None,
        request_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Accept a pending Bonus Chore."""

        with self._lock:
            mutation_time = now or _now()
            return self._idempotent(
                "accept_bonus_chore",
                request_id,
                mutation_time,
                lambda: self._accept_bonus_chore(session_id, chore_id, mutation_time),
            )

    def _start_session(
        self,
        chore_ids: list[str],
        *,
        now: datetime,
        started_by: Optional[str],
        participants: list[str],
        variants: dict[str, str],
        source_recommendation_snapshot_id: Optional[str],
        mode: str,
        recommendation_mode: str,
        time_budget_minutes: int,
        energy_level: str,
    ) -> dict[str, Any]:
        if not chore_ids:
            raise SessionLifecycleError("session must include at least one chore")

        session_id = self._id_factory("session")
        items: list[dict[str, Any]] = []
        for chore_id in chore_ids:
            chore = self._chore(chore_id)
            variant = variants.get(chore_id, "normal")
            if variant not in chore.variants:
                raise SessionLifecycleError("variant must exist on the Chore")
            items.append(
                {
                    "session_item_id": self._id_factory("item"),
                    "chore_id": chore_id,
                    "variant": variant,
                    "status": "pending",
                    "started_at": None,
                    "completed_at": None,
                    "completed_by": None,
                }
            )

        self.store.sessions[session_id] = {
            "session_id": session_id,
            "source_recommendation_snapshot_id": source_recommendation_snapshot_id,
            "started_at": _iso(now),
            "ended_at": None,
            "started_by": started_by,
            "participants": list(participants),
            "mode": mode,
            "recommendation_mode": recommendation_mode,
            "target_time_window": None,
            "context_fingerprint": None,
            "time_budget_minutes": time_budget_minutes,
            "energy_level": energy_level,
            "location_preference": None,
            "selected_chores": list(chore_ids),
            "items": items,
            "current_chore": items[0]["chore_id"] if items else None,
            "bonus_chore_offered": None,
            "bonus_chore_accepted": False,
            "bonus_chore_expires_at": None,
            "status": "active",
        }
        return self._session_response(session_id)

    def _pause_session(self, session_id: str) -> dict[str, Any]:
        session = self._session(session_id)
        self._expire_bonus_if_needed(session, _now())
        if session["status"] != "active":
            raise SessionLifecycleError("only active sessions can be paused")
        session["status"] = "paused"
        return {"session_id": session_id, "status": "paused"}

    def _complete_chore(
        self,
        chore_id: str,
        *,
        session_id: Optional[str],
        session_item_id: Optional[str],
        variant: str,
        completed_by: Optional[str],
        source: str,
        completed_at: datetime,
    ) -> dict[str, Any]:
        chore = self._chore(chore_id)
        item: Optional[dict[str, Any]] = None
        session: Optional[dict[str, Any]] = None

        if session_id is not None:
            session = self._session(session_id)
            self._expire_bonus_if_needed(session, completed_at)
            if session["status"] not in {"active", "paused", "bonus_active"}:
                raise SessionLifecycleError("session cannot accept completions")

            if session["status"] == "bonus_active":
                if chore_id != session.get("bonus_chore_offered"):
                    raise SessionLifecycleError("bonus_active session only accepts the Bonus Chore")
                item = self._bonus_item(session)
            else:
                if session_item_id is None:
                    raise SessionLifecycleError("session_item_id is required")
                item = self._item(session, session_item_id)
                if item["chore_id"] != chore_id:
                    raise SessionLifecycleError("session item does not match chore_id")
                variant = item["variant"]

            if item["status"] == "done":
                completion = self._completion_for_item(session_id, item["session_item_id"])
                return {
                    "session_id": session_id,
                    "session_item_id": item["session_item_id"],
                    "completion_id": completion["completion_id"] if completion else None,
                    "status": "done",
                    "duplicate": True,
                }
            if item["status"] not in PLANNED_ITEM_STATUSES:
                raise SessionLifecycleError("session item is no longer completable")

            try:
                completed_by = resolve_completed_by(
                    session.get("participants", []),
                    session.get("started_by"),
                    completed_by,
                )
            except HomekeepValidationError as err:
                raise SessionLifecycleError(str(err)) from err

        if variant not in chore.variants:
            raise SessionLifecycleError("variant must exist on the Chore")

        state = self._state(chore_id)
        updated_state = apply_completion_to_state(chore, state, completed_at, variant)
        self.store.states[chore_id] = updated_state

        completion_id = self._id_factory("completion")
        completion = ChoreCompletion(
            completion_id=completion_id,
            chore_id=chore_id,
            session_id=session_id,
            completed_at=completed_at,
            completed_by=completed_by,
            variant=variant,
            credit=chore.variants[variant].credit,
            source=source,
        )
        self.store.completions.append(completion)

        if item is not None and session is not None:
            item["status"] = "done"
            item["completed_at"] = _iso(completed_at)
            item["completed_by"] = completed_by
            item["completion_id"] = completion_id
            if session["status"] == "bonus_active":
                session["status"] = "completed"
                session["ended_at"] = _iso(completed_at)

        return {
            "session_id": session_id,
            "session_item_id": item["session_item_id"] if item else None,
            "completion_id": completion_id,
            "status": "done",
            "completed_by": completed_by,
            "duplicate": False,
        }

    def _set_item_terminal_status(
        self, chore_id: str, session_id: str, session_item_id: str, status: str
    ) -> dict[str, Any]:
        session = self._session(session_id)
        if session["status"] not in {"active", "paused"}:
            raise SessionLifecycleError("session item cannot be changed")
        item = self._item(session, session_item_id)
        if item["chore_id"] != chore_id:
            raise SessionLifecycleError("session item does not match chore_id")
        if item["status"] == "done":
            raise SessionLifecycleError("completed items cannot be changed")
        item["status"] = status
        return {"session_id": session_id, "session_item_id": session_item_id, "status": status}

    def _snooze_chore(
        self,
        chore_id: str,
        *,
        snooze_minutes: int,
        session_id: Optional[str],
        session_item_id: Optional[str],
        now: datetime,
    ) -> dict[str, Any]:
        if not isinstance(snooze_minutes, int) or snooze_minutes < 5 or snooze_minutes > 1440:
            raise SessionLifecycleError("snooze_minutes must be between 5 and 1440")
        self._chore(chore_id)
        if session_id is not None:
            if session_item_id is None:
                raise SessionLifecycleError("session_item_id is required")
            self._set_item_terminal_status(chore_id, session_id, session_item_id, "skipped")

        state = self._state(chore_id)
        self.store.states[chore_id] = replace(
            state,
            snoozed_until=now + timedelta(minutes=snooze_minutes),
            snooze_events=prune_event_timestamps([*state.snooze_events, now], now),
            last_snoozed_at=now,
        )
        return {
            "chore_id": chore_id,
            "snoozed_until": _iso(now + timedelta(minutes=snooze_minutes)),
            "status": "snoozed",
        }

    def _dismiss_chore(
        self,
        chore_id: str,
        *,
        session_id: Optional[str],
        session_item_id: Optional[str],
        now: datetime,
    ) -> dict[str, Any]:
        self._chore(chore_id)
        if session_id is not None:
            if session_item_id is None:
                raise SessionLifecycleError("session_item_id is required")
            session = self._session(session_id)
            if session["status"] not in {"active", "paused", "bonus_pending"}:
                raise SessionLifecycleError("session cannot accept dismissals")
            if session["status"] != "bonus_pending":
                self._set_item_terminal_status(chore_id, session_id, session_item_id, "skipped")

        state = self._state(chore_id)
        self.store.states[chore_id] = replace(
            state,
            dismissal_events=prune_event_timestamps([*state.dismissal_events, now], now),
            last_dismissed_at=now,
        )
        return {"chore_id": chore_id, "status": "dismissed"}

    def _end_session(
        self,
        session_id: str,
        *,
        status: str,
        offer_bonus_chore: bool,
        bonus_chore_id: Optional[str],
        now: datetime,
    ) -> dict[str, Any]:
        if status not in {"completed", "cancelled"}:
            raise SessionLifecycleError("end_session status must be completed or cancelled")
        session = self._session(session_id)
        self._expire_bonus_if_needed(session, now)

        if session["status"] in TERMINAL_SESSION_STATUSES:
            if session["status"] == status:
                return {"session_id": session_id, "status": status, "bonus_chore": None}
            raise SessionLifecycleError("terminal sessions cannot transition")

        if status == "cancelled":
            if session["status"] not in {"active", "paused", "bonus_active"}:
                raise SessionLifecycleError("session cannot be cancelled")
            session["status"] = "cancelled"
            session["ended_at"] = _iso(now)
            return {"session_id": session_id, "status": "cancelled"}

        if offer_bonus_chore:
            if session["status"] not in {"active", "paused"}:
                raise SessionLifecycleError("session cannot offer a Bonus Chore")
            if session.get("bonus_chore_offered") is not None:
                raise SessionLifecycleError("session already offered a Bonus Chore")
            if not _planned_items_complete(session):
                raise SessionLifecycleError("planned session items must be complete")
            if bonus_chore_id is None:
                raise SessionLifecycleError("bonus_chore_id is required")
            self._chore(bonus_chore_id)
            expires_at = now + timedelta(minutes=BONUS_CHORE_TTL_MINUTES)
            session["status"] = "bonus_pending"
            session["bonus_chore_offered"] = bonus_chore_id
            session["bonus_chore_accepted"] = False
            session["bonus_chore_expires_at"] = _iso(expires_at)
            return {
                "session_id": session_id,
                "status": "bonus_pending",
                "bonus_chore": {"chore_id": bonus_chore_id},
                "bonus_chore_expires_at": _iso(expires_at),
            }

        if session["status"] not in {"active", "paused", "bonus_pending"}:
            raise SessionLifecycleError("session cannot be completed")
        session["status"] = "completed"
        session["ended_at"] = _iso(now)
        return {"session_id": session_id, "status": "completed", "bonus_chore": None}

    def _accept_bonus_chore(
        self, session_id: str, chore_id: str, now: datetime
    ) -> dict[str, Any]:
        session = self._session(session_id)
        self._expire_bonus_if_needed(session, now)
        if session["status"] == "completed" and session.get("bonus_chore_expires_at"):
            raise SessionLifecycleError("bonus_chore_expired")
        if session["status"] != "bonus_pending":
            raise SessionLifecycleError("session is not bonus_pending")
        if chore_id != session.get("bonus_chore_offered"):
            raise SessionLifecycleError("Bonus Chore does not match")

        session["status"] = "bonus_active"
        session["bonus_chore_accepted"] = True
        item = {
            "session_item_id": self._id_factory("item"),
            "chore_id": chore_id,
            "variant": "normal",
            "status": "active",
            "started_at": _iso(now),
            "completed_at": None,
            "completed_by": None,
            "bonus": True,
        }
        session["items"].append(item)
        return {
            "session_id": session_id,
            "status": "bonus_active",
            "chore_id": chore_id,
            "session_item_id": item["session_item_id"],
        }

    def _idempotent(
        self,
        operation: str,
        request_id: Optional[str],
        now: datetime,
        mutate: Callable[[], dict[str, Any]],
    ) -> dict[str, Any]:
        self._prune_idempotency(now)
        if not request_id:
            return mutate()
        key = f"{operation}:{request_id}"
        record = self.store.idempotency_records.get(key)
        if record and _parse(record["expires_at"]) > now:
            return record["result"]
        result = mutate()
        self.store.idempotency_records[key] = {
            "request_id": request_id,
            "operation": operation,
            "created_at": _iso(now),
            "expires_at": _iso(now + timedelta(hours=IDEMPOTENCY_TTL_HOURS)),
            "result": result,
        }
        self._prune_idempotency(now)
        return result

    def _prune_idempotency(self, now: datetime) -> None:
        records = self.store.idempotency_records
        expired = [
            key for key, record in records.items() if _parse(record["expires_at"]) <= now
        ]
        for key in expired:
            records.pop(key, None)
        if len(records) <= MAX_IDEMPOTENCY_RECORDS:
            return
        ordered = sorted(records.items(), key=lambda item: _parse(item[1]["created_at"]))
        for key, _record in ordered[: len(records) - MAX_IDEMPOTENCY_RECORDS]:
            records.pop(key, None)

    def _session(self, session_id: str) -> dict[str, Any]:
        session = self.store.sessions.get(session_id)
        if session is None:
            raise SessionLifecycleError("unknown session_id")
        return session

    def _chore(self, chore_id: str):
        chore = self.store.chores.get(chore_id)
        if chore is None:
            raise SessionLifecycleError("unknown chore_id")
        return chore

    def _state(self, chore_id: str):
        state = self.store.states.get(chore_id)
        if state is None:
            from .models import ChoreState

            state = ChoreState.new_for_chore(self._chore(chore_id))
            self.store.states[chore_id] = state
        return state

    def _item(self, session: dict[str, Any], session_item_id: str) -> dict[str, Any]:
        for item in session["items"]:
            if item["session_item_id"] == session_item_id:
                return item
        raise SessionLifecycleError("unknown session_item_id")

    def _bonus_item(self, session: dict[str, Any]) -> dict[str, Any]:
        for item in session["items"]:
            if item.get("bonus"):
                return item
        raise SessionLifecycleError("Bonus Chore has not been accepted")

    def _completion_for_item(
        self, session_id: str, session_item_id: str
    ) -> Optional[dict[str, Any]]:
        session = self._session(session_id)
        item = self._item(session, session_item_id)
        completion_id = item.get("completion_id")
        if completion_id is None:
            return None
        for completion in self.store.completions:
            if completion.completion_id == completion_id:
                return completion.to_dict()
        return None

    def _expire_bonus_if_needed(self, session: dict[str, Any], now: datetime) -> None:
        if session["status"] != "bonus_pending":
            return
        expires_at = session.get("bonus_chore_expires_at")
        if expires_at and now >= _parse(expires_at):
            session["status"] = "completed"
            session["ended_at"] = _iso(now)
            session["bonus_chore_accepted"] = False

    def _session_response(self, session_id: str) -> dict[str, Any]:
        session = self._session(session_id)
        return {
            "session_id": session_id,
            "source_recommendation_snapshot_id": session.get(
                "source_recommendation_snapshot_id"
            ),
            "status": session["status"],
            "items": [
                {
                    "session_item_id": item["session_item_id"],
                    "chore_id": item["chore_id"],
                    "variant": item["variant"],
                    "status": item["status"],
                    "estimated_minutes": self._chore(item["chore_id"]).estimated_minutes,
                    "area_id": self._chore(item["chore_id"]).area_id,
                }
                for item in session["items"]
            ],
        }


def _planned_items_complete(session: dict[str, Any]) -> bool:
    return all(
        item["status"] == "done"
        for item in session["items"]
        if not item.get("bonus")
    )


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(value: datetime) -> str:
    return value.isoformat()


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _default_id_factory(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"
