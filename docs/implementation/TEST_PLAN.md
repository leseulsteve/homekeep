# Test Plan

## Unit Tests

`test_health.py`

- staleness is `0` immediately after a full-credit completion
- staleness is `0` immediately after a tiny completion but returns sooner
  according to credit
- tiny completion with credit `0.25` sets `next_due_at` to one quarter of the
  adaptive interval
- normal completion with credit `1.0` sets `next_due_at` to one adaptive
  interval
- deep completion with credit greater than `1.0` extends `next_due_at`
- changing variant credit after completion does not change stored completion
  credit or existing `next_due_at`
- staleness increases with elapsed time
- display staleness is capped
- priority staleness can exceed display cap
- Home Health respects `health_weight`
- Area Health changes after completion
- health recomputes correctly after simulated cache loss
- completion followed by cache loss still yields correct Home Health
- missing cached health does not affect recommendation correctness
- startup rebuilds or lazily computes health values
- area health changed event fires when Area Health crosses bucket boundary
- area health changed event fires when absolute Area Health delta is at least
  10 points
- area health changed event does not fire for same-bucket changes below 10
  points
- area health changed event does not fire during startup/cache rebuild
- adaptive interval clamps to `min_interval_days` after frequent completions
- adaptive interval clamps to `max_interval_days` after late completions
- snooze, skip, dismiss, and cancel do not change adaptive interval
- tiny completion does not train adaptive interval
- completing a snoozed chore clears `snoozed_until`
- storage load repairs out-of-bounds adaptive interval
- ChoreVariant requires a normal variant
- ChoreVariant credit rejects non-finite or out-of-bounds values

`test_scoring.py`

- all component scores are bounded `0-100`
- missing optional signals default to neutral
- one fresh dismissal subtracts 12 score points before caps
- repeated fresh dismissals cap at 36 score points
- dismissal penalty decays linearly over 14 days
- dismissal events older than 14 days are pruned and ignored
- dismissal cooldown suppresses the exact same chore only when alternatives
  exist
- snoozes do not add to dismissal penalty
- future `snoozed_until` excludes a chore from normal recommendations
- expired `snoozed_until` is ignored or cleared before recommendations
- high staleness can still overcome history penalties
- priority staleness `>= 100` caps effective dismissal penalty at 18
- priority staleness `>= 150` caps effective dismissal penalty at 8
- history context bucket is deterministic
- history context bucket converts UTC datetimes with
  `homeassistant.util.dt.as_local()` before deriving day type or time block
- a UTC timestamp that falls on a different local day gets the local
  weekday/weekend bucket
- evening/night boundary tests use Home Assistant local time, not UTC
- history context bucket includes bounded mood dimension
- context_fingerprint is deterministic for the same normalized payload
- context_fingerprint changes when energy, goal, area, mood, enabled chores, or
  calendar context version changes
- context_fingerprint ignores volatile created_at timestamps
- context_fingerprint does not include raw calendar descriptions
- context_fingerprint is not the same value or purpose as context_bucket
- target_time_window parses ISO windows to Home Assistant local aware datetimes
- target_time_window parses supported natural text with python-dateutil
- target_time_window normalizes to local ISO start/end window
- Ready-Now Mode accepts null target_time_window
- Scheduled-Suggestion Mode rejects null target_time_window
- target_time_window rejects end before start and windows longer than 24 hours
- context_fingerprint uses normalized target_time_window instead of raw input
- sparse history falls back to broader buckets
- no matching history returns neutral history score
- overly specific buckets do not prevent learning when broader data exists
- explanations include the dominant scoring reason
- explicit mood overrides inferred mood
- no mood signals returns unknown with low confidence
- low energy and short time budget can infer tired
- repeated skips/snoozes/dismissals can infer overwhelmed
- recent Bonus Chore acceptance can infer energized
- inferred mood does not override explicit energy or goal
- inferred mood does not hide urgent stale chores
- Mood Context expires after 60 minutes
- raw calendar descriptions are not stored in Mood Context

`test_recommendations.py`

- returns best Chore Bundle, best single chore, easiest useful chore
- every recommendation has a stable recommendation_id
- recommendation payload matches documented shape
- limits alternates
- returns empty state when nothing fits
- area grouping is preferred when area context is strong
- cross-area bundles are preferred when purpose impact is higher

`test_sessions.py`

- generate_smart_chore_list never creates a Chore Session
- start_recommendation creates a Chore Session from a recommendation
- start_recommendation infers session setup fields when optional generation
  fields are omitted
- start_recommendation response includes materialized session items with
  non-null `session_item_id`
- session item completion records bounded learned duration samples when real
  active timing is available
- cached RecommendationItem `session_item_id` is null and never used for
  completion
- start Chore Bundle rejects expired recommendation snapshot
- start Chore Bundle rejects invalidated recommendation snapshot
- start recommendation can materialize bundle or single-chore recommendations
- Scheduled-Suggestion generation does not create an active session
- Scheduled-Suggestion generation returns `snapshot_id`, `target_time_window`,
  `expires_at`, and recommendations
- Scheduled-Suggestion generation never returns `session_id: null`
- ChoreSession copies context_fingerprint from RecommendationSnapshot
- starting a fresh Scheduled-Suggestion recommendation creates a session
- starting an expired Scheduled-Suggestion recommendation is rejected and asks
  the caller to regenerate
- active session remains valid after source recommendation snapshot expires
- materialized snapshot cannot start a second session except idempotent retry
- duplicate valid operation/request_id within 24 hours returns stored result
- same request_id for different operations does not collide
- expired idempotency record is treated as a new request
- idempotency records older than 24 hours are pruned
- idempotency record store is capped at 1000 records by pruning oldest records
- completed_by in session participants is accepted
- completed_by outside session participants is rejected
- omitted completed_by defaults to started_by when available
- session item and ChoreCompletion store matching completed_by
- complete chore in session
- skip/snooze/dismiss do not create completions
- skip_chore with session_id requires materialized session_item_id
- snooze_chore with session_id requires materialized session_item_id
- dismiss_chore with session_id requires materialized session_item_id for
  planned session items
- dismiss_chore with session_id updates history using the session context
  bucket
- dismiss_chore without session_id does not guess an active session
- snooze_minutes below 5 is rejected
- snooze_minutes above 1440 is rejected
- snooze_minutes equal to 1440 is accepted
- snooze_chore stores `snoozed_until`
- repeated snooze replaces `snoozed_until` instead of extending it
- dismiss_chore appends one bounded dismissal event
- duplicate dismiss_chore requests with the same request_id create one
  dismissal event
- end session completed
- end session cancelled
- Bonus Chore is optional and bounded
- end_session with offer_bonus_chore moves session to bonus_pending
- end_session with offer_bonus_chore sets bonus_chore_expires_at 15 minutes
  after offer
- paused session with all planned items complete can move to bonus_pending
- paused session with incomplete planned items cannot move to bonus_pending
- expired bonus_pending session lazily becomes completed
- accept_bonus_chore after expiry raises bonus_chore_expired
- bonus_active session is not expired by bonus_chore_expires_at
- accepting Bonus Chore moves session to bonus_active
- accept_bonus_chore rejects non-matching chore
- Bonus Chore completion uses original session_id
- unrelated chore completion is rejected while bonus_active
- completing Bonus Chore ends session completed and does not offer another bonus
- stale session response does not mutate current session
- duplicate complete_chore calls for one session item create one completion
- concurrent complete and skip on same item resolves deterministically

`test_storage.py`

- empty storage initializes
- version `2` loads
- version `1` store migrates to version `2`
- v1-to-v2 migration adds `snoozed_until`, `dismissal_events`,
  `snooze_events`, `last_dismissed_at`, and `last_snoozed_at`
- v1-to-v2 migration removes `recent_dismissals` and `recent_snoozes`
- v1-to-v2 migration does not fabricate timestamp events from old integer
  counters
- v1-to-v2 migration preserves completion and scheduling fields
- unsupported future storage version is rejected clearly
- invalid stored values are rejected or sanitized
- migration hook exists
- save/load round trip preserves definitions, state, and history

`test_calendar_context.py`

- guest event creates guest prep context
- travel event creates pre-travel context
- trash event creates trash context
- unknown event does not create surprising recommendation context
- selected calendar entity state change invalidates affected snapshots
- expired snapshot is refreshed or ignored before recommendation scoring
- changed source calendar entity version makes snapshot invalid
- manual refresh is not required for normal calendar updates
- raw calendar details are not stored in long-lived snapshots

## Home Assistant Integration Tests

`test_config_flow.py`

- config entry can be created
- optional calendar entities can be selected later
- unload/reload succeeds

`test_services.py`

- malformed payloads produce clear errors
- unknown chore IDs produce clear errors
- answer_session_question is not registered in MVP
- complete service updates state
- skip/snooze/dismiss services do not create completions
- generate service returns bounded Smart Chore List
- generate service defaults include_alternates to true and returns up to 3
  alternates
- generate service with include_alternates=false returns an empty alternates
  list
- generate service is registered with response-only action response support
- generate service response matches `docs/specs/RECOMMENDATION_PAYLOADS.md`
- start_recommendation is registered with response-only action response support
- start_recommendation response includes `session_id` and
  `source_recommendation_snapshot_id`
- start_recommendation response includes concrete materialized session item IDs
- start_recommendation response uses learned Chore duration when timing samples
  exist
- action response payloads are JSON-serializable dictionaries
- service errors raise exceptions instead of returning error dictionaries

`test_todo.py`

- recommendation To-do entity mirrors Smart Chore List
- active session To-do entity mirrors session items
- completing To-do item calls Homekeep completion logic
- completing To-do item without valid Homekeep metadata is rejected
- adding To-do item is rejected or reverted and does not create a Chore
- adding a To-do item triggers an entity state refresh from Homekeep projection
- deleting a To-do item is rejected or reverted and does not remove a Chore
- deleting a To-do item triggers an entity state refresh from Homekeep
  projection
- renaming/editing To-do item is rejected or reverted and does not mutate state
- renaming/editing a To-do item triggers an entity state refresh from Homekeep
  projection
- reordering To-do item is rejected or reverted unless explicitly supported later
- unsupported reorder triggers an entity state refresh from Homekeep projection
- To-do entity does not become source of truth

App UI tests

- Scheduled-Suggestion app flow uses `generate_smart_chore_list` for planning
- Scheduled-Suggestion app flow uses Refresh/regenerate when the proposal is
  expired
- Scheduled-Suggestion app flow does not depend on `session_id: null`

`test_entities.py`

- Home Health sensor updates after completion
- due chore count sensor updates
- best next chore sensor updates
- due binary sensor changes when chore becomes due

## Reproducible MVP Check

1. Create at least two non-private Chores through `homekeep.create_chore`.
2. Start a 15-minute Ready-Now session.
3. Generate Smart Chore List.
4. Start best bundle.
5. Complete one chore.
6. Skip one chore.
7. End session.
8. Verify health changed only for completed chore.
9. Ask for one more.
10. Verify Bonus Chore is optional and bounded.
