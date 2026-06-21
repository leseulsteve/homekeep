# Decision Log

This file records the winning implementation interpretation when Homekeep docs
conflict or older planning text is ambiguous.

Codex must read this before implementation. If another document conflicts with
this file, follow this file and update the conflicting document in the same
implementation pass.

## Service Flow

- `homekeep.generate_smart_chore_list` creates a RecommendationSnapshot and
  returns a Smart Chore List action response.
- `homekeep.start_recommendation` is the canonical MVP service that creates a
  Chore Session.
- There is no MVP `homekeep.start_chore_session` service.
- There is no MVP `homekeep.answer_session_question` service. Bubble Card
  collects setup answers locally and calls `generate_smart_chore_list`.
- `homekeep.start_chore_bundle` may exist only as a compatibility alias for
  bundle callers; new code should use `start_recommendation`.
- Scheduled-Suggestion Mode creates saved proposals, not sessions. It never
  returns `session_id: null`.
- Expired or invalidated RecommendationSnapshots cannot start new sessions.
- Once a Chore Session is created, later snapshot expiry does not invalidate
  that active session.

## Home Assistant Responses

- Data-producing services must use Home Assistant action responses.
- `generate_smart_chore_list`, `start_recommendation`,
  `accept_bonus_chore`, and `end_session` use `SupportsResponse.ONLY`.
- `refresh_calendar_context` and simple mutation services may use
  `SupportsResponse.OPTIONAL`.
- Service handlers return JSON-serializable dictionaries, not internal model
  objects.

## Session Item Identity

- Recommendation payload items are proposals.
- `RecommendationItem.session_item_id` is null before materialization.
- `start_recommendation` returns materialized `SessionItem` records with real
  `session_item_id` values.
- Bubble Card and other callers must use the `start_recommendation` response
  for `complete_chore`, `skip_chore`, and `snooze_chore`.

## To-do Projections

- Homekeep storage is the source of truth.
- Home Assistant To-do entities are projections.
- To-do completion is the only MVP write-through operation.
- To-do create, delete, rename, edit, and reorder must not mutate Homekeep
  storage.
- Unsupported To-do mutation handlers should call
  `self.async_write_ha_state()` so the Home Assistant UI snaps back to the
  Homekeep projection.

## Chore State And Health

- Current storage version is `2`.
- Version 1 ChoreState integer counters `recent_dismissals` and
  `recent_snoozes` migrate to version 2 timestamp-list fields by dropping the
  old counters and adding empty event lists.
- Home Health, Area Health, Group Health, Staleness, and Projected Impact are
  derived values.
- Cached health or staleness values are disposable and rebuildable.
- Health scores must remain correct after cache loss or restart.
- `homekeep_area_health_changed` fires only on Area Health bucket crossing or
  absolute delta of at least 10 points. It does not fire during startup/cache
  rebuild.

## Completion Credit

- `ChoreVariant.credit` controls scheduling relief:
  `next_due_at = completed_at + adaptive_interval_days * credit`.
- Tiny completions create real ChoreCompletion records and update
  `next_due_at`, but do not train `adaptive_interval_days`.
- Normal and deep completions train `adaptive_interval_days`.
- Staleness derives from `next_due_at` when available.

## Adaptive Intervals

- `adaptive_interval_days` is clamped on every write to the Chore definition's
  `[min_interval_days, max_interval_days]`.
- Only real normal/deep completions train adaptive intervals.
- Snoozes, skips, dismissals, swaps, and cancellations do not train adaptive
  intervals.

## Snooze And Dismissal

- `snooze_minutes` must be an integer from `5` to `1440`, inclusive.
- Snooze sets `snoozed_until` and excludes a chore from normal recommendations
  until that time.
- Snooze does not add to `dismissal_penalty`.
- Session dismissals must pass `session_id` and materialized `session_item_id`
  for planned session items.
- Dismissal history uses explicit session or snapshot context; it must not
  guess from an ambient active session.
- Dismissal penalty uses 14-day linear decay, 12 points per weighted dismissal,
  and a 36-point cap.
- Dismissals never permanently hide stale chores.

## Calendar And Time

- Calendar Context snapshots must have max-age checks and selected calendar
  entity invalidation.
- Calendar-derived durable data should avoid raw event descriptions whenever
  possible.
- Session-History Learning time buckets use Home Assistant local time.
- Convert datetimes with `homeassistant.util.dt.as_local()` before deriving
  day type or time block.
- `context_bucket` is the broad Session-History Learning key.
- `context_fingerprint` is a `ctx:v1:<sha256>` hash of exact normalized
  recommendation context and is copied from RecommendationSnapshot to
  ChoreSession.
- `python-dateutil` is the boundary parser for user-facing or config-facing
  date/time text. Core logic must receive normalized Home Assistant local
  datetimes, timedeltas, or explicit internal values.
- Use `python-dateutil` to parse supported user-facing `target_time_window`
  strings, then normalize through Home Assistant local timezone helpers.
- Declare `python-dateutil` as an integration requirement in `manifest.json`
  during scaffolding.
- Store and fingerprint the normalized local ISO target window, not raw input
  text.

## Mood Context

- Homekeep may infer lightweight Mood Context when useful for planning and
  suggestions.
- Mood values are `unknown`, `calm`, `focused`, `tired`, `overwhelmed`, and
  `energized`.
- Explicit user mood, energy, and goal choices override inference.
- Mood inference must be local-first, explainable, short-lived, and
  user-correctable.
- Mood Context must not make medical or mental health claims and must not hide
  urgent stale chores by itself.

## Bonus Chores

- Bonus Chores use the original session through `bonus_pending` and
  `bonus_active`.
- A session may offer at most one Bonus Chore in MVP.
- Pending Bonus Chore offers expire after 15 minutes.
- Expired pending Bonus Chore offers lazily mark the session `completed`.
- Late `accept_bonus_chore` calls after expiry raise `bonus_chore_expired`.
- `active -> bonus_pending` and `paused -> bonus_pending` are both valid when
  all planned items are complete.
- Pausing does not block Bonus Chore eligibility.

## Participants

- For session completions, `completed_by` must be null or one of
  `ChoreSession.participants`.
- If omitted and `started_by` is set, `completed_by` may default to
  `started_by`.
- Session item attribution and ChoreCompletion attribution must match.

## Idempotency

- Durable mutations run through the engine mutation lock.
- Idempotency key scope is `operation + request_id`.
- Idempotency records use a 24-hour TTL.
- Idempotency storage is capped at 1000 records after pruning expired records.
- Duplicate valid retries return the stored result, not a recomputed result.

## MVP Scope

- Stay inside MVP unless Steve explicitly expands scope.
- Bubble Card is the MVP dashboard layer.
- No complex fairness scoring, punitive gamification, or broad future scope in
  MVP.
