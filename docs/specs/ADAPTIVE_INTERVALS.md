# Adaptive Intervals

Adaptive intervals let Homekeep learn how often chores are actually completed
without letting the schedule collapse or drift into uselessness.

## Source Bounds

Every Chore has definition-level bounds:

```yaml
base_interval_days: float
min_interval_days: float
max_interval_days: float
```

These bounds are not only validation hints. They must be enforced every time
`ChoreState.adaptive_interval_days` is written.

## Write-Time Clamp

Any adaptive interval write must use:

```text
adaptive_interval_days =
  clamp(candidate_interval_days, min_interval_days, max_interval_days)
```

This applies to:

- initial state creation
- completion updates
- storage migration
- storage repair
- YAML import
- service-driven definition updates

If stored state contains an out-of-bounds adaptive interval, load or migration
must clamp it and log/diagnose the repair.

## V1 Update Formula

Only real Chore completions train the adaptive interval.

```text
actual_gap_days = completed_at - previous_completed_at
candidate_interval_days =
  old_adaptive_interval_days * 0.70
+ actual_gap_days * 0.30
adaptive_interval_days =
  clamp(candidate_interval_days, min_interval_days, max_interval_days)
```

If there is no previous completion:

```text
adaptive_interval_days = clamp(base_interval_days, min_interval_days, max_interval_days)
```

## Variant Effects

Chore Variants affect scheduling relief through `ChoreVariant.credit`. Use
`docs/specs/COMPLETION_CREDIT.md` as the source of truth for `next_due_at` and
Staleness behavior.

Recommended MVP behavior:

```text
tiny:
- sets next_due_at using adaptive_interval_days * credit
- does not train adaptive_interval_days

normal:
- sets next_due_at using adaptive_interval_days * credit
- trains adaptive_interval_days

deep:
- sets next_due_at using adaptive_interval_days * credit
- trains adaptive_interval_days
- may extend next_due_at by variant credit, still bounded by credit rules
```

## Snoozes, Skips, And Dismissals

These actions must not train `adaptive_interval_days`:

```text
skip
snooze
dismiss
cancel
```

They may affect recommendation penalties or Session-History Learning, but they
must not make a chore look naturally less frequent.

This prevents a perpetually snoozed chore from drifting toward a very long
interval such as 365 days.

## Convergence Expectations

Given repeated normal completions at a stable cadence, the adaptive interval
should approach that cadence gradually while staying within bounds.

Examples:

```text
base=7, min=3, max=14
daily completions cannot push adaptive_interval_days below 3.

base=14, min=7, max=30
late completions cannot push adaptive_interval_days above 30.
```

## Tests Required

- daily completions clamp at `min_interval_days`
- very late completions clamp at `max_interval_days`
- snoozes do not alter `adaptive_interval_days`
- skips/dismissals/cancelled sessions do not alter `adaptive_interval_days`
- storage load repairs out-of-bounds adaptive intervals
- first completion initializes from clamped base interval
- tiny completion updates next_due_at without training adaptive_interval_days
- normal and deep completions update next_due_at and train adaptive_interval_days
