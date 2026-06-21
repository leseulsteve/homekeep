# Private Live Test Results

This is the result note for the first Homekeep private HACS live test. It is
not a public release note.

## Test Candidate

- Date: 2026-06-21
- Homekeep commit at final diagnostics confirmation: `08fdf6e`
- Install method: HACS custom repository
- Home Assistant target:
  - Core: `2026.6.3`
  - Supervisor: `2026.06.2`
  - Operating System: `17.3`
  - Frontend: `20260527.6`
- Synthetic Chore set: bundled `custom_components/homekeep/sample_chores.yaml`
  with 22 synthetic Chores
- Calendar entity used: `calendar.activites`

## Passed

- HACS install and config entry setup.
- Private dev-mode sample Chore seeding.
- Due-count and per-Chore due binary sensors after sample due-state repair.
- Home Health and core Homekeep sensors present.
- `homekeep.generate_smart_chore_list` ready-now recommendation response.
- `homekeep.start_recommendation` materialized sessions with concrete
  `session_item_id` values.
- `homekeep.complete_chore`, duplicate completion idempotency, `skip_chore`,
  `snooze_chore`, and `end_session` smoke tests.
- To-do projections for recommendations and active sessions.
- To-do UI completion write-through to an active Homekeep session.
- Unsupported To-do edit/create/delete/reorder paths blocked by UI or
  Homekeep validation.
- Calendar Context manual refresh with minimized derived output only.
- Recommendation generation after Calendar Context refresh.
- Reload and restart recovery.
- Privacy/diagnostics scan for Homekeep logs after fixes.

## Fixed During Test

- Bundled sample Chores initially created entities but did not make any Chores
  due because `next_due_at` was `null`.
- Dev-mode sample seeding was changed to make unstarted sample Chores
  immediately due for private testing.
- To-do projection metadata initially caused UI completion to fail with
  `projected item is not attached to an active session`.
- To-do projections now resolve matching recommendation items to active-session
  metadata and expose documented entity ids:
  - `todo.homekeep_recommendations`
  - `todo.homekeep_active_session`
- Sample Chore YAML loading initially caused Home Assistant blocking file I/O
  warnings during setup. Loading now uses Home Assistant's executor when
  `hass` is available.

## Open Items

- Explicit Calendar Context invalidation after modifying a selected calendar
  entity was not confirmed; the calendar context sensor stayed `clear`.
- Calendar listener behavior after reload is not live-confirmed.
- Manual unload was not available in the Home Assistant UI; local automated
  unload tests cover this path.
- Bubble Card dashboard MVP was not live-tested in this pass.
- Home Assistant package-backed automated integration tests are still missing.

## Release Blockers

- Do not treat this as public-release ready.
- Before any version bump or public release, add or run Home Assistant
  package-backed tests for config flow, services, entities, To-do projections,
  calendar invalidation, reload/unload, and service responses.
- Resolve or explicitly accept the remaining Calendar Context invalidation
  uncertainty.
- Complete Bubble Card helper/script live testing if dashboard readiness is
  part of the release target.
- Update mock adequacy review for the release diff.
- Get explicit Steve approval before any release, deploy, publish, or tag.
