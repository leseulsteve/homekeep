# Home Assistant Contract

## Integration Domain

```text
homekeep
```

## Source Of Truth

Homekeep internal storage owns durable state:

- Chore definitions
- Chore state
- Chore completions
- Chore Sessions
- Recommendation snapshots
- Calendar Context snapshots
- Session-History Learning stats

Home Assistant To-do entities are projections of Homekeep state.

## Planned Entities

```text
sensor.homekeep_home_health
sensor.homekeep_due_chore_count
sensor.homekeep_best_next_chore
sensor.homekeep_next_calendar_context
todo.homekeep_recommendations
todo.homekeep_active_session
todo.homekeep_<area>
binary_sensor.homekeep_<chore_id>_due
```

## To-do Projection Rules

Completion of an existing projected To-do item is the only supported
write-through operation in the MVP. Direct create, delete, rename, edit, and
move/reorder operations from the Home Assistant To-do UI must be rejected or
immediately reverted by refreshing the projection from Homekeep state.

Because the Home Assistant frontend may optimistically render unsupported
To-do mutations as successful, Homekeep's `todo.py` mutation handlers must
force a state refresh from Homekeep storage after rejecting or ignoring those
mutations. Call `self.async_write_ha_state()` on the To-do entity when the
entity instance is available so the UI snaps back to the authoritative
projection. Verify exact handler method names against the supported Home
Assistant core version during implementation.

`todo.homekeep_recommendations`
: Projection of the latest Smart Chore List. Items may be regenerated when
context changes. Completing an item must call Homekeep completion logic.
Creating, deleting, renaming, editing, or reordering items must not mutate
Homekeep state.

`todo.homekeep_active_session`
: Projection of the active Chore Session. Completing an item marks that session
item done. Skipped, snoozed, swapped, or cancelled items do not count as
completed. Creating, deleting, renaming, editing, or reordering items must not
mutate Homekeep state.

`todo.homekeep_<area>`
: Optional area-focused projection for dashboards. It should use Home Assistant
Area names when available. Completion may write through only when the projected
item has valid Homekeep metadata.

## Planned Services

```text
homekeep.generate_smart_chore_list
homekeep.start_recommendation
homekeep.start_chore_bundle
homekeep.create_chore
homekeep.complete_chore
homekeep.skip_chore
homekeep.snooze_chore
homekeep.dismiss_chore
homekeep.refresh_calendar_context
homekeep.pause_session
homekeep.accept_bonus_chore
homekeep.end_session
```

`homekeep.generate_smart_chore_list` creates proposals only.
`homekeep.start_recommendation` is the only canonical MVP service that creates
Chore Sessions. There is no MVP `homekeep.start_chore_session` service.
`homekeep.create_chore` creates a Chore definition for the chore list and does
not create a Chore Session.
Scheduled-Suggestion Mode returns saved proposals with `snapshot_id`,
`target_time_window`, and `expires_at`; it must not return `session_id: null`.
See `docs/SCHEDULED_SUGGESTION_UX.md`.

After `homekeep.start_recommendation`, callers must use the materialized
`SessionItem` list returned by that service for future `complete_chore` calls.
Smart Chore List `RecommendationItem.session_item_id` values are proposal-only
and null before materialization.

`homekeep.answer_session_question` is not an MVP service. Lovelace should
collect context locally and call `homekeep.generate_smart_chore_list` with the
final answers.

Homekeep does not expose private dev mode or a sample-loading service. Config
entry setup loads existing storage only and must not create synthetic Chores or
clear durable data for test setup.

## Action Response Rules

Homekeep must use Home Assistant action/service responses for services that
produce data. Do not rely only on entity state changes for generated
recommendations or created sessions.

- Register `homekeep.generate_smart_chore_list` with
  `supports_response=SupportsResponse.ONLY`.
- Register `homekeep.start_recommendation` with
  `supports_response=SupportsResponse.ONLY`.
- Register `homekeep.start_chore_bundle` with
  `supports_response=SupportsResponse.ONLY` if the compatibility alias exists.
- Register `homekeep.create_chore` with
  `supports_response=SupportsResponse.OPTIONAL`.
- Register `homekeep.accept_bonus_chore` and `homekeep.end_session` with
  `supports_response=SupportsResponse.ONLY`.
- Register `homekeep.refresh_calendar_context` with
  `supports_response=SupportsResponse.OPTIONAL`.
- Mutation services may use `SupportsResponse.OPTIONAL` for acknowledgement
  dictionaries.

Returned dictionaries must match `docs/RECOMMENDATION_PAYLOADS.md` and
`docs/SERVICE_SCHEMAS.md`. Verify the exact `SupportsResponse` import and
registration signature against the supported Home Assistant core version during
implementation.

## Calendar Context Invalidation

Homekeep must listen for state changes on selected calendar entities.

On calendar state change:

- invalidate affected Calendar Context snapshots
- invalidate recommendation snapshots that used those snapshots
- update `sensor.homekeep_next_calendar_context`
- refresh lazily on the next recommendation request or active dashboard update

`homekeep.refresh_calendar_context` is a manual refresh hook, not the only
freshness mechanism.

## Service Validation Rules

- Unknown chore IDs return a clear service error.
- Unknown session IDs return a clear service error.
- Mutation services should accept optional `request_id` values and avoid double
applying the same mutation.
- Non-finite durations, intervals, weights, and credits are rejected.
- Adaptive interval writes must be clamped to the Chore definition's
`min_interval_days` and `max_interval_days`.
- Invalid variants are rejected.
- Session-based `completed_by` values must be null or present in the session's
participants list.
- Bonus Chores use the original Chore Session. `complete_chore` may complete a
Bonus Chore only when the session is `bonus_active`.
- Expired or invalidated RecommendationSnapshot records must not start new
Chore Sessions.
- Once a RecommendationSnapshot is materialized into a Chore Session, later
snapshot expiry must not invalidate that active session.
- Stale session responses must not mutate the current active session.
- Cancelled, skipped, snoozed, and dismissed chores must not be saved as
completed.

## Planned Events

```text
homekeep_chore_offered
homekeep_chore_completed
homekeep_chore_snoozed
homekeep_chore_became_due
homekeep_session_started
homekeep_session_ended
homekeep_area_health_changed
```

## Event Emission Rules

`homekeep_area_health_changed`

Purpose:
: Notify automations when an Area Health change is meaningful enough to act on.
It must not fire for every tiny recalculation.

Payload:

```yaml
area_id: string
old_area_health: float
new_area_health: float
old_bucket: critical | poor | fair | good
new_bucket: critical | poor | fair | good
reason: completion | recalculation
```

Buckets:

```text
critical: 0 <= score < 40
poor:     40 <= score < 60
fair:     60 <= score < 80
good:     80 <= score <= 100
```

Fire the event only when at least one is true:

```text
bucket changed
absolute delta >= 10 points
```

Do not fire the event:

```text
on Home Assistant startup cache rebuild
on storage load/migration repair
when old value is unknown
when absolute delta < 10 and bucket is unchanged
```

Entity state should still update for smaller changes; the event threshold is
only to keep automations and logs from becoming noisy.

## Lovelace MVP

Lovelace is the MVP dashboard layer.

Expected controls:

- "I'm ready" session launcher
- Add Chore flow
- Time selection
- Energy selection
- Goal selection
- Recommendation display
- Start, done, skip, snooze, dismiss, end actions
- Optional "one more" Bonus Chore action

Lovelace should call Homekeep services. It should not become the source of
truth.
