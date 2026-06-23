# Decision Log

This file records the winning implementation interpretation when Homekeep docs
conflict or older planning text is ambiguous.

Codex must read this before implementation. If another document conflicts with
this file, follow this file and update the conflicting document in the same
implementation pass.

## Service Flow

- `homekeep.create_chore` creates an enabled Chore definition and initial
  ChoreState for the chore list. It does not create, schedule, or start a
  Chore Session.
- `homekeep.generate_smart_chore_list` creates a RecommendationSnapshot and
  returns a Smart Chore List action response.
- `homekeep.start_recommendation` is the canonical MVP service that creates a
  Chore Session.
- There is no MVP `homekeep.start_chore_session` service.
- There is no MVP `homekeep.answer_session_question` service. Homekeep app
  collects setup answers locally and calls `generate_smart_chore_list`.
- `homekeep.start_chore_bundle` may exist only as a compatibility alias for
  bundle callers; new code should use `start_recommendation`.
- Scheduled-Suggestion Mode creates saved proposals, not sessions. It never
  returns `session_id: null`.
- Expired or invalidated RecommendationSnapshots cannot start new sessions.
- Once a Chore Session is created, later snapshot expiry does not invalidate
  that active session.
- `start_recommendation` infers session setup fields from the stored
  RecommendationSnapshot and selected recommendation. Callers should not need
  to provide mode, time budget, energy, target window, or area again.

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
- Homekeep app and other callers must use the `start_recommendation` response
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

- Current storage version is `3`.
- Version 1 ChoreState integer counters `recent_dismissals` and
  `recent_snoozes` migrate to version 2 timestamp-list fields by dropping the
  old counters and adding empty event lists.
- Version 2 ChoreState records migrate to version 3 by adding
  `duration_samples_minutes: []`.
- Home Health, Area Health, Group Health, Staleness, and Projected Impact are
  derived values.
- Cached health or staleness values are disposable and rebuildable.
- Health scores must remain correct after cache loss or restart.
- Area Health is a `0..100` derived, health-weighted average of enabled Chore
  health for one Home Assistant Area. It answers how much that area would
  benefit from care now, not what percent of its Chores are completed.
- Area Health contributor explanations should use inspectable derived reasons
  such as Staleness, health weight, and Projected Impact.
- `homekeep_area_health_changed` fires only on Area Health bucket crossing or
  absolute delta of at least 10 points. It does not fire during startup/cache
  rebuild.
- Chore duration learning uses bounded real session timing samples. Homekeep
  keeps the user-entered `estimated_minutes` as the fallback/base suggestion,
  not authoritative truth.
- Recommendation duration uses the learned median as the base when samples
  exist, then adapts it lightly to current Mood/Readiness, inferred Capacity,
  and recent session momentum. Low/quiet contexts should bias shorter; ready or
  strong contexts may allow a fuller duration; already-completed session work
  should cap added ambition.
- Duration learning trains only from actual active work intervals. Reading,
  deciding, paused time, skips, removals, snoozes, dismissals, and invalid
  timing must not train duration.
- Future storage may split learned duration samples by Chore Variant and
  readiness/context bucket; until then, context adjustment is derived and
  disposable.

## Completion Credit

- `ChoreVariant.credit` controls scheduling relief:
  `next_due_at = completed_at + adaptive_interval_days * credit`.
- Tiny completions create real ChoreCompletion records and update
  `next_due_at`, but do not train `adaptive_interval_days`.
- Normal and deep completions train `adaptive_interval_days`.
- Staleness derives from `next_due_at` when available.

## Keeps

- Keeps are a lightweight signal of care returned by the home, not productivity
  points, money, wages, or a score on the user.
- Keeps come from the home as a whole, not from individual Home Assistant Areas.
- Keeps are tied to care completion, not speed, streaks, rankings, optimization,
  or performance.
- Full-reset Keeps represent harmony in a coherent suggested bundle, not a
  pressure reward for obeying the app.
- Optional Chores can add Keeps, but optional continuation must not create a
  reward chain.
- User-facing Keeps values that are always positive should not use a `+` prefix.
- Avoid `earn`, `earned`, `spend`, `bank`, `redeem`, shop, wallet, upgrade,
  exchange-rate, coin, trophy, badge-heavy, and leaderboard metaphors.
- Keeps can help tiny Chores feel like they count. Home Health explains where
  care helps; Keeps acknowledge that care happened.
- Keeps may support quiet care reflection later, but not leaderboards, rankings,
  shopping, upgrades, or total-chasing surfaces.

## Adaptive Intervals

- `adaptive_interval_days` is clamped on every write to the Chore definition's
  `[min_interval_days, max_interval_days]`.
- Only real normal/deep completions train adaptive intervals.
- Snoozes, skips, dismissals, swaps, and cancellations do not train adaptive
  intervals.

## Recommendation Engine

- Recommendation selection uses a two-stage pipeline: hard constraints first,
  scoring second. Hard constraints such as explicit time, explicit Area,
  hidden/unmanaged Areas, future snoozes, invalid metadata, and active-session
  exclusions cannot be overridden by a high score.
- Recommendation scoring keeps Home need and user fit conceptually separate.
  Home need comes from Staleness, Home/Area Health, Projected Impact, and
  relevant Calendar Context. User fit comes from time, inferred Capacity, Mood
  Context, explicit Area, and bounded Session-History Learning.
- Homekeep may apply a bounded care nudge toward useful Home need, but the
  nudge must be capped, explainable, and unable to override explicit user
  constraints.
- When useful care is too large for the moment, prefer a smaller Chore Variant
  before rejecting the care opportunity.
- Optional continuation Chores after a completed planned bundle use the same
  Recommendation Engine principles with stricter bounds: small duration,
  stronger mood/time fit, no current-flow repeats, useful health/staleness
  impact, and no unbounded chaining.
- Shuffle should vary within a stable family of good fits rather than producing
  random or contradictory suggestions.
- User correction signals such as removal, skip, dismiss, and snooze should
  soften, resize, defer, or retime suggestions before suppressing useful care.

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
- Calendar-derived durable data stores minimized derived signals, source entity
  versions, and freshness metadata, not raw event descriptions.
- Selected calendar entities are Home Assistant config entry options.
- Calendar Context source versions are based on selected calendar entity state,
  `last_changed`, and `last_updated`.
- Calendar Context also stores a hash of minimized event facts so added or
  modified events can make a snapshot stale even when the Home Assistant
  calendar entity state remains unchanged. The hash may include event
  start/end times and derived category flags, but not raw event summary,
  description, or location text.
- Calendar Context keyword matching supports English and basic French terms
  for guest/visit, travel/departure, and trash/recycling/compost signals.
- Calendar entity state changes invalidate the current Calendar Context and
  dependent RecommendationSnapshots; recommendation refresh remains lazy.
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
- String-based local signal guessing uses shared English/basic-French keyword
  matching with case/accent normalization. This applies to Calendar Context
  event classification and Recommendation Engine calendar-fit guesses from
  Chore names, groups, and Home Assistant Area ids.

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
- Post-prototype direction: consider evolving Mood Context into broader
  Readiness Context where recommendation behavior primarily uses capacity,
  energy, time, chore friction, explicit modes, and user correction. Mood should
  remain optional and should not become a hidden diagnosis layer. See
  `docs/product/MOOD_READINESS_FEATURE_PLAN.md`.

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

## Home Assistant Services And To-do Projections

- Home Assistant service handlers are thin adapters around the local Homekeep
  service runtime, which delegates durable mutations to `SessionEngine` and
  recommendation work to `RecommendationEngine`.
- Service payload validation is split between Home Assistant voluptuous schemas
  and core Homekeep validation so unit tests can exercise behavior without a
  live Home Assistant runtime.
- Data-producing Homekeep services use Home Assistant service responses.
  Mutation services may return optional action responses when the caller asks
  for one.
- Home Assistant To-do entities are projections, not source of truth.
- To-do entities expose update support so projected item completion can write
  through to Homekeep.
- To-do creates, deletes, edits/renames, and moves/reorders are rejected and the
  projection refreshes from Homekeep storage.
- Recommendation To-do items are launchable suggestions only in Phase 5; only
  active-session To-do items with valid Homekeep projection metadata can be
  completed directly from Home Assistant.
- If a recommendation To-do item is completed while a matching Chore is already
  present as a pending item in an active Chore Session, Homekeep may resolve the
  write-through to that active session item. Recommendation-only completion
  without a matching active session remains rejected.
- Homekeep no longer exposes private dev mode, bundled sample Chore seeding,
  or `homekeep.load_sample_chores`.
- Config entry setup must load existing Homekeep storage only. It must not
  create synthetic Chores, repair sample state, or clear durable data for
  private testing.

## Homekeep Dashboard

- The canonical Homekeep UI direction is a Home Assistant sidebar app.
- Lovelace is not part of the Homekeep UI implementation plan.
- Do not build, restore, ship, or maintain Lovelace dashboard templates,
  Lovelace helper/script bridge flows, or Lovelace-specific tests.
- Former dashboard examples are no longer part of the MVP direction.
- The app may hold temporary UI identifiers from action responses while durable
  state remains in Homekeep storage.
- The first Homekeep sidebar app implementation is a mocked Ready Now prototype.
  It registers a non-iframe custom panel and uses synthetic local UI state only;
  it must not be treated as durable Homekeep state or backend service wiring.
- Home Assistant sensors and To-do entities remain projections instead of
  duplicating recommendation or session state in dashboard-only durable data.
- Stored legacy completion records with source `bubble_card` migrate to
  `dashboard`; new service calls should use `dashboard`.
- The app Add Chore flow calls `homekeep.create_chore`; it must not use
  To-do create operations as a write-through path.

## MVP Scope

- Stay inside MVP unless Steve explicitly expands scope.
- Homekeep's sidebar app is the MVP dashboard layer.
- No complex fairness scoring, punitive gamification, or broad future scope in
  MVP.
