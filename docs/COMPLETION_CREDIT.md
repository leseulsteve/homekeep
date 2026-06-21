# Completion Credit

## Goal

Chore Variant credit defines how much scheduling relief a completion gives.
It must be deterministic so Staleness, `next_due_at`, and recommendation
scoring agree after tiny, normal, and deep completions.

## Credit Meaning

`ChoreVariant.credit` is a multiplier of the current adaptive interval.

```text
credit_days = adaptive_interval_days * variant.credit
next_due_at = completed_at + credit_days
```

Examples with `adaptive_interval_days = 8`:

```text
tiny credit 0.25  -> next due in 2 days
normal credit 1.0 -> next due in 8 days
deep credit 1.5   -> next due in 12 days
```

`credit` affects scheduling relief. It does not directly change
`adaptive_interval_days`.

The credit used for a completion is copied from the Chore Variant at completion
time and stored on `ChoreCompletion.credit`. Later edits to the Chore
definition or variant credit must not retroactively change that historical
completion or the existing `ChoreState.next_due_at`.

## Variant Rules

`tiny`
: Creates a real `ChoreCompletion`, updates `last_completed_at`, clears
`snoozed_until`, and sets `next_due_at = completed_at + adaptive_interval_days
* credit`. It does not train `adaptive_interval_days`.

`normal`
: Creates a real `ChoreCompletion`, updates `last_completed_at`, clears
`snoozed_until`, trains `adaptive_interval_days`, and sets `next_due_at` from
the updated adaptive interval and credit.

`deep`
: Creates a real `ChoreCompletion`, updates `last_completed_at`, clears
`snoozed_until`, trains `adaptive_interval_days`, and may extend `next_due_at`
with credit greater than `1.0`.

## Bounds

MVP credit bounds:

```text
0.1 <= credit <= 2.0
```

`next_due_at` must also respect chore definition bounds:

```text
effective_credit_days =
  clamp(adaptive_interval_days * credit, min_interval_days * 0.1, max_interval_days * 2.0)
```

This allows tiny work to help without pretending the chore is done for a full
cycle, and allows deep work to last longer without becoming unbounded.

## Staleness

Staleness is derived from `next_due_at` when available.

```text
if next_due_at is null:
  use last_completed_at + adaptive_interval_days
elif now <= next_due_at:
  staleness_score = 0
else:
  overdue_days = now - next_due_at
  staleness_score = overdue_days / adaptive_interval_days * 100
```

A tiny completion can make Staleness `0` immediately after completion, but only
until its shorter credited window expires. It is not a full reset for the whole
adaptive interval.

If a Chore definition changes after a completion, keep the existing
`next_due_at` until another real completion or explicit schedule repair updates
it. Do not recompute existing `next_due_at` from the new variant credit.

## Tests Required

Implementation must test:

- tiny completion with credit `0.25` sets `next_due_at` to one quarter of the
  adaptive interval
- tiny completion does not train `adaptive_interval_days`
- normal completion with credit `1.0` sets `next_due_at` to one adaptive
  interval and trains `adaptive_interval_days`
- deep completion with credit greater than `1.0` extends `next_due_at`
- staleness is `0` immediately after any accepted completion with positive
  credit
- tiny completion becomes stale again sooner than normal completion
- changing a Chore Variant credit after completion does not alter the stored
  completion credit or existing `next_due_at`
- credit values outside `0.1..2.0` are rejected
