# Storage Migrations

## Goal

Homekeep storage migrations must be explicit, idempotent, and safe for early
development stores. Do not rely on validation repair for known schema changes.

## Current Version

```text
current_storage_version = 2
```

## Migration Order

On load:

```text
if version is missing:
  treat as version 1 only if the shape matches the early v1 draft
elif version > current_storage_version:
  reject with a clear unsupported-version error
while version < current_storage_version:
  run the next migration
  increment version
validate final store
save migrated store
```

Migrations must be safe to run once. Validation/repair may still sanitize
non-finite values, but it must not silently replace a documented migration.

## Version 1 To 2

Reason:
: Early v1 drafts stored `recent_dismissals: int` and `recent_snoozes: int` on
`ChoreState`. Current storage uses timestamp lists and explicit snooze state.

Input shape:

```yaml
version: 1
states:
  <chore_id>:
    chore_id: string
    last_completed_at: datetime | null
    adaptive_interval_days: float
    next_due_at: datetime | null
    recent_dismissals: int
    recent_snoozes: int
```

Output shape:

```yaml
version: 2
states:
  <chore_id>:
    chore_id: string
    last_completed_at: datetime | null
    adaptive_interval_days: float
    next_due_at: datetime | null
    snoozed_until: datetime | null
    dismissal_events: list[datetime]
    snooze_events: list[datetime]
    last_dismissed_at: datetime | null
    last_snoozed_at: datetime | null
```

Migration rules for every `ChoreState`:

- add `snoozed_until: null` when missing
- add `dismissal_events: []` when missing
- add `snooze_events: []` when missing
- add `last_dismissed_at: null` when missing
- add `last_snoozed_at: null` when missing
- remove `recent_dismissals`
- remove `recent_snoozes`
- keep `last_completed_at`, `adaptive_interval_days`, and `next_due_at`
- clamp/repair `adaptive_interval_days` after migration using
  `docs/ADAPTIVE_INTERVALS.md`

Do not attempt to fabricate dismissal or snooze timestamps from the old integer
counters. A count without timestamps cannot support decay or expiry. Dropping
those counters is intentional.

If a v1 state already contains new fields because an early development branch
partially applied the new schema, keep valid new fields, add missing new fields,
and still remove old integer counters.

## Tests Required

Implementation must test:

- version 1 store with `recent_dismissals` and `recent_snoozes` migrates to
  version 2
- migration adds `snoozed_until`, `dismissal_events`, `snooze_events`,
  `last_dismissed_at`, and `last_snoozed_at`
- migration removes `recent_dismissals` and `recent_snoozes`
- migration does not fabricate timestamp events from old integer counters
- migration preserves completion and scheduling fields
- migration is idempotent after version is 2
- unsupported future storage versions are rejected clearly
