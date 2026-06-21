# Implementation Readiness Review

This review records gaps found before scaffolding and the contracts added to
avoid implementation guesswork.

Implementation conflict resolution now lives in `docs/DECISION_LOG.md`. If this
readiness review or any older planning doc conflicts with the decision log, the
decision log wins.

## Holes Closed

Calendar freshness:
: Calendar Context snapshots now have invalidation rules, source entity version
tracking, and max-age checks.

Adaptive interval bounds:
: `adaptive_interval_days` must be clamped on every write and trained only by
real completions.

Recommendation snapshot lifecycle:
: Expired or invalidated snapshots cannot start new sessions. Sessions already
materialized from a snapshot remain valid.

Session-History Learning buckets:
: `context_bucket` now has deterministic v1 dimensions, fallback matching, and
neutral scoring for sparse history.

To-do projection writes:
: To-do completion is the only supported write-through operation. Create,
delete, rename, edit, and reorder are rejected or reverted.

Participant attribution:
: `completed_by` is validated against session participants when participants
are present.

Bonus Chore lifecycle:
: Bonus Chores use the original session through `bonus_pending` and
`bonus_active`, with explicit `accept_bonus_chore`.

Derived health:
: Home Health, Area Health, Staleness, and Projected Impact are derived values.
Caches are disposable.

Session materialization:
: `start_recommendation` is the canonical service for bundle and single-chore
recommendations. `generate_smart_chore_list` creates proposals only.
Scheduled-Suggestion Mode does not create active sessions. There is no MVP
`start_chore_session` service.

Concurrency and idempotency:
: Durable mutations require engine serialization and optional `request_id`
handling.

Recommendation payloads:
: Smart Chore List entries now have a stable documented payload shape.

## Residual Implementation Decisions

These should be decided during scaffolding, not left implicit:

- Exact Home Assistant service response support and whether each service returns
data or only updates entities.
- Exact HA storage key names.
- Exact config flow fields and options flow shape.
- Whether MVP exposes per-chore due binary sensors for every chore or only for
enabled/high-priority chores.
- Whether area-focused To-do projections are enabled by default or opt-in.
- Exact Bubble Card YAML after the first entities/services exist.

## Scaffold Readiness

The project is ready to scaffold when Codex can implement from:

1. `AGENTS.md`
2. `docs/DECISION_LOG.md`
3. `docs/IMPLEMENTATION_PROGRESS.md`
4. `docs/IMPLEMENTATION_PLAN.md`
5. `docs/SCAFFOLDING_TASKS.md`
6. `docs/ARCHITECTURE.md`
7. `docs/HOME_ASSISTANT_CONTRACT.md`
8. `docs/SERVICE_SCHEMAS.md`
9. `docs/DATA_MODEL.md`
10. `docs/RECOMMENDATION_PAYLOADS.md`
11. `docs/TEST_PLAN.md`
