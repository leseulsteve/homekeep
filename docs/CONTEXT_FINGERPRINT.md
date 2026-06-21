# Context Fingerprint

## Goal

`context_fingerprint` identifies the exact recommendation context that produced
a RecommendationSnapshot and the Chore Session materialized from it.

It is not the same as `context_bucket`.

## Difference From Context Bucket

`context_bucket`
: A broad, human-readable grouping key for Session-History Learning. It
intentionally collapses many similar situations together.

`context_fingerprint`
: A stable hash of the exact normalized recommendation context. It is for
snapshot/session provenance, stale-response diagnostics, and debugging.

## Format

Use a versioned SHA-256 fingerprint:

```text
ctx:v1:<sha256_hex>
```

The hash input is canonical JSON:

```text
json.dumps(payload, sort_keys=True, separators=(",", ":"))
```

Use UTF-8 bytes of that canonical JSON as the SHA-256 input.

## V1 Payload

The v1 payload must include only normalized, durable, non-secret context:

```yaml
schema_version: 1
recommendation_mode: ready_now | scheduled_suggestion
target_time_window: string | null
time_budget_minutes: int | null
energy_level: low | normal | high | quiet | null
goal: quick_wins | overdue | visible_impact | prevent_future_mess | full_reset | null
area_id: string | null
mood: unknown | calm | focused | tired | overwhelmed | energized | null
calendar_context_id: string | null
calendar_context_version: string | null
chore_definition_version: string
enabled_chore_ids: list[string]
home_assistant_area_ids: list[string]
user_id: string | null
```

Normalization rules:

- sort all list values before hashing
- use `null` instead of missing optional fields
- use stable IDs, not names
- do not include raw calendar event text
- do not include secrets, tokens, private endpoints, or raw Home Assistant
  state blobs
- do not include volatile timestamps such as `created_at`
- include `target_time_window` only as the normalized local ISO window from
  `docs/TARGET_TIME_WINDOW.md`, not the raw user input text

## Storage Rules

`RecommendationSnapshot.context_fingerprint`
: Required. Generated when the snapshot is created.

`ChoreSession.context_fingerprint`
: Copied from the source RecommendationSnapshot when the session is
materialized. It must not be recomputed from later state.

If a session is created without a RecommendationSnapshot in a future non-MVP
path, `context_fingerprint` may be null until that path defines its own
fingerprint payload.

## Uses

Use `context_fingerprint` for:

- debugging why a recommendation was produced
- detecting delayed UI responses from older recommendation contexts
- comparing a session to its source snapshot
- explaining why a Scheduled-Suggestion proposal was invalidated or refreshed

Do not use `context_fingerprint` for:

- Session-History Learning lookup
- user-facing labels
- security decisions
- deduplicating different users' private context across households

## Tests Required

Implementation must test:

- same normalized payload produces the same fingerprint
- list ordering does not change the fingerprint
- changed energy, goal, area, mood, enabled chores, or calendar context version
  changes the fingerprint
- volatile `created_at` does not change the fingerprint
- raw calendar descriptions are not included in the payload
- ChoreSession copies the fingerprint from RecommendationSnapshot
- `context_bucket` and `context_fingerprint` are different concepts and values
