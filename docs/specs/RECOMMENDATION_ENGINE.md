# Recommendation Engine

## Goal

Generate Smart Chore Lists that are useful, light, explainable, and bounded.

Homekeep should rank chores by usefulness in context, not only by due date.

## Recommendation Modes

Ready-Now Mode:
: User is ready now. Recommend an immediate Light Session.

Scheduled-Suggestion Mode:
: User or calendar context asks for a future window. Recommend a planned Chore
Session for that time.

## V1 Scoring Formula

Every component is normalized to `0-100`.

```text
recommendation_score =
  staleness_score * 0.30
+ health_impact_score * 0.25
+ time_fit_score * 0.15
+ energy_fit_score * 0.10
+ area_fit_score * 0.10
+ calendar_context_score * 0.05
+ history_fit_score * 0.05
- dismissal_penalty
```

## Component Definitions

`staleness_score`
: How much the chore needs attention now or by the target time window.

`health_impact_score`
: Estimated Home Health, Area Health, or Group Health improvement.

`time_fit_score`
: How well the chore fits the user's available time.

`energy_fit_score`
: How well the chore fits the selected or inferred energy level. Mood Context
may help choose a default energy level when the user does not provide one, but
explicit user choices always win.

`area_fit_score`
: Whether the chore matches the selected or detected Home Assistant Area.

`calendar_context_score`
: Whether the chore helps prepare for or recover from Calendar Context.
Calendar Context must be fresh. If the snapshot is expired or a source calendar
entity changed, refresh before scoring or score without Calendar Context.
  When this component guesses from Chore names, groups, or Home Assistant Area
  ids, it uses the shared English/basic-French text-signal matcher rather than
  English-only keywords.

`history_fit_score`
: Whether similar users or sessions historically accept or complete this chore.
Uses the bounded context bucket strategy in
`docs/specs/SESSION_HISTORY_LEARNING.md`. If matching history is sparse, fall back to
broader buckets and then to a neutral score.

`Mood Context`
: A lightweight inferred or explicit context from `docs/specs/MOOD_CONTEXT.md`.
Mood Context may influence energy defaults, session length, recommendation
wording, and how many choices Homekeep shows. It must not hide urgent stale
chores by itself.

`dismissal_penalty`
: Bounded, decaying penalty from recent dismissals. It uses the formula in
`docs/specs/DISMISSAL_PENALTY.md`. Snoozes do not add to this penalty in MVP; they
only hide a chore until the explicit snooze target time.

Snoozed chores with a future `snoozed_until` are excluded from normal
recommendations before scoring, following `docs/specs/SNOOZE_POLICY.md`.

The scoring implementation must compute:

```text
base_score =
  staleness_score * 0.30
+ health_impact_score * 0.25
+ time_fit_score * 0.15
+ energy_fit_score * 0.10
+ area_fit_score * 0.10
+ calendar_context_score * 0.05
+ history_fit_score * 0.05

recommendation_score = clamp(base_score - effective_dismissal_penalty, 0, 100)
```

Dismissals may temporarily lower or cool down recommendations. They must not
permanently suppress stale chores.

## Smart Chore List Shape

The first Smart Chore List should include at most:

```text
1 best Chore Bundle
1 best single chore
1 easiest useful chore
up to 3 alternates
```

Each recommendation must include:

- stable `recommendation_id`
- kind
- title
- chore items
- estimated minutes
- Projected Impact
- short explanation
- suggested action

If Mood Context influenced the recommendation, the explanation should say so in
practical language without claiming to know the user's inner state.

Use the payload shape in `docs/specs/RECOMMENDATION_PAYLOADS.md`.

## Explanation Examples

```text
Reason: high Kitchen Health impact, fits 5 minutes, and you often choose
kitchen tasks after work.
```

```text
Reason: guests are on the calendar tomorrow, and this improves Bathroom Health
quickly.
```

## Empty State

If no good recommendation exists:

```text
No useful chore fits this session.
Options:
- loosen filters
- show all due chores
- schedule a session for later
- end for now
```

## Light Session Rules

- Prefer short sessions.
- Finishing the planned session is always a success.
- Offer a Bonus Chore only after completion.
- Bonus Chores are optional and bounded.
- Asking for "one more" is positive history, not permission for an unbounded
queue.
- Bonus Chores use the original Chore Session in `bonus_pending` /
  `bonus_active` states; they do not create an implicit new session in MVP.
