"""Deterministic Recommendation Engine V1."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from .health import clamp_score, projected_impact, priority_staleness
from .history import context_bucket, history_fit_score
from .models import ChoreDefinition, ChoreState, prune_event_timestamps
from .sessions import SessionEngine
from .storage import HomekeepStore
from .text_signals import (
    GUEST_PREP_CHORE_KEYWORDS,
    TRASH_KEYWORDS,
    has_any_keyword,
    normalize_guess_text,
)


SNAPSHOT_TTL_MINUTES = 30


class RecommendationError(ValueError):
    """Raised when recommendation generation or materialization is invalid."""


def context_fingerprint(payload: dict[str, Any]) -> str:
    """Return a versioned deterministic context fingerprint."""

    normalized = _normalize_fingerprint_payload(payload)
    encoded = json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode()
    return f"ctx:v1:{hashlib.sha256(encoded).hexdigest()}"


class RecommendationEngine:
    """Generate and materialize deterministic Smart Chore Lists."""

    def __init__(
        self, store: HomekeepStore, session_engine: Optional[SessionEngine] = None
    ) -> None:
        self.store = store
        self.session_engine = session_engine or SessionEngine(store)

    def generate_smart_chore_list(
        self,
        *,
        now: Optional[datetime] = None,
        recommendation_mode: str = "ready_now",
        target_time_window: Optional[str] = None,
        time_budget_minutes: Optional[int] = None,
        energy_level: Optional[str] = None,
        goal: Optional[str] = None,
        area_id: Optional[str] = None,
        mood: Optional[str] = None,
        user_id: Optional[str] = None,
        include_alternates: bool = True,
    ) -> dict[str, Any]:
        """Generate and store a Smart Chore List result."""

        created_at = now or _now()
        enabled_chores = {
            chore_id: chore
            for chore_id, chore in self.store.chores.items()
            if chore.enabled
            and not _is_snoozed(self.store.states.get(chore_id), created_at)
        }
        calendar_context = _fresh_calendar_context(self.store.calendar_context, created_at)
        fingerprint_payload = {
            "schema_version": 1,
            "recommendation_mode": recommendation_mode,
            "target_time_window": target_time_window,
            "time_budget_minutes": time_budget_minutes,
            "energy_level": energy_level,
            "goal": goal,
            "area_id": area_id,
            "mood": mood,
            "calendar_context_id": (
                calendar_context.get("calendar_context_id")
                if calendar_context
                else None
            ),
            "calendar_context_version": (
                calendar_context.get("calendar_context_version")
                if calendar_context
                else None
            ),
            "chore_definition_version": "v1",
            "enabled_chore_ids": sorted(enabled_chores),
            "home_assistant_area_ids": sorted(
                {chore.area_id for chore in enabled_chores.values() if chore.area_id}
            ),
            "user_id": user_id,
        }
        fingerprint = context_fingerprint(fingerprint_payload)
        snapshot_id = _stable_id("snapshot", fingerprint, created_at.isoformat())
        expires_at = created_at + timedelta(minutes=SNAPSHOT_TTL_MINUTES)
        bucket = context_bucket(
            recommendation_mode=recommendation_mode,
            when=created_at,
            energy_level=energy_level,
            goal=goal,
            area_id=area_id,
            mood=mood,
        )

        scored = [
            self._score_chore(
                chore,
                snapshot_id=snapshot_id,
                expires_at=expires_at,
                now=created_at,
                time_budget_minutes=time_budget_minutes,
                energy_level=energy_level,
                area_id=area_id,
                calendar_context=calendar_context,
                bucket=bucket,
                user_id=user_id,
            )
            for chore in enabled_chores.values()
        ]
        scored.sort(
            key=lambda item: (-item["score"], item["estimated_minutes"], item["title"])
        )

        best_single = _with_kind(scored[0], "single") if scored else None
        easiest = _with_kind(
            sorted(
                scored,
                key=lambda item: (
                    item["estimated_minutes"],
                    -item["score"],
                    item["title"],
                ),
            )[0],
            "easiest",
        ) if scored else None
        best_bundle = self._best_bundle(scored, snapshot_id, expires_at)

        used_chore_ids = {
            item["chore_id"]
            for rec in (best_single, easiest, best_bundle)
            if rec is not None
            for item in rec["chore_items"]
        }
        alternates = (
            [
                _with_kind(item, "alternate")
                for item in scored
                if item["chore_items"][0]["chore_id"] not in used_chore_ids
            ][:3]
            if include_alternates
            else []
        )

        result = {
            "snapshot_id": snapshot_id,
            "recommendation_mode": recommendation_mode,
            "target_time_window": target_time_window,
            "expires_at": expires_at.isoformat(),
            "mood_context": None,
            "best_bundle": best_bundle,
            "best_single_chore": best_single,
            "easiest_chore": easiest,
            "alternates": alternates,
            "empty_state": (
                None
                if scored
                else {
                    "message": "No useful chore fits this session.",
                    "actions": [
                        "loosen_filters",
                        "show_due",
                        "schedule_later",
                        "end_now",
                    ],
                }
            ),
        }
        snapshot = {
            "snapshot_id": snapshot_id,
            "created_at": created_at.isoformat(),
            "recommendation_mode": recommendation_mode,
            "context_fingerprint": fingerprint,
            "context_bucket": bucket,
            "mood_context": None,
            "candidate_scores": [item["score_breakdown"] for item in scored],
            "selected_recommendations": [
                rec for rec in [best_bundle, best_single, easiest, *alternates] if rec
            ],
            "explanations": [
                rec["reason"] for rec in [best_bundle, best_single, easiest, *alternates] if rec
            ],
            "expires_at": expires_at.isoformat(),
            "invalidated_at": None,
            "invalidation_reason": None,
            "materialized_session_id": None,
            "calendar_context_id": (
                calendar_context.get("calendar_context_id")
                if calendar_context
                else None
            ),
            "calendar_context_version": (
                calendar_context.get("calendar_context_version")
                if calendar_context
                else None
            ),
            "result": result,
        }
        self.store.recommendations[snapshot_id] = snapshot
        return result

    def start_recommendation(
        self,
        snapshot_id: str,
        recommendation_id: str,
        *,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        now: Optional[datetime] = None,
    ) -> dict[str, Any]:
        """Materialize a fresh RecommendationSnapshot into a Chore Session."""

        mutation_time = now or _now()
        snapshot = self._fresh_snapshot(snapshot_id, mutation_time)
        if snapshot.get("materialized_session_id"):
            raise RecommendationError("recommendation snapshot already materialized")
        recommendation = _find_recommendation(snapshot, recommendation_id)
        if recommendation is None:
            raise RecommendationError("unknown recommendation_id")

        chore_ids = [item["chore_id"] for item in recommendation["chore_items"]]
        variants = {
            item["chore_id"]: item["variant"] for item in recommendation["chore_items"]
        }
        result = self.session_engine.start_session(
            chore_ids,
            started_at=mutation_time,
            started_by=user_id,
            participants=[user_id] if user_id else [],
            variants=variants,
            source_recommendation_snapshot_id=snapshot_id,
            recommendation_mode=snapshot["recommendation_mode"],
            request_id=request_id,
        )
        session = self.store.sessions[result["session_id"]]
        session["context_fingerprint"] = snapshot["context_fingerprint"]
        snapshot["materialized_session_id"] = result["session_id"]
        return result

    def invalidate_snapshot(
        self, snapshot_id: str, *, reason: str, now: Optional[datetime] = None
    ) -> None:
        """Invalidate a stored RecommendationSnapshot."""

        snapshot = self.store.recommendations.get(snapshot_id)
        if snapshot is None:
            raise RecommendationError("unknown snapshot_id")
        snapshot["invalidated_at"] = (now or _now()).isoformat()
        snapshot["invalidation_reason"] = reason

    def _fresh_snapshot(self, snapshot_id: str, now: datetime) -> dict[str, Any]:
        snapshot = self.store.recommendations.get(snapshot_id)
        if snapshot is None:
            raise RecommendationError("unknown snapshot_id")
        if snapshot.get("invalidated_at"):
            raise RecommendationError("recommendation snapshot is invalidated")
        if now >= _parse(snapshot["expires_at"]):
            raise RecommendationError("recommendation snapshot is expired")
        return snapshot

    def _score_chore(
        self,
        chore: ChoreDefinition,
        *,
        snapshot_id: str,
        expires_at: datetime,
        now: datetime,
        time_budget_minutes: Optional[int],
        energy_level: Optional[str],
        area_id: Optional[str],
        calendar_context: Optional[dict[str, Any]],
        bucket: str,
        user_id: Optional[str],
    ) -> dict[str, Any]:
        state = self.store.states.get(chore.id) or ChoreState.new_for_chore(chore)
        stale = clamp_score(priority_staleness(chore, state, now))
        impact = projected_impact(chore, state, now)
        time_fit = _time_fit(chore.estimated_minutes, time_budget_minutes)
        energy_fit = _energy_fit(chore.energy, energy_level)
        area_fit = (
            100.0
            if area_id and chore.area_id == area_id
            else 50.0
            if area_id is None
            else 0.0
        )
        history = history_fit_score(
            self.store.user_preference_stats.values(),
            bucket=bucket,
            chore_id=chore.id,
            area_id=chore.area_id,
            user_id=user_id,
        )
        calendar_score = _calendar_context_score(chore, calendar_context)
        penalty = _dismissal_penalty(state, now, priority_staleness(chore, state, now))
        total = clamp_score(
            stale * 0.30
            + impact * 0.25
            + time_fit * 0.15
            + energy_fit * 0.10
            + area_fit * 0.10
            + calendar_score * 0.05
            + history * 0.05
            - penalty
        )
        recommendation_id = _stable_id("rec", snapshot_id, chore.id, "normal")
        reason = _reason(chore, stale, impact, time_fit, history)
        return {
            "recommendation_id": recommendation_id,
            "kind": "single",
            "title": chore.name,
            "estimated_minutes": chore.estimated_minutes,
            "chore_items": [_item_payload(chore)],
            "projected_impact": {
                "home_health_delta": round(impact, 3),
                "area_health_delta": (
                    {chore.area_id: round(impact, 3)} if chore.area_id else {}
                ),
            },
            "reason": reason,
            "score": round(total, 3),
            "source_snapshot_id": snapshot_id,
            "expires_at": expires_at.isoformat(),
            "score_breakdown": {
                "recommendation_id": recommendation_id,
                "total_score": round(total, 3),
                "components": {
                    "staleness_score": round(stale, 3),
                    "health_impact_score": round(impact, 3),
                    "time_fit_score": round(time_fit, 3),
                    "energy_fit_score": round(energy_fit, 3),
                    "area_fit_score": round(area_fit, 3),
                    "calendar_context_score": round(calendar_score, 3),
                    "history_fit_score": round(history, 3),
                    "dismissal_penalty": round(penalty, 3),
                },
            },
        }

    def _best_bundle(
        self, scored: list[dict[str, Any]], snapshot_id: str, expires_at: datetime
    ) -> Optional[dict[str, Any]]:
        if len(scored) < 2:
            return None
        first = scored[0]
        second = next(
            (
                candidate
                for candidate in scored[1:]
                if candidate["chore_items"][0]["area_id"]
                == first["chore_items"][0]["area_id"]
            ),
            scored[1],
        )
        items = [first["chore_items"][0], second["chore_items"][0]]
        score = round((first["score"] + second["score"]) / 2, 3)
        area_delta: dict[str, float] = {}
        for rec in (first, second):
            for area, delta in rec["projected_impact"]["area_health_delta"].items():
                area_delta[area] = round(area_delta.get(area, 0.0) + delta, 3)
        return {
            "recommendation_id": _stable_id(
                "rec",
                snapshot_id,
                "bundle",
                *sorted(item["chore_id"] for item in items),
            ),
            "kind": "bundle",
            "title": f"{first['title']} + {second['title']}",
            "estimated_minutes": sum(item["estimated_minutes"] for item in items),
            "chore_items": items,
            "projected_impact": {
                "home_health_delta": round(
                    sum(
                        rec["projected_impact"]["home_health_delta"]
                        for rec in (first, second)
                    ),
                    3,
                ),
                "area_health_delta": area_delta,
            },
            "reason": "Reason: useful bundle with strong combined Home Health impact.",
            "score": score,
            "source_snapshot_id": snapshot_id,
            "expires_at": expires_at.isoformat(),
        }


def _item_payload(chore: ChoreDefinition) -> dict[str, Any]:
    return {
        "chore_id": chore.id,
        "variant": "normal",
        "estimated_minutes": chore.estimated_minutes,
        "area_id": chore.area_id,
        "session_item_id": None,
    }


def _with_kind(recommendation: dict[str, Any], kind: str) -> dict[str, Any]:
    copied = {
        key: value
        for key, value in recommendation.items()
        if key != "score_breakdown"
    }
    copied["kind"] = kind
    copied["recommendation_id"] = _stable_id(
        "rec",
        copied["source_snapshot_id"],
        kind,
        *(item["chore_id"] for item in copied["chore_items"]),
    )
    return copied


def _find_recommendation(
    snapshot: dict[str, Any], recommendation_id: str
) -> Optional[dict[str, Any]]:
    for recommendation in snapshot.get("selected_recommendations", []):
        if recommendation["recommendation_id"] == recommendation_id:
            return recommendation
    return None


def _normalize_fingerprint_payload(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "schema_version",
        "recommendation_mode",
        "target_time_window",
        "time_budget_minutes",
        "energy_level",
        "goal",
        "area_id",
        "mood",
        "calendar_context_id",
        "calendar_context_version",
        "chore_definition_version",
        "enabled_chore_ids",
        "home_assistant_area_ids",
        "user_id",
    }
    normalized = {key: payload.get(key) for key in allowed}
    for key in ("enabled_chore_ids", "home_assistant_area_ids"):
        normalized[key] = sorted(normalized.get(key) or [])
    return normalized


def _is_snoozed(state: Optional[ChoreState], now: datetime) -> bool:
    return bool(state and state.snoozed_until and state.snoozed_until > now)


def _fresh_calendar_context(
    calendar_context: dict[str, Any], now: datetime
) -> Optional[dict[str, Any]]:
    if not calendar_context or calendar_context.get("invalidated_at"):
        return None
    expires_at = calendar_context.get("expires_at")
    if not expires_at:
        return None
    if now >= _parse(expires_at):
        return None
    return calendar_context


def _calendar_context_score(
    chore: ChoreDefinition, calendar_context: Optional[dict[str, Any]]
) -> float:
    if calendar_context is None:
        return 50.0
    score = 50.0
    guess_text = normalize_guess_text(
        " ".join(part for part in (chore.name, chore.group_id, chore.area_id) if part)
    )
    if calendar_context.get("has_guests_soon"):
        if has_any_keyword(guess_text, GUEST_PREP_CHORE_KEYWORDS):
            score += 30.0
    if calendar_context.get("trash_day_tomorrow"):
        if has_any_keyword(guess_text, TRASH_KEYWORDS):
            score += 35.0
    if calendar_context.get("leaving_home_soon") and chore.estimated_minutes <= 5:
        score += 15.0
    if calendar_context.get("busy_evening") and chore.estimated_minutes <= 10:
        score += 10.0
    return clamp_score(score)


def _time_fit(estimated_minutes: int, budget: Optional[int]) -> float:
    if budget is None:
        return 75.0
    if estimated_minutes <= budget:
        return 100.0
    return clamp_score(100.0 - ((estimated_minutes - budget) / max(budget, 1)) * 100.0)


def _energy_fit(chore_energy: str, selected: Optional[str]) -> float:
    if selected is None:
        return 75.0
    if chore_energy == selected:
        return 100.0
    if selected == "low" and chore_energy in {"normal", "quiet"}:
        return 60.0
    if selected == "quiet" and chore_energy == "low":
        return 70.0
    return 40.0


def _dismissal_penalty(state: ChoreState, now: datetime, stale_score: float) -> float:
    weighted = 0.0
    for event in prune_event_timestamps(state.dismissal_events, now):
        age_days = (now - event).total_seconds() / (24 * 60 * 60)
        weighted += max(0.0, 1 - age_days / 14)
    penalty = min(weighted * 12, 36)
    if stale_score >= 150:
        return min(penalty, 8)
    if stale_score >= 100:
        return min(penalty, 18)
    return penalty


def _reason(
    chore: ChoreDefinition, stale: float, impact: float, time_fit: float, history: float
) -> str:
    parts = []
    if stale >= 80:
        parts.append("high Staleness")
    if impact >= 50:
        parts.append(f"strong {chore.area_id or 'Home'} Health impact")
    if time_fit >= 90:
        parts.append("fits the time available")
    if history > 60:
        parts.append("matches prior session history")
    if not parts:
        parts.append("balanced usefulness for this context")
    return "Reason: " + ", ".join(parts[:3]) + "."


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]
    return f"{prefix}_{digest}"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
