# Mood And Readiness Feature Plan

## Status

This is a post-prototype feature plan. It does not replace the MVP Mood Context
rules in `docs/MOOD_CONTEXT.md`.

MVP behavior remains:

- Mood Context is lightweight, local-first, explainable, short-lived, and
  user-correctable.
- Mood values are `unknown`, `calm`, `focused`, `tired`, `overwhelmed`, and
  `energized`.
- Explicit user mood, energy, and goal choices override inference.
- Mood Context must not make medical or mental-health claims.
- Mood Context must not hide urgent stale chores by itself.

## Product Direction

After the MVP prototype, evolve Mood Context into broader Readiness Context.
Mood should become one optional input, while recommendation behavior should
mostly use practical planning signals:

- capacity
- energy
- time budget
- recent chore friction
- explicit session mode
- user correction
- derived Home Assistant context
- opt-in wearable signals

The goal is to make Homekeep better at choosing a useful chore posture without
sounding like it is diagnosing the user.

## Conversation Scope Captured

This plan consolidates the mood-related future work discussed after the MVP
Mood Context docs were written:

- the relationship between mood and chore suggestions
- whether Energy and Mood should merge into a broader Readiness concept
- user-facing Bubble Card behavior for inferred mood and session posture
- post-prototype chore-friction learning
- safer explanation wording
- explicit session modes
- Home Assistant context signals
- Android watch and wearable signals
- open-source and local-first sources such as Gadgetbridge
- privacy and storage guardrails for wearable, calendar, and Home Assistant
  signals

The MVP docs remain authoritative for the prototype. This plan is the future
feature direction once the prototype behavior is proven.

## Relationship To Energy And Mood

The MVP keeps Energy and Mood separate:

- Energy describes effort capacity: `low`, `normal`, `high`, or `quiet`.
- Mood describes lightweight readiness context: `unknown`, `calm`, `focused`,
  `tired`, `overwhelmed`, or `energized`.

Post-prototype UX should consider merging the front-facing concepts into
Readiness or Session Mode. Internally, Homekeep may still keep separate fields
for explicit energy, optional mood, inferred posture, and recommendation
context.

Reasonable future shape:

```yaml
energy_level: low | normal | high | quiet | null
mood_context: MoodContext | null
readiness_context: ReadinessContext | null
session_mode: auto | quick_win | light_session | focus_session | reset_mode | quiet_chores
```

Explicit user choices always win over inferred context.

## Naming

Use user-facing language that describes the session, not the person.

Preferred user-facing concepts:

- `Auto`
- `Quick win`
- `Light session`
- `Focus session`
- `Reset mode`
- `Quiet chores`

Avoid user-facing claims such as:

- "You seem stressed."
- "You are overwhelmed."
- "Your behavior suggests anxiety."

Internal naming may use:

- `readiness_context`
- `session_posture`
- `chore_readiness`

## Readiness Context Shape

Future implementation may introduce a derived context object like:

```yaml
readiness_context:
  posture: auto | quick_win | light_session | focus_session | reset_mode | quiet_chores
  confidence: low | medium | high
  source: explicit | inferred | fallback
  reason: string
  created_at: datetime
  expires_at: datetime
  signals_used:
    - energy_level
    - time_budget
    - chore_friction
    - calendar_context
```

`signals_used` should list broad derived signal groups, not raw private data.

## User-Facing Behavior

Bubble Card should keep the feature small and correctable.

Recommended controls:

```text
Mode: Auto | Quick win | Light session | Focus session | Reset mode | Quiet chores
```

If `Auto` infers a posture, show the posture gently:

```text
Auto: light session
```

or:

```text
Auto: quick win
```

The user should be able to override the posture with one tap. That correction
becomes a future learning signal.

Mood labels may remain available as an advanced or secondary control, but the
primary front-end concept should be the kind of chore session the user wants.

## Recommendation Behavior

Readiness Context may influence:

- default energy level when the user does not choose one
- default goal
- recommended session length
- number of recommendations shown
- bundle size
- choice between quick wins, low-energy chores, quiet chores, visible-impact
  chores, and larger reset chores
- explanation wording
- whether Homekeep asks fewer questions

Readiness Context must not:

- hide urgent stale chores by itself
- create punitive scoring
- override explicit user choices
- make medical or mental-health claims
- store raw wearable or calendar details as durable history

Suggested mode mapping:

```text
quick_win:
  prefer easiest useful chores and visible progress

light_session:
  prefer low-energy chores, tiny variants, and short sessions

focus_session:
  prefer bundles that fit the time budget

reset_mode:
  allow larger visible-impact chores when time and energy fit

quiet_chores:
  prefer quiet, low-disruption maintenance

auto:
  infer a posture conservatively from explicit inputs and derived context
```

## Chore Friction Signals

Track chore friction rather than trying to infer deeper emotional state.

Useful signals:

- user started the recommendation
- user completed the recommendation
- user skipped the recommendation
- user snoozed the recommendation
- user dismissed the recommendation
- user accepted a Bonus Chore
- user repeatedly chose quick wins in similar contexts
- user abandoned longer sessions
- user corrected the inferred mode
- user completed chores faster or slower than expected

These signals should be summarized into bounded, local derived values. Do not
store sensitive emotional history.

## Home Assistant Signals

Homekeep may use already-configured Home Assistant entities when the user opts
into Readiness Context.

Useful derived signals:

- home, away, or recently arrived
- room or area presence
- time since arriving home
- quiet evening scene or bedtime mode
- Do Not Disturb mode
- media player active
- calendar-derived flags such as `busy_window`, `guests_soon`, `travel`, or
  `recovery_window`
- weather-derived friction such as heat, snow, rain, or poor air quality
- household activity level, expressed as broad derived context

Homekeep should prefer derived flags over raw entity details.

## Wearable Signals

Wearable signals are optional, opt-in, and low-confidence unless the user
explicitly chooses a matching session mode.

Candidate signals:

- recent sleep duration or sleep quality
- resting heart-rate trend
- heart-rate variability trend, when available
- current heart rate, only as a soft readiness signal
- step count or activity level today
- workout or exercise detected recently
- bedtime mode
- Do Not Disturb mode
- on-body state
- watch interactive state
- manual watch shortcut such as `quick win`, `light`, or `focus`

Wearable health signals must be treated as practical planning hints, not health
interpretations. Homekeep should never explain a recommendation by saying the
user is stressed, anxious, depressed, unhealthy, or medically fatigued.

## Open-Source And Local-First Sources

Potential future sources to evaluate:

- Home Assistant Companion Wear OS sensors for Home Assistant-native watch
  entities such as activity state, heart rate, steps, bedtime mode, Do Not
  Disturb, on-body state, light, proximity, battery, and interactive state.
- Gadgetbridge as an open-source Android wearable bridge for supported devices,
  activity/sleep data, and local-first wearable workflows.
- Android Health Connect as an optional Android data broker when the user
  already uses it. Treat it as optional because it is platform infrastructure,
  not a Homekeep-owned source of truth.

Before implementation, verify the exact sensors and permissions against the
installed Home Assistant Companion App, the user's watch, and the current
official docs.

## Explanations

Explanations should describe why the chore session fits the context.

Good examples:

```text
A short quick-win session fits your recent pattern.
```

```text
You picked low energy, so I prioritized lighter chores.
```

```text
This is short enough for the time you chose.
```

Avoid:

```text
You seem stressed.
```

```text
Your behavior suggests you are overwhelmed.
```

```text
Your heart rate means you should rest.
```

## Storage And Privacy

Durable storage may keep:

- derived Readiness Context
- short non-creepy reason
- broad signal categories used
- expiration timestamp
- explicit user correction
- bounded chore-friction summaries

Durable storage must not keep:

- raw heart-rate history
- raw sleep history
- raw calendar event text
- private message content
- microphone or camera data
- medical conclusions
- personality labels
- hidden mood labels shown as facts

Default expiry should stay short. The MVP `mood_context_ttl_minutes = 60`
remains a reasonable starting point for inferred readiness.

## Implementation Phases

Post-prototype implementation should be split into small phases:

1. Add Readiness Context docs and schemas while preserving MVP Mood Context.
2. Add explicit session mode input to service schemas and Bubble Card.
3. Map explicit modes to recommendation defaults and explanations.
4. Add chore-friction summaries from existing session history.
5. Add user correction capture and bounded learning.
6. Add opt-in Home Assistant derived sensor inputs.
7. Add opt-in wearable-derived inputs.
8. Harden privacy tests, explanation tests, and stale-chore override behavior.

## Tests Required

Future tests should cover:

- explicit mode overrides inferred readiness
- explicit energy and goal still override inference
- `Auto` falls back to normal recommendations when signals are sparse
- low confidence changes wording/defaults more than ranking
- urgent stale chores are not hidden by Readiness Context
- raw calendar details are not stored
- raw wearable health history is not stored
- chore-friction summaries are bounded and local
- user correction changes future posture suggestions without creating punitive
  scoring
- generated explanations avoid medical and mental-health claims
- unavailable sensors fail closed to `unknown` or neutral readiness
