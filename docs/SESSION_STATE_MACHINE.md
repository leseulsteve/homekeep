# Session State Machine

Chore Sessions must have explicit state transitions. Recommendation proposals
are not sessions until the user starts one.

## Status Values

```text
active
paused
bonus_pending
bonus_active
completed
cancelled
```

## Allowed Transitions

```text
new -> active
active -> paused
paused -> active
active -> bonus_pending
paused -> bonus_pending
active -> completed
paused -> completed
active -> cancelled
paused -> cancelled
bonus_pending -> bonus_active
bonus_pending -> completed
bonus_active -> completed
bonus_active -> cancelled
```

Disallowed:

```text
completed -> active
cancelled -> active
completed -> bonus_active
cancelled -> bonus_active
bonus_pending -> paused
bonus_active -> paused
```

## Paused Sessions

Paused means the user is not actively working from the UI, but the session can
still receive valid item completions from another participant, a projected
To-do item, voice, automation, or delayed service call.

If all planned items are complete while a session is paused, the next
`end_session(status=completed, offer_bonus_chore=true)` call may transition:

```text
paused -> bonus_pending
```

Pausing does not block Bonus Chore eligibility. Eligibility depends on planned
session completion and the one-bonus-per-session rule, not whether the previous
state was `active` or `paused`.

## Starting Sessions

Ready-Now Mode creates a RecommendationSnapshot first. It does not create a
Chore Session until the user starts a recommendation.

Scheduled-Suggestion Mode creates a RecommendationSnapshot only. It must not
create an active Chore Session until the user explicitly starts a
recommendation.

Scheduled-Suggestion callers receive a proposal with `snapshot_id`, not a
`session_id: null`. If the proposal expires before `start_recommendation`, the
caller must regenerate recommendations.

## Starting Recommendations

The MVP must support starting:

```text
Chore Bundle recommendation
single chore recommendation
easiest chore recommendation
```

Canonical service:

```text
homekeep.start_recommendation
```

`homekeep.start_chore_bundle` may remain as a bundle-only alias, but new code
should use `start_recommendation`.

## Session Items

A Chore Session must store concrete session items at start time:

```yaml
items: list[SessionItem]
```

Do not rely on the source RecommendationSnapshot after materialization.
