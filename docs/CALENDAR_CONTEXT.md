# Calendar Context Freshness

Calendar Context must not go stale silently. Recommendations that depend on
calendar data must either use a fresh snapshot or refresh the context before
scoring.

## Sources Of Invalidation

Calendar Context snapshots become stale when any of these happen:

- A selected calendar entity changes state.
- A selected calendar entity has a newer `last_changed` or `last_updated` value
than the snapshot recorded.
- The fetched events for the selected window produce a different minimized
  event fingerprint.
- The snapshot exceeds its max age.
- The target time window changes.
- The selected calendar entity list changes.
- The user manually calls `homekeep.refresh_calendar_context`.

## Automatic Trigger

Homekeep should register Home Assistant state listeners for selected calendar
entities.

On calendar entity state change:

```text
1. Mark affected CalendarContextSnapshot records stale.
2. Update sensor.homekeep_next_calendar_context.
3. Invalidate recommendation snapshots that used the stale Calendar Context.
4. Regenerate recommendations only when needed by an active flow or entity
   update; avoid unbounded background work.
```

The manual `homekeep.refresh_calendar_context` service is still useful, but it
must not be the only refresh path.

## Max-Age Policy

Recommended initial limits:

```text
Ready-Now Mode Calendar Context: 15 minutes
Scheduled-Suggestion Mode Calendar Context: 60 minutes
Calendar Context with guests/travel/trash signals: expires at the relevant event boundary when sooner
```

At recommendation time, Homekeep must check snapshot freshness:

```text
if no snapshot exists:
  refresh Calendar Context
elif snapshot is expired:
  refresh Calendar Context
elif source calendar entity version changed:
  refresh Calendar Context
elif minimized event fingerprint changed:
  refresh Calendar Context
else:
  use snapshot
```

If refresh fails, the Recommendation Engine should continue without Calendar
Context and include a non-fatal explanation in diagnostics.

## Snapshot Entity Versions

Snapshots should record source calendar entity versions using Home Assistant
state metadata:

```yaml
source_calendar_versions:
  calendar.family:
    state: "on"
    last_changed: "2026-06-21T15:00:00+00:00"
    last_updated: "2026-06-21T15:00:00+00:00"
```

Exact values can be implementation-specific, but they must be sufficient to
detect a calendar change after snapshot creation.

## Event Fingerprint

Homekeep stores a `source_calendar_event_fingerprint` hash alongside the
Calendar Context snapshot. The fingerprint is built from minimized event facts
such as start/end times and derived category flags for guest, travel, trash,
and evening signals. It must not include raw event summary, description, or
location text.

Calendar signal keyword matching supports English and basic French phrases for
private live testing, including guest/visit/supper, departure/airport/travel,
and trash/recycling/compost terms.

Recommendation generation checks this fingerprint before reusing Calendar
Context. This covers Home Assistant calendars where editing or adding events
does not change the calendar entity state while it remains `off`.
