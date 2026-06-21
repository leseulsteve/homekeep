"""Session-History Learning helpers."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable, Optional

from .health import clamp_score


MINIMUM_OBSERVATIONS = 3


def context_bucket(
    *,
    recommendation_mode: str = "ready_now",
    when: datetime,
    energy_level: Optional[str] = None,
    goal: Optional[str] = None,
    area_id: Optional[str] = None,
    mood: Optional[str] = None,
) -> str:
    """Build the deterministic v1 Session-History Learning bucket."""

    day_type = "weekend" if when.weekday() >= 5 else "weekday"
    return (
        f"mode={recommendation_mode}"
        f"|day={day_type}"
        f"|time={_time_block(when)}"
        f"|energy={energy_level or 'any'}"
        f"|goal={goal or 'any'}"
        f"|area={f'selected:{area_id}' if area_id else 'any'}"
        f"|mood={mood or 'any'}"
    )


def history_fit_score(
    stats: Iterable[dict[str, Any]],
    *,
    bucket: str,
    chore_id: str,
    area_id: Optional[str],
    user_id: Optional[str] = None,
) -> float:
    """Return a bounded history fit score with broad fallbacks."""

    ordered = list(stats)
    candidates = [
        lambda row: row.get("context_bucket") == bucket
        and row.get("user_id") == user_id
        and row.get("chore_id") == chore_id,
        lambda row: row.get("context_bucket") == bucket
        and row.get("user_id") is None
        and row.get("chore_id") == chore_id,
        lambda row: row.get("context_bucket") == _without_area(bucket)
        and row.get("user_id") == user_id
        and row.get("chore_id") == chore_id,
        lambda row: row.get("context_bucket") == _without_area(bucket)
        and row.get("user_id") is None
        and row.get("chore_id") == chore_id,
        lambda row: row.get("context_bucket") == _with_dimension(bucket, "mood", "any")
        and row.get("user_id") is None
        and row.get("chore_id") == chore_id,
        lambda row: row.get("context_bucket")
        == _with_dimension(_with_dimension(bucket, "energy", "any"), "goal", "any")
        and row.get("user_id") is None
        and row.get("chore_id") == chore_id,
        lambda row: row.get("area_id") == area_id and row.get("chore_id") is None,
    ]

    for matcher in candidates:
        matched = [row for row in ordered if matcher(row)]
        attempts = sum(_attempts(row) for row in matched)
        if attempts >= MINIMUM_OBSERVATIONS:
            return _score(matched)
    return 50.0


def _score(rows: Iterable[dict[str, Any]]) -> float:
    accepted = sum(int(row.get("accepted_count", 0)) for row in rows)
    completed = sum(int(row.get("completed_count", 0)) for row in rows)
    skipped = sum(int(row.get("skipped_count", 0)) for row in rows)
    snoozed = sum(int(row.get("snoozed_count", 0)) for row in rows)
    attempts = accepted + completed + skipped + snoozed
    raw_score = (
        50 + ((accepted + completed - skipped - snoozed) / max(attempts, 1)) * 50
    )
    return clamp_score(raw_score)


def _attempts(row: dict[str, Any]) -> int:
    return (
        int(row.get("accepted_count", 0))
        + int(row.get("completed_count", 0))
        + int(row.get("skipped_count", 0))
        + int(row.get("snoozed_count", 0))
    )


def _time_block(value: datetime) -> str:
    hour = value.hour
    if 5 <= hour <= 10:
        return "morning"
    if 11 <= hour <= 13:
        return "midday"
    if 14 <= hour <= 16:
        return "afternoon"
    if 17 <= hour <= 21:
        return "evening"
    return "night"


def _without_area(bucket: str) -> str:
    return _with_dimension(bucket, "area", "any")


def _with_dimension(bucket: str, dimension: str, value: str) -> str:
    parts = bucket.split("|")
    return "|".join(
        f"{dimension}={value}" if part.startswith(f"{dimension}=") else part
        for part in parts
    )
