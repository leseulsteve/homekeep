# Homekeep Architecture

## Goal

Homekeep is a Home Assistant custom integration. The integration should keep
the chore engine separate from Home Assistant entity/service glue so the core
logic can be tested without a running Home Assistant instance.

## Boundaries

```text
Home Assistant boundary:
- config entries
- services/actions
- sensor, binary_sensor, and todo entities
- calendar entity access
- Bubble Card dashboard calls

Homekeep core:
- chore definitions and state
- health score calculations
- recommendation scoring
- Chore Session lifecycle
- Session-History Learning
- storage migrations
```

## Suggested Module Layout

```text
custom_components/homekeep/
  __init__.py
  manifest.json
  const.py
  config_flow.py
  services.yaml
  strings.json
  sensor.py
  binary_sensor.py
  todo.py
  coordinator.py
  storage.py
  models.py
  engine.py
  scoring.py
  health.py
  recommendations.py
  sessions.py
  calendar_context.py
  history.py
```

## Module Responsibilities

`models.py`
: Dataclasses or typed models for chore definitions, state, completions,
sessions, recommendation snapshots, and user preference stats.

`storage.py`
: Versioned Home Assistant storage helpers, migrations, load/save validation,
and default empty store creation.

`health.py`
: Derived Staleness, Home Health, Area Health, Group Health, and Projected
Impact. Health values are computed from durable chore state and completions;
cached values are disposable.

`scoring.py`
: Bounded component scoring helpers and the deterministic v1 scoring formula.

`recommendations.py`
: Smart Chore List generation, Chore Bundle selection, empty states, and
recommendation explanations.

`sessions.py`
: Chore Session lifecycle: start, complete, skip, snooze, dismiss, pause, end,
RecommendationSnapshot materialization, and Bonus Chore handling.

`calendar_context.py`
: Reads Home Assistant calendar data and converts it into small derived
Calendar Context signals. Owns snapshot freshness checks, max-age policy, and
calendar entity invalidation handling.

`history.py`
: Session-History Learning stats, deterministic context buckets, fallback
matching, and bounded updates after sessions.

`engine.py`
: Facade used by Home Assistant services and entities. Coordinates storage,
health, recommendation, session, and history operations. Owns mutation locking
and idempotency dispatch.

`coordinator.py`
: Home Assistant update coordinator and entity notification bridge.

## Design Rules

- Homekeep storage is the source of truth.
- Durable mutations must be serialized through the engine to avoid duplicate
completions and conflicting session item updates.
- Home Assistant To-do entities are projections.
- To-do completion may write through to Homekeep logic, but To-do create,
  delete, rename, edit, and reorder operations must be rejected or reverted.
- Core recommendation behavior must be local-first.
- Home Health, Area Health, Group Health, Staleness, and Projected Impact are
  derived values, not authoritative stored state.
- Recommendation generation must be bounded and explainable.
- Calendar details should be minimized in long-lived storage.
- Calendar Context must be refreshed automatically when selected calendar
  entities change or when snapshots exceed their max age.
- Recommendation snapshots are proposals. They must be fresh to start a Chore
  Session, but active Chore Sessions remain valid after source snapshot expiry.
- Adaptive intervals must be clamped on every write and trained only by real
  completions.
- Skips, snoozes, dismissals, and cancellations must not count as completions.
