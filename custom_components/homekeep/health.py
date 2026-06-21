"""Derived health, staleness, and adaptive interval helpers."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from typing import Iterable, Mapping, Optional

from .models import (
    ChoreDefinition,
    ChoreState,
    HomekeepValidationError,
    VariantKey,
    clamp_adaptive_interval,
    ensure_positive_number,
)


SECONDS_PER_DAY = 24 * 60 * 60
DISPLAY_STALENESS_CAP = 100.0
HEALTH_MIN = 0.0
HEALTH_MAX = 100.0
ADAPTIVE_OLD_WEIGHT = 0.70
ADAPTIVE_NEW_WEIGHT = 0.30
NON_TRAINING_ACTIONS = {"skip", "snooze", "dismiss", "cancel"}


def clamp_score(value: float) -> float:
    """Clamp a health-style score to the 0..100 display range."""

    return max(HEALTH_MIN, min(HEALTH_MAX, value))


def calculate_staleness(
    chore: ChoreDefinition,
    state: ChoreState,
    now: datetime,
    *,
    cap: Optional[float] = None,
) -> float:
    """Derive staleness from durable scheduling facts."""

    due_at = state.next_due_at
    if due_at is None and state.last_completed_at is not None:
        due_at = state.last_completed_at + timedelta(
            days=state.adaptive_interval_days
        )
    if due_at is None:
        return DISPLAY_STALENESS_CAP if cap is None else min(DISPLAY_STALENESS_CAP, cap)
    if now <= due_at:
        return 0.0

    interval_days = clamp_adaptive_interval(state.adaptive_interval_days, chore)
    overdue_days = (now - due_at).total_seconds() / SECONDS_PER_DAY
    staleness = overdue_days / interval_days * 100.0
    if cap is not None:
        return min(staleness, cap)
    return staleness


def display_staleness(
    chore: ChoreDefinition, state: ChoreState, now: datetime
) -> float:
    """Return user-facing staleness capped to 100."""

    return calculate_staleness(chore, state, now, cap=DISPLAY_STALENESS_CAP)


def priority_staleness(
    chore: ChoreDefinition, state: ChoreState, now: datetime
) -> float:
    """Return uncapped staleness for prioritization."""

    return calculate_staleness(chore, state, now)


def chore_health(chore: ChoreDefinition, state: ChoreState, now: datetime) -> float:
    """Derive a single Chore's health from display staleness."""

    if not chore.enabled:
        return HEALTH_MAX
    return clamp_score(HEALTH_MAX - display_staleness(chore, state, now))


def home_health(
    chores: Mapping[str, ChoreDefinition],
    states: Mapping[str, ChoreState],
    now: datetime,
) -> float:
    """Derive weighted Home Health from enabled Chores."""

    return _weighted_health(chores.values(), states, now)


def area_health(
    chores: Mapping[str, ChoreDefinition],
    states: Mapping[str, ChoreState],
    now: datetime,
    area_id: Optional[str],
) -> float:
    """Derive weighted Area Health for one Home Assistant Area."""

    return _weighted_health(
        (chore for chore in chores.values() if chore.area_id == area_id),
        states,
        now,
    )


def projected_impact(
    chore: ChoreDefinition,
    state: ChoreState,
    now: datetime,
    *,
    variant: str = "normal",
) -> float:
    """Estimate health points recovered by completing a Chore now."""

    current_health = chore_health(chore, state, now)
    projected_state = apply_completion_to_state(chore, state, now, variant)
    return clamp_score(chore_health(chore, projected_state, now) - current_health)


def update_adaptive_interval(
    chore: ChoreDefinition,
    state: ChoreState,
    completed_at: datetime,
    *,
    train: bool = True,
) -> float:
    """Update or preserve adaptive interval according to MVP training rules."""

    if not train:
        return state.adaptive_interval_days
    if state.last_completed_at is None:
        return clamp_adaptive_interval(chore.base_interval_days, chore)

    actual_gap_days = max(
        0.0,
        (completed_at - state.last_completed_at).total_seconds() / SECONDS_PER_DAY,
    )
    candidate = (
        state.adaptive_interval_days * ADAPTIVE_OLD_WEIGHT
        + actual_gap_days * ADAPTIVE_NEW_WEIGHT
    )
    return clamp_adaptive_interval(candidate, chore)


def adaptive_interval_after_non_completion_action(
    state: ChoreState, action: str
) -> float:
    """Return unchanged interval for skip, snooze, dismiss, and cancel."""

    if action not in NON_TRAINING_ACTIONS:
        raise HomekeepValidationError(f"unsupported non-completion action: {action}")
    return state.adaptive_interval_days


def effective_credit_days(
    chore: ChoreDefinition, adaptive_interval_days: float, credit: float
) -> float:
    """Return bounded scheduling relief for a Chore Variant credit."""

    interval = clamp_adaptive_interval(adaptive_interval_days, chore)
    variant_credit = ensure_positive_number(credit, "variant.credit")
    return max(
        chore.min_interval_days * 0.1,
        min(chore.max_interval_days * 2.0, interval * variant_credit),
    )


def next_due_after_completion(
    chore: ChoreDefinition,
    adaptive_interval_days: float,
    completed_at: datetime,
    credit: float,
) -> datetime:
    """Derive the next due time after a real completion."""

    return completed_at + timedelta(
        days=effective_credit_days(chore, adaptive_interval_days, credit)
    )


def apply_completion_to_state(
    chore: ChoreDefinition,
    state: ChoreState,
    completed_at: datetime,
    variant: str,
) -> ChoreState:
    """Return durable ChoreState facts produced by a real completion."""

    variant_key = VariantKey(variant).value
    if variant_key not in chore.variants:
        raise HomekeepValidationError("variant must exist on the Chore")

    should_train = variant_key in {VariantKey.NORMAL.value, VariantKey.DEEP.value}
    adaptive_interval_days = update_adaptive_interval(
        chore, state, completed_at, train=should_train
    )
    next_due_at = next_due_after_completion(
        chore,
        adaptive_interval_days,
        completed_at,
        chore.variants[variant_key].credit,
    )
    return replace(
        state,
        last_completed_at=completed_at,
        adaptive_interval_days=adaptive_interval_days,
        next_due_at=next_due_at,
        snoozed_until=None,
    )


def area_health_bucket(score: float) -> str:
    """Return the Area Health bucket for a 0..100 health score."""

    value = clamp_score(score)
    if value < 40:
        return "critical"
    if value < 60:
        return "poor"
    if value < 80:
        return "fair"
    return "good"


def should_fire_area_health_changed(
    old_area_health: Optional[float],
    new_area_health: float,
    *,
    startup_or_rebuild: bool = False,
) -> bool:
    """Return whether Homekeep should emit an Area Health changed event."""

    if startup_or_rebuild or old_area_health is None:
        return False
    return (
        area_health_bucket(old_area_health) != area_health_bucket(new_area_health)
        or abs(new_area_health - old_area_health) >= 10
    )


def _weighted_health(
    chores: Iterable[ChoreDefinition],
    states: Mapping[str, ChoreState],
    now: datetime,
) -> float:
    weighted_total = 0.0
    total_weight = 0.0

    for chore in chores:
        if not chore.enabled:
            continue
        state = states.get(chore.id)
        if state is None:
            state = ChoreState.new_for_chore(chore)
        weighted_total += chore_health(chore, state, now) * chore.health_weight
        total_weight += chore.health_weight

    if total_weight <= 0:
        return HEALTH_MAX
    return clamp_score(weighted_total / total_weight)


def utc_datetime(
    year: int, month: int, day: int, hour: int = 0, minute: int = 0
) -> datetime:
    """Small helper for tests and deterministic callers."""

    return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)
