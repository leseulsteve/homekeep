# Data Model

## Storage Versioning

Homekeep storage must include a version number from the first scaffold.

```yaml
version: 3
chores: {}
states: {}
completions: []
sessions: {}
recommendations: {}
calendar_context: {}
user_preference_stats: {}
idempotency_records: {}
```

Current storage version is `3`. Version `1` was an early draft that used
`recent_dismissals` and `recent_snoozes` integer fields on `ChoreState`.
Version `2` added bounded dismissal/snooze timestamp fields. Version `3` adds
bounded learned duration samples. Migration rules are documented in
`docs/STORAGE_MIGRATIONS.md`.

## ChoreDefinition

```yaml
id: string
name: string
area_id: string | null
group_id: string | null
base_interval_days: float
min_interval_days: float
max_interval_days: float
estimated_minutes: int
energy: low | normal | high | quiet
visibility: low | medium | high
health_weight: float
variants: dict[str, ChoreVariant]
pairs_with: list[string]
enabled: bool
```

Validation:

- `id` is stable and unique.
- intervals are finite and positive.
- `min_interval_days <= base_interval_days <= max_interval_days`.
- `estimated_minutes` is finite and positive.
- `health_weight` is finite and non-negative.

## ChoreVariant

```yaml
label: string
credit: float
```

Validation:

- variant keys are limited to `tiny`, `normal`, and `deep`
- every enabled chore must have a `normal` variant
- `credit` must be finite and positive
- MVP recommended credit bounds are `0.1 <= credit <= 2.0`
- `credit` is a scheduling-relief multiplier documented in
  `docs/COMPLETION_CREDIT.md`

## ChoreState

```yaml
chore_id: string
last_completed_at: datetime | null
adaptive_interval_days: float
next_due_at: datetime | null
snoozed_until: datetime | null
dismissal_events: list[datetime]
snooze_events: list[datetime]
last_dismissed_at: datetime | null
last_snoozed_at: datetime | null
duration_samples_minutes: list[int]
```

`ChoreState` stores durable scheduling facts. It must not store authoritative
Home Health, Area Health, Group Health, or Staleness values. Those values are
derived on read or cached as disposable data.

`adaptive_interval_days` write rules:

- Must always be finite and positive.
- Must always be clamped to the chore definition's
  `[min_interval_days, max_interval_days]`.
- Must be clamped on initial state creation, completion update, storage load,
  migration, import, and definition update.
- Must only be trained by real completions, not by snoozes, skips, dismissals,
  swaps, or cancellations.

Dismissal and snooze event rules:

- `recent_dismissals` and `recent_snoozes` are derived counts, not stored
  authoritative fields.
- "Recent" means events within the last 14 days.
- Store bounded event timestamps so scoring can decay penalties over time.
- On storage load and event write, prune events older than 14 days and keep at
  most the newest 10 timestamps per event type.
- Dismissal scoring uses `docs/DISMISSAL_PENALTY.md`.
- Snooze validation and `snoozed_until` behavior use `docs/SNOOZE_POLICY.md`.
- Snoozes do not add to dismissal penalty in MVP.

Duration learning rules:

- `estimated_minutes` on `ChoreDefinition` remains the user-entered fallback.
- `duration_samples_minutes` stores at most the newest 10 valid real session
  item durations.
- Valid learned duration samples are integer minutes from `1` to `240`.
- Samples are trained only from real session item completions with a recorded
  `started_at` before `completed_at`.
- Skips, snoozes, dismissals, swaps, cancellations, direct non-session
  completions, and invalid/non-positive timing do not train duration.
- Recommendation time fit and materialized session display use the median
  learned duration when samples exist, otherwise `estimated_minutes`.

Storage migration note:

- Version 1 stores may contain `recent_dismissals: int` and
  `recent_snoozes: int`.
- Version 2 stores must not keep those fields.
- The v1-to-v2 migration adds timestamp-list fields and drops the old counters.
- Do not fabricate timestamps from old counters.

## ChoreCompletion

```yaml
completion_id: string
chore_id: string
session_id: string | null
completed_at: datetime
completed_by: string | null
variant: tiny | normal | deep
credit: float
source: service | todo | dashboard | voice | automation
```

Only real completions create `ChoreCompletion` records.

`credit` stores the Chore Variant credit used at completion time so derived
Staleness and audit/debug views can explain how `next_due_at` was calculated.
It is historical. Later Chore definition edits must not mutate stored
`ChoreCompletion.credit`.

## ChoreSession

```yaml
session_id: string
source_recommendation_snapshot_id: string | null
started_at: datetime
ended_at: datetime | null
started_by: string | null
participants: list[string]
mode: quick_wins | overdue | visible_impact | prevent_future_mess | full_reset
recommendation_mode: ready_now | scheduled_suggestion
target_time_window: string | null
context_fingerprint: string | null
time_budget_minutes: int
energy_level: low | normal | high | quiet
location_preference: string | null
selected_chores: list[string]
items: list[SessionItem]
current_chore: string | null
bonus_chore_offered: string | null
bonus_chore_accepted: bool
bonus_chore_expires_at: datetime | null
status: active | paused | bonus_pending | bonus_active | completed | cancelled
```

`context_fingerprint` is copied from the source RecommendationSnapshot when the
session is materialized. It is not the same as `context_bucket`; see
`docs/CONTEXT_FINGERPRINT.md`.

`bonus_chore_expires_at` rules:

- Set only when status moves to `bonus_pending`.
- MVP TTL is 15 minutes after the Bonus Chore offer.
- Used to lazily expire unaccepted Bonus Chore offers.
- Once a Bonus Chore is accepted and status moves to `bonus_active`,
  `bonus_chore_expires_at` no longer blocks completing the accepted Bonus
  Chore.
- Expiry behavior is defined in `docs/BONUS_CHORE_LIFECYCLE.md`.

## Session Item

```yaml
session_item_id: string
chore_id: string
variant: tiny | normal | deep
status: pending | active | done | skipped | swapped
started_at: datetime | null
completed_at: datetime | null
completed_by: string | null
```

`session_item_id` is the stable identity for item mutations and idempotent
completion. Do not infer item identity from chore name.

`SessionItem` records are created only when a recommendation is materialized
into a Chore Session. Recommendation payload items are proposal items and must
not be used for completion identity.

Participant attribution rules:

- For session completions, `completed_by` must be null or one of
  `ChoreSession.participants`.
- If `completed_by` is omitted and `started_by` is set, completion may default
  to `started_by`.
- Session item `completed_by` and `ChoreCompletion.completed_by` must match.

## RecommendationSnapshot

```yaml
snapshot_id: string
created_at: datetime
recommendation_mode: ready_now | scheduled_suggestion
context_fingerprint: string
mood_context: MoodContext | null
candidate_scores: list[ScoreBreakdown]
selected_recommendations: list[Recommendation]
explanations: list[string]
expires_at: datetime | null
invalidated_at: datetime | null
invalidation_reason: string | null
materialized_session_id: string | null
```

`context_fingerprint` is required on RecommendationSnapshot and generated from
the normalized recommendation context. It must follow
`docs/CONTEXT_FINGERPRINT.md`.

Lifecycle rules:

- A fresh snapshot may be used to start a Chore Session.
- An expired or invalidated snapshot must not start a new Chore Session.
- Once a snapshot is materialized into a Chore Session, the session owns its
selected chores and does not depend on snapshot freshness.
- `materialized_session_id` is for audit/debugging and stale-response
diagnostics.

## MoodContext

```yaml
mood: unknown | calm | focused | tired | overwhelmed | energized
confidence: low | medium | high
source: explicit | inferred | fallback
reason: string
created_at: datetime
expires_at: datetime
```

Mood Context is derived, short-lived recommendation context. It must not store
raw private signals. See `docs/MOOD_CONTEXT.md`.

## CalendarContextSnapshot

Store derived context, not raw calendar events whenever possible.

```yaml
snapshot_id: string
created_at: datetime
expires_at: datetime
target_time_window: string | null
has_guests_soon: bool
free_window_minutes: int | null
leaving_home_soon: bool
trash_day_tomorrow: bool
busy_evening: bool
source_calendar_entities: list[string]
source_calendar_versions: dict[string, CalendarEntityVersion]
invalidated_at: datetime | null
invalidation_reason: string | null
```

Freshness rules:

- A snapshot is invalid if `expires_at` is in the past.
- A snapshot is invalid if any source calendar entity has changed since the
snapshot was created.
- A snapshot is invalid if the target time window changes.
- Recommendation generation must refresh or ignore invalid Calendar Context
instead of silently using it.

## UserPreferenceStats

```yaml
user_id: string | null
context_bucket: string
bucket_dimensions: dict[string, string]
chore_id: string | null
area_id: string | null
accepted_count: int
completed_count: int
skipped_count: int
snoozed_count: int
last_updated_at: datetime
```

`context_bucket` must follow the v1 format documented in
`docs/SESSION_HISTORY_LEARNING.md`. It is not an arbitrary string.

`context_bucket` is a broad learning key and must not be substituted for
`context_fingerprint`.

## IdempotencyRecord

```yaml
request_id: string
operation: string
created_at: datetime
result: dict
expires_at: datetime
```

Idempotency record rules:

- `expires_at = created_at + 24 hours`.
- The identity key is `operation + request_id`.
- Duplicate requests with the same valid key return the stored `result`.
- Expired records are ignored and pruned.
- The store is capped at `1000` records after pruning expired records.
- If the cap is still exceeded, remove oldest `created_at` records first.

See `docs/CONCURRENCY_AND_IDEMPOTENCY.md`.
