# Scaffolding Tasks

Use this as the first implementation checklist.

## 1. Create Integration Skeleton

- `custom_components/homekeep/manifest.json`
- Add `python-dateutil` to `manifest.json` requirements for
  `target_time_window` parsing.
- `custom_components/homekeep/const.py`
- `custom_components/homekeep/__init__.py`
- `custom_components/homekeep/config_flow.py`
- `custom_components/homekeep/services.yaml`
- `custom_components/homekeep/strings.json`

## 2. Add Core Models

- Create `models.py`.
- Define enums for energy, variant, session status, item status, mode, source.
- Define typed structures for stored objects.
- Add validation helpers.
- Add context fingerprint helper from `docs/specs/CONTEXT_FINGERPRINT.md`.
- Add target time window parser from `docs/specs/TARGET_TIME_WINDOW.md`.

## 3. Add Storage

- Create `storage.py`.
- Add versioned storage key.
- Add empty store factory.
- Add load/save helpers.
- Add migration hook.
- Implement v1-to-v2 migration from `docs/architecture/STORAGE_MIGRATIONS.md`.

## 4. Add Health

- Create `health.py`.
- Implement derived staleness calculation.
- Implement completion credit and `next_due_at` rules from
  `docs/specs/COMPLETION_CREDIT.md`.
- Implement adaptive interval update helper with write-time clamping.
- Implement Home Health, Area Health, Group Health, and Projected Impact as
  derived calculations.
- Implement `homekeep_area_health_changed` threshold rules from
  `docs/specs/DERIVED_HEALTH.md`.
- If adding caches, make them disposable and rebuildable.

## 5. Add Scoring And Recommendations

- Create `scoring.py`.
- Create `recommendations.py`.
- Generate `context_fingerprint` for every RecommendationSnapshot.
- Normalize `target_time_window` before scoring, snapshot storage, and context
  fingerprinting.
- Implement v1 weighted scoring.
- Implement dismissal penalty exactly as documented in
  `docs/specs/DISMISSAL_PENALTY.md`.
- Exclude future-snoozed chores according to `docs/specs/SNOOZE_POLICY.md`.
- Implement explanations.
- Implement empty state.
- Implement best bundle, best single chore, easiest useful chore.
- Give every returned recommendation a stable `recommendation_id`.
- Use the shared Recommendation payload shape.

## 6. Add Sessions

- Create `sessions.py`.
- Implement session lifecycle.
- Validate RecommendationSnapshot freshness before starting a Chore Bundle.
- Implement `start_recommendation` for bundles and single-chore recommendations.
- Store `source_recommendation_snapshot_id` on created sessions.
- Copy `context_fingerprint` from RecommendationSnapshot to ChoreSession.
- Implement session item mutation.
- Store bounded dismissal and snooze event timestamps.
- Store and clear `snoozed_until` according to `docs/specs/SNOOZE_POLICY.md`.
- Validate session completion attribution against participants.
- Implement Bonus Chore lifecycle with `bonus_pending` and `bonus_active`.
- Implement `accept_bonus_chore`.
- Protect against stale session mutation.
- Ensure only real completions train adaptive intervals.

## 7. Add History

- Create `history.py`.
- Implement bounded Session-History Learning stats.
- Implement deterministic v1 context bucket generation.
- Convert Home Assistant datetimes with `homeassistant.util.dt.as_local()`
  before deriving history `day_type` or `time_block`.
- Implement Mood Context inference from `docs/specs/MOOD_CONTEXT.md`.
- Implement fallback bucket matching and neutral score fallback.
- Update stats after accept, complete, skip, snooze, dismiss.
- Do not use Session-History Learning as a replacement for the deterministic
  dismissal penalty formula.

## 8. Add Calendar Context

- Create `calendar_context.py`.
- Read selected calendar entities.
- Convert events into derived context.
- Add source calendar entity version tracking.
- Add max-age freshness checks.
- Add Home Assistant state listeners for selected calendar entities.
- Invalidate affected snapshots on calendar entity changes.
- Add rule matching for guests, travel, trash, maintenance, busy windows.

## 9. Add Home Assistant Glue

- Create `engine.py`.
- Create `coordinator.py`.
- Register services.
- Register data-producing services with Home Assistant action response support
  according to `docs/specs/ACTION_RESPONSES.md`.
- Add mutation lock and request-id idempotency handling.
- Implement idempotency record TTL and pruning from
  `docs/architecture/CONCURRENCY_AND_IDEMPOTENCY.md`.
- Add sensors.
- Add binary sensors.
- Add To-do projections.
- Reject or revert unsupported To-do mutations: create, delete, rename, edit,
  and reorder.
- In `todo.py` unsupported mutation handlers, call `self.async_write_ha_state()`
  after rejecting or ignoring the mutation so the Home Assistant UI refreshes
  from Homekeep storage.
- Require valid Homekeep metadata for To-do completion write-through.

## 10. Add Homekeep Sidebar App

- Add the app shell after the Home Assistant frontend extension approach has
  been verified.
- Include launcher, question controls, recommendation display, and session
  actions.

## 11. Add Tests

- Add tests in the order listed in `docs/implementation/TEST_PLAN.md`.
- Prioritize storage, health, scoring, sessions, and services before app UI.

## 12. Documentation Pass

- Verify `PROJECT_BRIEF.md` is human-readable.
- Verify docs match actual service names.
- Verify config entry setup does not seed or mutate storage.
