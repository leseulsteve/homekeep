# Homekeep Voice System

This document defines how Homekeep should speak to users. It is a product and
design guide for future UI work, not an implementation spec yet.

Homekeep should not use random strings. It should use a structured voice system:
clear message intent, Mood Context tone rules, reusable copy families, slot-based
templates, and repetition control.

## Purpose

Homekeep helps people care for their home without turning tasks into guilt,
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
A small bundle is ready.
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

Homekeep should speak from a mutual-care point of view: the home is cared for,
and the home also helps care for the humans, pets, and plants inside it. This is
the main product goal, not a side theme. Keep it practical and environmental. Do
not make claims about a person's health, feelings, or mental state.

Voice refinement rules:

- Use `care` as an anchor verb.
- Use `Complete` only where the interface needs a clear action label; prefer
  warmer feedback such as `That helped` or `The home feels a little lighter`.
- Use `ready` carefully for invitations, such as `A small bundle is ready`, but
  do not overuse it across every state.
- Keep moods implicit. Do not say `Since you're tired`; say
  `Let's keep this light`.
- Use one main metaphor family: home, care, lightness, useful passes, fresh starts, and
  steady step.
- Avoid mixing in game, battle, productivity, fitness, or optimization
  metaphors.
- Let silence be part of the voice. Not every state needs a sentence; sometimes
  a chip, title, and button are enough.
- Use `we` rarely. It can feel cozy in small doses, but overuse can feel fake.

Approved voice refinements:

- Homekeep should treat the home as the emotional center of the app. The user is
  helping the home; the app is not grading the user.
- Homekeep treats the home as a reciprocal care environment: it can help protect
  quiet, comfort, plant care, pet routines, and household rhythm, while still
  avoiding medical, psychological, or productivity-coach language.
- Tone should stay consistent across screens: calm, practical, softly
  assistant-like, and never needy for attention.
- Variation should be deep enough to avoid repetition, but controlled enough
  that Homekeep still sounds like the same product every time.
- Use warmth most strongly at moments of transition: greeting, choosing a
  bundle, completing a Task, stopping, and choosing whether to do One more.
- Keep routine controls plain and stable. Buttons, chip labels, timers, and
  status labels should not become poetic.
- Use playful language only when it makes the Task feel more inviting or more
  memorable, especially in Task Bundle titles. Do not make every line playful.
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
They are a small sign of care returned by the home when care is flowing.
Keeps should always be framed as coming from the home as a whole, not from an
individual Home Assistant Area.

Keeps are the language of mutual care, not only Task completion. Humans care
for the home. Animals and pets can be cared for and can shape the home's care
rhythm. Plants can care for air, humidity, shade, beauty, and presence. Objects
and Home Assistant devices can carry part of the care, such as a washing
machine helping with laundry or a coffee machine making good coffee. Quiet-hour
and comfort routines can protect rest and household rhythm. The home itself can
contribute by keeping shelter, quiet, comfort, safety, and readiness steady.
Keeps can acknowledge all of this later, as care circulating through the home.

The home is the broker of Keeps. Home Assistant helps the home notice care by
providing local device, entity, Area, sensor, automation, and event signals.
Voice should keep the emotional agency with the home, not with Home Assistant.
Say `the home noticed care`, not `Home Assistant awarded points`.

Keeps language should feel:

- warm
- grateful
- reciprocal
- light
- non-competitive

Keeps language should not feel like:

- a scorecard
- a wage
- a task tax
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
- When explaining Home Assistant's role, use practical signal language: `Home
  Assistant helped notice this`, `the washer cycle was seen`, or `the purifier
  signal helped the home recognize air care`.
- Do not say `Home Assistant gave Keeps`, `Home Assistant paid out`, or
  `the device earned points`.
- For future plant, air, comfort, or routine care, prefer grounded copy such as
  `Fern helped the air today`, `Bedroom air stayed lighter`, `The purifier kept
  things steady`, `Watering helped the room breathe`, `The coffee helped the
  morning start kindly`, or `The home kept a little more comfort today`.
- For shared human/device care, use collaborative language such as `The washer
  carried part of this bundle` or `You and the washer moved laundry along`.
  Avoid making devices sound like employees, competitors, or score owners.
- Prefer Bundle Keeps or care-together language over bonus/currency language,
  such as `4 bundle Keeps`.
- Do not use hype language such as `maximum reward`.
- Do not use money-like mechanics such as wallets, shops, upgrades, or exchange
  rates.
- Explain the non-scarce Keeps model as abundance, not scoring: `Keeps are the
  home noticing care. They are not a currency. They do not run out.`
- Never imply one care source takes Keeps from another. More care sources means
  more care can be noticed.
- Make Keeps visually soft if represented with an icon or effect.
- Avoid coin, trophy, badge-heavy, or scoreboard-like visual metaphors.
- Make the no-loss rule clear in the design: users never lose Keeps by stopping,
  skipping, snoozing, or ending.
- Use Keeps to help tiny Tasks feel like they count.
- Let Home Health say where care helps and Keeps say care happened. They should
  support each other, not compete for attention.
- Treat care source language as important as Area language. `Where care helped`
  and `who or what carried care` are both central to Homekeep's voice.
- Name source care clearly when useful: a human changed a filter, a litter
  routine cared for a pet, a purifier helped the air, a washer carried laundry,
  a coffee machine made the morning kinder.
- Keeps totals by care source can be proudly displayed in reflection surfaces:
  humans, pets, plants, devices, air, comfort, quiet routines, and other
  contributors. Use language of appreciation, not ranking.
- Keeps may support proud reflection later, such as `The home was cared for from
  many sides this week`, but not a leaderboard or total-chasing surface.

Contribution voice:

- Keep `Task` as the individual item.
- Use `Contribution` as the user-facing frame for a suggested or completed Task
  Bundle.
- Contribution copy should feel like invitation, fit, appreciation, and shared
  care. Avoid duty, debt, pressure, productivity, or moral language.
- Do not imply the user owes the home a Contribution.
- Do not imply the home is disappointed when a person stops, skips, snoozes, or
  chooses not to continue.
- Humans, animals, pets, plants, objects, devices, routines, home systems, and
  the home itself can contribute when there is a meaningful care signal.
- Use `Contribution` where it helps the bundle feel coherent. Keep visible Task
  lists clear so the user still knows what they are choosing.

Prefer:

```text
This contribution fits the moment.
```

```text
A small kitchen contribution is ready.
```

```text
Adjust the Tasks before starting.
```

```text
The washer carried part of this contribution.
```

```text
The home kept things quiet overnight.
```

Avoid:

```text
You need to contribute more.
```

```text
Contribution required.
```

```text
You failed to contribute today.
```

```text
The home is waiting on you.
```

Area Health contribution voice:

- Area Health naturally drifts down as care gets stale. Say this like a rhythm,
  not a failure.
- Proudly name who or what helped when useful: humans, pets, plants, devices,
  air, comfort, and routines.
- Separate appreciation from the next action. `Helped lately` should feel
  proud; `Could help next` should feel practical.
- Avoid winner/loser language between contributors.
- Avoid implying that a contributor failed because an Area still needs care.

Prefer:

```text
The kitchen drifted down, but it was cared for from many sides.
Coffee helped the morning. The purifier kept air moving. You cleared dishes.
Counters would help most next.
```

```text
You and the washer carried this room this week.
```

Avoid:

```text
Washer contributed more than you.
Kitchen lost health because nobody kept up.
Fern only added 1 Keep.
```

Right Now contribution voice:

- Right Now should sound like a human invitation to join the home's care flow,
  not a command to clear tasks.
- Speak to contribution, fit, and care. Avoid productivity, assignment, or work
  queue language.
- Let Mood, Time, and Area feel like ways to shape how the person can contribute
  now.
- End-state copy should say what the human added to the home.

Prefer:

```text
Something small you can add right now.
```

```text
This helps you join what the home already has going.
```

```text
You added care to the kitchen today.
```

Avoid:

```text
Start your task queue.
```

```text
Complete these tasks to improve your score.
```

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
sparingly. Homekeep may say things like `I found a small bundle` when it makes
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
- offer a Bonus Task
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
A small bundle might fit right now.
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
There is a small bundle ready when you are.
```

### Focused

Use direct, concise, momentum-oriented language.

Good qualities:

- crisp
- clear
- efficient

Example tone:

```text
This kitchen bundle fits the next 10 minutes.
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
There is a good bundle ready to knock out.
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
- Suggested Task Session framing
- Recommendation reason summary
- Primary action label
- Context adjustment prompt
- Active Task Session progress
- Completion acknowledgement
- Skip acknowledgement
- Snooze acknowledgement
- Done for now ending
- Bonus Task offer
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
Good evening. A quick kitchen bundle could fit 10 minutes.
Let's keep this light. The entryway lift is small and useful.
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

The Ready Now greeting should be ambient first, then the suggested Task Session can
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
The kitchen bundle fits about 10 minutes.
Start gently
```

This keeps the first moment feeling like a voice assistant rather than a task
manager yelling the next task.

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

Stopping after a planned Task Session should feel successful, not like quitting.

Good ending lines:

```text
That counts.
Good stopping point.
Enough for now is still progress.
Nice. The home got a little lighter.
```

Avoid:

```text
Only one task completed.
You still have overdue tasks.
Don't stop now.
```

## Bonus Task Voice

Bonus Tasks should feel optional and positive.

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
You can still add a task or plan something for later.
```

Avoid:

```text
No data.
No tasks found.
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
