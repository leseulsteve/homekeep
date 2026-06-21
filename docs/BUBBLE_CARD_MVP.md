# Bubble Card MVP

Bubble Card is the MVP dashboard layer. It should trigger Homekeep services and
display Homekeep entities; it should not own state.

Bubble Card should collect setup answers locally. It must not call
`homekeep.answer_session_question` in MVP.

## First Dashboard Flow

```text
I'm ready
-> choose time
-> choose energy
-> optionally accept or override Mood: Auto
-> choose goal
-> generate Smart Chore List
-> start Chore Bundle or single chore
-> replace proposal UI with start_recommendation response items
-> complete / skip / snooze
-> done for now / one more
```

## Scheduled-Suggestion Flow

Scheduled-Suggestion Mode is a planning flow, not a half-started session.
Bubble Card must never expect `session_id: null`.

```text
Plan chores
-> choose future window
-> choose time, energy, goal, optional area
-> call homekeep.generate_smart_chore_list with scheduled_suggestion
-> show saved proposal with target window and expires_at
-> later: user opens proposal
-> if fresh, Start calls homekeep.start_recommendation
-> if expired or invalidated, Refresh regenerates the Smart Chore List
```

If a planned proposal expires before the user starts it, the UI should show a
short "This plan is out of date" state and regenerate with the same visible
context. Do not silently start an expired proposal.

## Controls

Time:

```text
2 min
5 min
15 min
30 min
```

Energy:

```text
low
normal
high
quiet
```

Mood:

```text
auto
calm
focused
tired
overwhelmed
energized
```

Goal:

```text
quick_wins
overdue
visible_impact
prevent_future_mess
full_reset
```

Actions:

```text
Generate
Plan
Refresh
Start
Done
Skip
Snooze
End
One more
```

## Entities To Display

```text
sensor.homekeep_home_health
sensor.homekeep_due_chore_count
sensor.homekeep_best_next_chore
todo.homekeep_recommendations
todo.homekeep_active_session
```

## Services To Call

```text
homekeep.generate_smart_chore_list
homekeep.start_recommendation
homekeep.complete_chore
homekeep.skip_chore
homekeep.snooze_chore
homekeep.accept_bonus_chore
homekeep.end_session
```

## UX Rules

- Keep sessions light.
- Show at most a few recommendations.
- Prefer action labels over explanation paragraphs.
- Show Projected Impact when available.
- If Mood Context is inferred, show it as a soft Auto suggestion and let the
  user override it quickly.
- Always make "Done for now" a valid success state.
- "One more" should offer a Bonus Chore, not a new full queue.
- Scheduled-Suggestion proposals must show their target window and expiry.
- Expired Scheduled-Suggestion proposals must be refreshed before start.
- After Start, Bubble Card must use materialized `session_item_id` values from
  the `start_recommendation` response. It must not use cached recommendation
  item IDs.
- Session dismiss actions must pass `session_id` and materialized
  `session_item_id` so history learning uses the correct session context.

## Phase 7 Dashboard Gap

Bubble Card can represent the touch surface with pop-ups, select cards,
buttons, sub-buttons, and Home Assistant call-service actions. It should not be
treated as the owner of Homekeep state.

The MVP dashboard example uses Home Assistant helper entities and small scripts
as a bridge because dashboard cards do not cleanly persist service response
payloads such as `snapshot_id`, `recommendation_id`, `session_id`, and
`session_item_id` for later button calls.

The scripts should:

- read local setup helpers for time, energy, goal, and mood
- call Homekeep services
- store returned ids in helper entities for the next action
- leave the authoritative Chore Session and To-do projections in Homekeep
  storage

The dashboard itself displays Homekeep sensors and To-do projections rather
than copying recommendation or session state into Lovelace-only data.
