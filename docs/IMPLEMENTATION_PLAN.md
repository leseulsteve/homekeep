# Implementation Plan

## Phase 0: Scaffold

- Create Home Assistant custom integration skeleton.
- Add `manifest.json`, `const.py`, `__init__.py`, `config_flow.py`.
- Add `python-dateutil` to `manifest.json` requirements.
- Add initial tests and Home Assistant test fixtures.
- Add storage helper with current version `2`.
- Implement v1-to-v2 storage migration for old ChoreState dismissal/snooze
  fields.
- Register empty services with schemas.
- Register data-producing services with Home Assistant action response support.

Done when:

- The integration loads.
- Config flow can create an entry.
- Tests can import the integration.
- Empty storage loads and saves.
- Version 1 stores migrate to version 2 deterministically.
- Service registration tests verify response support for data-producing
actions.

## Phase 1: Core Models And Health

- Implement typed models.
- Validate chore definitions.
- Implement ChoreState.
- Implement context fingerprint generation from normalized recommendation
  context.
- Implement target time window parsing and normalization with `python-dateutil`
  and Home Assistant local timezone helpers.
- Enforce `adaptive_interval_days` write-time clamping against
  `min_interval_days` and `max_interval_days`.
- Implement derived staleness calculation.
- Implement completion credit and `next_due_at` derivation for tiny, normal,
  and deep variants.
- Implement Home Health and Area Health as derived read-time calculations or
  disposable caches rebuilt from durable state.
- Implement `homekeep_area_health_changed` only for bucket crossing or at least
  10-point Area Health delta.
- Add tests for invalid intervals, non-finite values, adaptive interval clamping,
  and health weighting.

Done when:

- Sample chores produce deterministic health scores.
- Tiny, normal, and deep completion credit produce deterministic `next_due_at`
  and Staleness behavior.
- Health scores can be recomputed after cache loss or restart.
- Area Health events are meaningful and do not fire during cache rebuild.
- Invalid data fails clearly.

## Phase 2: Chore Sessions

- Implement Chore Session materialization through `start_recommendation`.
- Track selected chores and session item status.
- Validate RecommendationSnapshot freshness before starting a Chore Bundle.
- Implement `start_recommendation` so bundle and single-chore recommendations
can both be materialized.
- Return materialized `SessionItem` records with concrete `session_item_id`
  values from `start_recommendation`.
- Materialize snapshot contents into a Chore Session so active sessions do not
depend on later snapshot freshness.
- Implement complete, skip, snooze, dismiss, pause, and end.
- Store bounded dismissal and snooze event timestamps on ChoreState.
- Store `snoozed_until` and enforce the 5-to-1440-minute snooze bound in
  `docs/SNOOZE_POLICY.md`.
- Validate `completed_by` against session participants for session completions.
- Ensure only completion creates ChoreCompletion.
- Add adaptive interval update on completion.
- Ensure snooze, skip, dismiss, swap, and cancel do not train adaptive interval.
- Make dismiss_chore idempotent when request_id is supplied.
- Implement bounded Bonus Chore lifecycle using `bonus_pending` and
`bonus_active`.
- Allow `active -> bonus_pending` and `paused -> bonus_pending` when planned
  items are complete and a Bonus Chore is offered.
- Set and enforce 15-minute `bonus_chore_expires_at` for pending Bonus Chore
  offers.
- Implement `accept_bonus_chore`.
- Add engine mutation locking and request-id idempotency.
- Store idempotency records for 24 hours and prune expired or over-cap records.

Done when:

- A session can start, update, and end through services.
- Expired or invalidated RecommendationSnapshot records cannot start new
sessions.
- Active sessions remain valid after source snapshot expiry.
- Duplicate service retries do not create duplicate sessions or completions.
- Idempotency records remain useful for slow retries and are bounded by TTL and
  max record count.
- Session completion attribution is validated and stored consistently.
- Bonus Chore uses the original session_id and cannot create an unbounded chain.
- Pending Bonus Chore offers expire and complete the session lazily.
- Paused sessions can offer a Bonus Chore only after planned items are complete.
- Completion updates durable state; health recomputes correctly on read.
- Skips/snoozes/dismissals do not mutate completion history or adaptive
intervals.
- Snoozes cannot hide chores for longer than 24 hours per request.

## Phase 3: Recommendation Engine V1

- Implement normalized component scoring.
- Implement best bundle, best single chore, easiest useful chore.
- Implement recommendation explanations.
- Implement empty state.
- Implement conservative Mood Context inference for planning defaults and
  recommendation wording.
- Generate `context_fingerprint` for every RecommendationSnapshot and copy it
  to materialized Chore Sessions.
- Normalize target time windows before snapshot creation and fingerprinting.
- Implement dismissal penalty with the formula, decay, cooldown, and staleness
  override in `docs/DISMISSAL_PENALTY.md`.
- Exclude chores with future `snoozed_until` before normal recommendation
  scoring.
- Add bounded Session-History Learning stats with deterministic context buckets
  and fallback matching.
- Convert datetimes to Home Assistant local time with
  `homeassistant.util.dt.as_local()` before deriving history day/time buckets.

Done when:

- A Ready-Now request returns a bounded Smart Chore List.
- Recommendations include explanations and Projected Impact.
- Context fingerprint is deterministic and distinct from context bucket.
- Target time windows parse consistently and are stored as normalized local ISO
  windows.
- Mood Context can influence defaults and wording without overriding explicit
  user choices.
- Recent dismissals reduce future recommendations with bounded decay and never
hide stale chores forever.
- Future-snoozed chores are excluded until their target time and re-enter
recommendations afterward.
- Sparse history falls back to broader buckets or neutral scoring.
- History buckets match local Home Assistant day/time, not UTC day/time.

## Phase 4: Home Assistant Entities

- Add sensors for Home Health, due chore count, best next chore, and calendar
context.
- Add due binary sensors.
- Add To-do projections for recommendations and active session.
- Ensure To-do completion calls Homekeep completion logic.
- Reject or revert To-do create/delete/rename/edit/reorder attempts so To-do
entities cannot become a second source of truth.

Done when:

- Entities update after session changes.
- To-do entities are projections, not a second source of truth.
- Unsupported To-do mutations do not mutate Homekeep state.

## Phase 5: Calendar Context

- Select calendar entities in options.
- Read upcoming calendar data.
- Convert events into derived Calendar Context.
- Register state listeners for selected calendar entities.
- Invalidate Calendar Context snapshots when selected calendar entities change.
- Enforce max-age freshness checks before recommendation scoring.
- Support simple rule-based matching for guests, travel, trash, maintenance,
and busy windows.

Done when:

- Calendar Context can influence a Scheduled-Suggestion recommendation.
- Adding or modifying a calendar event invalidates stale Calendar Context.
- Expired Calendar Context is refreshed or ignored before scoring.
- Raw event details are not stored in long-lived history unless necessary.

## Phase 6: Homekeep App MVP

- Build a Home Assistant sidebar app shell.
- Build an "I'm ready" setup view.
- Wire time, energy, and goal controls to services.
- Show Smart Chore List and active session.
- Add Scheduled-Suggestion planned proposal view with target window, expiry,
  start, refresh, and dismiss actions.
- Add "Done for now" and "One more" actions.

Done when:

- A user can run the main Ready-Now flow from Home Assistant UI.
- A user can plan a Scheduled-Suggestion proposal and refresh it if it expires
before starting.

## Phase 7: Hardening

- Add storage migration tests.
- Add malformed service payload tests.
- Add stale session response tests.
- Add reload/unload behavior.
- Add basic documentation.

Done when:

- The MVP acceptance criteria pass.
