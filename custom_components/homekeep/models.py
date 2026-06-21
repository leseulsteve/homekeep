"""Core typed models and validation helpers for Homekeep."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from math import isfinite
from typing import Any, Dict, Iterable, List, Mapping, Optional


DISMISSAL_EVENT_WINDOW_DAYS = 14
MAX_EVENT_TIMESTAMPS = 10
VALID_VARIANT_KEYS = {"tiny", "normal", "deep"}
MIN_VARIANT_CREDIT = 0.1
MAX_VARIANT_CREDIT = 2.0


class HomekeepValidationError(ValueError):
    """Raised when stored or imported Homekeep data is invalid."""


class EnergyLevel(str, Enum):
    """Supported Chore energy levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    QUIET = "quiet"


class Visibility(str, Enum):
    """Supported Chore visibility levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class VariantKey(str, Enum):
    """Supported Chore Variant keys."""

    TINY = "tiny"
    NORMAL = "normal"
    DEEP = "deep"


class CompletionSource(str, Enum):
    """Supported completion sources."""

    SERVICE = "service"
    TODO = "todo"
    BUBBLE_CARD = "bubble_card"
    VOICE = "voice"
    AUTOMATION = "automation"


class SessionMode(str, Enum):
    """Supported Chore Session modes."""

    QUICK_WINS = "quick_wins"
    OVERDUE = "overdue"
    VISIBLE_IMPACT = "visible_impact"
    PREVENT_FUTURE_MESS = "prevent_future_mess"
    FULL_RESET = "full_reset"


class RecommendationMode(str, Enum):
    """Supported recommendation modes."""

    READY_NOW = "ready_now"
    SCHEDULED_SUGGESTION = "scheduled_suggestion"


class SessionStatus(str, Enum):
    """Supported Chore Session statuses."""

    ACTIVE = "active"
    PAUSED = "paused"
    BONUS_PENDING = "bonus_pending"
    BONUS_ACTIVE = "bonus_active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SessionItemStatus(str, Enum):
    """Supported Session Item statuses."""

    PENDING = "pending"
    ACTIVE = "active"
    DONE = "done"
    SKIPPED = "skipped"
    SWAPPED = "swapped"


def ensure_finite_number(value: Any, field_name: str) -> float:
    """Return a finite float or raise a validation error."""

    try:
        number = float(value)
    except (TypeError, ValueError) as err:
        raise HomekeepValidationError(f"{field_name} must be a finite number") from err
    if not isfinite(number):
        raise HomekeepValidationError(f"{field_name} must be finite")
    return number


def ensure_positive_number(value: Any, field_name: str) -> float:
    """Return a finite positive float or raise a validation error."""

    number = ensure_finite_number(value, field_name)
    if number <= 0:
        raise HomekeepValidationError(f"{field_name} must be positive")
    return number


def ensure_non_negative_number(value: Any, field_name: str) -> float:
    """Return a finite non-negative float or raise a validation error."""

    number = ensure_finite_number(value, field_name)
    if number < 0:
        raise HomekeepValidationError(f"{field_name} must be non-negative")
    return number


def ensure_positive_int(value: Any, field_name: str) -> int:
    """Return a positive integer or raise a validation error."""

    if isinstance(value, bool) or not isinstance(value, int):
        raise HomekeepValidationError(f"{field_name} must be a positive integer")
    if value <= 0:
        raise HomekeepValidationError(f"{field_name} must be positive")
    return value


def require_string(value: Any, field_name: str) -> str:
    """Return a non-empty string or raise a validation error."""

    if not isinstance(value, str) or not value:
        raise HomekeepValidationError(f"{field_name} must be a non-empty string")
    return value


def optional_string(value: Any, field_name: str) -> Optional[str]:
    """Return an optional string or raise a validation error."""

    if value is None:
        return None
    return require_string(value, field_name)


def parse_datetime(value: Any, field_name: str) -> Optional[datetime]:
    """Parse an ISO datetime value into an aware datetime."""

    if value is None:
        return None
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as err:
            raise HomekeepValidationError(f"{field_name} must be an ISO datetime") from err
    else:
        raise HomekeepValidationError(f"{field_name} must be an ISO datetime")

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def datetime_to_json(value: Optional[datetime]) -> Optional[str]:
    """Serialize datetimes to JSON-safe ISO strings."""

    if value is None:
        return None
    return value.isoformat()


def enum_value(enum_type: Any, value: Any, field_name: str) -> str:
    """Validate a string enum value and return its raw value."""

    try:
        return enum_type(value).value
    except ValueError as err:
        allowed = ", ".join(item.value for item in enum_type)
        raise HomekeepValidationError(
            f"{field_name} must be one of: {allowed}"
        ) from err


def clamp_adaptive_interval(candidate: Any, chore: "ChoreDefinition") -> float:
    """Clamp an adaptive interval write to the Chore definition bounds."""

    interval = ensure_positive_number(candidate, "adaptive_interval_days")
    return max(chore.min_interval_days, min(chore.max_interval_days, interval))


def prune_event_timestamps(
    values: Iterable[Any], now: Optional[datetime] = None
) -> List[datetime]:
    """Keep valid recent event timestamps, capped to the newest values."""

    if now is None:
        now = datetime.now(timezone.utc)
    parsed_values: List[datetime] = []
    cutoff = now - timedelta(days=DISMISSAL_EVENT_WINDOW_DAYS)

    for index, value in enumerate(values):
        try:
            parsed = parse_datetime(value, f"event timestamp {index}")
        except HomekeepValidationError:
            continue
        if parsed is not None and parsed >= cutoff:
            parsed_values.append(parsed)

    parsed_values.sort()
    return parsed_values[-MAX_EVENT_TIMESTAMPS:]


@dataclass(frozen=True)
class ChoreVariant:
    """A completion variant for a Chore."""

    label: str
    credit: float

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ChoreVariant":
        """Build and validate a Chore Variant from stored data."""

        variant = cls(
            label=require_string(data.get("label"), "variant.label"),
            credit=ensure_positive_number(data.get("credit"), "variant.credit"),
        )
        variant.validate()
        return variant

    def validate(self) -> None:
        """Validate variant fields."""

        if self.credit < MIN_VARIANT_CREDIT or self.credit > MAX_VARIANT_CREDIT:
            raise HomekeepValidationError(
                "variant.credit must be between 0.1 and 2.0"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize this variant."""

        return {"label": self.label, "credit": self.credit}


@dataclass(frozen=True)
class ChoreDefinition:
    """A durable Chore definition."""

    id: str
    name: str
    area_id: Optional[str]
    group_id: Optional[str]
    base_interval_days: float
    min_interval_days: float
    max_interval_days: float
    estimated_minutes: int
    energy: str
    visibility: str
    health_weight: float
    variants: Dict[str, ChoreVariant]
    pairs_with: List[str] = field(default_factory=list)
    enabled: bool = True

    @classmethod
    def from_dict(cls, chore_id: str, data: Mapping[str, Any]) -> "ChoreDefinition":
        """Build and validate a Chore definition from stored data."""

        raw_variants = data.get("variants")
        if not isinstance(raw_variants, Mapping):
            raise HomekeepValidationError("variants must be a mapping")

        variants: Dict[str, ChoreVariant] = {}
        for key, value in raw_variants.items():
            if key not in VALID_VARIANT_KEYS:
                raise HomekeepValidationError(
                    "variant keys must be limited to tiny, normal, and deep"
                )
            if not isinstance(value, Mapping):
                raise HomekeepValidationError("variant values must be mappings")
            variants[key] = ChoreVariant.from_dict(value)

        pairs_with = data.get("pairs_with", [])
        if not isinstance(pairs_with, list) or not all(
            isinstance(item, str) for item in pairs_with
        ):
            raise HomekeepValidationError("pairs_with must be a list of strings")

        chore = cls(
            id=require_string(data.get("id", chore_id), "chore.id"),
            name=require_string(data.get("name"), "chore.name"),
            area_id=optional_string(data.get("area_id"), "chore.area_id"),
            group_id=optional_string(data.get("group_id"), "chore.group_id"),
            base_interval_days=ensure_positive_number(
                data.get("base_interval_days"), "base_interval_days"
            ),
            min_interval_days=ensure_positive_number(
                data.get("min_interval_days"), "min_interval_days"
            ),
            max_interval_days=ensure_positive_number(
                data.get("max_interval_days"), "max_interval_days"
            ),
            estimated_minutes=ensure_positive_int(
                data.get("estimated_minutes"), "estimated_minutes"
            ),
            energy=enum_value(EnergyLevel, data.get("energy"), "energy"),
            visibility=enum_value(Visibility, data.get("visibility"), "visibility"),
            health_weight=ensure_non_negative_number(
                data.get("health_weight"), "health_weight"
            ),
            variants=variants,
            pairs_with=pairs_with,
            enabled=bool(data.get("enabled", True)),
        )
        chore.validate()
        return chore

    def validate(self) -> None:
        """Validate Chore definition invariants."""

        if self.min_interval_days > self.base_interval_days:
            raise HomekeepValidationError(
                "min_interval_days must be <= base_interval_days"
            )
        if self.base_interval_days > self.max_interval_days:
            raise HomekeepValidationError(
                "base_interval_days must be <= max_interval_days"
            )
        if self.enabled and "normal" not in self.variants:
            raise HomekeepValidationError("enabled chores must have a normal variant")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize this Chore definition."""

        return {
            "id": self.id,
            "name": self.name,
            "area_id": self.area_id,
            "group_id": self.group_id,
            "base_interval_days": self.base_interval_days,
            "min_interval_days": self.min_interval_days,
            "max_interval_days": self.max_interval_days,
            "estimated_minutes": self.estimated_minutes,
            "energy": self.energy,
            "visibility": self.visibility,
            "health_weight": self.health_weight,
            "variants": {
                key: variant.to_dict() for key, variant in self.variants.items()
            },
            "pairs_with": list(self.pairs_with),
            "enabled": self.enabled,
        }


@dataclass(frozen=True)
class ChoreState:
    """Durable scheduling state for a Chore."""

    chore_id: str
    last_completed_at: Optional[datetime]
    adaptive_interval_days: float
    next_due_at: Optional[datetime]
    snoozed_until: Optional[datetime] = None
    dismissal_events: List[datetime] = field(default_factory=list)
    snooze_events: List[datetime] = field(default_factory=list)
    last_dismissed_at: Optional[datetime] = None
    last_snoozed_at: Optional[datetime] = None

    @classmethod
    def new_for_chore(cls, chore: ChoreDefinition) -> "ChoreState":
        """Create an initial state for a Chore definition."""

        return cls(
            chore_id=chore.id,
            last_completed_at=None,
            adaptive_interval_days=clamp_adaptive_interval(
                chore.base_interval_days, chore
            ),
            next_due_at=None,
        )

    @classmethod
    def from_dict(
        cls,
        chore_id: str,
        data: Mapping[str, Any],
        chore: ChoreDefinition,
        now: Optional[datetime] = None,
    ) -> "ChoreState":
        """Build a Chore state from stored data, repairing bounded event lists."""

        return cls(
            chore_id=require_string(data.get("chore_id", chore_id), "state.chore_id"),
            last_completed_at=parse_datetime(
                data.get("last_completed_at"), "last_completed_at"
            ),
            adaptive_interval_days=clamp_adaptive_interval(
                data.get("adaptive_interval_days"), chore
            ),
            next_due_at=parse_datetime(data.get("next_due_at"), "next_due_at"),
            snoozed_until=parse_datetime(
                data.get("snoozed_until"), "snoozed_until"
            ),
            dismissal_events=prune_event_timestamps(
                data.get("dismissal_events", []), now
            ),
            snooze_events=prune_event_timestamps(data.get("snooze_events", []), now),
            last_dismissed_at=parse_datetime(
                data.get("last_dismissed_at"), "last_dismissed_at"
            ),
            last_snoozed_at=parse_datetime(
                data.get("last_snoozed_at"), "last_snoozed_at"
            ),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize this Chore state."""

        return {
            "chore_id": self.chore_id,
            "last_completed_at": datetime_to_json(self.last_completed_at),
            "adaptive_interval_days": self.adaptive_interval_days,
            "next_due_at": datetime_to_json(self.next_due_at),
            "snoozed_until": datetime_to_json(self.snoozed_until),
            "dismissal_events": [
                datetime_to_json(value) for value in self.dismissal_events
            ],
            "snooze_events": [
                datetime_to_json(value) for value in self.snooze_events
            ],
            "last_dismissed_at": datetime_to_json(self.last_dismissed_at),
            "last_snoozed_at": datetime_to_json(self.last_snoozed_at),
        }


@dataclass(frozen=True)
class ChoreCompletion:
    """A durable real completion event."""

    completion_id: str
    chore_id: str
    session_id: Optional[str]
    completed_at: datetime
    completed_by: Optional[str]
    variant: str
    credit: float
    source: str

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ChoreCompletion":
        """Build and validate a Chore completion from stored data."""

        return cls(
            completion_id=require_string(
                data.get("completion_id"), "completion_id"
            ),
            chore_id=require_string(data.get("chore_id"), "completion.chore_id"),
            session_id=optional_string(data.get("session_id"), "session_id"),
            completed_at=_required_datetime(data.get("completed_at"), "completed_at"),
            completed_by=optional_string(data.get("completed_by"), "completed_by"),
            variant=enum_value(VariantKey, data.get("variant"), "variant"),
            credit=ensure_positive_number(data.get("credit"), "completion.credit"),
            source=enum_value(CompletionSource, data.get("source"), "source"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize this completion."""

        return {
            "completion_id": self.completion_id,
            "chore_id": self.chore_id,
            "session_id": self.session_id,
            "completed_at": datetime_to_json(self.completed_at),
            "completed_by": self.completed_by,
            "variant": self.variant,
            "credit": self.credit,
            "source": self.source,
        }


def resolve_completed_by(
    participants: Iterable[str],
    started_by: Optional[str],
    completed_by: Optional[str],
) -> Optional[str]:
    """Apply MVP participant attribution rules for session completions."""

    participant_list = list(participants)
    if completed_by is not None:
        if participant_list and completed_by not in participant_list:
            raise HomekeepValidationError("completed_by must be a session participant")
        return completed_by
    if started_by is not None:
        return started_by
    return None


def _required_datetime(value: Any, field_name: str) -> datetime:
    parsed = parse_datetime(value, field_name)
    if parsed is None:
        raise HomekeepValidationError(f"{field_name} is required")
    return parsed
