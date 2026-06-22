# Mock Adequacy Review

This review supports pre-`1.0` version-bump readiness. It does not approve a
release by itself and does not replace live Home Assistant validation.

## Current Status

Homekeep is pre-`1.0`. A version bump is not ready to publish unless the
changed behavior is covered by realistic local mocks or by an approved live
candidate workflow.

For the `0.0.3` startup-fix implementation pass, mock coverage is adequate for
a private HACS publish and developer readiness checkpoint, but not yet adequate
for a public production release.

## Covered By Local Tests

Storage:

- empty store loading
- v1-to-v2 migration
- v2 loading with missing optional sections
- future-version rejection
- invalid stored value rejection
- stale state for unknown Chore ids ignored on load
- store round trip for definitions, state, completions, sessions, snapshots,
  calendar context, stats, and idempotency records

Services:

- service schema construction is exercised with lightweight Home Assistant and
  voluptuous stand-ins, covering missing schema constants before live startup
- malformed payloads rejected before raw `KeyError`
- unknown Chore ids and session ids return clear validation errors
- duplicate request ids avoid duplicate session mutations
- stale session responses after cancellation do not create completions or
  reopen terminal sessions

Home Assistant lifecycle:

- config entry unload calls platform unload
- successful unload removes entry storage and calendar state listener
- failed platform unload preserves storage and listener
- source checks confirm config flow no longer exposes private dev mode
- source checks confirm setup no longer seeds bundled sample Chores

To-do projections:

- projected active-session completion writes through
- invalid projected completion is rejected
- create/delete/edit/rename/reorder traps refresh projection and do not mutate
  Homekeep storage

Calendar Context:

- selected calendar source versions are tracked
- derived snapshots do not store raw summary, description, or location text
- max-age, target-window, and source-version changes make snapshots stale
- selected calendar state changes invalidate Calendar Context and dependent
  RecommendationSnapshots

Recommendation snapshots:

- stable recommendation ids
- sparse history fallback
- expired snapshot rejection
- fresh materialization into sessions

Adaptive intervals and derived health:

- cache-loss and restart recomputation
- min/max adaptive interval clamping
- skip/snooze/dismiss/cancel do not train intervals

## Mock Gaps Before Public Release

Home Assistant package-backed tests:

- The local environment does not currently install Home Assistant, so service
  registration, config flow, entity lifecycle, To-do entity methods, calendar
  services, and action-response behavior are tested with source checks and
  local fakes rather than Home Assistant's test harness.

Frontend/dashboard:

- The former dashboard examples have been removed.
- The sidebar app direction still needs frontend-specific mocks once the
  Home Assistant extension approach is chosen.

Dynamic entity behavior:

- Runtime additions/removals of Chores after setup are not yet covered by
  entity registry mocks.
- Per-area To-do projections are still deferred.

Calendar:

- Event fetching is mocked with synthetic event dictionaries. A Home Assistant
  calendar integration test should verify `calendar.get_events` response shape
  against the supported Home Assistant core version.

## Release Readiness Decision

Mock coverage is adequate for continuing MVP implementation and for a
private `0.0.3` HACS publish, provided the version bump does not claim live
Home Assistant production readiness.

Mock coverage is not yet adequate for a public pre-`1.0` release without one
of these follow-up actions:

- add Home Assistant package-backed tests for config flow, services, entities,
  To-do projections, and calendar services
- or run an approved live candidate workflow with synthetic data and document
  the result before release
