# MVP Acceptance Criteria

The MVP is successful when all of these are true.

## Core

- A user can create or load Chore definitions.
- Homekeep stores Chore state with migration-ready versioning.
- Homekeep current storage version is `2`, with documented v1-to-v2 migration
for early ChoreState dismissal/snooze fields.
- Homekeep calculates Staleness, Home Health, and Area Health as derived values.
- Health and Staleness remain correct after cache loss or restart.
- `homekeep_area_health_changed` fires only on Area Health bucket crossing or
at least 10-point delta, and does not fire during startup/cache rebuild.
- Invalid definitions fail with clear errors.

## Sessions

- A user can generate a Ready-Now Smart Chore List and start a selected
recommendation as a Chore Session.
- Scheduled-Suggestion recommendations do not create active sessions until the
user starts a recommendation.
- Scheduled-Suggestion UI flow treats generated recommendations as saved
proposals with `snapshot_id`, `target_time_window`, and `expires_at`, not as
sessions with `session_id: null`.
- Expired Scheduled-Suggestion proposals are refreshed before start.
- Both Chore Bundle and single-chore recommendations can be started.
- Homekeep asks or accepts time, energy, and goal context.
- Homekeep can infer or accept Mood Context when useful, and explicit user
choices override inference.
- MVP does not register `homekeep.answer_session_question`; context answers are
passed directly to `homekeep.generate_smart_chore_list`.
- A user can complete, skip, snooze, dismiss, pause, and end a Chore Session.
- Session completion attribution validates `completed_by` against session
participants when participants are present.
- Expired or invalidated recommendation snapshots cannot start new Chore
Sessions.
- Active Chore Sessions remain valid if their source recommendation snapshot
expires after session creation.
- Duplicate service retries do not create duplicate completions or sessions.
- Idempotency records use a 24-hour TTL and a bounded store size.
- Completing a chore updates durable Chore state and adaptive interval; derived
Staleness and health scores recompute correctly.
- Variant credit deterministically updates `next_due_at`; tiny completions
provide shorter scheduling relief without training adaptive cadence.
- Adaptive interval writes are always clamped to the Chore definition's
`min_interval_days` and `max_interval_days`.
- Snooze duration is bounded to `5..1440` minutes and invalid values are
rejected.
- Skipped, snoozed, dismissed, and cancelled chores do not count as completed.
- Skipped, snoozed, dismissed, and cancelled chores do not train adaptive
intervals.

## Recommendations

- Homekeep generates a bounded Smart Chore List with explanations.
- The list includes a best Chore Bundle, best single chore, and easiest useful
chore when available.
- Projected Impact is shown for recommendations.
- Empty recommendations return a clear empty state.
- Session-History Learning can influence Ready-Now recommendations with bounded
scoring.
- Session-History Learning uses deterministic context buckets with fallback
matching and neutral scoring when history is sparse.
- Mood Context can influence defaults, wording, and session lightness without
making medical claims or hiding urgent stale chores.
- Dismissal penalty has a documented formula, 14-day decay, capped score
impact, and stale-chore override.
- Dismissed chores can be temporarily cooled down but are never permanently
hidden by dismissals.
- Snoozed chores are hidden only until `snoozed_until` and then re-enter normal
recommendations.

## Home Assistant

- Home Assistant To-do entities reflect recommendations and active session
tasks as projections.
- Data-producing services use Home Assistant action responses instead of
requiring callers to scrape entity state.
- `homekeep.generate_smart_chore_list` returns the documented Smart Chore List
Result dictionary as its action response.
- To-do completion write-through works only for projected items with valid
Homekeep metadata.
- Direct To-do create, delete, rename, edit, and reorder operations are rejected
or reverted and do not mutate Homekeep state.
- Homekeep app can trigger the main Ready-Now flow through Home Assistant
services.
- Basic sensors expose Home Health, due chore count, best next chore, and
Calendar Context.

## Calendar

- Calendar Context can influence at least one Scheduled-Suggestion
recommendation.
- Calendar Context is automatically invalidated when selected calendar entities
change.
- Expired Calendar Context is refreshed or ignored before recommendation
scoring.
- Derived Calendar Context is stored instead of raw calendar descriptions when
possible.

## Light Rewards

- Bonus Chores can be offered after a completed Light Session.
- Bonus Chores use the original Chore Session through `bonus_pending` and
`bonus_active` states.
- Pending Bonus Chore offers expire after 15 minutes and late acceptance is
rejected clearly.
- Paused sessions remain eligible for Bonus Chores once all planned items are
complete.
- Declining a Bonus Chore still counts the planned session as successful.
- Asking for one more does not create an unbounded queue.

## Reliability

- Malformed service payloads produce clear errors.
- Unknown chore IDs produce clear errors.
- Stale session responses do not mutate current sessions.
- Reload and unload behavior does not lose durable state.
