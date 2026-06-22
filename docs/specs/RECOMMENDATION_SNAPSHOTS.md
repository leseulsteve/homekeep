# Recommendation Snapshot Lifecycle

Recommendation snapshots are proposals. Chore Sessions are durable work records.
The implementation must not confuse the two.

Every RecommendationSnapshot stores a `context_fingerprint` generated from the
exact normalized recommendation context. A Chore Session materialized from the
snapshot copies that fingerprint for provenance and stale-response diagnostics.
See `docs/specs/CONTEXT_FINGERPRINT.md`.

## Snapshot States

```text
fresh:
- can be used to start a Chore Session

expired:
- cannot be used to start a new Chore Session
- can remain stored for audit/debugging

invalidated:
- cannot be used to start a new Chore Session
- caused by changed Calendar Context, changed Chore definitions, or changed
  source context

materialized:
- already used to create a Chore Session
- the Chore Session owns its selected chores from this point forward
```

## Starting From A Snapshot

`homekeep.start_recommendation` must validate the snapshot before creating a
session:

```text
if snapshot does not exist:
  reject
elif snapshot is expired:
  reject and ask caller to regenerate recommendations
elif snapshot is invalidated:
  reject and ask caller to regenerate recommendations
elif recommendation_id is not in snapshot:
  reject
else:
  create Chore Session from snapshot contents
  copy context_fingerprint onto ChoreSession
  mark snapshot materialized
```

`homekeep.start_chore_bundle` is a bundle-only alias.

## Scheduled-Suggestion Snapshots

Scheduled-Suggestion snapshots are saved proposals for a future window. They
are not Chore Sessions and must not return `session_id: null`.

The caller flow is:

```text
generate_smart_chore_list(scheduled_suggestion)
-> store/display snapshot_id, recommendations, target_time_window, expires_at
-> later call start_recommendation only if the snapshot is still fresh
-> regenerate if expired or invalidated
```

If a scheduled proposal expires before the user starts it,
`start_recommendation` must reject it. The UI should regenerate from the same
visible context instead of trying to recover the expired snapshot.

See `docs/specs/SCHEDULED_SUGGESTION_UX.md`.

## Active Sessions

Once a Chore Session has been created, it must not depend on the freshness of
the source RecommendationSnapshot.

If the RecommendationSnapshot expires after session creation:

```text
- the active Chore Session remains valid
- completing session items remains valid
- stale session response protections still apply by session_id/current session
- the session should retain source_recommendation_snapshot_id and
  context_fingerprint for audit/debugging only
```

## Stale Session Protection

Stale session response protection applies to Chore Session mutations, not to
RecommendationSnapshot freshness.

Example:

```text
1. Snapshot A is fresh.
2. User starts Bundle A, creating Session 1.
3. Snapshot A expires.
4. Session 1 remains valid.
5. A delayed UI response tries to mutate old Session 0.
6. Homekeep rejects the stale Session 0 mutation.
```

## Expired Snapshot UX

If a user tries to start an expired recommendation:

```text
That recommendation is out of date. I refreshed the list.
```

Homekeep should regenerate a Smart Chore List when practical, but the service
must not silently start a session from expired context.
