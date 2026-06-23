# Homekeep App Design Brief

This is the human product and design document for the Homekeep app. It is the
place to decide how the app should feel, what each workflow should do, and what
we want the experience to be before translating the plan into Codex
implementation instructions.

Implementation details belong later. This document should stay readable by a
person who wants to understand the app, not only by an engineer preparing a
build pass.

## Core Recommendation

Plan the Homekeep dashboard around real household workflows, not around what
widgets can be shown.

Homekeep's primary interface should feel like a small Home Assistant app for
deciding and doing household care. The long-term canonical experience should be
a Homekeep sidebar app.

Lovelace is not part of the Homekeep UI implementation plan. Do not build,
restore, ship, or maintain Lovelace dashboard templates for Homekeep. Homekeep
may still expose Home Assistant sensors and To-do projections, but the user
experience should be designed and implemented as a native Homekeep app surface.

The recommended direction is:

- Add a Home Assistant sidebar entry for Homekeep.
- Build the main Homekeep surface as an app-like panel view, not in an iframe.
- Remove former dashboard examples from the MVP direction.
- Treat Lovelace as out of scope for Homekeep UI implementation.

This matches the product model: Homekeep storage is the source of truth, Home
Assistant To-do entities are projections, and the frontend should not become a
second source of interaction state.

## Product Principle

The dashboard should answer household questions in the order a person actually
has them:

```text
What should I do right now?
How is the home doing?
What is coming up?
What just happened?
What can I adjust?
```

The UI should avoid making the user confront a giant overdue list. It should
offer a small, explainable path into a Task Session, make stopping feel
successful, and keep tasks practical rather than punitive.

## Main Product Goal: Mutual Care

Homekeep's main goal is mutual care: the home and its inhabitants care for each
other.

The current MVP is about tasks, Home Health, Task Sessions, and practical
household readiness, but every design and implementation choice should point
toward this larger direction. The house should not only ask for care; it should
also help take care of its humans, pets, and plants through practical,
environmental, and routine-aware support.

Examples of this future direction:

- plant care that adapts to season, sunlight, weather, and missed watering
- pet care reminders that feel warm, ordinary, and reliable
- household comfort nudges for air quality, humidity, temperature, noise, and
  quiet hours
- human support that protects rest and stopping, such as `you have done enough
  for now`
- shared routines where the home helps keep the household rhythm gentle and
  visible

This should not become a wellness coach, medical system, psychological
diagnosis, or productivity optimizer. Homekeep should stay practical and
environmental: the house cares by making life lighter, calmer, safer, and easier
to maintain.

This is the source of the existing care-bias principle. Homekeep's quiet agenda
is not productivity; it is mutual care. Sometimes the app nudges the user to
care for the home. Sometimes it protects the user, pet, plant, or household
rhythm from being overextended.

Canonical mutual-care model:

```text
Care Source -> Care Contribution -> Keeps -> Area/Home Health context
```

Meaning:

- `Care Source`: who or what contributed care, such as a human, pet, plant,
  device, air/comfort system, quiet routine, or household rhythm
- `Care Contribution`: the concrete thing that happened, such as completing a
  Task, cleaner air, good coffee, protected quiet, watering, or a device cycle
- `Keeps`: the home noticing care as non-scarce recognition
- `Area/Home Health context`: where that care helped and what could help next

Broker model:

- The home is the broker of Keeps.
- Home Assistant is the local signal layer that helps Homekeep see care:
  entities, devices, Areas, sensors, automations, service calls, state changes,
  and events.
- Homekeep interprets those signals into care contributions.
- The home returns Keeps as recognition of care.
- Home Assistant should not be presented as the emotional giver of Keeps. It is
  the trusted integration fabric that lets the home notice care accurately.
- Homekeep should avoid pretending every Home Assistant event is care. A signal
  becomes a care contribution only when it maps to a meaningful household care
  outcome.

Keeps and Area Health have distinct jobs:

- Keeps show that care flowed through the home.
- Area Health shows where care helped, where care is naturally drifting down,
  and what would help next.
- Care contributions can be attributed to Areas and sources, but Keeps still
  come from the home as a whole.

Care sources are a first-class axis alongside Areas:

- Area care answers `where did care help?`
- Source care answers `who or what carried care?`
- A single contribution can belong to both, such as `Changed bedroom purifier
  filter`: Bedroom is the Area, and the human plus purifier are care sources.
- Pet care such as emptying litter, device care such as running a washer cycle,
  plant care such as watering, and comfort care such as good coffee should be
  visible as meaningful care, not treated as secondary to cleaning an Area.
- The UI should eventually let users inspect both views: care by Area and care
  by source.

Product review recommendations:

- Introduce mutual care gradually. The first UI expression should be felt in
  Right Now copy, completion feedback, and Area Health contribution language
  before Homekeep builds a full care-source ledger.
- Let Right Now carry the first human-facing expression: the human joins the
  home's care flow, contributes at a fitting scale, and sees what they added.
- Let Home Health carry the first area-facing expression: each Area can show
  `Helped lately` and `Could help next` so natural health decline does not erase
  pride in contribution.
- Let Keeps remain simple in active sessions. Show Task Keeps and Bundle
  Keeps now; save proud care-source totals for later reflection surfaces.
- Only attribute device, plant, pet, or routine care when the signal is
  meaningful. Do not invent contribution just because a Home Assistant entity
  exists.
- Keep the emotional model bigger than tasks, but keep MVP implementation
  narrower than the emotional model. Tasks are the first concrete expression of
  mutual care, not the whole destination.
- Avoid over-explaining Keeps in the main workflow. The user should feel the
  care loop first and inspect the model later.
- Protect the non-scarce model. A contributor's Keeps never reduce another
  contributor's Keeps, and contribution totals should never become a ranking.
- Protect the two-axis model. Do not collapse all care into Area Health, and do
  not collapse all care into source totals. Homekeep needs both: places that
  need care and contributors that carry care.
- Protect the broker model. The home returns Keeps; Home Assistant helps provide
  the evidence; Homekeep interprets that evidence into care.

## User-Facing Text Direction

Homekeep should use a structured voice system, not random strings. Prominent
copy should be organized by message intent, adjusted to Mood Context, and drawn
from copy families with clear tone rules and repetition control.

See `docs/product/HOMEKEEP_VOICE_SYSTEM.md`.

## Implementation Boundary

The Homekeep UI plan must not include:

- Lovelace dashboard YAML
- Lovelace helper/script bridge flows
- Lovelace dashboard examples
- Lovelace-specific tests
- Lovelace-specific product acceptance criteria

If users want to place Homekeep entities on their own Home Assistant dashboards,
that is supported only through normal Home Assistant entities and projections.
It is not a Homekeep-authored dashboard surface.

## How We Will Design This

Before implementing the Homekeep app, review each workflow with Steve and
record the chosen product behavior in this document.

Use one design question at a time. Each answer should tighten the app's
behavior, information hierarchy, interaction model, and visual direction before
implementation begins.

The workflow review order is:

1. Ready Now / Ready-Now Mode
2. Smart Task List
3. Active Task Session
4. Optional Task continuation and session completion
5. Home Health and Areas
6. Plan / Scheduled Tasks
7. Add Task
8. Activity
9. Settings and diagnostics

For each workflow, document the human experience first:

- user intent
- first thing the user sees
- primary action
- secondary actions
- empty state
- loading state
- error or stale-state handling
- mobile priority
- desktop priority
- emotional tone
- what should feel effortless
- what should stay out of the way

Then, later, translate the workflow into implementation instructions:

- data dependencies
- service calls
- temporary UI state
- validation and stale-state rules
- tests or source checks
- acceptance criteria

Do not implement the frontend until the Ready Now / Ready-Now Mode, Smart Task
List, Active Task Session, and optional Task continuation workflows have
approved MVP behavior.

## Questions To Answer Before Implementation

The design review should answer these questions before code starts:

- What is the first screen a person sees when they open Homekeep?
- Does Homekeep lead with a recommended session, a readiness launcher, or both?
- How much explanation should a recommendation show before the user asks for
  more?
- During an active Task Session, is the experience guided one step at a time,
  or shown as a compact list?
- How should stopping after a session feel successful?
- How visible should Home Health be on the main screen?
- Should Home Health be a score, a status, or mostly area-level language?
- Where should Plan / Scheduled Tasks live in the navigation?
- How lightweight should Add Task be in the first app version?
- What belongs in Settings for MVP, and what can wait?

## Later: Codex Implementation Instructions

Before code starts, the app implementation pass must have:

- verified the supported Home Assistant sidebar/custom panel approach against
  the installed Home Assistant package or official developer docs
- confirmed that the app is not iframe-embedded
- identified how the frontend calls Homekeep services and receives action
  responses
- identified how the frontend refreshes entity/projection state after service
  calls
- documented how temporary UI identifiers such as `snapshot_id`,
  `recommendation_id`, `session_id`, and `session_item_id` are stored in the
  app during a flow
- documented how stale responses, expired RecommendationSnapshots, and ended
  sessions are handled in the UI
- added focused tests or source checks for the selected frontend registration
  approach

## Implementation Note: Mocked Ready Now Prototype

The first frontend implementation registers Homekeep as a Home Assistant
sidebar custom panel using a local JavaScript module. It is not iframe-embedded.
The verified Home Assistant approach is:

```text
hass.http.async_register_static_paths(...)
frontend.async_register_built_in_panel(component_name="custom", ...)
_panel_custom.module_url = /homekeep_static/homekeep-panel.js
_panel_custom.embed_iframe = false
```

This was checked against official Home Assistant source for
`frontend.async_register_built_in_panel`, `panel_custom`, and
`http.StaticPathConfig` on 2026-06-22 because the local Python environment did
not include an importable `homeassistant` package.

Current prototype boundary:

- mocked Ready Now suggestion data
- mocked context chips and fuzzy/refining state
- mocked Task Bundle shuffle and chip-driven suggestion changes
- mocked active Task Session state
- mocked timer, completion feedback, final summary, and inline optional Tasks
- local temporary UI state only

Not wired yet:

- `homekeep.generate_smart_chore_list`
- `homekeep.start_recommendation`
- `homekeep.complete_chore`
- `homekeep.skip_chore`
- `homekeep.snooze_chore`
- `homekeep.end_session`
- `homekeep.accept_bonus_chore`
- stale RecommendationSnapshot or ended-session recovery
- entity/projection refresh after service calls

Future service wiring should keep the same data path:

```text
visible context chips
-> homekeep.generate_smart_chore_list
-> user confirms one recommendation
-> homekeep.start_recommendation
-> materialized session_item_id values from the action response
-> complete / skip / end-session service calls
```

Temporary identifiers such as `snapshot_id`, `recommendation_id`,
`session_id`, and `session_item_id` belong in frontend memory for the active
flow. Homekeep storage remains the source of truth.

## Planning Status Before Live Test

The Homekeep app/dashboard is not fully planned yet.

The current plan is complete enough to live-test the mocked Ready Now slice and
evaluate whether the main loop feels right:

- Ready Now / Ready-Now Mode
- Mood-aware greeting and context chips
- Smart Task List presentation
- suggested Task Bundle confirmation
- mocked active Task Session behavior
- inline optional Tasks after planned session completion
- final session summary
- Homekeep Voice System direction
- Home Assistant sidebar app direction

The live test should be treated as a product-feel review of this narrow slice,
not as validation of the full Homekeep app.

The following areas still need planning or deeper review before implementation:

- Home Health and Area Health as a full app view
- Plan / Scheduled Tasks
- Add Task UX
- Activity and recent history
- Settings and diagnostics
- full navigation model
- real service-wired stale state, expired RecommendationSnapshot, and ended
  session recovery
- entity/projection refresh after service calls

Do not implement those later areas from inference during the Ready Now live
test. Record observations, tune the mock when useful, and continue product
planning after the Ready Now flow is reviewed.

## Why An App View Fits The Product

Homekeep's core interaction depends on short-lived service response data:

- `snapshot_id`
- `recommendation_id`
- `session_id`
- `session_item_id`
- planned Task surfacing state
- optional Task state

A Homekeep app view can own the temporary UI state while leaving durable state
inside Homekeep storage. That makes the main workflow clearer:

```text
choose context
-> generate Smart Task List
-> inspect reasons and Projected Impact
-> start a Task Session
-> complete / skip
-> optional Tasks appear inline after the planned bundle is complete
-> final session summary
```

## Primary Workflows

This section is the working review log. Each workflow starts with a draft
direction and should be updated as Steve answers design questions.

### Ready-Now Mode

Status: under review.

The main screen should make Ready-Now Mode immediate. Use a hybrid layout:
Mood-aware greeting first, then the best suggested Task Session, with an
"I'm ready" customization path available without making the screen feel busy.

Decision: Right Now should balance the home's needs with the user's current
predisposition.

Homekeep should have a respectful internal tension: the home may need care, and
the user may have limited time, capacity, mood, or attention. The app should
honor explicit user context, but it should also have a quiet care bias toward
tasks that meaningfully help the home when they still fit the moment. This
gives Homekeep a small agenda: help the home get cared for. That agenda must be
transparent in recommendation reasons, easy to correct through context chips,
and never guilt-based, punitive, or manipulative.

Good behavior:

- prefer a meaningful stale/high-impact Task when it still fits the user's
  stated time and inferred capacity
- offer a tiny/light variant when the home needs care but the user seems low
  capacity
- explain the nudge softly, such as `This helps the kitchen most right now`
- let explicit user choices override inference

Avoid:

- hiding the reason for a recommendation
- pushing hard against the user's explicit constraints
- framing the home need as the user's failure
- using guilt, streaks, penalties, or alarm language to force action

Important Right Now tension rules:

1. Use `stretch, do not shove`. Homekeep may suggest one slightly more
   meaningful Task than the user might choose alone, but it should stay inside
   the user's stated time, inferred capacity, and context.
2. Offer a softer variant of the real need. If the home needs care but the user
   is low capacity, suggest a tiny or light version of the helpful Task rather
   than the full catch-up.
3. Make the nudge visible in the reason. Explain gently why this suggestion is
   a little more useful than the easiest option.
4. Keep escape hatches beside every nudge. Context chips, randomize, remove,
   restore, skip, and clean session exit make the care bias respectful.
5. Do not hide urgent stale Tasks just because the user's current context is
   light. Keep meaningful care in the candidate pool, but resize the suggested
   variant to fit the moment.
6. Use any care-debt concept internally only. User-facing copy must avoid debt,
   failure, backlog, or burden language.
7. Never use guilt gradients. Avoid red danger treatment, escalating warning
   language, streak pressure, or punitive UI unless a future true safety/urgent
   state is explicitly designed.
8. Let user correction teach tone and fit, not obedience. Repeated removals or
   dismissals in a context should lead to lighter variants or better timing, not
   permanent suppression of useful care.
9. A Task Bundle may include one honest `the home needs this` item when it is
   small enough to fit, balanced by easier Tasks that match the user's current
   predisposition.
10. Stop cleanly. Ending a session must always feel successful, even when
    Homekeep can still recommend more.

Short design principle:

```text
Homekeep is gently opinionated, never coercive.
```

Suggested Task Engine direction:

- Use a two-stage engine: hard constraints first, then scoring.
- Keep `home need` and `user fit` separate internally so the app can balance
  Home Health/Staleness against the user's current readiness.
- Allow a bounded care nudge toward useful home needs, but cap it so it never
  overrides explicit Time, Area, or Mood choices.
- Prefer small Task Variants over rejecting useful care when the full Task is
  too much for the moment.
- Exclude Tasks just removed, skipped, dismissed, snoozed, or completed in the
  current flow.
- Make optional Tasks stricter than the main suggested bundle: smaller,
  better-fit, useful, and bounded.
- Explain one human reason, not the scoring math.
- Avoid repetitive bundles and incoherent mixed-area bundles.
- Keep shuffle stable within a family of good fits, not random.
- Learn conservatively from correction signals. Soften, resize, defer, or
  retime before suppressing useful care.
- Treat the time entered when creating a Task as a starting estimate, not the
  final truth. Homekeep should learn from real active-session duration and adapt
  the recommendation length to current Mood/Readiness, inferred Capacity, and
  recent session momentum.
- Use adaptive duration to resize care, not shame the user. If the full Task is
  too much for the moment, prefer a tiny/light Task Variant or shorter pass.

Decision: Right Now is the human contribution gateway into mutual care.

Right Now is not merely the task screen. It is the place where a human says,
`I am here, I can contribute now, what would help?`

The home has ongoing care from plants, pets, devices, routines, time, and prior
human work. Right Now is specifically for the human who wants to join that care
flow at a scale that fits this moment.

Implications:

- the greeting should feel like an invitation to contribute, not a command
- Time, Mood, and Area are contribution-fit controls, not productivity filters
- the suggested Task Bundle is an invitation to join the home's care flow, not
  an assignment
- the recommendation should show how the human contribution fits beside
  existing care sources when useful
- the primary action should feel like accepting a care moment, not starting a
  work queue
- active session feedback should proudly show the person's contribution
- the ending summary should say what the human added to the home, not only what
  they completed
- Right Now should connect back to Area Health contribution, showing how this
  person is joining the humans, pets, plants, devices, and routines that already
  help the home

Useful design phrase:

```text
Right Now helps a person join the home's care flow at the scale that fits this
moment.
```

Decision: Ready Now layout order should be:

```text
Greeting
Context chips
Suggested Task Bundle
Compact Home Health / Area Health lines inside the bundle
```

This lets the screen start human, gives the user quick control over context,
then presents the best suggested Task Bundle with health context attached to
the recommendation.

Decision: When a Task Session is active, Ready Now should become the active
session view.

The user should not have to navigate to a separate screen to continue a session.
While a Task Session is active, Ready Now should show the active session state.
After the session is complete, Ready Now should return to the normal greeting,
context chips, and suggested Task Bundle layout.

Decision: Visually, Homekeep should show only one active Task Session at a
time.

The UI should not present multiple active sessions, stacked session cards, or a
session switcher in the Ready Now experience. If a session is active, Ready Now is about
that session until it ends. This applies to the mocked prototype and should
remain the default expectation for the real app unless a later workflow
explicitly introduces multi-session behavior.

Decision: If Homekeep cannot generate a suggested Task Bundle, Ready Now should
show a gentle no-suggestion state.

The user should keep the same context chips visible so they can adjust time,
mood, or area. Do not show Energy or Goal as top-level chips for the second
Right Now live test; Capacity and Goal should be inferred from Mood Context and
other context. If applicable, the normal shuffle/regenerate affordance can
remain available, but the main recovery path should be changing visible context.

Capacity is the internal replacement for a visible Energy control. It describes
what a Task Bundle can reasonably ask of the user, not how the user feels.
Use `auto`, `low`, `steady`, `mobile`, and `strong`.

Mood maps to Capacity by default:

- `auto -> auto`
- `low` or `quiet -> low`
- `focused -> steady`
- `restless -> mobile`
- `ready -> strong`

Capacity should be evaluated against effort, movement, setup friction,
duration, and interruption tolerance. Low Capacity should prefer short,
low-effort, low-transition Tasks. Mobile Capacity can include walking between
rooms, light carrying, and visible lift work. Strong Capacity can include
heavier, longer, overdue, or more physically involved Tasks.

Mood also maps to the internal Goal by default:

- `auto -> visible lift`
- `low -> quick wins`
- `quiet -> fresh start`
- `focused -> overdue care`
- `restless -> visible lift`
- `ready -> overdue care`

Example:

```text
Nothing fits this moment yet.
Try changing the time, mood, or area.
```

Decision: The first mocked Ready Now prototype should include the full mocked
active-session flow after bundle confirmation.

The prototype should not stop at `bundle selected` with a placeholder. It should
let Steve evaluate the feeling of the complete Ready Now loop, even with synthetic
data.

Decision: The mocked live session should correspond to realistic live usage.

The mock should use synthetic data, but the interaction should feel like the
real app flow a household would use. Avoid placeholder-only states, fake actions
that make the session impossible to judge, or flows that would not exist in
production.

Mocked Ready Now prototype flow:

```text
Ready Now suggestion
-> confirm Task Bundle
-> mocked active Task Session
-> start Tasks in any order
-> complete Tasks
-> completed Tasks stay visible with a soft done state
-> optional Tasks appear inline in the active session list
-> final session summary
-> return to Ready Now
```

The mocked flow should include visible Keeps, Task-level start/complete
actions, the active Task timer state, the small completion effect, and the
inline optional Task continuation. Backend service wiring can come later.

Mock behavior should preserve real usage expectations:

- bundle confirmation starts a plausible active session state
- only one Task can be ongoing at a time
- starting a Task changes its state to ongoing
- completing a Task keeps it visible as a near-normal Task row with a soft
  congratulatory done state
- the timer appears only while a Task is ongoing
- completing the final planned Task adds a short list of optional Tasks
  directly into the active session list
- optional Tasks can be started, completed, or skipped like other session
  Tasks
- disabled/no-op controls should be limited to features intentionally not wired
  in the first mock, such as backend redraw logic

Decision: The main shuffle button in the first mocked Ready Now prototype should
swap to another mocked Task Bundle.

The shuffle button should not be a dead control in the Ready Now mock. It should
visually exercise the real usage expectation by changing the suggested bundle to
a second plausible mocked option. The mock does not need backend recommendation
logic, but it should make the layout, fuzzy/refining state, and replacement
bundle feel testable.

Decision: Context chip changes in the first mocked Ready Now prototype should
change the mocked suggestion.

The chips should not be decorative. When the user changes time, mood, or area,
the mock should show the inline selector, run the fuzzy/refining state, and
then swap to a plausible mocked suggestion that reflects the changed context.

Decision: The first mocked Ready Now prototype should include `4-5` mocked Task
Bundle variants.

The variants should cover different time, inferred Capacity, mood, and
area contexts so shuffle and chip changes feel meaningful. They should use
synthetic household data only.

Decision: Always use realistic synthetic mocks for UI prototypes.

Do not use generic placeholders such as `Area 1`, `Task 1`, or fake lorem ipsum
copy. Mocked data should feel like plausible household care while remaining
synthetic and privacy-safe.

Example mock Areas:

- `Kitchen`
- `Entryway`
- `Bathroom`
- `Laundry`
- `Living room`

Decision: In the mocked Ready Now prototype, completing the final planned Task
should add a short list of optional Tasks directly into the active session
list.

The optional Tasks can use synthetic data, but they should be selected from a
larger candidate pool using Recommendation Engine-like scoring. The intended
flow is: the planned bundle feels complete, completed rows stay visible, and a
few small additional Tasks appear inline without a separate `One more`
reveal/accept step. The mock does not need real backend redraw or service
eligibility logic yet.

Mock data decisions:

- Use `4-5` Task Bundle variants.
- Use mostly single-area bundles so Area Health impact is easy to understand.
- Include one multi-area bundle to test bundle-level area display and mixed-area
  behavior.
- Use realistic synthetic areas: `Kitchen`, `Entryway`, `Bathroom`, `Laundry`,
  and `Living room`.
- Use realistic synthetic tasks such as `Clear dishes`, `Wipe counters`,
  `Take out compost`, `Shake entry rug`, `Clear bathroom sink`, `Start a small
  laundry load`, and `Clear coffee table`.
- Include varied bundle sizes: one short `5 min` bundle, a couple of `10-15
  min` bundles, and one fuller `20-25 min` bundle.
- Include varied Mood and Capacity contexts: auto, low, quiet, focused, restless,
  and ready.
- Include Keeps per Task and visible Bundle Keeps opportunities.
- Include Home Health and Area Health mock numbers that line up with the
  suggested bundle, such as `Home 74`, `Kitchen 48`, and `Kitchen 24`.
- Include one no-suggestion mock state.
- Include `2-3` mocked optional Tasks with Keeps.
- Choose mocked optional Tasks through stricter Recommendation Engine-like
  scoring rather than a fixed visible list.
- Keep all data synthetic and privacy-safe.
- Avoid generic labels, lorem ipsum, fake entity IDs, private household details,
  and real calendar text.

Mock interaction decisions:

- Main shuffle swaps to a different mocked Task Bundle.
- Context chip changes swap to a plausible mocked Task Bundle after the
  fuzzy/refining state.
- Bundle confirmation starts the mocked active session.
- The mocked active session uses real-feeling Task states: ready, ongoing,
  completed.
- Only one Task can be ongoing at a time.
- The timer appears only while a Task is ongoing.
- Completed Tasks stay visible as near-normal Task rows with a soft
  congratulatory done state.
- Completing the final planned Task appends optional Tasks inline.
- The final summary can return to Ready Now after the optional list is handled.

The visual model should feel closer to a modern voice assistant surface than to
a conventional dashboard. The first screen should feel conversational, ambient,
and responsive, while still being useful as a touch interface.

The first screen should include a substantial greeting set that adapts to the
user's current Mood Context. The greeting should make Homekeep feel aware of
the user's readiness without making medical, mental-health, or diagnostic
claims.

Greeting goals:

- make the first screen feel human and current
- reflect the user's selected or inferred Mood Context
- gently frame the kind of Task Session that may fit the moment
- keep the user in control by making mood easy to override
- avoid guilt, pressure, or exaggerated cheerfulness
- use a substantial set of possible greeting strings rather than a single
  repeated phrase

Voice-assistant design qualities:

- centered, conversational first impression
- large readable greeting
- clear listening/ready state
- soft motion or ambient state when available
- minimal chrome
- strong single primary action
- secondary controls revealed only when useful
- mobile-first, thumb-friendly controls
- restrained delight
- not a grid of status cards
- not a generic admin dashboard
- not chatty or constantly animated

```text
I'm ready
-> choose time
-> optionally accept or override Mood: Auto
-> infer Capacity from Mood and context
-> infer Goal from Mood and context
-> generate Smart Task List
-> start a Task Bundle or single Task
```

The UI should show only a few recommendations and make the reason for each one
clear without becoming a report.

Suggested Task Session display:

- Show the collapsed version by default.
- The collapsed view should include an evocative Task Bundle title, estimated
  time, compact context, short reason, primary bundle-selection action, shuffle
  action, and expand affordance.
- Do not show the full Task Bundle contents by default. Let the user expand
  when they want details.
- Expanded details should open inline below the suggestion, not in a separate
  detail view. The user should remain anchored on Ready Now.
- Expanded details should include Projected Impact by default. The impact
  system should feel simple, encouraging, and lightly gamified, while staying
  positive and non-punitive.
- Expanded details should show only the selected suggested bundle. Do not show
  alternate suggestions underneath. The shuffle action is how the user asks for
  another suggestion.
- Use one shuffle button only. It should remain visible in a consistent
  location whether the suggestion is collapsed or expanded, and it should never
  be duplicated.
- The main action on the suggested Task Session should confirm the bundle
  selection. It should not imply that the user has started doing the first
  Task yet.
- After the user confirms a bundle, Homekeep should move into an active Task
  Session where the user can start or complete individual Tasks in the order
  they choose.
- Expanded Task Bundle details should show each Task with its estimated time.
  The time estimate should help the user trust the overall session fit without
  making the list feel dense or managerial.
- Expanded Task Bundle details should show the Keeps available for each Task.
  Keeps should be visible while suggesting bundles, not only after completion.
- Bundle Keeps should be shown at the bundle level, such as
  `4 bundle Keeps`.
- In the suggested bundle card, show Bundle Keeps before the visible Task list.
  This care-together signal is part of the offer and should be understood before
  the user scans the individual Tasks.
- Area display should be conditional. If all Tasks in the bundle share the
  same Home Assistant Area, show that area at the bundle level only. If the
  bundle spans multiple Home Assistant Areas, show the relevant area on each
  Task row so the user understands where each step happens.
- Expanded Task rows should include a small pre-start remove affordance. This
  should feel lightweight and optional, letting the user tune a suggestion
  before starting without turning the bundle into a full editor.

Pre-start edit direction:

- Keep remove visually secondary.
- Use icons with accessible labels.
- Do not make editing feel required before starting.
- Recalculate time and Projected Impact after edits.
- Keep the original recommendation recoverable through shuffle or visible
  context changes.
- Avoid allowing edits that break service/session validity.
- Removing a Task before starting should happen instantly with row-level
  restore, not a confirmation dialog. This keeps tuning fast and reversible
  without adding a duplicate temporary undo toast.
- Do not include per-Task swap in the MVP. Use the shuffle action when the user
  wants a different suggestion.
- By default, removing a Task before starting should affect only the current
  unsaved suggestion. It should not automatically train future recommendations.
- The UI may offer an optional explicit preference signal, such as
  `Suggest this less in short sessions`, when the user wants Homekeep to
  remember a context-specific pattern. This should be user-chosen, reversible,
  and phrased as a preference rather than a punishment.
- Do not show an undo toast when the removed Task remains visible with
  row-level restore. The row itself is the recovery path.
- Optional context-specific preference learning can come later in a separate,
  explicit preference surface if Homekeep can describe the context clearly.
- Preference examples may include `less in short sessions`, `less when Capacity
  is low`, `less for evening bundles`, or `less in this Home Assistant Area`.
  Do not offer a context-specific preference when the context would be vague or
  misleading.
- Do not rely on temporary toast state for reversibility when the removed row
  itself can stay visible and restorable.

Projected Impact direction:

- Make the benefit of a suggested Task Session easy to understand at a glance.
- Show impact as encouragement, not as a grade or judgment.
- Keep the display simple enough to scan quickly.
- Use positive motion, progress, or Keeps-like language where it helps the
  session feel rewarding.
- Prefer "this helps" language over "you are behind" language.
- Connect impact to Home Health, Area Health, or visible household benefit.
- Avoid complex scoring formulas in the UI.
- Avoid competitive, punitive, or streak-loss mechanics.
- Make small sessions feel worthwhile.

Possible impact treatments:

- area improvement, such as `Kitchen 24`
- Home Health improvement, such as `Home 7`
- compact projected gain, such as `Kitchen 24`
- friendly impact label, such as `Visible lift`, `Small win`, or
  `Big kitchen boost`
- soft celebration after completion when projected impact is realized

Chosen impact presentation:

- Use a combination of numbers and friendly labels.
- Numbers provide satisfying progress and explainability.
- Labels make the impact feel human and easy to choose.
- Pair concise metrics with plain-language benefit, such as
  `Kitchen 24 · Big kitchen boost`.
- Keep the presentation compact enough for mobile.

Task Bundle title direction:

- Titles should be evocative, memorable, and inviting.
- A user should be able to remember the title later.
- A user should feel that choosing the bundle is pleasant, not like accepting a
  punishment list.
- Titles should sound like a small household mission, lift, or useful moment,
  not a raw list of tasks.
- Titles must stay truthful to the bundle contents.
- Titles must avoid guilt, shame, or exaggerated hype.

Good title qualities:

- concrete
- short
- household-specific
- easy to say out loud
- memorable but restrained
- aligned with Mood Context where possible

Draft title examples:

- `Kitchen Lift`
- `Tiny Trash Run`
- `Countertop Comeback`
- `Entryway Fresh Start`
- `Laundry Launch`
- `Quiet Bathroom Refresh`
- `Five-Minute Floor Rescue`
- `Evening Lift`

Draft greeting directions:

- `auto`: neutral, welcoming, easy to steer
- `low`: gentle, permission-giving, small-scope
- `quiet`: steady, low-pressure, quietly capable
- `focused`: direct, crisp, momentum-oriented
- `restless`: visible, movement-friendly, still contained
- `ready`: action-ready, a little more ambitious, still practical

Example greeting pattern:

```text
Good evening. Want a small bundle that fits this moment?
```

The greeting should not replace the core action. It should frame the Ready Now
screen and help the user feel met before choosing or starting a Task Session.

Chosen direction:

- Ready Now uses a hybrid layout.
- Top: substantial Mood Context greeting.
- Middle: best suggested Task Session or helpful empty state.
- Primary action: confirm the suggested Task Bundle when available.
- Homekeep should auto-generate the best suggested Task Session when the app
  opens, using inferred or default context.
- Secondary action: "I'm ready" or equivalent customization path for changing
  time and mood before generating a Smart Task List.
- Include a light shuffle action that regenerates the Smart Task List using the
  current visible context. It should feel easy and low-pressure, not like rejecting
  Homekeep's recommendation.
- Visual style should evoke a modern voice assistant rather than a card-heavy
  dashboard.
- Bundle-selection action copy should come from a small set of string
  variations instead of one fixed label. The tone should be inviting and may
  adapt to Mood Context.
- Inferred/default context should be shown as compact chips with icons and
  colors, such as time, Mood Context, and Area. Chips should make the
  current context easy to scan and adjust without turning Ready Now into a form.
  Capacity and Goal remain inferred internal signals rather than top-level
  chips for the second Right Now live test.
- Tapping a context chip should open a small inline selector in place, not a
  full edit screen. The selector should have large enough touch targets, keep
  the user anchored on Ready Now, and refresh the suggestion after the value
  changes.
- When the user changes a chip, Homekeep should wait briefly before refreshing
  so the user can change another chip. This should feel like refining a search,
  not submitting a form.

Auto-generation behavior:

- Use safe inferred/default context when the user has not explicitly chosen
  time or mood.
- Make the inferred/default context visible enough to correct quickly.
- Do not make the user answer setup questions before seeing the first useful
  suggestion.
- Refresh the suggestion when the user changes time, mood, or relevant home
  context.
- Use a short debounce-style refresh after chip changes. During the wait and
  refresh, show a lightweight searching/refining state so the user understands
  Homekeep is finding a better fit.
- If no useful suggestion exists, show a calm empty state and a customization
  path rather than a blank dashboard.

Refining state direction:

- Keep the current suggestion visible until the new result is ready.
- During refinement, the current best suggested Task Session may become softly
  fuzzy/blurred to show that it is being reconsidered.
- Show subtle motion or text such as `Finding a better fit`.
- Do not include an assistant orb/pulse in the MVP. The safer first version is
  the blurred suggestion plus a small status line.
- Do not flash or fully reset the screen for every chip change.
- If several chips change quickly, refresh once with the final visible context.
- The fuzzy state must be temporary, gentle, and accessible. Do not blur text so
  heavily that the UI feels broken, unreadable, or like hidden information. Pair
  the visual treatment with a clear refining label or accessible status.

Shuffle action direction:

- Use a recognizable shuffle icon.
- Keep the button compact and approachable.
- Add a tooltip or accessible label such as `Shuffle suggestions`.
- Regenerate the Smart Task List with the current chip context.
- Use the same fuzzy/refining state while the new list is generated.
- Avoid punitive wording such as `reject`, `dismiss`, or `not good`.
- Avoid making shuffle the dominant action over confirming the suggested
  bundle.
- Keep shuffle always visible on the suggested session surface, including when
  details are expanded.
- Shuffle should regenerate immediately, even if the user has removed Tasks
  from the current suggestion. Do not ask for confirmation.
- Consider mood-aware microcopy such as `Try another fit`, `Shuffle`, or
  `Find another`.
- Do not make shuffle copy jokey or attention-seeking.

Bundle-selection action copy directions:

- Use varied, human labels so the app does not feel mechanical.
- Maintain a substantial set of available strings for each major mood.
- Keep labels short enough for mobile buttons.
- Avoid pressure, guilt, or fake cheerfulness.
- Prefer softer labels for `low`, `quiet`, and `auto`.
- Allow more direct labels for `focused`, `restless`, and `ready`.

Draft bundle-selection action strings:

- `Start this bundle`
- `Use this bundle`
- `This works`
- `Set this up`
- `Let's use this`
- `Pick this one`
- `Start this bundle`

The app should choose from this set based on context, with enough variation to
feel alive but not random or distracting.

### Active Task Session

Status: under review.

Once a Task Session starts, the app should switch into a focused active
session view.

The active session should show all selected Tasks, but gently highlight the
best first Task. The user can start or complete Tasks in any order. Homekeep
may suggest the next best step, but it must not lock the user into a sequence.

Active sessions should feel more dynamic and rewarding than the selection
screen. Use positive gamification, Keeps/effects, encouraging action text, and
a dynamic timer/chrono treatment where it helps the session feel alive.

Gamification direction:

- make progress visible and satisfying
- show Keeps, impact, or reward effects for completed Tasks
- show Keeps for completed Tasks and completed bundles
- keep rewards positive and non-punitive
- make small Tasks feel worthwhile
- never punish stopping
- never imply failure for skipping, snoozing, or ending
- avoid competitive pressure or streak-loss mechanics
- avoid arcade-like effects or noisy celebration
- connect rewards to Home Health, Area Health, Projected Impact, or session
  progress
- celebrate the completed suggested bundle more clearly than an individual
  Task, because that is the main recommendation being fulfilled
- after optional Tasks are added, make each optional completion feel
  gradually warmer without turning it into a scoreboard
- make completing the originally suggested Task Bundle intact more rewarding
  than completing an edited bundle, without making edits feel wrong

Keeps direction:

- Use `Keeps` as a lightweight signal of care returned by the home.
- Frame Keeps as gratitude from the home, not a score on the user, money, a
  wage, or productivity scoring.
- Frame Keeps as coming from the home as a whole, not from individual Home
  Assistant Areas.
- Treat Keeps as care circulating through the home. Humans care for the home;
  plants can care for air, humidity, shade, beauty, and presence; purifiers can
  care for air quality; pets and pet routines can reflect care for another
  living inhabitant; quiet-hour and comfort routines can protect rest and
  household rhythm; a coffee machine can care through comfort, ritual, and good
  coffee.
- In future mutual-care features, Keeps may be associated with care sources such
  as `human_care`, `plant_care`, `pet_care`, `device_care`, `air_care`,
  `comfort_care`, `quiet_care`, and `routine_care`. These are explanation
  categories, not currencies, accounts, or rankings.
- Home Assistant devices can participate in care attribution. A laundry Task
  can split or share Keeps between the person doing the human parts of the
  Task and the washing machine doing the machine part. The UI should make this
  feel like collaboration in the home, not like a competition between humans and
  devices.
- Example future copy: `Fern helped the air today`, `Bedroom air stayed
  lighter`, `The purifier kept things steady`, `Watering helped the room
  breathe`, `The washer carried part of this bundle`, `The coffee helped the
  morning start kindly`, and `The home kept a little more comfort today`.
- Return or recognize Keeps for care completed, not for speed, optimization,
  streaks, or performance.
- Show Keeps per Task when suggesting a bundle and when the session is active.
- Show Bundle Keeps as harmony for a coherent suggested bundle, not as a
  pressure reward for obeying the app. Use language such as `4 bundle Keeps`.
- Optional Tasks can add Keeps, but must not create another reward loop.
- Do not subtract Keeps for removing, skipping, snoozing, ending, or stopping.
- Edited bundles can still receive Task Keeps and a smaller Bundle Keeps
  opportunity when appropriate.
- Keeps use a non-scarce care model: they are the home noticing care, not a
  currency that runs out. A plant helping the air does not reduce the Keeps
  available to a person. A coffee machine making good coffee does not take Keeps
  away from the washing machine. More care sources means more care can be
  noticed.
- Do not design Keeps around scarcity: no spending, trading, stealing,
  depletion, exchange rates, shops, debt, or source-vs-source competition.
- Keep Keeps math simple enough to explain in one line.
- Do not show a persistent running total of Keeps received in the active session
  MVP. Show Keeps per Task and Bundle Keeps opportunities instead.
- Future reflection surfaces should proudly display total Keeps by care source:
  humans, pets, plants, devices, air/comfort systems, quiet routines, and other
  meaningful contributors. This should feel like the home appreciating its care
  network, not a leaderboard or ranking.
- Care-source totals should be grouped and named warmly, such as `Humans`,
  `Plants`, `Pets`, `Devices`, `Air`, `Comfort`, and `Routines`, with the
  option to show individual contributors like a coffee machine, washer, fern,
  purifier, or pet when the data is meaningful.
- Use Keeps sparingly in prose and avoid transactional language such as `earn`,
  `earned`, `spend`, `bank`, or `redeem`.
- Prefer quiet reciprocal language, such as `The home gives a little back`.
- Keep Keeps visuals soft; avoid coins, trophies, badges everywhere, or
  scoreboard metaphors.
- Use Keeps to help tiny Tasks feel like they count.
- Let Home Health say where care helps and Keeps say care happened; do not make
  them compete.
- Keeps may support a proud daily or weekly reflection later, such as `The home
  was cared for from many sides this week`, but should not become a leaderboard,
  ranking, or total-chasing surface.

Best-first highlight direction:

- gently highlight the recommended first Task
- explain the highlight briefly, such as `good first step`
- allow any Task to be started first
- update the suggested next Task after completions, skips, or manual starts
- keep the highlight helpful, not commanding

Dynamic session elements:

- encouraging Start button copy for individual Tasks
- visible session progress
- dynamic chrono/timer treatment
- completion effects that are satisfying but not excessive
- Keeps or impact gain display
- a clear completed-session path

Completion feedback:

- Completing a Task should trigger a quick reward effect.
- The effect should be immediate, satisfying, and lightweight.
- Do not interrupt the user with a full summary after every Task.
- Show Keeps or impact gained briefly, then return focus to the remaining
  Tasks and suggested next step.
- Respect reduced-motion preferences in the eventual implementation.
- Completed Tasks should stay visible inline, almost as-is, so the user can see
  the session history without opening anything.
- Completed Task rows should keep the Task name, Area, duration, and Keeps
  line, remove active controls, and add a soft congratulatory signal such as
  `Nice, done`.
- Do not put completed Tasks behind an expand/collapse control in the active
  session.

Completed-bundle continuation:

- After the final planned Task is completed, add a short list of optional
  Tasks directly into the active session list instead of showing `Done for
  now` / `One more` buttons.
- Keep completed planned Tasks visible above the optional Tasks.
- Show a subtle session progress line, such as `2 of 3 planned done · optional
  care available`.
- Add a persistent inline milestone row when the suggested bundle is complete,
  such as `Suggested bundle complete · The home feels lighter`.
- Visually separate the optional Tasks with a compact inline divider, such as
  `A few more that fit`.
- Include a tiny explanation for why the optional Tasks appeared, such as
  `Picked for small effort, current fit, and useful home lift`.
- Do not automatically exit the user from the flow.
- Keep an exit action available once optional Tasks appear so optional really
  means optional.
- Use positive momentum language, not pressure.
- Shift idle support copy after planned completion toward `Stop here, or pick
  one more small thing.`
- Show a clear celebration flash when the suggested bundle is done before the
  optional Tasks appear.
- Optional Tasks should be small, useful, and easy to skip.
- Use softer skip copy such as `Not now` on optional Tasks.
- Optional Task completion feedback should ramp gently as additional optional
  Tasks are completed.
- Optional Tasks should be generated from the same Recommendation Engine
  principles as the main suggestion, but with stricter bounds: small duration,
  mood/time fit, no recent skip/remove/dismiss/snooze, useful Home Health or
  Area Health impact, and no chaining forever.
- Optional Tasks can bias toward useful overdue Tasks when they fit the
  current context, especially small tasks with high Projected Impact.
- Overdue bias must preserve the light optional feeling. Do not offer large
  overdue Tasks that feel like a second session unless a tiny/light variant is
  available.
- Do not offer Tasks the user just removed, skipped, snoozed, or dismissed.
- Do not use guilt-based overdue language. Phrase overdue optional Tasks as
  positive opportunities, not obligations.

Final summary:

- Exiting the completed session should show a short final
  celebration/summary before returning to Ready Now.
- The summary should feel positive and complete, not like a report card.
- Include completed Tasks, Keeps received, Bundle Keeps if received, and friendly
  Home/Area impact where available.
- Keep it brief enough to read at a glance.
- Make stopping feel like success.
- After a short moment, the summary should return the user to Ready Now
  automatically. It should not require a close/return tap.
- Do not include a share, log, or `View details` option in the MVP final
  summary. Keep it ephemeral. Detailed history can live later in Activity.

Timer behavior:

- The active session timer should run only when a Task is `ongoing`.
- Confirming a bundle should not start the timer.
- Viewing, reordering mentally, choosing, pausing, or deciding what to do next
  should not count as active task time.
- When no Task is ongoing, show the session as ready or paused rather than
  timing the user.
- The timer should support the user, not pressure them.
- Pause should be combined with the Task Session timer/chrono control. When
  the user pauses, Homekeep pauses the current ongoing Task rather than
  presenting Pause as a separate primary action.
- The timer should clearly show paused state and offer a simple way to resume
  the same Task.
- Completing a Task should use a separate prominent Complete button. Stopping
  or pausing the timer should not be overloaded with completion choices.

Required actions:

- complete
- skip
- pause
- end
- optional Task start/complete/skip after planned completion

Action visibility:

- Start and Complete should be the prominent Task-level actions.
- Skip should be tucked behind a secondary or overflow action.
- Skip must remain available after a Task has started. Skipping an ongoing
  Task stops that Task's timer, marks it skipped rather than completed, and
  moves the session toward the next pending Task when one exists.
- Do not offer Snooze on active-session Tasks. Snooze remains a
  recommendation or planning-level `later` action, not an in-session task
  control.
- The surface should feel encouraging and focused on progress, not cluttered
  with exception handling.

The active session view should use materialized `session_item_id` values from
`homekeep.start_recommendation`. It must not act on stale recommendation item
IDs.

### Home Health

Status: under review.

Home Health should be visible, but not the emotional center of the app.

It should help the user understand where attention matters:

- whole-home status
- Home Assistant Areas that need care
- tasks that are stale enough to matter
- Projected Impact from the offered Task Session

Health should be presented as useful context, not a grade.

Decision: Home Health and Area Health should include visible numbers.

The number should provide clarity, progress, and quick comparison. It should not
feel like a grade on the user. Pair the number with friendly household language
so the meaning is obvious without making the screen clinical.

Decision: Home Health should lead with a friendly status label, supported by
area-level language, with the numeric score visible but visually secondary.

The primary read should be human and household-oriented, such as `The home is
holding steady`. Area-level language should explain where care would help, such
as `Kitchen could use attention`. The number should remain available for
clarity and comparison, but it should not be the emotional headline of the view.

Decision: Home Health and Area Health use a `0-100` scale where higher is
healthier.

Area Health should communicate `how much would this area benefit from care
right now?` rather than `what percent of tasks are done?` It is a household
status signal, not a personal score. In MVP, the score comes from the derived
health of enabled Tasks in that Home Assistant Area, weighted by each Task's
health impact and driven mostly by Staleness.

Preferred presentation:

- whole-home health number with a friendly status label
- area health numbers for the areas that matter most right now
- short area-level language beside the number, such as `Kitchen could use care`
  or `Entryway is holding steady`
- small area trends where useful
- projected improvement numbers when a suggested Task Bundle would help an
  area, such as `Kitchen 24`

Suggested Area Health labels:

- `90-100`: `Fresh` or `Feeling good`
- `75-89`: `Holding steady`
- `60-74`: `Starting to build up`
- `40-59`: `Could use care`
- `0-39`: `Needs care`

Example Area Health language:

```text
Kitchen 48 · Could use care
Entryway 82 · Holding steady
Bathroom 64 · Starting to build up
Living room 91 · Feeling good
```

Decision: Area Health rows may show small trends too.

Area trends should be visually smaller than the health number and status label.
They should help the user understand recent movement without turning each row
into analytics. Use the same `last 7 days` period as the Home Health header
unless implementation discovers a better derived context.

Decision: Show Area Health trends only when they are meaningful.

Do not show a trend on every Area card by default. Show trend text or movement
only when it explains something useful, such as a recent decline, a notable
improvement, or a change that affects the next care recommendation. Quiet,
steady Areas can omit trend detail.

Examples:

```text
Kitchen 48 · Could use care · -4
Entryway 82 · Holding steady · +3
Bathroom 64 · Starting to build up · down a little
```

Ready Now should use Area Health to explain why a suggestion matters without
showing every area all the time. Prefer a compact Area Health strip tied to the
current suggestion, such as:

```text
Kitchen 48 · 24 with this bundle
Entryway 82 · steady
```

Area Health colors should be warm and calm. Use green, blue, amber, coral, or
soft rose. Avoid red-heavy warning treatment unless a future explicit urgent
state exists.

Decision: Area Health cards should always use emphasis color related to health.

Do not rely on custom decorative colors per area for the primary visual signal.
Color should help the user understand the area's current health state. Area
identity can still come from the Home Assistant Area name and icon, but the
main emphasis color should be derived from Area Health.

Decision: Show Area Health color as a soft card tint.

Avoid heavy warning bars or loud status pills as the primary treatment. A soft
card tint gives the area card a health-related mood while keeping the view calm
and inspectable. Text contrast must remain accessible.

Decision: Area Health cards should display the Home Assistant configured Area
icon.

The Home Assistant Area icon should provide area identity alongside the area
name. The icon should not replace the health emphasis color; identity and
health state should work together.

Decision: Ready Now should show both whole-home health and the most
attention-worthy Area Health, but keep them compact and tied to the current
suggestion.

Live review correction: the first mocked Right Now live test did not provide a
way to inspect Home Health as its own view or full experience.

Treat Home Health visibility as still unvalidated in live use. The mocked Right
Now card may show compact health/impact context, but that does not count as a
live review of the Home Health view, Home Health navigation, Area Health card
layout, trends, or explanations.

Live Test 2 decision: include Home Health visibility/navigation in the pass.
The test should verify that Home Health is reachable from the Homekeep app,
opens clearly, and can return to Right Now without crowding the recommendation
flow. This does not expand the pass to Plan, Add Task, Activity, Settings,
diagnostics, service wiring, or full Home Health behavior validation.

Decision: Right Now should show compact Home Health context only when it helps
explain the current recommendation.

Do not make Home Health an always-visible status strip on Right Now. If the
suggested Task Bundle is clearly driven by an attention-worthy Area Health
state, stale care, or a meaningful Projected Impact, show compact context inside
the suggestion. If the suggestion is neutral, light, or self-explanatory, let
the suggestion stand without extra health context.

The whole-home number gives the satisfying sense that the home is being cared
for. The area number explains why the current Task Bundle matters. The UI
should avoid turning this into a large dashboard section.

Recommended Ready Now treatment:

```text
Home 74 · Mostly steady
Kitchen 48 · This bundle helps most
```

Recommended expanded-bundle treatment:

```text
Kitchen 24 · Big kitchen boost
```

Decision: On Ready Now, the compact Home Health and Area Health treatment should
live inside the suggested Task Bundle, visible in the collapsed bundle state.

This keeps health context directly attached to the recommendation it explains.
It also prevents Ready Now from becoming a dashboard made of separate health cards.
The treatment should read as a small support line inside the suggestion, not as
a standalone analytics section.

Recommended collapsed bundle structure:

```text
Evening Kitchen Lift
12 min · calm · Kitchen
Home 74 · Mostly steady
Kitchen 48 · This bundle helps most
Fits your time and gives the kitchen a visible lift.
```

When the bundle expands, show the stronger before/after Area Health impact near
Projected Impact rather than duplicating the same collapsed lines.

Decision: `Home Health` should be a central place in the Homekeep panel.

Ready Now should only show the compact health context needed to explain the current
suggestion. The dedicated `Home Health` view should be the central place where
the user checks Area Health and sees what they can do to help the home.

Product role:

- Ready Now answers `what should I do right now?`
- Home Health answers `how is the home doing, area by area?`
- Home Health also answers `what can I do to help this area?`

The view should feel actionable, not merely informational. It should help the
user understand which areas need care, why, and what small direct action is
available without making the page feel punitive or like a second Ready Now screen.

Decision: Home Health should not show much detail when there is not much to
report.

Healthy, steady, or uneventful Areas should stay compact and calm. Do not
manufacture explanations, trends, or actions just to fill the card. Richer
detail belongs where there is a meaningful reason: low Area Health, recent
decline, stale high-impact Tasks, a useful next care action, or a notable
recent improvement.

Decision: The `Home Health` view should be organized primarily as a
list of large Home Assistant Area cards.

Use a scannable card list rather than a home map, room diagram, or pure ranked
`needs care most` view. Each Home Assistant Area should have a large enough
card to show the area number, status, small trend, and useful detail without
feeling cramped. The list may still sort or highlight areas that need care, but
the user's mental model should remain `these are the areas of my home`.

Decision: Area Health cards should lead with the Area name, then the friendly
status label.

People think first in terms of places in the home, such as `Kitchen` or
`Entryway`, then ask how that place is doing. The status label should sit close
to the Area name, with the numeric Area Health score visible but secondary to
the place/status read.

Decision: Use one vertical column of large Area Health cards.

Do not use a two-column grid on desktop. A single vertical column gives the Home
Health view a calmer inspection feel and keeps each area easy to read. It also
fits the role of Home Health as a central place to understand and care for the
home, not a dense analytics dashboard.

Decision: The Area Health list should default sort by lowest health first.

This makes the view immediately useful because the areas that could use care
rise to the top. The UI should still feel like a calm area list, not an alarm
queue. Areas with healthy scores should remain visible lower in the list so the
home still feels whole and cared for.

Decision: Do not add Area Health filters or chips for MVP.

Most homes will have a small number of Home Assistant Areas in this view, likely
around `4-5`. Use the default lowest-health-first sorting and keep the full list
visible. Filters such as `All`, `Needs care`, or `Steady` would add complexity
without much benefit at that size.

Each Area Health card should show:

- area name
- Area Health number
- friendly status label
- small trend where useful
- what the user can do to help the area
- primary visible area action
- recent care or recent improvement when useful
- next upcoming Task for healthy areas
- one main contributing Task for areas below `70`, plus a compact `more ways
  to help` line when there are additional contributors
- suggested next care opportunity when appropriate

Decision: Place the Area Health number large on the right side of each card.

The top-left of the card should carry area identity with the Home Assistant
Area icon and area name. The large right-side number makes health easy to scan
down the vertical card list without crowding the area name.

Recommended card header pattern:

```text
[icon] Kitchen                    48
Could use care · -4
```

Decision: Place the Area card primary action at the bottom after the details.

The card should first explain the area's state, then offer the next care action.
This avoids making the action feel like a command before the user understands
why it helps.

Recommended card flow:

```text
[icon] Kitchen                    48
Could use care · -4
Dishes are carrying the most staleness.
Clear dishes · 14
[Care for this area]
```

The Home Health view as a whole should also show the whole-home health number
and friendly status in the large header above the area cards.

Decision: Home Health should use all Home Assistant Areas configured in Home
Assistant by default.

The Home Health area list should be based on the user's Home Assistant Areas,
not a separate Homekeep-only area model. Provide a Homekeep configuration option
to hide specific Home Assistant Areas from Home Health when the user does not
want them included.

Area visibility rules:

- include all configured Home Assistant Areas by default
- automatically include newly created Home Assistant Areas
- allow the user to hide selected Areas in configuration
- hidden Areas should not appear in the Home Health card list
- hidden Areas should not drive Home Health UI emphasis
- hidden Areas should be treated as unmanaged by Homekeep
- hiding an Area should not delete existing Tasks or change Home Assistant
  itself
- use safe neutral copy such as `Hide from Home Health`

Decision: Newly created Home Assistant Areas should be automatically taken in
charge by Homekeep.

Homekeep should not require a separate manual area import step. When a new Home
Assistant Area appears, Homekeep should include it in Home Health by default,
subject to the user's hidden-area configuration.

Decision: Hidden Areas should be considered unmanaged by Homekeep.

When an Area is hidden in Homekeep configuration, Homekeep should not use that
Area for Home Health, Area Health, Ready Now suggestions, Bonus Tasks, or
Homekeep-managed direct care actions. The Area may still exist normally in Home
Assistant, but it is outside Homekeep's managed care surface.

Unmanaged Area rules:

- exclude from Home Health cards
- exclude from whole-home health calculations where practical
- exclude from recommendation and Bonus Task eligibility
- exclude from Homekeep UI emphasis and area health summaries
- do not delete or modify the Home Assistant Area
- mark existing Homekeep Tasks in that Area inactive, not deleted

Decision: Tasks in hidden/unmanaged Areas should become inactive and
recoverable.

When a managed Area is hidden from Homekeep, existing Homekeep Tasks assigned
to that Area should become inactive. They should not be suggested, shown as
active care opportunities, or counted toward Home Health while the Area is
unmanaged.

If the user re-includes the Area in Homekeep later, those inactive Tasks should
be recoverable and can become active again. Homekeep should preserve enough
metadata to restore them without forcing the user to recreate their task setup.

Decision: Hide and re-include Area controls should live in Settings only.

Do not put hide/re-include controls in each Home Health Area card. Area cards
should stay focused on understanding and caring for the area. Settings is the
right place for deciding which Home Assistant Areas Homekeep manages.

Decision: Settings should use a multi-select to choose managed Areas.

The configuration model should be framed positively as choosing which Home
Assistant Areas Homekeep manages. Selected Areas are managed. Unselected Areas
are unmanaged.

Managed Areas config rules:

- show all Home Assistant Areas in a multi-select
- select all Areas by default
- newly created Home Assistant Areas should become selected/managed by default
- unselecting an Area makes it unmanaged
- reselecting an Area makes it managed again and can recover inactive Tasks
- use clear copy such as `Managed Areas`

Decision: Hide Home Health freshness by default unless data is stale.

Do not show routine timestamps like `Updated 12 min ago` during normal use.
They make the view feel more technical without helping the main workflow. If
health data is stale, expired, or failed to update, show a soft stale-state
message without a manual refresh button.

Decision: Do not add refresh buttons anywhere in the Homekeep UI plan.

Homekeep can update automatically, regenerate through explicit workflow actions
such as shuffle, or recover when the user changes visible context. Do not expose
generic `Refresh` or `Refresh Home Health` buttons in the user interface.

Examples:

```text
Health may be out of date
```

```text
Health is catching up
```

Decision: Area cards below `70` should show one main contributing Task plus a
small `more ways to help` line.

A contributing Task is a Task that is currently pulling the Area Health down
or would provide a clear Projected Impact if completed. It should be explainable
through Staleness, Area Health impact, Projected Impact, or a useful small
variant.

Show one top contributing Task visibly so the card has a clear next action.
Represent the remaining contributors as a compact line, such as `2 more ways to
help`, only when there are genuinely useful extra contributors. Do not list
`2-3` Tasks by default on every Area card, because that turns Home Health into
another overdue list. This keeps the cards calm and scannable while still
indicating that the area has more useful care options when that is true.

Decision: Tapping `2 more ways to help` should expand the extra Tasks inline
inside the Area Health card.

Do not open a separate Task list view for this interaction. Inline expansion
keeps the user in the area context and makes the extra options feel like
supporting details, not a second workflow.

Inline expansion should show the remaining contributing Tasks compactly:

```text
2 more ways to help
Wipe counters · 8
Take out compost · 6
```

Tapping any expanded Task should open that Task's details, with the same
direct single-Task start rules as the main contributing Task.

Decision: Inline extra Tasks should collapse again when another Area card's
`more ways to help` section is expanded.

Only one Area card should show expanded extra Tasks at a time. This keeps the
vertical Home Health view calm and prevents multiple area cards from growing
into a long task list.

Decision: Area cards should be open by default with details visible.

The Home Health view should feel substantial and immediately useful, not like a
collapsed index that requires opening each area. Cards can still use visual
hierarchy to keep the page scannable.

Open card details:

- areas below `70` show one main contributing Task and a compact `more ways to
  help` line
- healthy areas show recent care and next upcoming Task
- all cards keep the number, status label, and small trend visible
- details should stay compact enough that the list remains easy to scan

Decision: Only areas below a certain health threshold should show contributing
Task details.

Healthy areas should not be forced to expose contributing Tasks because that
can make the whole home feel like a problem list. When an area is healthy, its
card can simply show the number, friendly status, and recent care or steady
state.

Decision: Show contributing Task details for areas below `70`.

This keeps the area list calmer. Areas can show `Starting to build up` without
immediately exposing a task breakdown, while lower-health areas show the
specific Tasks that would help.

Contributor explanations should stay short and inspectable. Prefer reasons
that connect directly to derived Homekeep values:

- the Task is stale enough to pull the area down
- the Task has high Area Health impact
- the Task offers clear Projected Impact for the area
- a small variant would provide useful care without turning the area into a
  problem list

Avoid explanations that sound like judgment, diagnosis, or a hidden model the
user cannot correct. `Kitchen could use care because counters are overdue` is
better than `Kitchen health is poor due to neglected maintenance`.

Decision: Area Health should proudly show who and what helped the area.

Area Health naturally trends down as care gets stale. That decline should feel
like a normal rhythm of the home, not a failure. The UI should balance
`what needs care now` with `who helped keep this area well`.

Each Area Health card should be able to show recent area contributors when the
data is meaningful:

- humans who completed Tasks in that Area
- pets whose routines are tied to that Area
- plants contributing air, humidity, presence, or comfort in that Area
- devices such as purifiers, washers, dryers, dishwashers, vacuums, humidifiers,
  dehumidifiers, HVAC, grow lights, coffee machines, or other Home Assistant
  entities that contributed care
- routines that protected quiet, comfort, air, light, or household rhythm

This should be proud and warm. People, pets, plants, and devices are part of the
home's care network, and the UI should make that visible.

Suggested Area Health contribution UI:

- `Helped lately` row with small contributor chips
- `Care sources` mini summary when an Area is expanded
- `Kept this area steady` line for healthy Areas
- `Recent help` line for lower-health Areas so decline does not erase
  contribution
- optional contributor detail drawer in the future, not required for MVP

Example contributor chips:

```text
Helped lately: You 12 Keeps · Washer 5 · Fern 3
```

```text
Kept this area steady: Purifier · Fern · Quiet hours
```

```text
Recent help: You, the washer, and the drying rack moved laundry along.
```

Area Health should not only explain why the number is lower. It should also
explain why the area is not lower:

```text
Kitchen 64 · Starting to build up
Coffee, dishes, and the purifier helped this area hold together.
Counters would help most next.
```

```text
Laundry 72 · Holding steady
You and the washer carried this room this week.
Next: Put away clean laundry · tomorrow
```

Contribution display rules:

- show contribution as appreciation, not ranking
- never imply that a person, pet, plant, or device failed because Area Health
  drifted down
- do not sort contributors as winners and losers
- use warm source names like `Humans`, `Plants`, `Pets`, `Devices`, `Air`,
  `Comfort`, and `Routines`
- show individual contributors only when useful and not noisy
- keep the top action focused on what helps next
- make recent contribution visible even when the area still needs care
- use Home Assistant entity/device names only when they are friendly enough;
  otherwise map them to safer display labels

Recommendation: Area Health cards should visually separate `Helped lately` from
`Could help next`. This keeps pride and action from competing:

```text
[icon] Kitchen                    64
Starting to build up · -3
Helped lately: Coffee machine · Purifier · You
Could help next: Wipe counters · 8
[Care for this area]
```

Future reflection surfaces should use Area Health contribution history to show
that health is a living rhythm:

```text
The kitchen drifted down, but it was cared for from many sides.
Coffee helped the morning. The purifier kept air moving. You cleared dishes.
```

Future data-shape note, not MVP implementation:

```text
CareSource:
  source_id
  source_type: human | pet | plant | device | air | comfort | quiet | routine
  display_name
  home_assistant_entity_id: string | null

CareContribution:
  contribution_id
  source_id
  area_id: string | null
  care_kind
  keeps
  happened_at
  related_chore_id: string | null
  related_session_id: string | null
```

This model should stay explainable and local-first. Care contribution records
should use friendly display labels and avoid storing private calendar text,
sensitive device details, or personal routines beyond what is needed to explain
care.

Decision: All areas should be expandable.

Areas at `70+` should still be expandable for context, but they should not show
contributing Task details unless they drop below `70`. Healthy area expansion can
show steady-state information, recent care, or why the area is doing well.

Decision: Healthy expanded areas should show both recent care and the next
upcoming Task.

Recent care explains why the area is healthy. The next upcoming Task gives
useful planning context without making the area feel like a problem.

Example healthy expanded area:

```text
Entryway 82 · Holding steady
Recent care is helping this area stay ready.
Next: Shake entry rug · tomorrow
```

Example expanded area:

```text
Kitchen 48 · Could use care
Clear dishes · 14
Wipe counters · 8
Take out compost · 6
```

Decision: Tapping a contributing Task should open Task details only.

The Task details view should include a button to start that Task directly as
a single-Task flow. This direct start should not generate a Task Bundle, and
it should not offer Bundle Keeps.

This keeps Area Health exploratory first. The user can understand why the Task
matters before acting, but still has a clear direct path if they want to care
for that area immediately.

Direct Task start from Area Health:

- starts only the selected Task
- does not create a suggested bundle around it
- does not include Bundle Keeps
- can still show the Task's own Keeps and Projected Impact
- should show a small `Done for now` / `One more` ending when finished
- should not interrupt an active Task Session without a clear confirmation
  state

Direct Task details should use a softer primary action label than
`Start this Task`.

Preferred label direction:

- `Do this now`
- `Take care of this`
- `Care for this`
- `Help this area`

The label should still be clear that tapping it begins the selected Task
directly. Avoid labels that imply a bundle, such as `Start bundle` or
`Choose this bundle`.

Decision: Home Health should stay focused on Task details and direct
single-Task starts.

Do not add a primary action to generate a Task Bundle from a selected area in
the Home Health view. Bundle generation should stay centered in Ready Now /
Ready-Now Mode and the Smart Task List flow.

The Home Health view should help the user inspect areas, understand what is
affecting health, and optionally act on a single Task. It should not become a
parallel recommendation builder.

Decision: Each Area Health card should have a primary visible action like
`Care for this area`.

The primary area action should make the card feel actionable at a glance. It
should help the user move from understanding an area's health to helping that
area.

Decision: Tapping `Care for this area` should open the top contributing Task
details directly.

This gives the user one clear next step from an area card. The Task details
view can explain why that Task helps the area and offer the soft direct start
action. It must not silently create a Task Bundle or imply Bundle Keeps.

Pre-Live-Test-2 planning default: use Codex recommendations for remaining
Home Health questions needed before the second Right Now live test.

These defaults are accepted for moving to Live Test 2 and can be revisited after
the test:

- The full Home Health view lives as a top-level Homekeep app destination named
  `Home Health`.
- Live Test 2 should include the mocked Right Now component, its active
  session/ending loop, and basic Home Health visibility/navigation.
- The next build should prioritize Right Now interaction confidence while also
  confirming that Home Health is reachable and does not crowd Right Now.
- `Best fit` is the final visible label for automatic Time and Area in this
  pass.
- Keep the top-right projected-benefit action button as-is for this pass.
- Full Home Health behavior remains planned but unvalidated until a later
  dedicated Home Health review/test.

Decision: Area cards below `70` should use `Care for this area` as the primary
action label.

This label is direct but still soft. It matches the product goal of caring for
the home without using harsher language such as `fix`, `repair`, or `urgent`.

Example low-health area card:

```text
Kitchen 48 · Could use care · -4
Dishes are carrying the most staleness.
[Care for this area]
```

Decision: Healthy areas above `70` should keep a softer primary action that
opens the next upcoming Task details.

Healthy areas should remain actionable without feeling urgent. Use softer action
labels such as `Keep it steady` or `See next care` instead of the stronger
`Care for this area`.

Example healthy area card:

```text
Entryway 82 · Holding steady · +3
Recent care is helping this area stay ready.
Next: Shake entry rug · tomorrow
[Keep it steady]
```

Decision: Expose the `Home Health` view from the Homekeep panel side
navigation, but not from the Ready Now health line.

The `Home Health` view belongs as a panel-level navigation destination.
The compact Ready Now health lines should explain the current suggestion without
acting as a doorway to a larger health dashboard.

Decision: The panel navigation label for the dedicated health view should be
`Home Health`.

`Home Health` is broader than `Areas` and less vague than `Health`. The view can
still be organized primarily as a list of Home Assistant Areas.

Decision: After finishing a single Task started from Area Health, Homekeep
should show a small `Done for now` / `One more` ending first.

This ending should be lighter than the full suggested-bundle ending because the
user completed a single direct Task, not an intact Task Bundle.

Single-Task ending rules:

- show completion feedback for the Task
- show the Task's Keeps received
- show `Done for now` and `One more`
- do not show Bundle Keeps
- let `Done for now` return to the previous Area Health context or Ready Now
- let `One more` offer a small eligible Bonus Task, using the same optional
  Bonus Task model as other endings
- keep the copy low-pressure and clear that stopping is successful

Decision: `One more` after a single Area Health Task may choose from any
eligible area, but should tilt toward the current area.

The current area should receive a preference boost because the user is already
thinking about that part of the home. This should not be a hard filter. If a
better small eligible Bonus Task exists elsewhere, Homekeep may offer it.

Bonus Task eligibility from Area Health should consider:

- current area preference
- low effort fit
- high Projected Impact
- overdue care when it still feels light
- recent skips, snoozes, removals, and dismissals
- whether the Task was just completed

Avoid offering another Task in the same area if it would make the flow feel
like a hidden bundle or a second session.

The expanded view should still avoid grade-like treatment. It should answer
`where would care help?` rather than `what is wrong?`.

Decision: The `Home Health` view should show the whole-home number as a large
header at the top.

The header should make the view feel like a real destination. It should show the
whole-home health number, a friendly status label, and a short care-focused
summary. The area list should sit below the header.

Decision: The large Home Health header should include a small trend.

The trend should show recent movement in the home health number, such as
`+6 in the last 7 days`, without turning the header into an analytics
dashboard. Use the trend to reinforce that care is having an effect.

Decision: The Home Health trend period should default to `last 7 days`.

Use `last 7 days` instead of `this week` so the trend is clear and does not
depend on calendar-week boundaries.

Decision: Show negative trends as well as positive trends.

Negative trends should be visible because they help the user understand when
care would help. The wording and visual treatment should stay soft. Avoid
making a negative trend feel like a failure or warning unless a future explicit
urgent state exists.

Decision: Trend copy may use both numeric movement and soft wording.

Use numeric movement when it helps clarity, such as `+6 in the last 7 days` or
`-4 in the last 7 days`. Use soft wording when it better protects the tone,
such as `Down a little in the last 7 days`.

Examples:

```text
+6 in the last 7 days
-4 in the last 7 days
Down a little in the last 7 days
```

Example header:

```text
Home 74
Mostly steady
+6 in the last 7 days
The kitchen could use care, but the home is holding together.
```

The large header should still avoid scorecard treatment. It is a household
status, not a grade on the user.

Decision: The large Home Health header should not have a primary action.

The header should orient the user to the whole home's current state. Actions
should live on Area Health cards, where the care target is concrete. This avoids
competing with Ready Now's recommendation flow and avoids vague actions like
`care for the home` when the user needs to know which area they can help.

Avoid:

- presenting the number as a personal score
- red-heavy warning treatment for normal household staleness
- grades such as `A`, `C`, or `failing`
- shame wording such as dirty, bad, neglected, or behind
- exposing scoring formulas in the main UI

### Plan / Scheduled Tasks

Status: draft.

Plan should feel like setting aside intentional future care, not generating a
Smart Task List for later.

```text
Plan
-> choose a future time
-> choose or create set Tasks
-> optionally group them into a planned care item
-> save the planned Tasks
-> surface them on Ready Now when relevant
```

Decision: Users should not plan generated Smart Task Bundles for the future.

Generated Task Bundles belong to Ready Now / Ready-Now Mode, when the user is
actually ready to do household care. If the user wants a generated bundle, they
should wait until they are ready and use Ready Now.

Plan is for set Tasks or planned household projects the user already knows
they want to do, such as painting the house Saturday morning.

Decision: Plan should support longer project-style Tasks, while Ready Now
stays focused on short generated care bundles.

Ready Now answers `what can I do right now?` with generated, context-aware
Task Bundles. Plan answers `what do I already know I need or want to do
later?` with intentional set Tasks or projects. Plan may include longer work
such as painting, garage cleanup, seasonal prep, or other household projects
that do not fit the Ready Now generated-bundle model.

Example planned items:

```text
Paint the front porch
Saturday morning
Outdoor · 3 hr
```

```text
Clean out the garage shelf
This weekend
Garage · 45 min
```

```text
Wash guest bedding
Friday evening
Laundry · 30 min
```

Planned Tasks should not silently start. When the planned time is near, Ready Now
can surface them as intentional planned work.

Decision: Planned Tasks should appear on Ready Now only when they are relevant
soon, but creation and management should live in Plan.

Ready Now should surface saved planned Tasks when they are close and actionable,
such as `Painting is planned for Saturday morning`. The full workflow for
creating, inspecting, editing, deleting, and managing planned Tasks belongs in
the Plan view. This keeps Ready Now useful without turning it into a calendar.

Decision: Planning should use quick time chips first, with an optional natural
date/time field for precision.

The default Plan flow should feel lightweight and easy to choose from:

```text
Tonight
Tomorrow morning
This weekend
After work
```

When the quick options are not enough, the user can choose `Custom time` and
enter a natural date/time. This keeps common planning fast without removing
precision.

### Add Task

Status: draft.

Adding a Task should be available from the Homekeep app, but it should not
interrupt an active Task Session.

`homekeep.create_chore` creates a durable Task definition. It must not rely on
Home Assistant To-do create write-through, and it must not create a Task
Session by itself.

Questions to settle:

- Should Add Task start as a quick capture field, a full structured form, or a
  two-step quick-capture-to-details flow?
- Which fields are required in the first UI pass?

### Settings

Status: draft.

Settings should stay small and practical. It should not become a control room
or compete with the main care workflows.

Recommended MVP Settings:

- `Managed Areas`
- `Voice & Tone`
- `Diagnostics`

`Managed Areas` is the most defined Settings item. It should let the user choose
which Home Assistant Areas Homekeep manages through a multi-select. Home
Assistant remains the source for creating, renaming, deleting, and configuring
Areas. Homekeep only decides whether each Area is managed or unmanaged by
Homekeep.

Managed Areas settings behavior:

- show all Home Assistant Areas
- select all Areas by default
- automatically select newly created Home Assistant Areas by default
- unselected Areas become unmanaged by Homekeep
- reselecting an Area can recover inactive Tasks for that Area
- changes affect Homekeep behavior only; they do not modify Home Assistant
  Areas

Decision: Managed Areas changes should require a `Save` button.

Selecting or unselecting Areas should update the pending settings state, but
Homekeep should not apply management changes until the user saves. This makes
the choice intentional, especially because unselecting an Area makes it
unmanaged and marks its Homekeep Tasks inactive.

The Settings UI should clearly distinguish pending changes from saved Homekeep
behavior.

Decision: Saving Managed Areas changes that remove Areas should show a
confirmation message before applying.

The confirmation should explain the consequence plainly: removed Areas become
unmanaged by Homekeep, and existing Tasks in those Areas become inactive but
recoverable if the Area is managed again later. The confirmation should not
sound alarming because the change is reversible.

Example confirmation:

```text
Remove 2 areas from Homekeep?
Their tasks will become inactive, but they can come back if you manage those
areas again.
```

Decision: Saving Managed Areas changes that only add or re-include Areas should
apply without confirmation.

Adding management is low risk because it brings Areas back into Homekeep rather
than making existing care inactive. The saved change can apply directly.

Decision: Without Areas, there is no Home Health.

Home Health depends on Home Assistant Areas. If Home Assistant has zero
configured Areas, Homekeep should not show Home Health numbers, Area cards, or
care suggestions tied to Area Health.

Homekeep may show a minimal setup state explaining that Home Health needs Home
Assistant Areas, but it should not present that as a working Home Health view.
It should not offer to create Areas inside Homekeep because Home Assistant
remains the source for Area creation and configuration.

Example:

```text
No Home Assistant Areas yet
Homekeep uses Areas to understand where care helps.
Add Areas in Home Assistant to use Home Health.
```

Decision: If all Home Assistant Areas are unmanaged, there is no Home Health.

Home Health depends on managed Areas. If the user unselects every Area, the
Home Health panel should not pretend it has meaningful health data. It can show
a minimal Settings-oriented state, but it should not show Home Health numbers,
Area cards, Ready Now health lines, or care suggestions.

`Voice & Tone` should stay lightweight. It can later hold optional tone
intensity or variation controls, but it should not become a personality editor.

`Diagnostics` should include integration health, version, debug information, and
safe export/support tools when needed.

Later Settings candidates:

- `Mood & Readiness`
- `Notifications / Suggestions`
- `Privacy`
- selected calendars
- default time and capacity preferences

Keep notifications, deeper privacy controls, and advanced planning behavior for
later unless they become necessary during implementation.

## Proposed Information Architecture

### Ready Now

The default view.

Purpose:
: Decide what to do now.

Contains:

- Ready-Now setup
- current Smart Task List
- active Task Session, when present
- inline optional Task continuation, when the planned session is complete

### Home Health

Purpose:
: Check Area Health and see what can be done to help.

Contains:

- large whole-home health header
- one vertical column of large Home Assistant Area cards
- Area Health number, status, trend, and health-based tint
- Home Assistant configured Area icon
- one main contributing Task for areas below `70`
- compact `more ways to help` inline expansion
- direct Task details and single-Task starts

Does not contain:

- bundle generation from an Area
- Ready Now health-line navigation
- refresh buttons
- Area management controls

### Plan

Purpose:
: Create and manage intentional future Tasks and household projects.

Contains:

- target time window input
- planned set Tasks
- planned household projects
- optional Home Assistant Area
- saved planned items
- Ready Now surfacing when relevant

Does not contain:

- generated Smart Task Bundle planning
- Recommendation Engine bundle proposals for the future
- refresh buttons

### Activity

Purpose:
: Review recent household care without turning it into a scoreboard.

Contains:

- recent Task completions
- recent Task Sessions
- skipped, snoozed, and dismissed items
- lightweight Session-History Learning signals when useful

### Settings

Purpose:
: Adjust Homekeep behavior.

Contains:

- Managed Areas
- Voice & Tone
- Diagnostics

Later:

- Mood & Readiness
- Notifications / Suggestions
- Privacy
- selected calendars
- default time and capacity preferences

Settings can come later. The MVP should not let settings crowd the main flow.

## Visual Direction

Homekeep should feel calm, practical, and app-like.

Design guidance:

- Mobile-first layout.
- Dense enough to scan quickly.
- No giant overdue list as the first impression.
- No punitive colors or language.
- Use Home Health as context, not judgment.
- Prefer clear actions over explanatory paragraphs.
- Keep each screen focused on one household job.
- Make the active Task Session visually distinct from planning and history.

The interface should feel more like a gentle operational panel than a decorative
landing page.

## First Live Design Review

The first live review of the Homekeep sidebar app should start with design and
visuals, using the mocked Ready Now prototype. This review is intentionally about
product feel before service wiring.

Unless a review note is explicitly scoped to one screen or component, visual
feedback from this live review applies globally to the Homekeep app. Treat these
notes as design-system direction for future Ready Now, active session, Bonus
Task, Home Health, Plan, Activity, Settings, diagnostics, empty states, and
error/stale-state surfaces.

Review goals:

- confirm the first impression feels like Homekeep, not a generic dashboard
- check whether the Ready Now visual hierarchy leads naturally from greeting to
  context to suggested Task Bundle
- verify the screen works on mobile and desktop without text collisions,
  crowded controls, or oversized decorative sections
- confirm Home Health, Area Health, Projected Impact, and Keeps feel supportive
  rather than punitive
- confirm the active Task Session state feels distinct from setup and planning
- confirm inline optional Tasks feel positive, optional, and complete
- identify copy or motion that feels too chatty, too quiet, too cute, too
  clinical, or too much like a productivity score

Findings from this review should be grouped as:

- keep as-is
- change before service wiring
- acceptable for the mock but not for the wired app
- can wait for later workflow planning
- open product question

The next build after this live review should first apply any Ready Now
design/visual changes that affect confidence in the main loop. Only after that
should the app move on to real Homekeep service wiring.

Live review findings:

Change before service wiring:

- The mocked Ready Now colors do not fit Home Assistant dark theme yet. The
  palette reads too pale, with too many light/opaque surfaces and not enough
  dark-theme transparency. The next visual pass should use Home Assistant theme
  tokens where possible, darker translucent layered surfaces, softer borders,
  and less white/pale green treatment so the app feels embedded in the HA dark
  UI rather than pasted over it.
- The Suggested Task Bundle card needs a typography pass. Font sizes and line
  heights should be revised relative to each other so the bundle title, reason,
  metadata chips, health/impact line, Task rows, and action buttons have a
  clearer hierarchy and do not feel mismatched. Apply this rule broadly across
  the app wherever similar content appears: headings, supporting text, chips,
  rows, timers, summaries, and buttons should use a consistent type scale and
  line-height system instead of one-off sizing.
- Remove `Ready Now` as a prominent user-facing title. It is an internal product
  and implementation term, not a label the user needs to see above the main
  greeting. The opening screen should lead with the greeting and context
  controls.
- Do not mention the specific Task Bundle name in the invitation/greeting text.
  The greeting should invite the moment and set tone; the Suggested Task Bundle
  card should carry the bundle title and specific recommendation details. Apply
  this broadly to future recommendation surfaces so headings and invitation copy
  do not repeat each other.
- Generate the Right Now greeting once when Right Now loads, and regenerate it
  only when the user changes meaningful top-level readiness context such as
  time or mood. The greeting should be mood/readiness aware and
  stay separate from the specific Task Bundle title. Do not change the greeting
  on every shuffle or ordinary recommendation swap unless the user's
  top-level context meaningfully changed. Let the bundle card carry
  recommendation-specific details.
- Remove redundant section labels when the UI object is already clear. For
  example, do not show `Suggested Task Bundle` above the suggested bundle card;
  the card title, content, and action should make its purpose obvious. Use status
  labels only when they add real state, such as a refining/loading message.
- Do not add a separate invitation line above the recommendation card title.
  The page-level greeting already sets the tone; the card should lead directly
  with the Task Bundle title, reason, metadata, included Tasks, and action.
- Place the randomize/shuffle control with the filters and context chips, not
  inside the recommendation card. It changes the suggestion inputs/result set,
  so it belongs with the controls for shaping the current moment. Apply this
  broadly to future recommendation surfaces.
- In recommendation cards, combine the Area and health-gain metadata into one
  scoped impact chip. For single-area Task Bundles, show the area and gain
  together, such as `Kitchen 24`. For mixed-area bundles, use a truthful
  whole-home or mixed-area scope, such as `Home 3`, rather than showing a
  separate area chip that competes with the health chip. Do not use
  before/after notation such as `57 -> 74`, and do not prefix the gain with
  `+`; the chip already communicates a positive projected gain.
- Do not prefix positive Keeps, health gain, impact gain, or other
  always-positive reward/gain values with `+`.
- Fold the Projected Impact into the primary recommendation action instead of
  showing it as a separate chip. Use a compact emphasis button: projected benefit
  on the left, action icon on the right, stronger background color than secondary
  controls. The button may use an accessible label such as `Start this bundle`,
  but visible text should emphasize the projected benefit, such as `Kitchen 24`
  and `Big kitchen boost`.
- Place the projected-benefit/start action in the suggested Task Bundle card
  header, aligned to the top-right of the title/reason block on wider screens.
  It should not sit below the visible Task list, because that list has variable
  height and makes the primary action drift.
- Do not hide the suggested Tasks behind an expand/details control in the
  suggestion card. A Task Bundle is a set of Tasks, so the card should show
  the bundle contents by default while keeping the layout compact enough to
  scan. Expansion can be reserved for deeper explanations elsewhere, not for
  revealing the core Tasks being suggested.
- Suggested Tasks in a Task Bundle should be selected by default. The user is
  accepting a pre-built recommendation, not assembling the bundle from scratch.
  Make included Tasks visibly checked/selected and let the user remove
  exceptions.
- Removed Tasks should stay visible in the suggested bundle with a clear
  removed visual style. Do not make them disappear from the card. Use muted
  treatment, a removed indicator, and an easy restore action so the user can
  understand what changed and reverse it in place. Do not also show a duplicate
  undo toast for the same row-level restore action.
- Across the app, when Homekeep can reasonably infer the intended value or input
  state, prefill it. Forms and setup controls should start from useful guessed
  defaults so the user confirms or adjusts instead of filling everything from a
  blank state. Guesses must remain visible, correctable, and never treated as
  irreversible user preference learning unless the user explicitly confirms
  that behavior.
- Icons inside chips should sit in a distinct centered icon background. Treat
  this as an icon slot: the icon is centered within its own small backing
  surface, and chip spacing should be adjusted around that slot. Do not force
  this treatment onto every button; action buttons may use a simpler icon when
  that reads better.
- Context chips should not repeat visible labels when the icon is
  self-explanatory. Show the icon and current value; keep the label as an
  accessible name and tooltip.
- Keep internal `Auto` values for Time and Area, but render them as `Best fit`
  in the user-facing chips and selectors.
- Make inferred/default chip values subtly quieter than explicit user-selected
  values so Homekeep's assumptions do not look like user choices.
- The visible Right Now filter row should stay lean: Time, Mood, Area, and
  shuffle. Do not bring back Energy or Goal unless live testing shows a real
  comprehension gap. Keep Mood visually central by placing it between Time and
  Area.
- When Mood changes, update hidden Capacity and Goal immediately before
  rescoring. Mood is the main visible readiness control.
- Time in Ready Now should default to automatic availability when calendar or
  context permits. Do not expose an explicit `all the time` option. If the user
  does not choose a duration, Mood Context/readiness should drive bundle length:
  `low` and `quiet` bias shorter, `focused` and `restless` bias useful
  mid-sized bundles, and `ready` can bias fuller Task Bundles.
- On Right Now, the default Area context should be automatic, not a preselected
  Area that looks user-chosen. Let the Recommendation Engine pick the best Area
  from Home Health, Staleness, time, inferred Capacity, Mood Context, and fit.
  If the user
  selects a specific Area, treat that as a strong explicit filter. The selected
  recommendation may still show the chosen recommendation Area in metadata, but
  the Area control itself should distinguish `Auto` from a user-selected Area.
- Add one compact fit explanation line in the suggested bundle card, such as
  `Picked for a quiet 10-minute task bundle in the Bathroom`. It should explain how
  visible filters and inferred readiness shaped the bundle without becoming a
  technical score breakdown.
- When Area is explicit, the fit line should acknowledge that choice directly,
  such as `Kept to Bathroom because you picked it.`
- Shuffle should respect the visible filters. It may vary hidden Goal/fit a
  little when Mood is `auto`, but explicit Time and Area choices should remain
  intact.
- Label the shuffle control as `Try another fit` in tooltip/accessibility copy.
- Removed physical Tasks should act as short-lived feedback. If the user
  removes a heavier or longer Task before starting, soften inferred Capacity
  for the next shuffle.
- Show an included-count indicator near Bundle Keeps after removal, such as
  `2 of 3 included`.
- If explicit filters overconstrain the suggestion, show a specific empty state,
  such as `Nothing fits Bathroom with this mood right now.`
- During Live Test 2, specifically check whether `Best fit` for Time and Area
  is understandable and whether the mobile layout still has comfortable vertical
  density.

Right-now card next-build recommendations:

1. Make the recommendation surface feel less like a conventional card. With
   Tasks visible by default, use darker translucent layering, softer borders,
   and fewer nested boxed rows so the bundle reads as one coherent suggestion.
2. Add a compact bundle count, such as `3 tasks · 15 min`, so the visible list
   feels intentional and the user understands the bundle size immediately.
3. Make selected Task indicators quieter than completion indicators. Included
   Tasks should read as selected/included, not already completed.
4. Keep removed Tasks visible but compact and clearly excluded, with restore
   available on the row.
5. Keep the primary button feeling like the next step. Visible text should lead
   with the projected benefit, while the right-side icon carries the action.
   The accessible label should still name the action.
6. Show Bundle Keeps information before the Task list in a quiet,
   compact treatment. When a Task is deselected, the UI should indicate that
   Bundle Keeps or projected benefit is no longer active instead of
   pretending the original bundle reward still applies. Do not show this as a
   negative number; the user has not lost received Keeps.
7. Tighten reason text so it answers `why this now?` in one short human
   sentence without repeating area, health, or bundle title information already
   shown elsewhere.
8. Use one visual rhythm for filters, read-only metadata, and action buttons:
   same design family, clearly different roles.
9. Recheck mobile scan order after the visual pass. The right-now card should
   still read naturally on a narrow screen: invite, title/reason, bundle size,
   included Tasks, projected-benefit action.

## MVP App View

The first app-view implementation should stay narrow:

1. Sidebar entry opens Homekeep.
2. Ready Now view supports Ready-Now Mode.
3. Ready Now view can render a Smart Task List response.
4. Starting a recommendation switches to active Task Session state.
5. Active Task Session supports complete, skip, pause, and end.
6. Completing the planned Tasks adds a short inline optional Task list.
7. The optional Task list is bounded and cannot chain indefinitely.
8. Overview sensors and To-do projections remain available to Home Assistant.

Plan / Scheduled Tasks and Home Health can follow once the Ready Now flow is
solid.

## Implementation Phases

### Phase A: Product Shape

- Confirm sidebar app view as the canonical UI direction.
- Remove former dashboard example references.
- Add acceptance criteria for the app-view Ready Now flow.

### Phase B: Home Assistant Frontend Assumptions

- Verify the supported custom panel or frontend extension approach against the
  installed Home Assistant package or official developer docs.
- Record any Home Assistant API constraints before implementation.
- Decide how the app view will call Homekeep services and receive action
  responses.

### Phase C: Ready Now View

- Build the sidebar app shell.
- Implement Ready-Now setup controls.
- Render Smart Task List results.
- Start a recommendation and store temporary UI identifiers only in the app
  view state.
- Switch into active Task Session controls.

### Phase D: Home Assistant Projections

- Keep Home Assistant sensors and To-do entities useful as projections.
- Avoid duplicating complex session state outside the app view.

### Phase E: Expand Views

- Add Home Health view.
- Add Plan / Scheduled Tasks view.
- Add Activity view.
- Add Settings and diagnostics only where they support real use.

## Open Questions

- Should the first sidebar app be bundled with the integration, or should it be
  a separate frontend package?
- Which Home Assistant frontend extension path is stable enough for the MVP?
- How much of the active session state should be refreshed from entities versus
  held from action responses?
- Should the sidebar app be bundled with the integration, or delivered as a
  separate frontend artifact?

## Non-Goals

- Do not replace Homekeep storage with frontend state.
- Do not make Home Assistant To-do entities the source of truth.
- Do not build a broad admin console before the Ready Now flow works.
- Do not turn Home Health into a punitive scorecard.
- Do not implement complex gamification for the MVP.
