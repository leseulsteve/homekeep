# Mood Context

## Goal

Homekeep should sometimes infer the user's likely readiness context so it can
make planning and chore suggestions feel kinder and better timed.

Mood Context is practical, lightweight, local-first, and user-correctable. It is
not a mental health assessment and must not claim to know how the user feels.

## MVP Mood Values

Use a small bounded enum:

```text
auto
low
quiet
focused
restless
ready
```

Every inferred Mood Context must include:

```yaml
mood: auto | low | quiet | focused | restless | ready
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
- selected or inferred Capacity
- inferred Goal
- time/calendar pressure such as tight window, late evening, or free block
- time of day using Home Assistant local time
- recent behavior such as skipped or removed heavier chores, accepted quick
  resets, and completed fuller bundles
- current session context such as just finished something, paused often, or
  abandoned a session
- recent completion of fuller Chore Bundles
- derived Calendar Context such as open window, busy window, quiet hours,
  guests soon, travel, or recovery
- Home Assistant context such as time of day, presence, or configured quiet
  hours

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
explicit user mood -> use it with high confidence for the current context
user correction such as selecting low, quiet, focused, restless, or ready ->
  override inference for the moment
no signal -> auto, low confidence
clear constraints such as tight time, repeated recent removal of physical
  chores, or short-window context -> low, medium confidence
late evening or configured quiet hours -> quiet, medium confidence
normal open window with one clear high-need target -> focused, low or medium
  confidence
restless -> usually explicit only for MVP; infer only with strong future
  evidence
free block plus past completion of fuller bundles in similar contexts -> ready,
  medium confidence
paused often or abandoned a current session -> lower ambition, usually low or
  auto depending on confidence
just finished something successfully -> allow a slightly more ready default only
  when recent history supports it
```

When confidence is low, Mood Context should influence wording and defaults, not
strongly alter ranking.

Do not infer `low` because Homekeep thinks the user "seems tired." Do not infer
`ready` from vibes or a positive-sounding context alone. Mood is readiness
context, not diagnosis.

## Recommendation Behavior

Mood Context may influence:

- inferred Capacity when the user does not explicitly correct it
- inferred Goal
- recommended session length
- number of recommendations shown
- choice between quick wins, low-capacity chores, and visible-impact chores
- explanation wording
- whether Homekeep asks fewer questions

Mood Context must not:

- hide urgent stale chores by itself
- create punitive scoring
- override explicit user choices
- make claims like "you are tired", "you are anxious", or "you are depressed"

## Suggested Mapping

```text
auto:
  use normal scoring and keep inference easy to correct

low:
  prefer quick wins, low Capacity, tiny variants, short sessions

quiet:
  prefer steady contained chores, low stimulation, and gentle copy

focused:
  prefer one clear high-need target or a useful mid-sized reset

restless:
  prefer visible lift, movement-friendly chores, and contained multi-room resets

ready:
  allow fuller bundles when calendar and history fit support it
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

Homekeep app should let the user override the inferred mood quickly.

Recommended controls:

```text
Mood: Auto | Low | Quiet | Focused | Restless | Ready
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
`docs/product/MOOD_READINESS_FEATURE_PLAN.md`.

Strong direction:

```text
Mood should become one optional input, while recommendation behavior should
mostly use capacity, energy, time, recent chore friction, explicit session mode,
derived Home Assistant context, opt-in wearable signals, and user correction.
```

## Tests Required

Implementation must test:

- explicit mood overrides inferred mood for the current context
- no signals returns `auto` with low confidence
- clear constraints can infer `low`
- late evening or configured quiet hours can infer `quiet`
- normal open window with one clear high-need target can infer `focused`
- `restless` is mostly explicit in MVP
- free block plus past fuller-bundle completion can infer `ready`
- inferred mood does not override explicit user correction
- inferred mood does not hide urgent stale chores
- Mood Context expires after 60 minutes
- raw calendar descriptions are not stored in Mood Context
