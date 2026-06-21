# Service Schemas

These are draft service contracts for the first scaffold. Use Home Assistant
schema validation and keep errors explicit.

Services that produce data must use Home Assistant action response support.
Follow `docs/ACTION_RESPONSES.md` for `SupportsResponse.ONLY` and
`SupportsResponse.OPTIONAL` registration rules.

## Service Relationship

The MVP uses one proposal-generation service and one session-materialization
service.

```text
homekeep.generate_smart_chore_list
-> creates a RecommendationSnapshot and returns recommendations

homekeep.start_recommendation
-> validates the RecommendationSnapshot and materializes one recommendation
   into a Chore Session

homekeep.create_chore
-> creates a Chore definition for the chore list without starting a session
```

`homekeep.start_chore_session` is intentionally not part of the MVP service
contract. It overlaps with both steps, creates ambiguity in
Scheduled-Suggestion Mode, and would create a second path that could bypass
RecommendationSnapshot freshness validation.

## `homekeep.generate_smart_chore_list`

Generates a Smart Chore List without starting a Chore Session.

Response support:

```text
supports_response = SupportsResponse.ONLY
```

```yaml
user_id: string | null
recommendation_mode: ready_now | scheduled_suggestion
target_time_window: string | null
time_budget_minutes: int | null
energy_level: low | normal | high | quiet | null
goal: quick_wins | overdue | visible_impact | prevent_future_mess | full_reset | null
area_id: string | null
mood: unknown | calm | focused | tired | overwhelmed | energized | auto | null
infer_mood: bool
include_alternates: bool
request_id: string | null
```

`target_time_window` parsing and normalization must follow
`docs/TARGET_TIME_WINDOW.md`. Scheduled-Suggestion Mode requires a non-null
target window. Ready-Now Mode may use null to mean "now".

Default:

```text
infer_mood = true
include_alternates = true
```

When `include_alternates=true`, return up to 3 alternates. When false, return
an empty `alternates` list.

Result:

```yaml
snapshot_id: string
recommendation_mode: ready_now | scheduled_suggestion
target_time_window: string | null
expires_at: datetime
mood_context: MoodContext | null
best_bundle: Recommendation | null
best_single_chore: Recommendation | null
easiest_chore: Recommendation | null
alternates: list[Recommendation]
empty_state: EmptyState | null
```

Recommendation dictionaries must use the shape in
`docs/RECOMMENDATION_PAYLOADS.md`.

This service never creates a Chore Session.

If `mood` is `auto` or null and `infer_mood=true`, Homekeep may infer Mood
Context using `docs/MOOD_CONTEXT.md`. Explicit mood, energy, and goal choices
override inferred values.

In Scheduled-Suggestion Mode, callers must treat the result as a saved proposal.
They may call `homekeep.start_recommendation` later only while the snapshot is
fresh. If the snapshot is expired or invalidated, regenerate first. See
`docs/SCHEDULED_SUGGESTION_UX.md`.

## `homekeep.start_recommendation`

Starts a Chore Session from a generated recommendation. Use this for Chore
Bundle, best single chore, and easiest chore recommendations.

Response support:

```text
supports_response = SupportsResponse.ONLY
```

```yaml
recommendation_snapshot_id: string
recommendation_id: string
user_id: string | null
request_id: string | null
```

Validation:

- `recommendation_snapshot_id` must exist.
- The snapshot must be fresh, not expired, and not invalidated.
- `recommendation_id` must exist in the snapshot.
- If the snapshot has already been materialized into a session, reject unless
  the request is an idempotent retry for the same session.

Result:

```yaml
session_id: string
source_recommendation_snapshot_id: string
status: active
items: list[MaterializedSessionItem]
```

`StartRecommendationResult` is the action response returned by
`homekeep.start_recommendation`.

```yaml
StartRecommendationResult:
  session_id: string
  source_recommendation_snapshot_id: string
  status: active
  items: list[MaterializedSessionItem]
```

`MaterializedSessionItem` is the caller-facing session item shape. It is a
subset of the stored `SessionItem` plus display fields needed by Lovelace and
automations.

```yaml
MaterializedSessionItem:
  session_item_id: string
  chore_id: string
  variant: tiny | normal | deep
  status: pending | active
  estimated_minutes: int
  area_id: string | null
```

`items` contains the new concrete `session_item_id` values. Callers must use
these IDs for subsequent session item mutations. Do not use cached
`RecommendationItem.session_item_id` values from the Smart Chore List; those
are null before materialization.

After the session is created, later snapshot expiry must not invalidate the
active session.

## `homekeep.start_chore_bundle`

Bundle-only alias for callers that cannot use `start_recommendation`. New code
should prefer `homekeep.start_recommendation`.

Response support:

```text
supports_response = SupportsResponse.ONLY
```

```yaml
recommendation_snapshot_id: string
bundle_id: string
user_id: string | null
request_id: string | null
```

Validation follows `homekeep.start_recommendation`, but `bundle_id` maps to a
bundle recommendation in the snapshot.

## `homekeep.create_chore`

Creates an enabled Chore definition and initial ChoreState. This service is for
adding Chores to the Homekeep chore list; it does not create or schedule a
Chore Session.

Response support:

```text
supports_response = SupportsResponse.OPTIONAL
```

```yaml
chore_id: string | null
name: string
area_id: string | null
group_id: string | null
base_interval_days: float
min_interval_days: float | null
max_interval_days: float | null
estimated_minutes: int
energy_level: low | normal | high | quiet
visibility: low | medium | high
health_weight: float
request_id: string | null
```

Defaults:

```text
base_interval_days = 7
min_interval_days = max(1, base_interval_days / 2)
max_interval_days = base_interval_days * 2
estimated_minutes = 10
energy_level = normal
visibility = medium
health_weight = 1.0
```

Validation:

- If `chore_id` is omitted, Homekeep derives one from `name`.
- `chore_id` must be unique.
- `name` must be non-empty.
- Intervals, estimated minutes, and health weight must be finite values.
- Interval order must satisfy the normal Chore definition rules.
- The created Chore gets a normal Chore Variant with credit `1.0`.
- Duplicate `request_id` retries return the stored result.

Result:

```yaml
status: created
chore_id: string
chore: ChoreDefinition
```

## `homekeep.complete_chore`

Marks a chore as completed.

Response support:

```text
supports_response = SupportsResponse.OPTIONAL
```

```yaml
chore_id: string
session_id: string | null
session_item_id: string | null
variant: tiny | normal | deep
completed_by: string | null
source: service | todo | lovelace | voice | automation
request_id: string | null
```

Validation:

- `chore_id` must exist.
- `variant` must exist on the chore or default to `normal`.
- If `session_id` is provided, it must match an active, paused, or
  `bonus_active` session.
- If `session_id` is provided for a planned session item, `session_item_id`
  must identify the item to complete.
- If `session_id` is provided for a Bonus Chore, the session status must be
  `bonus_active` and the chore must match `bonus_chore_offered`.
- If `session_id` and `completed_by` are provided, `completed_by` must be in
  the session's `participants`.
- If `session_id` is provided, `completed_by` may default to session
  `started_by` when omitted.
- Repeated completion of the same session item must not create duplicate
  `ChoreCompletion` records.

## `homekeep.skip_chore`

Response support:

```text
supports_response = SupportsResponse.OPTIONAL
```

```yaml
chore_id: string
session_id: string | null
session_item_id: string | null
reason: string | null
request_id: string | null
```

Validation:

- If `session_id` is provided for a planned session item, `session_item_id`
  must identify the item to skip.

Skipping affects recommendation history but does not create a completion.

## `homekeep.snooze_chore`

Response support:

```text
supports_response = SupportsResponse.OPTIONAL
```

```yaml
chore_id: string
session_id: string | null
session_item_id: string | null
snooze_minutes: int
reason: string | null
request_id: string | null
```

Validation:

- `snooze_minutes` must be an integer from `5` to `1440`, inclusive.
- Invalid values must be rejected, not silently clamped.
- If `session_id` is provided for a planned session item, `session_item_id`
  must identify the item to snooze.

Behavior:

- Set `ChoreState.snoozed_until` to `now + snooze_minutes`.
- Append one bounded snooze timestamp to `ChoreState.snooze_events`.
- Do not create a `ChoreCompletion`.
- Do not train `adaptive_interval_days`.
- Do not add to `dismissal_penalty`.

See `docs/SNOOZE_POLICY.md`.

## `homekeep.dismiss_chore`

Response support:

```text
supports_response = SupportsResponse.OPTIONAL
```

```yaml
chore_id: string
session_id: string | null
session_item_id: string | null
recommendation_snapshot_id: string | null
reason: string | null
request_id: string | null
```

Validation:

- `chore_id` must exist.
- If `session_id` is provided, it must identify an active, paused, or
  `bonus_pending` session.
- If `session_id` is provided for a planned session item, `session_item_id`
  must identify the item to dismiss.
- If `recommendation_snapshot_id` is provided, it must exist for audit/history
  linkage, but it does not need to be fresh.
- If both `session_id` and `recommendation_snapshot_id` are provided, they must
  refer to the same recommendation context when the session has
  `source_recommendation_snapshot_id`.
- If `request_id` is supplied, duplicate retries must not append duplicate
  dismissal events.

Behavior:

- Append one bounded dismissal timestamp to `ChoreState.dismissal_events`.
- Set `last_dismissed_at`.
- Apply future recommendation penalty through `docs/DISMISSAL_PENALTY.md`.
- Update Session-History Learning using the session context bucket when
  `session_id` is provided.
- Otherwise update Session-History Learning from the RecommendationSnapshot
  context when available.
- Do not create a `ChoreCompletion`.
- Do not train `adaptive_interval_days`.

## `homekeep.answer_session_question`

Not implemented in MVP.

This service is reserved for a future multi-step Lovelace or Assist flow. Do
not register it in the MVP Home Assistant integration.

MVP behavior:

```text
Lovelace collects time, energy, goal, area, and mood locally
-> Lovelace calls homekeep.generate_smart_chore_list with those fields
-> Homekeep returns a RecommendationSnapshot and Smart Chore List
```

There is no MVP `DraftSessionContext` store, and answering a question must not
silently mutate an active Chore Session or regenerate recommendations.

Before this service can be implemented later, a future spec must define:

- the draft context storage key
- whether drafts are scoped by user, device, or session
- draft expiration
- whether answering a question triggers recommendation regeneration
- which answers are allowed after a Chore Session has started

Response support:

```text
supports_response = SupportsResponse.OPTIONAL
```

```yaml
session_id: string | null
question: time_budget | energy_level | goal | area | participant | mood
answer: string
request_id: string | null
```

## `homekeep.pause_session`

Response support:

```text
supports_response = SupportsResponse.OPTIONAL
```

```yaml
session_id: string
request_id: string | null
```

## `homekeep.accept_bonus_chore`

Moves a session from `bonus_pending` to `bonus_active`.

Response support:

```text
supports_response = SupportsResponse.ONLY
```

```yaml
session_id: string
chore_id: string
request_id: string | null
```

Validation:

- session must be `bonus_pending`
- `chore_id` must match `bonus_chore_offered`
- `bonus_chore_expires_at` must be in the future

Expired behavior:

- If `bonus_chore_expires_at <= now`, mark the session `completed`.
- Reject the service call with `bonus_chore_expired`.
- Do not create a new Bonus Chore implicitly.

Result:

```yaml
session_id: string
status: bonus_active
chore_id: string
session_item_id: string
```

## `homekeep.end_session`

Response support:

```text
supports_response = SupportsResponse.ONLY
```

```yaml
session_id: string
status: completed | cancelled
offer_bonus_chore: bool
request_id: string | null
```

If `offer_bonus_chore` is true and status is `completed`, Homekeep may return a
Bonus Chore and move the session to `bonus_pending`. The returned Bonus Chore
uses the original `session_id`.

Validation:

- current session status must be `active` or `paused` to offer a Bonus Chore
- all planned session items must be done before moving to `bonus_pending`
- paused sessions remain eligible for Bonus Chore offers when planned items are
  complete
- incomplete planned sessions must not move to `bonus_pending`
- when moving to `bonus_pending`, set `bonus_chore_expires_at = now + 15
  minutes`

If no Bonus Chore is available, the session is marked `completed` and
`bonus_chore` is `null`.

Result when a Bonus Chore is offered:

```yaml
session_id: string
status: bonus_pending
bonus_chore: Recommendation | null
bonus_chore_expires_at: datetime
```

## `homekeep.refresh_calendar_context`

Response support:

```text
supports_response = SupportsResponse.OPTIONAL
```

```yaml
target_time_window: string | null
calendar_entity_ids: list[string] | null
```

Result should contain derived Calendar Context only.

This service is a manual refresh hook. Homekeep must also refresh or invalidate
Calendar Context automatically when selected calendar entities change or when a
snapshot exceeds its max age.

## `homekeep.load_sample_chores`

Private live-test helper that loads bundled synthetic Chore definitions from
the installed integration package.

During private live testing, the config entry `dev_mode` option defaults to
true and setup automatically loads these bundled Chores when Homekeep storage
is empty. This service remains available for explicit reset flows.

Response support:

```text
supports_response = SupportsResponse.OPTIONAL
```

```yaml
replace_existing: bool
```

Validation:

- If Homekeep already has stored Chores, reject unless
  `replace_existing=true`.
- The bundled sample file must pass normal Chore validation.
- This service is not a general import API and must not accept arbitrary paths
  or live household data.

Behavior:

- Load bundled synthetic Chores.
- Create default ChoreState records for loaded Chores.
- When `replace_existing=true`, clear existing Chores, Chore state,
  completions, sessions, recommendations, Session-History Learning stats, and
  idempotency records before loading the bundled fixtures.

Result:

```yaml
status: loaded
chore_count: int
chore_ids: list[string]
replace_existing: bool
```
