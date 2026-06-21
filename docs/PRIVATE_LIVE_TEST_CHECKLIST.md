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

- [x] Confirm Homekeep options show Developer mode enabled after install
- [x] Confirm bundled synthetic Chores loaded automatically on setup
- [ ] If a reset is needed, use Developer Tools > Actions:
  `homekeep.load_sample_chores` with `replace_existing: true`
- [x] Do not use real private room routines or private schedule details
- [x] Confirm Homekeep storage contains Chore definitions and Chore state
- [x] Confirm sensors exist:
  - [x] `sensor.homekeep_home_health`
  - [x] `sensor.homekeep_due_chore_count`
  - [x] `sensor.homekeep_best_next_chore`
  - [x] `sensor.homekeep_next_calendar_context`
- [x] Confirm To-do entities exist:
  - [x] `todo.homekeep_recommendations`
  - [x] `todo.homekeep_active_session`
- [x] Confirm per-Chore due binary sensors are created for synthetic Chores

Gate 3 live result on 2026-06-21:

- HACS-installed Homekeep loaded bundled synthetic Chores.
- Per-Chore due binary sensors were present.
- Due count initially stayed at `0` because first-pass sample states had
  `next_due_at=null`.
- Commit `0ca0245` repaired the private dev-mode sample states so unstarted
  bundled sample Chores become immediately due.
- Steve confirmed after update/restart that counts and binary sensors are good.

## Gate 4: Service Smoke Test

Use Developer Tools > Actions.

- [ ] `homekeep.refresh_calendar_context` returns derived context only
- [ ] Calendar Context storage does not include raw event summary, description,
  or location text
- [x] `homekeep.generate_smart_chore_list` returns a Smart Chore List response
- [x] Response includes `snapshot_id`
- [x] Response includes best recommendation ids when chores are available
- [x] `homekeep.start_recommendation` starts a Chore Session from a fresh
  recommendation
- [x] Start response includes `session_id`
- [x] Start response includes materialized `session_item_id` values
- [x] `homekeep.complete_chore` completes a materialized session item
- [x] `homekeep.skip_chore` skips a materialized session item
- [x] `homekeep.snooze_chore` rejects values below `5`
- [x] `homekeep.snooze_chore` rejects values above `1440`
- [x] `homekeep.snooze_chore` snoozes a materialized session item with a valid
  duration
- [x] `homekeep.end_session` completes or cancels the session cleanly
- [x] Duplicate calls with the same `request_id` do not duplicate completions

Gate 4 partial live result on 2026-06-21:

- `homekeep.generate_smart_chore_list` returned a ready-now
  RecommendationSnapshot.
- Response included `snapshot_id`, `best_bundle`, `best_single_chore`,
  `easiest_chore`, alternates, projected impact, scores, and `empty_state:
  null`.
- Snapshot tested: `snapshot_b93db4c5efa1a15b`.
- `homekeep.start_recommendation` materialized
  `rec_d1624aaf78ed9387` into
  `session_f8552dcf5ebc4c80b85261b07eb4b53c`.
- Start response included materialized session item
  `item_bf5c684844974a93b6a90dc771b7482b` for
  `wipe_kitchen_counters`.
- `homekeep.complete_chore` completed the materialized item and returned
  `completion_6e042a39da4f47798abcba765ff498df` with `duplicate: false`.
- Repeating the same completion call with `request_id: live-complete-001`
  returned the same `completion_id`, confirming no duplicate completion was
  created. Response still reported `duplicate: false` because the stored
  response is replayed verbatim; this is a response-polish note, not a data
  safety blocker.
- `homekeep.end_session` completed
  `session_f8552dcf5ebc4c80b85261b07eb4b53c` with `bonus_chore: null`.
- Generated second ready-now snapshot `snapshot_c647bba6adf099c2` and started
  `rec_48fc5987fdfbeb9d` as
  `session_1e0123f1f2d946af95e198ced2aa4ce7` with materialized item
  `item_34b6df599e8940089a873e1049652c1d` for
  `tidy_living_room_surfaces`.
- `homekeep.skip_chore` skipped the materialized `tidy_living_room_surfaces`
  item in `session_1e0123f1f2d946af95e198ced2aa4ce7`.
- Generated third ready-now snapshot `snapshot_deb1ee0f2e38b2d1` and started
  easiest recommendation `rec_f653261c8046801e` as
  `session_c94456cf8a1f45ddb8dc2926a814eaae` with materialized item
  `item_4508cac3f0c649a59185b073ea0b9228` for `empty_compost`.
- `homekeep.snooze_chore` rejected invalid low value `4` and invalid high
  value `1441` with clear service validation errors.
- `homekeep.snooze_chore` accepted valid `15` minute snooze for
  `empty_compost` and returned `snoozed_until`.
- `homekeep.end_session` cancelled the snooze-test session
  `session_c94456cf8a1f45ddb8dc2926a814eaae`.

## Gate 5: To-do Projection Smoke Test

- [x] `todo.homekeep_recommendations` mirrors the latest Smart Chore List
- [x] `todo.homekeep_active_session` mirrors active session items
- [x] Completing a valid To-do item attached to an active session writes
  through to Homekeep
- [x] Completing an item without valid Homekeep metadata is rejected
- [x] Creating a To-do item is rejected or snaps back
- [x] Deleting a To-do item is rejected or snaps back
- [x] Renaming/editing a To-do item is rejected or snaps back
- [x] Reordering a To-do item is rejected or snaps back
- [x] Unsupported To-do mutations do not alter Homekeep storage

Gate 5 partial live result on 2026-06-21:

- Generated snapshot `snapshot_0f4c81eac60502aa` and started
  `rec_c8eadc98e094087a` as
  `session_0e0986ae0e8e4d52ab9e0ff4a4fbfaf6`.
- To-do completion failed with `projected item is not attached to an active
  session`, indicating the frontend action reached a recommendation-style
  projection or stale projection metadata rather than the active-session
  metadata.
- Patched To-do completion to resolve a recommendation projection to a matching
  pending active-session item for the same Chore. Recommendation completion
  without a matching active session remains rejected.
- Live retry still showed recommendation metadata with `session_id: null`.
  Patched recommendation projection generation to expose resolved
  active-session metadata when a matching active item exists.
- `todo.homekeep_active_session` was missing in the live entity list. Patched
  To-do projection names to include the Homekeep prefix so Home Assistant
  generates the documented entity ids.
- Follow-up hardening: To-do projections now set explicit documented entity ids
  and updated unique ids for `todo.homekeep_active_session` and
  `todo.homekeep_recommendations`.
- After updating through HACS, Steve confirmed `todo.homekeep_active_session`
  exists. A fresh active session populated the entity and To-do UI completion
  wrote through successfully.
- Renaming/editing a Homekeep To-do item was rejected with Home Assistant
  validation: `Entity does not support setting field: description`.
- Creating a new item was unavailable in the Home Assistant UI for the
  Homekeep To-do projection, so unsupported create was blocked at the frontend.
- Deleting a projected item was unavailable in the Home Assistant UI, so
  unsupported delete was blocked at the frontend.
- Reordering projected items was unavailable in the Home Assistant UI, so
  unsupported reorder was blocked at the frontend.
- Unsupported create/delete/reorder mutations were not exposed by the UI, and
  unsupported edit was rejected before Homekeep storage could be mutated.
- Invalid-metadata completion remains covered by automated tests; the live UI
  did not expose a practical way to create a projected item without Homekeep
  metadata.

## Gate 6: Calendar Context Smoke Test

- [x] Select at least one safe test calendar entity in Homekeep options
- [x] Refresh Calendar Context manually
- [x] Generate recommendations with fresh Calendar Context
- [ ] Modify/add a synthetic event on a selected calendar entity
- [ ] Confirm Calendar Context is invalidated or refreshed before reuse
- [ ] Confirm dependent RecommendationSnapshots become invalidated when the
  Calendar Context source changes
- [x] Confirm `sensor.homekeep_next_calendar_context` reflects stale/clear/guest
  or busy state as expected

Gate 6 partial live result on 2026-06-21:

- Selected safe test calendar entity `calendar.activites`.
- `homekeep.refresh_calendar_context` returned derived Calendar Context
  `calendar_a30c1f7449927faa`.
- Response included derived signals only, with `event_count: 0`,
  `source_calendar_versions`, and diagnostics
  `raw_event_details_stored: false`.
- `homekeep.generate_smart_chore_list` returned snapshot
  `snapshot_1fe27eef0c27b260` after Calendar Context refresh.
- `sensor.homekeep_next_calendar_context` reported `clear`.
- After a synthetic calendar check, Steve reported the calendar context sensor
  still `clear`; explicit stale invalidation is not yet confirmed.

## Gate 7: Reload And Unload

- [x] Reload the Homekeep config entry
- [x] Confirm durable state remains intact after reload
- [x] Confirm sensors and To-do entities return after reload
- [ ] Confirm calendar state listeners still invalidate Calendar Context after
  reload
- [x] Unload the Homekeep config entry
- [x] Confirm Homekeep entities are removed/unavailable as expected
- [x] Reload or restart and confirm Homekeep recovers stored state

Gate 7 partial live result on 2026-06-21:

- Steve reloaded Homekeep and confirmed the expected state/entities were all
  present afterward.
- Home Assistant UI did not expose an unload option for Homekeep during the
  private test, so manual unload was not available. Local automated tests still
  cover unload behavior.
- Steve restarted Home Assistant and confirmed Homekeep recovered stored state
  and expected entities.

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

- [x] No raw calendar descriptions are stored in durable Homekeep storage
- [x] No private entity ids or personal schedules are copied into tracked files
- [x] No credentials, tokens, cookies, or webhook URLs are present in logs or
  repo changes
- [x] Errors are clear enough to act on from Developer Tools
- [x] Logs do not expose raw calendar event details

Gate 9 live result on 2026-06-21:

- Reviewed Home Assistant log
  `home-assistant_2026-06-21T19-56-28.699Z.log`.
- Homekeep did not log raw calendar event summaries, descriptions, or
  locations.
- Homekeep did not log credentials, tokens, cookies, webhook URLs, or raw
  private calendar details.
- The log did show Homekeep blocking event-loop file I/O while reading bundled
  sample Chores during dev-mode setup repair. Patched sample Chore loading to
  use Home Assistant's executor when `hass` is available.
- Follow-up log `home-assistant_2026-06-21T20-01-17.982Z.log` no longer
  showed Homekeep blocking file I/O warnings after the executor fix.
- Other log warnings/errors were from unrelated integrations or Home Assistant
  custom integration notices.

## Gate 10: Result Notes

Codex should record results in a local note or a new docs file before any
release decision.

- [x] Home Assistant version:
- [x] Homekeep commit:
- [x] Install method:
- [x] Synthetic Chore set used:
- [x] Calendar entities used:
- [x] Service smoke test result:
- [x] To-do projection result:
- [x] Calendar invalidation result:
- [x] Reload/unload result:
- [x] Bubble Card result:
- [x] Bugs found:
- [x] Release blockers:

Result note:

- See `docs/PRIVATE_LIVE_TEST_RESULTS.md`.

## Public Release Still Requires

- [ ] Home Assistant package-backed tests or approved live synthetic candidate
  results
- [ ] Version bump decision
- [ ] Release notes
- [ ] Mock adequacy review updated for the release diff
- [ ] Explicit Steve approval for any deploy/release/publish action
