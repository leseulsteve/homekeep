# Homekeep Voice System

This document defines how Homekeep should speak to users. It is a product and
design guide for future UI work, not an implementation spec yet.

Homekeep should not use random strings. It should use a structured voice system:
clear message intent, Mood Context tone rules, reusable copy families, slot-based
templates, and repetition control.

## Purpose

Homekeep helps people care for their home without turning chores into guilt,
pressure, or a giant overdue list.

The voice should make the app feel:

- calm
- useful
- present
- lightly personal
- practical
- non-punitive
- easy to correct

The main goal is care for the home. Homekeep should prefer household and care
language over productivity language.

Prefer:

```text
The kitchen gets a little lighter.
This helps the entryway feel ready.
A small reset is ready.
```

Avoid:

```text
Task completed.
Productivity increased.
You completed 3 items.
```

Homekeep should talk about the home being cared for, not the user being
optimized.

Homekeep's voice should act like a care companion for the home, not a coach for
the person.

Voice refinement rules:

- Use `care` as an anchor verb.
- Use `Complete` only where the interface needs a clear action label; prefer
  warmer feedback such as `That helped` or `The home feels a little lighter`.
- Use `ready` carefully for invitations, such as `A small reset is ready`, but
  do not overuse it across every state.
- Keep moods implicit. Do not say `Since you're tired`; say
  `Let's keep this light`.
- Use one main metaphor family: home, care, lightness, reset, fresh start, and
  steady step.
- Avoid mixing in game, battle, productivity, fitness, or optimization
  metaphors.
- Let silence be part of the voice. Not every state needs a sentence; sometimes
  a chip, title, and button are enough.
- Use `we` rarely. It can feel cozy in small doses, but overuse can feel fake.

Approved voice refinements:

- Homekeep should treat the home as the emotional center of the app. The user is
  helping the home; the app is not grading the user.
- Tone should stay consistent across screens: calm, practical, softly
  assistant-like, and never needy for attention.
- Variation should be deep enough to avoid repetition, but controlled enough
  that Homekeep still sounds like the same product every time.
- Use warmth most strongly at moments of transition: greeting, choosing a
  bundle, completing a Chore, stopping, and choosing whether to do One more.
- Keep routine controls plain and stable. Buttons, chip labels, timers, and
  status labels should not become poetic.
- Use playful language only when it makes the Chore feel more inviting or more
  memorable, especially in Chore Bundle titles. Do not make every line playful.
- Use encouragement to make care feel possible, not to push the user into doing
  more.
- Homekeep may gently nudge toward what the home needs, but that nudge should
  feel like a respectful care bias, not pressure. Explain the home's need
  softly and keep the user in control.
- Homekeep is gently opinionated, never coercive. It may stretch the suggestion
  toward meaningful care, but never shove the user past their stated capacity.
- When Homekeep nudges, the reason should be honest and calm. Prefer language
  like `This helps the kitchen most right now` over urgency, debt, warning, or
  guilt language.
- `Done for now` must always sound complete and successful, even when more care
  remains possible.
- Let Done for now sound complete and successful even when the home still has
  future care needs.
- Prefer short sentence-level personality over mascot-like behavior.
- When copy is uncertain, choose the quieter version.

Keeps should follow the same principle. Keeps are not productivity points.
They are a small sign of care returned by the home when it is cared for.
Keeps should always be framed as coming from the home as a whole, not from an
individual Home Assistant Area.

Keeps language should feel:

- warm
- grateful
- reciprocal
- light
- non-competitive

Keeps language should not feel like:

- a scorecard
- a wage
- a chore tax
- an arcade currency
- a ranking system

Keeps copy and presentation rules:

- Use `Keeps` sparingly in prose.
- Show values like `8 Keeps` clearly, without a plus sign when the value is
  always positive, but do not over-explain them every time.
- Pair Keeps with care language.
- Avoid transactional language such as `earn`, `earned`, `spend`, `bank`, or
  `redeem`.
- Prefer quiet reciprocal language, such as `The home gives a little back`.
- Prefer full-reset or care-together language over bonus/currency language,
  such as `4 Keeps for the full reset`.
- Do not use hype language such as `maximum reward`.
- Do not use money-like mechanics such as wallets, shops, upgrades, or exchange
  rates.
- Make Keeps visually soft if represented with an icon or effect.
- Avoid coin, trophy, badge-heavy, or scoreboard-like visual metaphors.
- Make the no-loss rule clear in the design: users never lose Keeps by stopping,
  skipping, snoozing, or ending.
- Use Keeps to help tiny Chores feel like they count.
- Let Home Health say where care helps and Keeps say care happened. They should
  support each other, not compete for attention.
- Keeps may support quiet reflection later, such as `You helped the kitchen
  feel lighter this week`, but not a leaderboard or total-chasing surface.

The voice should not feel:

- robotic
- random
- scolding
- falsely cheerful
- diagnostic
- overly intimate
- chatty
- cute for its own sake
- like a productivity coach yelling about optimization

## Tone Calibration

Homekeep should be warm, varied, and quiet by default.

Delight should come from feeling understood, seeing useful progress, and having
clear next actions. It should not come from constant jokes, flashy language, or
over-personalized commentary.

Use this rule:

```text
Helpful first. Warm second. Playful only as seasoning.
```

The app should avoid:

- exclamation-heavy copy
- repeated quips
- too many changing phrases in one screen
- multiple playful elements competing at once
- copy that tries to sound like a human friend too often
- reward language that feels like a casino, arcade, or scoreboard

The app should prefer:

- short phrases
- stable labels
- varied phrasing within a controlled copy family
- one warm sentence at a time
- practical wording
- calm transitions
- small moments of delight after action, not before every action

If a screen already has a mood-aware greeting, the rest of the screen should be
quieter. If a completion reward has motion or Keeps feedback, the copy should
stay brief.

Varied does not mean random. Variation should come from message intent, Mood
Context, state, and recent-copy avoidance. The same screen should not feel
mechanically repetitive, but it also should not reshuffle every label on every
render.

First-person language is allowed for assistant-like moments, but should be used
sparingly. Homekeep may say things like `I found a small reset` when it makes
the interaction feel clear and helpful. Prefer neutral phrasing when repeated
first-person copy would feel chatty.

## Core Rule

Separate message intent from wording.

Every user-facing text moment should first answer:

```text
What job is this message doing?
```

Then Homekeep can choose wording that fits the user's Mood Context and the
current workflow.

## Message Intents

Homekeep should organize user-facing copy by intent, not by screen alone.

Primary intents:

- greet
- orient
- reassure
- explain recommendation
- invite action
- guide active session progress
- acknowledge completion
- support skipping or snoozing
- make stopping feel successful
- offer a Bonus Chore
- explain empty state
- explain stale or expired state
- recover from error
- confirm user correction

Each intent should have a small copy family with tone variants for Mood Context.

## Mood Context As Tone

Mood Context should change how Homekeep speaks, not what Homekeep claims about
the user.

Good:

```text
A small reset might fit right now.
```

Avoid:

```text
You seem overwhelmed.
```

Mood Context should be user-correctable and lightweight. It must not make
medical, mental-health, or diagnostic claims.

## Tone Rules

### Calm

Use steady, spacious, reassuring language.

Good qualities:

- low pressure
- simple confidence
- quiet usefulness

Example tone:

```text
There is a small reset ready when you are.
```

### Focused

Use direct, concise, momentum-oriented language.

Good qualities:

- crisp
- clear
- efficient

Example tone:

```text
This kitchen reset fits the next 10 minutes.
```

### Tired

Use gentle, low-effort, permission-giving language.

Good qualities:

- small scope
- no pressure
- explicit permission to stop

Example tone:

```text
One small thing is enough to count.
```

### Overwhelmed

Use grounding, simplified, one-step-at-a-time language.

Good qualities:

- reduce choices
- avoid urgency
- make the next action obvious

Example tone:

```text
Just one step. I found something small and useful.
```

### Energized

Use lively, confident, action-ready language.

Good qualities:

- upbeat
- practical
- momentum without hype
- still restrained

Example tone:

```text
There is a good reset ready to knock out.
```

### Unknown Or Auto

Use neutral, warm, easy-to-steer language.

Good qualities:

- welcoming
- flexible
- not presumptive

Example tone:

```text
I found a useful place to start.
```

## Copy Families

Homekeep should maintain separate copy families for each major workflow moment.
Do not create one global bucket of interchangeable strings.

Recommended copy families:

- Ready Now greeting
- Suggested Chore Session framing
- Recommendation reason summary
- Primary action label
- Context adjustment prompt
- Active Chore Session progress
- Completion acknowledgement
- Skip acknowledgement
- Snooze acknowledgement
- Done for now ending
- Bonus Chore offer
- Empty state
- Expired Scheduled-Suggestion state
- Error recovery
- Settings explanation

Each family should include:

- intent
- tone rules
- allowed slots
- examples by Mood Context
- prohibited wording

## Slot-Based Templates

Homekeep should use slot-based templates instead of fully random sentences.

Slots keep the facts stable while allowing tone to vary.

Example template:

```text
{greeting} {session_summary} could fit {time_budget}.
```

Possible rendered lines:

```text
Good evening. A quick kitchen reset could fit 10 minutes.
Let's keep this light. The entryway reset is small and useful.
One steady step. The bathroom refresh fits your current energy.
```

Useful slots:

- `{time_of_day}`
- `{area_name}`
- `{session_title}`
- `{time_budget}`
- `{energy_level}`
- `{goal}`
- `{projected_impact}`
- `{chore_count}`
- `{next_action}`
- `{expires_at}`

Slot values must be truthful and available from Homekeep state or service
responses. The voice system must not invent context.

## Repetition Control

Variation should feel intentional, not random.

Homekeep should avoid showing the same prominent phrase too often. The future
implementation can control repetition by:

- tracking recent copy keys in frontend memory
- rotating deterministically by mood, day, session, or workflow state
- preferring unused copy variants within the current family
- falling back to neutral wording when the system lacks enough context

Do not randomize every render. Copy should not flicker or change while the user
is reading unless the state actually changes.

## Ready Now Greeting Strategy

The Ready Now greeting should be ambient first, then the suggested Chore Session can
be specific underneath.

Good structure:

```text
Ambient greeting.
Specific suggestion summary.
Primary action.
```

Example:

```text
Let's keep this light.
The kitchen reset fits about 10 minutes.
Start gently
```

This keeps the first moment feeling like a voice assistant rather than a task
manager yelling the next chore.

## Recommendation Reasons

Recommendation reasons should be short and explainable. They should answer why
this suggestion fits now without exposing scoring internals.

Good:

```text
Fits your time, helps the kitchen, and starts with a small win.
```

Avoid:

```text
Score 87.4 because staleness weight exceeded dismissal penalty.
```

Reason copy can mention:

- time fit
- energy fit
- Home Assistant Area
- visible impact
- overdue care
- Calendar Context only as minimized derived context
- user-selected goal

Reason copy should not mention:

- private calendar event text
- raw scoring details
- guilt language
- assumptions about mental health

## Completion And Stopping

"Done for now" should be emotionally first-class.

Stopping after a planned Chore Session should feel successful, not like quitting.

Good ending lines:

```text
That counts.
Good stopping point.
Enough for now is still progress.
Nice. The home got a little lighter.
```

Avoid:

```text
Only one chore completed.
You still have overdue tasks.
Don't stop now.
```

## Bonus Chore Voice

Bonus Chores should feel optional and positive.

Good:

```text
Want one tiny extra?
There is one small bonus if you still have momentum.
You can stop here, or take one more easy win.
```

The offer must make stopping feel equally valid.

## Empty States

Empty states should be calm and useful.

Good:

```text
Nothing needs attention right now.
You can still add a chore or plan something for later.
```

Avoid:

```text
No data.
No chores found.
```

## Error And Stale-State Voice

Errors should be clear, short, and recoverable.

Good:

```text
That plan is out of date. I can find a fresh one.
This session already ended. Let's return to Ready Now.
I could not start that suggestion. Let's find a fresh one.
```

Avoid:

```text
Invalid RecommendationSnapshot.
Session mutation failed.
```

Technical details can appear in diagnostics, not in the primary user flow.

## Prohibited Language

Homekeep must avoid:

- shame
- blame
- scolding
- failure framing
- medical or mental-health claims
- raw productivity pressure
- exaggerated celebration
- implying the user is dirty, lazy, irresponsible, or behind
- exposing private calendar details
- treating Home Health as a personal grade

## Future Implementation Notes

When this becomes a Codex implementation task, translate this document into:

- copy family data structures
- stable copy keys
- Mood Context selection rules
- slot rendering helpers
- repetition-control behavior
- tests for prohibited language
- tests for missing-slot fallbacks
- tests that user-facing copy does not expose private calendar text

The first implementation should start small:

1. Ready Now greeting family.
2. Primary action label family.
3. Recommendation reason framing.
4. Done for now ending family.
5. Error/stale-state family.

Broader copy families can follow after the app flow is working.
