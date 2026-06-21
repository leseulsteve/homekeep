# Concurrency And Idempotency

Home Assistant service calls can arrive twice, overlap, or come from stale UI.
Homekeep must serialize durable mutations and make retries idempotent where
practical.

## Mutation Lock

All durable mutations should run through one engine-level async lock.

Protected operations:

```text
start_recommendation
start_chore_bundle
complete_chore
skip_chore
snooze_chore
dismiss_chore
pause_session
accept_bonus_chore
end_session
refresh_calendar_context
storage migration/import
```

Read-only recommendation scoring may run outside the lock, but must revalidate
snapshot freshness before materializing a session.

## Request IDs

Mutation services should accept an optional `request_id`.

```yaml
request_id: string | null
```

If the same `request_id` is received again for the same operation, return the
same result instead of applying the mutation twice.

Idempotency key scope:

```text
operation + request_id
```

The same `request_id` may be reused by different operations without collision,
but the same operation and request ID must return the stored result while the
record is valid.

## Idempotency Record TTL

MVP TTL:

```text
idempotency_record_ttl_hours = 24
max_idempotency_records = 1000
```

When storing an idempotency record:

```text
created_at = now
expires_at = created_at + 24 hours
```

Records must be pruned:

- on storage load
- before adding a new idempotency record
- after adding a new idempotency record if the store exceeds
  `max_idempotency_records`

Pruning order:

```text
1. remove records where expires_at <= now
2. if still above max_idempotency_records, remove oldest created_at first
```

If an expired `operation + request_id` is received again, treat it as a new
request. The TTL is long enough for slow Home Assistant UI, mobile, automation,
or network retries, but short enough to keep storage bounded.

When a duplicate valid request is received, return the stored `result`
dictionary exactly as originally returned. Do not recompute it from current
state.

MVP fallback if `request_id` is absent:

```text
- complete_chore must not create duplicate ChoreCompletion records for the same
  session item
- start_recommendation must not create multiple sessions from a materialized
  RecommendationSnapshot unless it is an idempotent retry
- end_session must be safe to retry for the same final state
```

## Duplicate Completion Protection

For session completions, uniqueness is:

```text
session_id + session_item_id
```

For non-session completions, duplicates are harder to detect. MVP may allow
them unless `request_id` is provided.

## Tests Required

- double `complete_chore` for the same session item creates one completion
- double `start_recommendation` with the same request ID returns the same
session
- duplicate valid `operation + request_id` within 24 hours returns the stored
result without mutating state
- same request_id used for different operations does not collide
- expired idempotency record is ignored and the request is treated as new
- idempotency records older than 24 hours are pruned on load or write
- idempotency record store prunes oldest records above 1000 entries
- materialized snapshot cannot create duplicate sessions without idempotency
- concurrent complete and skip on the same session item resolves
deterministically
- stale UI mutation after session end is rejected
