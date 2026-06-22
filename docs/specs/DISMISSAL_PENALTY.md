# Dismissal Penalty

## Goal

Dismissals should teach Homekeep that a chore was not wanted in that context.
They must not permanently hide work that is becoming stale or important.

## Stored Data

Homekeep stores bounded dismissal timestamps on `ChoreState`.

```yaml
dismissal_events: list[datetime]
snoozed_until: datetime | null
snooze_events: list[datetime]
last_dismissed_at: datetime | null
last_snoozed_at: datetime | null
```

`recent_dismissals` must not be stored as an authoritative integer. It is a
derived value:

```text
recent_dismissals = count(dismissal_events where age_days < 14)
```

On storage load and on every dismissal write:

- remove dismissal events older than 14 days
- remove snooze events older than 14 days
- cap each event list to the newest 10 timestamps
- ignore malformed timestamps after logging a repair warning

## Formula

Dismissal penalty is computed per chore at scoring time.

```text
dismissal_window_days = 14
dismissal_penalty_per_weight = 12
dismissal_penalty_cap = 36

event_weight = max(0, 1 - age_days / dismissal_window_days)
weighted_dismissals = sum(event_weight for each dismissal_event)
dismissal_penalty = min(weighted_dismissals * 12, 36)
```

The resulting penalty is in the same `0-100` scale as the recommendation score.

Example:

- dismissal now: `12` points
- same chore dismissed twice today: `24` points
- three fresh dismissals: `36` points, capped
- one dismissal after 7 days: `6` points
- one dismissal after 14 days: `0` points and pruned

## Cooldown

A fresh dismissal may suppress the exact same chore in the same context for a
short time.

```text
dismissal_cooldown_hours = 4
```

During cooldown, the exact chore should not be shown as the primary
recommendation if another useful option exists.

The cooldown is bypassed when:

- the chore's priority staleness is `>= 100`
- Calendar Context marks the chore as strongly relevant
- there are not enough useful alternatives to build a Smart Chore List

## Staleness Override

Dismissal penalty must never permanently hide stale chores.

Apply these caps after computing the base penalty:

```text
if priority_staleness_score >= 150:
  effective_dismissal_penalty = min(dismissal_penalty, 8)
elif priority_staleness_score >= 100:
  effective_dismissal_penalty = min(dismissal_penalty, 18)
else:
  effective_dismissal_penalty = dismissal_penalty
```

The final score is:

```text
final_score = clamp(base_score - effective_dismissal_penalty, 0, 100)
```

## Snoozes

Snoozes are not dismissals.

For MVP:

- a snooze can hide a chore until its explicit snooze target time
- snooze events can be stored for diagnostics and future learning
- snoozes do not add to `dismissal_penalty`
- snoozes do not train adaptive intervals

Snooze bounds and `snoozed_until` behavior are defined in
`docs/specs/SNOOZE_POLICY.md`.

## Service Behavior

When `homekeep.dismiss_chore` succeeds:

- append the current timestamp to `dismissal_events`
- set `last_dismissed_at`
- prune and cap stored dismissal events
- update Session-History Learning stats for the active context bucket
- do not create a `ChoreCompletion`
- do not update `last_completed_at`
- do not train `adaptive_interval_days`

Dismissal writes must be idempotent when a `request_id` is supplied. Retrying
the same dismissal request must not append duplicate dismissal events.

## Tests Required

Implementation must test:

- one fresh dismissal subtracts `12` points
- repeated fresh dismissals cap at `36` points
- dismissal penalty decays linearly over 14 days
- events older than 14 days are pruned and do not affect score
- cooldown suppresses the exact same chore only when alternatives exist
- high staleness reduces the effective penalty cap
- very high staleness reduces the effective penalty cap further
- dismissals never create completions or train adaptive intervals
- duplicate dismiss requests with the same `request_id` create one event
