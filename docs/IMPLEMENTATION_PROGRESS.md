# Implementation Progress

Codex must update this file at the end of every implementation phase.

Use it as the resume point for future sessions. Do not rely on chat memory.

## Current Status

```yaml
current_phase: 8
current_phase_name: Hardening and release readiness
last_updated: 2026-06-21
last_codex_summary: >
  Private live-test readiness is continuing after Phase 8. Calendar Context now
  stores a minimized event fingerprint and recommendation generation refreshes
  context when selected calendar events change even if the Home Assistant
  calendar entity state stays unchanged. Calendar signal matching now includes
  English and basic French terms, Gate 6 is live-confirmed in the private HACS
  test instance, and Gate 8 now has a pasteable helper/script example. No
  deploy or release was performed.
```

## Phase Checklist

- [x] Phase 0: Scaffold
- [x] Phase 1: Models and storage
- [x] Phase 2: Health and adaptive intervals
- [x] Phase 3: Chore Session lifecycle
- [x] Phase 4: Recommendation Engine V1
- [x] Phase 5: Home Assistant services and entities
- [x] Phase 6: Calendar Context
- [x] Phase 7: Bubble Card MVP
- [x] Phase 8: Hardening and release readiness

## Phase Log

Add a new entry after each implementation pass.

Template:

```markdown
### YYYY-MM-DD - Phase N: Name

Status: not_started | in_progress | completed | blocked

Implemented:
- ...

Tests/checks run:
- ...

Docs updated:
- ...

Important decisions:
- ...

Known gaps / next prompt:
- ...
```

### 2026-06-21 - Phase 1: Models and storage

Status: completed

Implemented:
- Added `custom_components/homekeep/models.py` with typed dataclasses/enums for
  Chore definitions, Chore Variants, Chore State, and Chore Completions.
- Added validation helpers for finite positive intervals, interval ordering,
  estimated durations, health weights, allowed Chore Variant keys, Variant
  credit bounds, adaptive interval clamping, bounded dismissal/snooze event
  timestamps, and MVP participant attribution.
- Added `custom_components/homekeep/storage.py` with canonical empty storage,
  current storage version `2`, a v1-to-v2 migration hook, unsupported future
  version rejection, validation on load, JSON-safe dump helpers, and sample
  chore loading for tests.
- Added focused `unittest` coverage for invalid intervals, Chore Variant
  validation, participant attribution, v1-to-v2 migration behavior, future
  version rejection, sample chore loading, and storage round trip.

Tests/checks run:
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`

Docs updated:
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept Phase 1 pure Python because the requested deliverables do not require
  Home Assistant APIs. No Home Assistant API behavior was assumed.
- Used a tiny fixture-specific YAML parser for `examples/sample_chores.yaml`
  because PyYAML is not installed in the current environment.
- Treated Steve's Phase 1 request as an explicit override of the resume rule
  that would otherwise start with incomplete Phase 0 scaffold work.

Known gaps / next prompt:
- Phase 0 Home Assistant scaffold remains incomplete: no manifest, config
  flow, service registration, or Home Assistant storage wrapper exists yet.
- Health, completion credit application, adaptive interval training, and
  Home/Area Health derivation remain for the next bounded implementation pass.
- Pytest and PyYAML are not installed in this environment; current tests use
  standard-library `unittest`.

### 2026-06-21 - Phase 0: Scaffold

Status: completed

Implemented:
- Added the Home Assistant custom integration scaffold:
  `manifest.json`, `config_flow.py`, `services.yaml`, and `strings.json`.
- Expanded `const.py` with Homekeep domain metadata, platform list, service
  names, service attributes, and allowed enum values used by service schemas.
- Implemented `async_setup`, `async_setup_entry`, and `async_unload_entry` in
  `__init__.py` with empty Phase 0 handlers and schema-validated service
  registration.
- Registered data-producing services with `SupportsResponse.ONLY` and mutation
  or refresh services with `SupportsResponse.OPTIONAL`; no recommendation or
  session logic was implemented.
- Added `HomekeepStorage`, a Home Assistant storage adapter around the existing
  versioned core store, so load paths migrate, validate, repair, and save the
  canonical storage shape.
- Added `tests/test_homekeep_scaffold.py` for manifest, config flow, response
  support wiring, service metadata, and HA storage adapter checks.

Tests/checks run:
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`

Docs updated:
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Home Assistant and Voluptuous are not installed in this local environment, so
  Home Assistant APIs were verified against official Home Assistant developer
  docs instead of installed package source.
- Kept Home Assistant imports lazy in `__init__.py` and `storage.py` so the
  pure core tests remain runnable without a local Home Assistant install.
- Used the backed-up GitHub Phase 0 scaffold as historical reference only; the
  implementation was adapted to the current Homekeep service names and storage
  version `2`.

Known gaps / next prompt:
- The scaffold services intentionally return no-op scaffold responses and do
  not generate recommendations, create sessions, or mutate chore state.
- Full Home Assistant integration tests were not run because Home Assistant,
  Voluptuous, and pytest are not installed locally.
- Next recommended prompt: Implement Phase 2 health/adaptive interval helpers:
  completion credit application, adaptive interval training, derived Staleness,
  Home Health, Area Health, and focused tests.

### 2026-06-21 - Phase 2: Health and adaptive intervals

Status: completed

Implemented:
- Added `custom_components/homekeep/health.py` with pure derived functions for
  Staleness, display/priority Staleness, Chore Health, Home Health, Area
  Health, Area Health buckets, Area Health event threshold decisions, and
  Projected Impact.
- Added adaptive interval helpers using the documented v1 formula:
  `old * 0.70 + actual_gap * 0.30`, clamped to each Chore's
  `[min_interval_days, max_interval_days]`.
- Added completion scheduling helpers for Chore Variant credit and
  `next_due_at` derivation, including tiny completions that update schedule
  relief without training adaptive intervals.
- Added explicit non-completion action handling so skip, snooze, dismiss, and
  cancel preserve `adaptive_interval_days`.
- Kept health and staleness out of durable storage; the implementation derives
  values from durable Chore definitions and Chore state on read.
- Added `tests/test_health.py` covering cache loss/restart recomputation,
  completion-followed-by-restart recomputation, min/max interval clamping,
  first completion behavior, tiny/normal/deep completion effects, non-training
  actions, Projected Impact, and Area Health event thresholds.

Tests/checks run:
- `python3 -m unittest tests.test_health -v`
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`

Docs updated:
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Used deterministic MVP health formulas where planning docs were qualitative:
  Chore Health is `100 - capped_display_staleness`; Home Health and Area
  Health are enabled-Chore, health-weighted averages.
- Treated missing completion history as fully stale for derived display health,
  while never persisting that staleness result.
- Kept Phase 2 pure Python and independent from Home Assistant runtime APIs.

Known gaps / next prompt:
- Session services still do not create completions or mutate Chore State; Phase
  3 should wire Chore Session lifecycle and service behavior through the engine.
- Group Health is not yet exposed separately because the Phase 2 prompt asked
  for Home Health, Area Health, Staleness, and Projected Impact.
- Next recommended prompt: Implement Phase 3 Chore Session lifecycle with
  materialized Session Items, completion/skip/snooze/dismiss state changes,
  participant attribution, Bonus Chore lifecycle, and focused tests.

### 2026-06-21 - Phase 3: Chore Session lifecycle

Status: completed

Implemented:
- Added `custom_components/homekeep/sessions.py` with a pure core
  `SessionEngine` that serializes durable mutations through an `RLock`.
- Implemented Chore Session start, pause, completion, skip, snooze, dismiss,
  end, Bonus Chore acceptance, lazy Bonus Chore expiry, and terminal-state
  transition guards.
- Materialized Session Items at session start with stable `session_item_id`
  values and caller-facing session response dictionaries.
- Wired completions through the Phase 2 completion helpers so completions update
  durable `ChoreCompletion`, `ChoreState.last_completed_at`,
  `adaptive_interval_days`, and `next_due_at`.
- Added participant attribution validation: out-of-session participants are
  rejected; omitted `completed_by` defaults to `started_by` when available.
- Implemented skip/snooze/dismiss item handling without creating completions or
  training adaptive intervals; snooze and dismissal update bounded ChoreState
  event timestamps.
- Implemented bounded `bonus_pending` and `bonus_active` lifecycle with a
  15-minute pending offer TTL, one Bonus Chore per session, original
  `session_id` reuse, and completion of the accepted Bonus Chore ending the
  session.
- Added request-id idempotency records with 24-hour TTL and 1000-record cap;
  duplicate valid retries return the stored result.
- Added `tests/test_sessions.py` for allowed/disallowed transitions, duplicate
  completion calls, request-id idempotency, participant attribution, skip vs
  complete conflicts, snooze/dismiss side effects, Bonus Chore acceptance,
  expiry, paused-session Bonus Chore eligibility, and incomplete-session
  rejection.

Tests/checks run:
- `python3 -m unittest tests.test_sessions -v`
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept Phase 3 pure Python and storage-backed rather than wiring Home Assistant
  services yet; Phase 0 service handlers still return scaffold responses.
- Stored sessions as JSON-safe dictionaries inside the existing versioned store
  so later service/entity layers can persist them without a migration.
- Implemented a small explicit `start_session` helper for tests and future
  service wiring; RecommendationSnapshot materialization remains for the
  Recommendation Engine pass.

Known gaps / next prompt:
- Home Assistant service handlers still need to call `SessionEngine`; they
  remain no-op scaffold handlers until the service/entity wiring phase.
- RecommendationSnapshot freshness/materialization is not implemented yet and
  should be handled with the Recommendation Engine V1 work.
- Next recommended prompt: Implement Phase 4 Recommendation Engine V1 with
  deterministic scoring, Smart Chore List payloads, RecommendationSnapshots,
  context fingerprints, dismissal/snooze effects, and focused tests.

### 2026-06-21 - Phase 4: Recommendation Engine V1

Status: completed

Implemented:
- Added `custom_components/homekeep/recommendations.py` with deterministic,
  local Recommendation Engine V1 scoring. No LLM or network behavior is used.
- Added normalized component scoring for Staleness, Projected Impact, time fit,
  energy fit, area fit, neutral Calendar Context, Session-History fit, and
  bounded dismissal penalty.
- Added bounded Smart Chore List generation with best Chore Bundle, best single
  chore, easiest useful chore, up to 3 alternates, empty state handling, short
  explanations, projected impact payloads, and stable `recommendation_id`
  values within a RecommendationSnapshot.
- Added RecommendationSnapshot storage with `context_fingerprint`,
  `context_bucket`, candidate score breakdowns, selected recommendations,
  explanations, expiry, invalidation fields, and materialization tracking.
- Added fresh snapshot materialization through the existing `SessionEngine`;
  expired or invalidated snapshots are rejected and fresh sessions copy the
  snapshot `context_fingerprint`.
- Added `custom_components/homekeep/history.py` with deterministic v1
  `context_bucket` generation and sparse Session-History fallback scoring to
  neutral `50.0` when observations are insufficient.
- Added `tests/test_recommendations.py` covering payload shape, stable IDs,
  context fingerprint normalization, sparse history fallback, expired snapshot
  rejection, and fresh snapshot materialization.

Tests/checks run:
- `python3 -m unittest tests.test_recommendations -v`
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept the Recommendation Engine pure Python and deterministic; Home Assistant
  service handlers are still scaffold no-ops until Phase 5 wiring.
- Used a neutral `50.0` Calendar Context score until Calendar Context snapshots
  are implemented.
- Used a deterministic `ctx:v1:<sha256>` context fingerprint from normalized
  non-secret context fields, ignoring volatile timestamps like `created_at`.

Known gaps / next prompt:
- Home Assistant services still need to call `RecommendationEngine` and
  `SessionEngine`, persist changed stores, and return action-response payloads.
- Calendar Context, Mood Context inference, and richer dismissal cooldown logic
  remain future phases or hardening work.
- Next recommended prompt: Implement Phase 5 Home Assistant service wiring and
  initial entities/to-do projections around the existing core engine.

### 2026-06-21 - Phase 5: Home Assistant services and entities

Status: completed

Implemented:
- Replaced the Phase 0 scaffold service handler with real Homekeep service
  handlers that load the active integration store, call a small
  `HomekeepServiceRuntime`, persist successful mutations, and translate core
  validation errors to Home Assistant service validation errors when Home
  Assistant is installed.
- Added `custom_components/homekeep/runtime.py` as a testable adapter over
  `RecommendationEngine` and `SessionEngine` for Smart Chore List generation,
  recommendation/session starts, complete/skip/snooze/dismiss, pause, accept
  Bonus Chore, end session, and a minimized calendar-context refresh stub.
- Enabled Phase 5 platforms: `sensor`, `binary_sensor`, and `todo`.
- Added initial sensors for Home Health, due Chore count, best next Chore, and
  minimized calendar context.
- Added per-Chore due binary sensors.
- Added To-do projections for latest recommendations and the active Chore
  Session. Active-session projected completions write through with Homekeep
  metadata; create/delete/edit/rename/move/reorder attempts refresh the
  projection and raise a Homekeep mutation error.
- Added tests for malformed service payloads, unknown IDs, service
  idempotency, valid projected To-do completion, invalid projection completion,
  and To-do mutation traps.

Home Assistant API verification:
- Home Assistant is not installed in the local test environment, so Phase 5 API
  assumptions were verified against official Home Assistant developer docs.
- Verified service action registration/response support expectations from the
  Home Assistant service developer docs.
- Verified `TodoListEntity`, `TodoItem`, `TodoItemStatus`, supported feature
  flags, and async create/delete/update/move handlers from the official To-do
  entity developer docs.
- Verified the basic sensor and binary sensor entity patterns from the official
  entity developer docs.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components/homekeep`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`

Docs updated:
- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept service behavior small and local: Home Assistant handlers adapt payloads
  and persistence, while existing Homekeep engines remain authoritative for
  durable mutations and recommendation behavior.
- To-do projections advertise update support only so Home Assistant can send
  completion updates; updates that are actually edits/renames are rejected and
  refreshed from storage.
- Recommendation To-do items remain non-completable suggestions until a
  recommendation is materialized into a session; active-session To-do items are
  the write-through completion surface.
- Calendar refresh remains a minimized Phase 5 stub with no raw calendar event
  details; the full Calendar Context phase still owns real calendar snapshot
  behavior.

Known gaps / next prompt:
- Home Assistant package is not installed locally, so Phase 5 was verified with
  unit tests plus official docs rather than an in-process Home Assistant test
  harness.
- Entity coverage is intentionally MVP-minimal; unload/reload behavior,
  dynamic entity additions after chore import, and richer action response
  payloads should be hardened in the Phase 9 test/reload pass.
- Calendar Context, Bubble Card dashboard wiring, and To-do area projections
  remain later phases.
- Next recommended prompt: Implement Phase 6 Calendar Context with minimized
  durable snapshots, freshness checks, entity invalidation, and tests.

### 2026-06-21 - Mood Context Post-Prototype Planning

Status: completed

Implemented:
- Added a post-prototype improvement note to `docs/MOOD_CONTEXT.md` for
  evolving Mood Context into broader Readiness Context after the MVP prototype.
- Captured the future direction in `docs/DECISION_LOG.md` so future
  implementation keeps mood optional, explainable, and subordinate to practical
  planning signals.

Tests/checks run:
- Not run; documentation-only update.

Docs updated:
- `docs/MOOD_CONTEXT.md`
- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- The MVP Mood Context rules remain unchanged.
- Post-prototype improvements should focus on chore friction, safer
  explanations, explicit session modes, and user correction rather than deeper
  emotional inference.

Known gaps / next prompt:
- Next implementation work remains Phase 5 Home Assistant service wiring unless
  Steve asks to revise Mood/Readiness Context docs further.

### 2026-06-21 - Mood And Readiness Feature Plan

Status: completed

Implemented:
- Added `docs/MOOD_READINESS_FEATURE_PLAN.md` as the coherent
  post-prototype plan for evolving Mood Context into Readiness Context.
- Consolidated session modes, chore-friction learning, safer explanation
  wording, Home Assistant signals, opt-in wearable signals, open-source/local
  source options, storage/privacy rules, implementation phases, and tests.
- Replaced the long post-prototype note in `docs/MOOD_CONTEXT.md` with a
  pointer to the dedicated feature plan.
- Updated `docs/DECISION_LOG.md` to reference the new plan.

Tests/checks run:
- `git diff --check -- docs/MOOD_READINESS_FEATURE_PLAN.md docs/MOOD_CONTEXT.md docs/DECISION_LOG.md docs/IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/MOOD_READINESS_FEATURE_PLAN.md`
- `docs/MOOD_CONTEXT.md`
- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- MVP Mood Context remains unchanged.
- Post-prototype Readiness Context should expose session posture to users
  rather than claiming to know the user's mood.
- Wearable and Home Assistant signals must be opt-in, derived, short-lived, and
  subordinate to explicit user choices.

Known gaps / next prompt:
- Next implementation work remains Phase 6 Calendar Context unless Steve asks
  for further Mood/Readiness planning.

### 2026-06-21 - Phase 6: Calendar Context

Status: completed

Implemented:
- Added `custom_components/homekeep/calendar_context.py` with selected calendar
  entity normalization, source version tracking, freshness checks, derived
  signal extraction, max-age expiry, context version hashes, and invalidation
  helpers.
- Added Home Assistant options for selecting calendar entities with a calendar
  entity selector.
- Wired `homekeep.refresh_calendar_context` to build minimized snapshots from
  selected or caller-provided calendar entities.
- Added lazy Calendar Context freshness refresh before Smart Chore List
  generation when selected calendars are configured.
- Added automatic invalidation listeners for selected calendar entity state
  changes during config entry setup, including dependent RecommendationSnapshot
  invalidation.
- Updated the Recommendation Engine to include fresh Calendar Context id/version
  in context fingerprints and RecommendationSnapshots, and to use a bounded
  derived calendar context score instead of a permanently neutral score.
- Updated the next-calendar-context sensor to report stale derived context when
  a snapshot has been invalidated.
- Added tests for derived snapshots, raw-detail minimization, max-age
  freshness, source version changes, target-window changes, calendar state
  invalidation, dependent recommendation invalidation, and runtime service
  wiring.

Home Assistant API verification:
- Home Assistant is not installed locally, so Phase 6 calendar assumptions were
  verified against official Home Assistant developer docs and current Home
  Assistant core source.
- Verified Calendar entities expose timezone-aware `async_get_events(hass,
  start_date, end_date)` patterns and `CalendarEvent` fields.
- Verified the built-in `calendar.get_events` service supports response data
  for event fetching.
- Verified `homeassistant.helpers.event.async_track_state_change_event` is the
  current state-change helper and that older `async_track_state_change` is
  deprecated.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_calendar_context -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Calendar Context stores only minimized derived signals and source version
  metadata; raw summary, description, and location text are used transiently
  during refresh and are not stored in durable snapshots.
- Recommendation generation refreshes stale selected Calendar Context lazily
  rather than doing unbounded background recommendation work on every calendar
  state change.
- The Phase 6 event fetch path uses Home Assistant's `calendar.get_events`
  service response instead of trying to reach into calendar entity internals.
- Calendar scoring remains bounded and explainable, with neutral behavior when
  there is no fresh context.

Known gaps / next prompt:
- Full in-process Home Assistant tests are still deferred because Home
  Assistant is not installed locally.
- Calendar signal extraction is MVP keyword-based and intentionally minimal;
  richer source-specific semantics can be hardened later.
- Existing uncommitted Mood/Readiness planning docs remain separate from Phase
  6 implementation work.
- Next recommended prompt: Implement Phase 7 Bubble Card MVP dashboard example
  and service wiring around the completed Homekeep services.

### 2026-06-21 - Phase 7: Bubble Card MVP dashboard example

Status: completed

Implemented:
- Added `examples/bubble_card_dashboard.yaml` with a Homekeep dashboard view,
  Ready-Now launcher, time/energy/goal/mood controls, recommendation display,
  active-session controls, Done for now, One more, and Accept one more flow.
- Used Bubble Card pop-ups, select cards, buttons, horizontal button stack, and
  sub-buttons for the touch-oriented dashboard surface.
- Used native Home Assistant To-do list and entities cards where Bubble Card is
  not the best fit for authoritative Homekeep projections or helper ids.
- Documented required companion helper entities and scripts in the example
  YAML so scripts can read local selections, call Homekeep services, and store
  returned response ids.
- Updated `docs/BUBBLE_CARD_MVP.md` with the Phase 7 capability gap and helper
  script bridge.

Bubble Card capability verification:
- Verified Bubble Card supports pop-up cards with nested cards.
- Verified Bubble Card supports button cards, name/state button types,
  sub-buttons, select cards for `input_select`/`select`, horizontal button
  stacks, and Home Assistant tap actions with `call-service` / `navigate`.
- Identified a gap: Bubble Card dashboard YAML should not be relied on to
  capture Home Assistant service response payloads and bind returned ids into
  later service calls.

Tests/checks run:
- `python3 - <<'PY' ...` dashboard example content check
- `git diff --check`

Docs updated:
- `docs/BUBBLE_CARD_MVP.md`
- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept the dashboard as an MVP example surface; Homekeep storage, sensors, and
  To-do projections remain authoritative.
- Used helper/script bridging for `snapshot_id`, `recommendation_id`,
  `session_id`, `session_item_id`, and Bonus Chore ids because those values
  come from Homekeep service responses or current session context.
- Did not add runtime code for scripts or helpers in Phase 7 because the prompt
  requested the dashboard example and not a Home Assistant package blueprint.

Known gaps / next prompt:
- The example assumes companion helpers and scripts exist. A future hardening
  pass can add packaged helper/script examples or native Homekeep entities that
  expose current recommendation/session ids directly.
- The dashboard YAML was syntax/content checked locally but not rendered in a
  live Home Assistant frontend with Bubble Card installed.
- Next recommended prompt: Implement Phase 8 hardening and release readiness:
  reload/unload behavior, migration edge cases, entity refresh behavior,
  service response polish, packaged helper/script examples, and focused Home
  Assistant integration tests where dependencies are available.

### 2026-06-21 - Phase 8: Hardening and release readiness

Status: completed

Implemented:
- Hardened `HomekeepServiceRuntime` so missing required service fields raise
  `HomekeepValidationError` instead of raw `KeyError`.
- Added malformed service payload tests for missing `chore_id`,
  `snooze_minutes`, `recommendation_snapshot_id`, `session_id`, and `status`.
- Added stale session response coverage: a stale completion attempt after
  session cancellation is rejected and does not create a completion or mutate
  terminal session state.
- Expanded storage migration tests for version `2` loading, missing optional
  sections, stale unknown-Chore state cleanup, and invalid stored values.
- Added config entry unload/reload mock coverage for platform unload success,
  failed platform unload preservation, and calendar listener cleanup.
- Added `docs/MOCK_ADEQUACY_REVIEW.md` for pre-`1.0` version-bump readiness.
- Updated `docs/IMPLEMENTATION_READINESS_REVIEW.md` with Phase 8 hardening
  notes and remaining public-release test gaps.

Deploy workflow status:
- Reviewed the working tree before changes.
- No version bump was requested or performed.
- No deploy, publish, tag, or release command was run.
- Pre-`1.0` mock adequacy was reviewed. Current mocks are adequate for local
  developer readiness, but not enough to claim public release readiness without
  Home Assistant package-backed tests or an approved live synthetic candidate.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_services tests.test_storage tests.test_reload_unload -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `git diff --check`

Docs updated:
- `docs/IMPLEMENTATION_PROGRESS.md`
- `docs/IMPLEMENTATION_READINESS_REVIEW.md`
- `docs/MOCK_ADEQUACY_REVIEW.md`

Important decisions:
- Kept Phase 8 scoped to local hardening and release readiness review. No
  deploy or version bump was performed because Steve explicitly said not to
  deploy unless asked.
- Used local fakes for Home Assistant lifecycle behavior because Home Assistant
  is not installed in the local environment.
- Treated Home Assistant package-backed integration tests as a remaining
  release-readiness gap rather than pretending source checks are equivalent.

Known gaps / next prompt:
- Add Home Assistant package-backed tests for config flow, service
  registration/action responses, sensors, binary sensors, To-do projections,
  calendar services, reload/unload, and entity refresh behavior.
- Add packaged helper/script examples for `examples/bubble_card_dashboard.yaml`
  if the dashboard should be one-copy deployable.
- Next recommended prompt: Add Home Assistant package-backed integration tests
  and release checklist automation, or ask explicitly for a version bump/release
  pass when ready.

### 2026-06-21 - Private HACS live-test seeding helper

Status: completed

Implemented:
- Added bundled synthetic Chore fixtures to the installed integration package
  for private HACS testing.
- Added a private `dev_mode` config/options toggle, defaulting to true, so a
  new config entry seeds bundled sample Chores automatically when storage is
  empty. The options flow reloads Homekeep when the toggle changes.
- Added `homekeep.load_sample_chores` with a `replace_existing` guard so the
  private test instance can explicitly reset synthetic Homekeep data from
  Developer Tools > Actions.
- Expanded the bundled fixture to 22 synthetic Chores across kitchen,
  bathroom, living room, entryway, laundry, bedroom, plants, office, hallway,
  and admin groups.
- Updated the private live-test checklist to use the bundled seed service.
- Adjusted README language so it describes Steve's private test status without
  public-user expectations.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_homekeep_scaffold tests.test_reload_unload tests.test_services tests.test_storage -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_services tests.test_storage -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `README.md`
- `docs/DECISION_LOG.md`
- `docs/HOME_ASSISTANT_CONTRACT.md`
- `docs/SERVICE_SCHEMAS.md`
- `docs/PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept sample loading as a private test seed helper, not a general Chore import
  API.
- Automatic setup seeding is gated by private dev mode and only runs when
  Homekeep storage has no Chores, so install/reload does not overwrite existing
  live-test data.
- The helper refuses to overwrite existing stored Chores unless
  `replace_existing=true`, and replacement intentionally resets other durable
  Homekeep test state to avoid mixed old/new synthetic data.

Known gaps / next prompt:
- Push the private dev-mode seeding update, then update/re-download Homekeep
  through HACS and run Gate 3 by confirming automatic synthetic Chore setup.

### 2026-06-21 - Private HACS live-test due-state repair

Status: completed and live-confirmed

Implemented:
- Updated bundled sample Chore seeding so synthetic Chore states are
  immediately due for private live testing instead of having `next_due_at=null`.
- Added a dev-mode setup repair for existing previously seeded sample Chores:
  if a bundled sample Chore exists, has no completion history, and has no
  `next_due_at`, setup marks it due without replacing Chore definitions or
  touching completed/scheduled Chores.
- Added regression coverage using the actual due-count sensor and per-Chore
  binary sensor classes.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_reload_unload tests.test_services tests.test_storage -v`

Important decisions:
- Kept normal `ChoreState.new_for_chore` unchanged. Only private bundled sample
  seed/repair behavior marks chores immediately due.
- Existing live-test stores from the first seed pass can be repaired by
  updating through HACS and restarting with dev mode enabled.

Known gaps / next prompt:
- Gate 3 synthetic data setup is live-confirmed on the private HACS install.
- Next prompt: run Gate 4 service smoke tests from Developer Tools > Actions,
  starting with `homekeep.generate_smart_chore_list`.

### 2026-06-21 - Calendar Context live-test hardening

Status: completed locally, pending private HACS live retest

Implemented:
- Added `source_calendar_event_fingerprint` to Calendar Context snapshots.
- Built the fingerprint from minimized event facts: event start/end times and
  derived guest, travel, trash, and evening flags. Raw event summary,
  description, and location text are not stored.
- Updated Calendar Context freshness checks so recommendation generation can
  detect added or modified selected calendar events even when the Home
  Assistant calendar entity state metadata remains unchanged.
- Changed Calendar Context refresh to invalidate dependent
  RecommendationSnapshots when the refreshed minimized calendar context version
  changes.

Tests/checks run:
- `python3 -m unittest tests.test_calendar_context -v`
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`

Docs updated:
- `docs/DECISION_LOG.md`
- `docs/CALENDAR_CONTEXT.md`
- `docs/PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/PRIVATE_LIVE_TEST_RESULTS.md`
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept the durable calendar data minimized by storing only a hash of reduced
  event facts and derived category flags.
- Treated event additions/modifications as enough to refresh Calendar Context
  before recommendation reuse, because some Home Assistant calendar providers
  may keep the calendar entity state as `off` after an event edit.

Known gaps / next prompt:
- Update Homekeep through HACS, restart/reload, then retest Gate 6 by adding or
  modifying a synthetic event on the selected test calendar and generating a
  fresh Smart Chore List. Confirm the Calendar Context snapshot changes and the
  old dependent RecommendationSnapshot is not reused.
- Bubble Card dashboard Gate 8 still needs private live testing.
- Home Assistant package-backed automated tests remain a public-release
  blocker.

### 2026-06-21 - Calendar Context French keyword support

Status: completed locally, pending private HACS live retest

Implemented:
- Added basic French Calendar Context keywords alongside the existing English
  terms for guest/visit, travel/departure, and trash/recycling/compost signals.
- Centralized keyword checks so derived Calendar Context signals and minimized
  event fingerprints classify events consistently.
- Added regression coverage using synthetic French calendar event titles.

Tests/checks run:
- `python3 -m unittest tests.test_calendar_context -v`

Docs updated:
- `docs/CALENDAR_CONTEXT.md`
- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept this as simple local keyword matching for private live testing, not a
  language model or broad localization system.
- Included accented and unaccented French forms for common live-test calendar
  phrases.

Known gaps / next prompt:
- Commit and push, update through HACS, then retest with a synthetic French
  event title such as `Visite d'invités pour souper`.

### 2026-06-21 - Gate 6 Calendar Context live confirmation

Status: completed and live-confirmed

Implemented:
- No code change in this pass; recorded private HACS live-test evidence for
  Calendar Context event-fingerprint and French keyword behavior.

Tests/checks run:
- Private HACS live test on Home Assistant Core `2026.6.3`.
- `homekeep.refresh_calendar_context` with selected calendar entity
  `calendar.activites`.
- `homekeep.generate_smart_chore_list` after refreshed Calendar Context.
- `sensor.homekeep_next_calendar_context` state check.

Docs updated:
- `docs/PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/PRIVATE_LIVE_TEST_RESULTS.md`
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Treated Gate 6 as live-confirmed after Homekeep detected a synthetic French
  event, derived `has_guests_soon: true`, stored only
  `source_calendar_event_fingerprint`, generated a fresh Smart Chore List, and
  exposed `guests` through `sensor.homekeep_next_calendar_context`.

Known gaps / next prompt:
- Calendar listener behavior after reload is still not separately
  live-confirmed.
- Bubble Card dashboard Gate 8 remains the next private live-test gate.
- Home Assistant package-backed automated tests remain a public-release
  blocker.

### 2026-06-21 - Bilingual string-signal guessing

Status: completed locally

Implemented:
- Added a shared `text_signals` helper for local English/basic-French keyword
  matching with case and accent normalization.
- Moved Calendar Context keyword classification onto the shared helper so
  derived signals and event fingerprints continue to treat French calendar text
  consistently.
- Updated Recommendation Engine calendar-fit guesses from Chore names, Chore
  groups, and Home Assistant Area ids so French terms such as `salle de bain`,
  `poubelles`, and `recyclage` can influence guest-prep and trash-day scoring.
- Added focused recommendation coverage for French Chore string guesses.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_recommendations tests.test_calendar_context -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `git diff --check`

Docs updated:
- `docs/CALENDAR_CONTEXT.md`
- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_PROGRESS.md`
- `docs/RECOMMENDATION_ENGINE.md`

Important decisions:
- Kept this as bounded local keyword matching, not a broad localization system
  or language model.
- Treated French support as a shared rule for all current string-based signal
  guesses rather than only Calendar Context event text.

Known gaps / next prompt:
- Full Home Assistant package-backed automated tests remain a public-release
  blocker.
- Bubble Card dashboard Gate 8 remains the next private live-test gate.

### 2026-06-21 - Bubble Card companion helper example

Status: completed locally, pending private HACS live retest

Implemented:
- Added `examples/bubble_card_helpers.yaml` with the input helpers and bridge
  scripts expected by `examples/bubble_card_dashboard.yaml`.
- Updated `accept_bonus_chore` responses to include the materialized bonus
  `session_item_id`, so the Bubble Card bridge can continue after accepting
  One more without scraping To-do internals.
- Updated Bubble Card and service docs to point at the companion helper file
  and document the bonus accept response.

Tests/checks run:
- `python3 -m unittest tests.test_sessions -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `python3 -m unittest discover -s tests -v`
- `git diff --check`

Docs updated:
- `docs/BUBBLE_CARD_MVP.md`
- `docs/SERVICE_SCHEMAS.md`
- `docs/PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept helper state in Home Assistant helper entities only as dashboard bridge
  state. Homekeep storage remains authoritative for Chores, sessions, and
  projections.
- The dashboard bridge stores the best single recommendation by default, with
  bundle/easiest fallback, because Lovelace cards cannot comfortably capture
  arbitrary service response choices without scripts.

Known gaps / next prompt:
- Run focused tests, commit, push, update through HACS, then paste/create the
  helpers/scripts and dashboard YAML in Home Assistant for Gate 8 live testing.

## Resume Instructions

When resuming implementation:

1. Read `AGENTS.md`.
2. Read this file.
3. Read the docs for the next incomplete phase.
4. Check `git status --short`.
5. Continue from the first unchecked phase unless Steve asks otherwise.
