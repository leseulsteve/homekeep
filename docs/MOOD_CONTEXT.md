# Mood Context

## Goal

Homekeep should sometimes infer the user's likely mood or readiness so it can
make planning and chore suggestions feel kinder and better timed.

Mood Context is practical, lightweight, local-first, and user-correctable. It is
not a mental health assessment.

## MVP Mood Values

Use a small bounded enum:

```text
unknown
calm
focused
tired
overwhelmed
energized
```

Every inferred Mood Context must include:

```yaml
mood: unknown | calm | focused | tired | overwhelmed | energized
confidence: low | medium | high
source: explicit | inferred | fallback
reason: string
created_at: datetime
expires_at: datetime
```

`reason` must be short and non-creepy, for example:

```text
Reason: busy calendar window and you often choose quick wins at this time.
```

## Inputs

Allowed MVP signals:

- explicit user-selected mood
- selected energy level
- selected goal
- time budget
- time of day using Home Assistant local time
- recent accepted, skipped, snoozed, dismissed, and completed chores
- recent Bonus Chore acceptance
- derived Calendar Context such as busy window, guests soon, travel, or recovery
- Home Assistant presence or area context when already configured

Disallowed MVP signals:

- raw calendar event descriptions in long-lived storage
- private message content
- microphones or cameras
- medical, mental health, or personality labels
- hidden mood labels shown as facts

## Inference Rules

Mood inference must be conservative.

Suggested MVP rules:

```text
explicit user mood -> use it with high confidence
low energy + short time budget -> tired, medium confidence
many skips/snoozes/dismissals in recent sessions -> overwhelmed, medium confidence
Bonus Chore accepted recently -> energized, medium confidence
quiet energy selected -> calm, medium confidence
busy calendar window soon -> overwhelmed, low or medium confidence
no signal -> unknown, low confidence
```

When confidence is low, Mood Context should influence wording and defaults, not
strongly alter ranking.

## Recommendation Behavior

Mood Context may influence:

- default energy level when the user does not choose one
- default goal
- recommended session length
- number of recommendations shown
- choice between quick wins, low-energy chores, and visible-impact chores
- explanation wording
- whether Homekeep asks fewer questions

Mood Context must not:

- hide urgent stale chores by itself
- create punitive scoring
- override explicit user choices
- make claims like "you are anxious" or "you are depressed"

## Suggested Mapping

```text
tired:
  prefer low-energy chores, tiny variants, short sessions

overwhelmed:
  prefer one best next step, quick wins, visible progress, fewer choices

focused:
  prefer bundles that fit the time budget

energized:
  allow normal/deep variants and optional Bonus Chore

calm:
  prefer quiet chores and steady maintenance

unknown:
  use normal scoring
```

## Storage

Mood Context may be stored inside RecommendationSnapshot for audit and
explanation:

```yaml
mood_context:
  mood: string
  confidence: string
  source: explicit | inferred | fallback
  reason: string
  created_at: datetime
  expires_at: datetime
```

Do not store long-lived raw signals used to infer mood. Store the derived mood
context and short reason only.

MVP expiry:

```text
mood_context_ttl_minutes = 60
```

## UI Behavior

Lovelace should let the user override the inferred mood quickly.

Recommended controls:

```text
Mood: Auto | Calm | Focused | Tired | Overwhelmed | Energized
```

When Homekeep infers mood, show it gently:

```text
Mood: Auto - looks like a quick-win session fits
```

Avoid making mood the main visible feature. It should make Homekeep feel
thoughtful, not invasive.

## Post-Prototype Feature Plan

After the MVP prototype, consider evolving Mood Context into broader Readiness
Context. The coherent post-prototype plan lives in
`docs/MOOD_READINESS_FEATURE_PLAN.md`.

Strong direction:

```text
Mood should become one optional input, while recommendation behavior should
mostly use capacity, energy, time, recent chore friction, explicit session mode,
derived Home Assistant context, opt-in wearable signals, and user correction.
```

## Tests Required

Implementation must test:

- explicit mood overrides inferred mood
- no signals returns `unknown` with low confidence
- low energy and short time budget infer `tired`
- repeated skips/snoozes/dismissals can infer `overwhelmed`
- recent Bonus Chore acceptance can infer `energized`
- inferred mood does not override explicit energy or goal
- inferred mood does not hide urgent stale chores
- Mood Context expires after 60 minutes
- raw calendar descriptions are not stored in Mood Context
