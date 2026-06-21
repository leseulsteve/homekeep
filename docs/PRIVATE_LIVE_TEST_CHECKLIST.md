# Private Live Test Checklist For Codex

This is a Codex runbook for preparing Homekeep for a private live test in a
Home Assistant instance. It is not a public release checklist.

Codex should use synthetic data first. Do not start with real household
routines, private calendar text, personal schedules, or live credentials in
tracked files.

When a step requires access to Steve's live Home Assistant instance, private
calendar data, a deployment target, or a release decision, stop and ask Steve
before proceeding.

## Gate 0: Repository Readiness

- [x] Inspect the working tree: `git status --short`
- [x] Review intended changes and leave unrelated user work alone
- [x] Run current local tests:
  `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- [x] Run syntax compile:
  `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- [x] Run diff hygiene before any live-test commit: `git diff --check`
- [x] Review `docs/MOCK_ADEQUACY_REVIEW.md`
- [x] Confirm this is a private synthetic candidate, not a public release

## Gate 1: Home Assistant Test Instance

- [x] Ask Steve which disposable or clearly test-scoped Home Assistant instance
  to use
- [x] Ask Steve for the Home Assistant version targeted for the private test
- [x] Ask Steve whether Bubble Card dashboard testing is included
- [x] Confirm no production automations depend on Homekeep entities yet
- [x] Confirm selected calendar entities are synthetic or safe
- [x] Confirm backups/snapshots exist before installing the custom integration

Steve confirmed Gate 1 on 2026-06-21:

- target is Home Assistant OS private live-test instance
- Bubble Card dashboard testing is included
- no production automations depend on Homekeep entities yet
- selected calendar entities are synthetic or safe
- backup/snapshot exists before install

Target version reported by Steve:

```text
Home Assistant OS
Core: 2026.6.3
Supervisor: 2026.06.2
Operating System: 17.3
Frontend: 20260527.6
```

## Gate 2: Install Path

- [x] Decide the install method for `custom_components/homekeep`
- [x] Document the exact copy/sync command used
- [x] Ask before running commands that write outside this repository
- [x] Confirm `https://github.com/leseulsteve/homekeep` is public; HACS cannot
  install private GitHub repositories
- [x] Confirm HACS is installed and configured in the target Home Assistant
  instance
- [x] Add `https://github.com/leseulsteve/homekeep` as a HACS custom
  repository with type `Integration`
- [x] Download Homekeep from HACS
- [x] Restart Home Assistant after installing the integration
- [x] Verify Homekeep appears in integrations
- [x] Create one Homekeep config entry
- [x] Open Homekeep options and select test calendar entities if needed

Install method selected by Steve: HACS custom repository.

## Gate 3: Synthetic Data Setup

- [ ] Confirm Homekeep options show Developer mode enabled after install
- [ ] Confirm bundled synthetic Chores loaded automatically on setup
- [ ] If a reset is needed, use Developer Tools > Actions:
  `homekeep.load_sample_chores` with `replace_existing: true`
- [ ] Do not use real private room routines or private schedule details
- [ ] Confirm Homekeep storage contains Chore definitions and Chore state
- [ ] Confirm sensors exist:
  - [ ] `sensor.homekeep_home_health`
  - [ ] `sensor.homekeep_due_chore_count`
  - [ ] `sensor.homekeep_best_next_chore`
  - [ ] `sensor.homekeep_next_calendar_context`
- [ ] Confirm To-do entities exist:
  - [ ] `todo.homekeep_recommendations`
  - [ ] `todo.homekeep_active_session`
- [ ] Confirm per-Chore due binary sensors are created for synthetic Chores

## Gate 4: Service Smoke Test

Use Developer Tools > Actions.

- [ ] `homekeep.refresh_calendar_context` returns derived context only
- [ ] Calendar Context storage does not include raw event summary, description,
  or location text
- [ ] `homekeep.generate_smart_chore_list` returns a Smart Chore List response
- [ ] Response includes `snapshot_id`
- [ ] Response includes best recommendation ids when chores are available
- [ ] `homekeep.start_recommendation` starts a Chore Session from a fresh
  recommendation
- [ ] Start response includes `session_id`
- [ ] Start response includes materialized `session_item_id` values
- [ ] `homekeep.complete_chore` completes a materialized session item
- [ ] `homekeep.skip_chore` skips a materialized session item
- [ ] `homekeep.snooze_chore` rejects values below `5`
- [ ] `homekeep.snooze_chore` rejects values above `1440`
- [ ] `homekeep.end_session` completes or cancels the session cleanly
- [ ] Duplicate calls with the same `request_id` do not duplicate completions

## Gate 5: To-do Projection Smoke Test

- [ ] `todo.homekeep_recommendations` mirrors the latest Smart Chore List
- [ ] `todo.homekeep_active_session` mirrors active session items
- [ ] Completing a valid active-session To-do item writes through to Homekeep
- [ ] Completing an item without valid Homekeep metadata is rejected
- [ ] Creating a To-do item is rejected or snaps back
- [ ] Deleting a To-do item is rejected or snaps back
- [ ] Renaming/editing a To-do item is rejected or snaps back
- [ ] Reordering a To-do item is rejected or snaps back
- [ ] Unsupported To-do mutations do not alter Homekeep storage

## Gate 6: Calendar Context Smoke Test

- [ ] Select at least one safe test calendar entity in Homekeep options
- [ ] Refresh Calendar Context manually
- [ ] Generate recommendations with fresh Calendar Context
- [ ] Modify/add a synthetic event on a selected calendar entity
- [ ] Confirm Calendar Context is invalidated or refreshed before reuse
- [ ] Confirm dependent RecommendationSnapshots become invalidated when the
  Calendar Context source changes
- [ ] Confirm `sensor.homekeep_next_calendar_context` reflects stale/clear/guest
  or busy state as expected

## Gate 7: Reload And Unload

- [ ] Reload the Homekeep config entry
- [ ] Confirm durable state remains intact after reload
- [ ] Confirm sensors and To-do entities return after reload
- [ ] Confirm calendar state listeners still invalidate Calendar Context after
  reload
- [ ] Unload the Homekeep config entry
- [ ] Confirm Homekeep entities are removed/unavailable as expected
- [ ] Reload or restart and confirm Homekeep recovers stored state

## Gate 8: Bubble Card Dashboard

Use `examples/bubble_card_dashboard.yaml` only after companion helpers/scripts
exist.

- [ ] Create required `input_select` helpers:
  - [ ] `input_select.homekeep_time_budget`
  - [ ] `input_select.homekeep_energy_level`
  - [ ] `input_select.homekeep_goal`
  - [ ] `input_select.homekeep_mood`
- [ ] Create required `input_text` helpers:
  - [ ] `input_text.homekeep_recommendation_snapshot_id`
  - [ ] `input_text.homekeep_recommendation_id`
  - [ ] `input_text.homekeep_session_id`
  - [ ] `input_text.homekeep_session_item_id`
  - [ ] `input_text.homekeep_chore_id`
  - [ ] `input_text.homekeep_bonus_chore_id`
- [ ] Create bridge scripts documented in the dashboard example
- [ ] Paste/import `examples/bubble_card_dashboard.yaml`
- [ ] Ready-Now launcher opens
- [ ] Time, energy, goal, and mood controls work
- [ ] Generate button calls the bridge script
- [ ] Recommendation display updates from Homekeep entities/projections
- [ ] Start button materializes a recommendation
- [ ] Done, Skip, Snooze, Done for now, One more, and Accept one more call the
  intended scripts

## Gate 9: Privacy And Diagnostics

- [ ] No raw calendar descriptions are stored in durable Homekeep storage
- [ ] No private entity ids or personal schedules are copied into tracked files
- [ ] No credentials, tokens, cookies, or webhook URLs are present in logs or
  repo changes
- [ ] Errors are clear enough to act on from Developer Tools
- [ ] Logs do not expose raw calendar event details

## Gate 10: Result Notes

Codex should record results in a local note or a new docs file before any
release decision.

- [ ] Home Assistant version:
- [ ] Homekeep commit:
- [ ] Install method:
- [ ] Synthetic Chore set used:
- [ ] Calendar entities used:
- [ ] Service smoke test result:
- [ ] To-do projection result:
- [ ] Calendar invalidation result:
- [ ] Reload/unload result:
- [ ] Bubble Card result:
- [ ] Bugs found:
- [ ] Release blockers:

## Public Release Still Requires

- [ ] Home Assistant package-backed tests or approved live synthetic candidate
  results
- [ ] Version bump decision
- [ ] Release notes
- [ ] Mock adequacy review updated for the release diff
- [ ] Explicit Steve approval for any deploy/release/publish action
