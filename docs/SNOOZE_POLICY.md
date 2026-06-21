# Snooze Policy

## Goal

Snooze means "not until later." It must not become an unbounded way to hide a
chore forever.

## MVP Bounds

`homekeep.snooze_chore` accepts `snooze_minutes`.

```text
min_snooze_minutes = 5
max_snooze_minutes = 1440
```

The maximum MVP snooze is 24 hours.

Validation:

- reject values below `5`
- reject values above `1440`
- reject non-integer, non-finite, null, or missing values
- do not silently clamp invalid values

Recommended UI presets:

```text
15 minutes
1 hour
3 hours
tomorrow
```

The `tomorrow` preset must still resolve to `<= 1440` minutes. If the desired
local time would exceed 24 hours, cap the preset in the UI before calling the
service or ask the user to dismiss instead.

## Stored Data

`ChoreState` stores:

```yaml
snoozed_until: datetime | null
snooze_events: list[datetime]
last_snoozed_at: datetime | null
```

When a snooze succeeds:

- compute `snoozed_until = now + snooze_minutes`
- append the current timestamp to `snooze_events`
- set `last_snoozed_at`
- prune `snooze_events` older than 14 days
- cap `snooze_events` to the newest 10 timestamps

If a chore is already snoozed and the user snoozes it again, replace
`snoozed_until` with the new target time and append a new bounded event. Do not
extend by adding to the existing target time.

## Recommendation Behavior

Before scoring a chore:

- if `snoozed_until` is in the future, exclude the chore from normal
  recommendations
- if `snoozed_until` is null or in the past, clear or ignore it
- if Calendar Context marks the chore as urgent, the engine may show it as an
  alternate with an explanation, but it should not become the primary
  recommendation while snoozed unless no useful alternatives exist

Snooze does not add to `dismissal_penalty`. Dismissal is "not this again in this
context"; snooze is "not before this time."

## Completion Interaction

If a snoozed chore is completed manually or through a projected To-do item:

- create the normal `ChoreCompletion`
- clear `snoozed_until`
- do not treat the snooze as a completion

Snoozes must not train `adaptive_interval_days`.

## Tests Required

Implementation must test:

- `snooze_minutes < 5` is rejected
- `snooze_minutes > 1440` is rejected
- `snooze_minutes = 1440` is accepted
- accepted snooze stores `snoozed_until`
- repeated snooze replaces `snoozed_until` instead of extending it
- snoozed chores are excluded from normal recommendations until the target time
- expired snoozes are ignored or cleared
- completing a snoozed chore clears `snoozed_until`
- snooze does not create completions, train adaptive intervals, or add to
  dismissal penalty
