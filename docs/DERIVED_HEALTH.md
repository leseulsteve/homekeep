# Derived Health And Staleness

Home Health, Area Health, Group Health, Staleness, and Projected Impact are
derived values. They must not be treated as authoritative durable state.

## Durable Inputs

Health calculations should derive from:

```text
ChoreDefinition
ChoreState.last_completed_at
ChoreState.adaptive_interval_days
ChoreState.next_due_at
ChoreCompletion records
current time
selected context
```

## Non-Authoritative Caches

The implementation may cache derived health values for entity updates or
performance, but cached values must be disposable.

Cache rules:

```text
- never rely on cached health as source of truth
- rebuild cache on Home Assistant startup
- rebuild cache after storage load/migration
- rebuild cache after ChoreCompletion writes
- if cache is missing or stale, compute health lazily on read
```

## Atomicity Rule

Completion should persist only durable facts:

```text
1. ChoreCompletion
2. ChoreState.last_completed_at
3. ChoreState.adaptive_interval_days
4. ChoreState.next_due_at
```

If Home Assistant crashes after completion is written but before entity updates,
Homekeep must recompute health from durable facts on the next read/startup.

## ChoreState

`ChoreState` should not store authoritative `staleness_score`.

Staleness should derive from `ChoreState.next_due_at` when available. Completion
variant credit determines `next_due_at`; see `docs/COMPLETION_CREDIT.md`.
Existing `next_due_at` values are durable schedule facts and must not be
retroactively recomputed from edited Chore Variant definitions.

If a cached staleness value is used, name it explicitly:

```yaml
cached_staleness_score: float | null
cache_updated_at: datetime | null
```

The MVP can skip storing this cache entirely.

## Area Health Event Threshold

Area Health is derived, but Homekeep may emit `homekeep_area_health_changed`
after mutations when the derived value changes enough to matter.

Use these buckets:

```text
critical: 0 <= score < 40
poor:     40 <= score < 60
fair:     60 <= score < 80
good:     80 <= score <= 100
```

Emit `homekeep_area_health_changed` only when:

```text
bucket changed
or
abs(new_area_health - old_area_health) >= 10
```

Do not emit it during startup/cache rebuild, storage load, migration repair, or
when the previous value is unknown. Those paths may update entities, but should
not create historical event noise.

## Tests Required

- health can be recomputed from durable state after simulated cache loss
- completion followed by cache loss still yields correct Home Health
- stale or missing cached health does not affect recommendation correctness
- startup rebuilds or lazily computes health values
- stored `staleness_score` is not required for correctness
- area health changed event fires on bucket crossing
- area health changed event fires on absolute delta of at least 10 points
- area health changed event does not fire for smaller same-bucket changes
- area health changed event does not fire during startup/cache rebuild
