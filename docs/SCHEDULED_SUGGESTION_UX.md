# Scheduled-Suggestion UX

## Goal

Scheduled-Suggestion Mode plans a future Chore Session. It does not start work
and it never returns `session_id: null` as a pretend session.

The user journey is:

```text
plan future session
-> receive RecommendationSnapshot and recommendations
-> show saved proposal for the target window
-> when the user is ready later, validate freshness
-> start recommendation or regenerate
```

## Service Flow

Planning a future suggestion:

```text
homekeep.generate_smart_chore_list
  recommendation_mode: scheduled_suggestion
  target_time_window: next Friday 17:00-18:00

returns:
  snapshot_id
  recommendations
  expires_at
  target_time_window
```

The service must parse and normalize `target_time_window` using
`docs/TARGET_TIME_WINDOW.md`. The response should contain the normalized window,
not the raw input text.

Starting later:

```text
homekeep.start_recommendation
  recommendation_snapshot_id: <snapshot_id>
  recommendation_id: <recommendation_id>

returns:
  session_id
```

There is no MVP `homekeep.start_chore_session` service and no
`session_id: null` response. Until `start_recommendation` succeeds, the user
has a proposal, not a Chore Session.

## Homekeep app Flow

Homekeep app should provide a planned-session view:

```text
Plan chores
-> choose future window
-> choose time budget, energy, goal, optional area
-> call generate_smart_chore_list with scheduled_suggestion
-> show the Smart Chore List as a saved proposal
-> show target window and expiry
-> offer actions: Start now, Refresh, Dismiss proposal
```

When the user opens the saved proposal later:

```text
if snapshot is fresh:
  Start calls homekeep.start_recommendation
else:
  show "This plan is out of date"
  call generate_smart_chore_list again with the same visible context
  replace the saved proposal with the new response
```

Homekeep app must not call `start_recommendation` silently from an expired
proposal. It should refresh first, then let the user start one of the new
recommendations.

## Snapshot Freshness

Scheduled-Suggestion snapshots are intentionally temporary.

MVP freshness policy:

```text
default_expires_after = 60 minutes
```

For future windows more than 60 minutes away, Homekeep may regenerate proposals
closer to the target window. The original snapshot is a planning preview, not a
guarantee that the exact recommendation can be started later.

If a caller tries to start an expired or invalidated scheduled suggestion,
`homekeep.start_recommendation` must reject it with a clear service error.
The caller should regenerate using the same user-visible context.

## Response Shape

`generate_smart_chore_list` responses for Scheduled-Suggestion Mode must include
the normal Smart Chore List Result plus enough metadata for the UI:

```yaml
snapshot_id: string
recommendation_mode: scheduled_suggestion
target_time_window: string
expires_at: datetime
best_bundle: Recommendation | null
best_single_chore: Recommendation | null
easiest_chore: Recommendation | null
alternates: list[Recommendation]
empty_state: EmptyState | null
```

`target_time_window` is the normalized local ISO window described in
`docs/TARGET_TIME_WINDOW.md`.

## Tests Required

Implementation must test:

- scheduled-suggestion generation returns a snapshot and recommendations, not a
  session
- scheduled-suggestion response includes `target_time_window` and `expires_at`
- starting a fresh scheduled-suggestion recommendation creates a session
- starting an expired scheduled-suggestion recommendation is rejected
- starting an invalidated scheduled-suggestion recommendation is rejected
- Homekeep app uses Refresh/regenerate instead of a null session path
