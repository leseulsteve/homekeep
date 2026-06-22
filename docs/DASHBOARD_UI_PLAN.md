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
offer a small, explainable path into a Chore Session, make stopping feel
successful, and keep chores practical rather than punitive.

## User-Facing Text Direction

Homekeep should use a structured voice system, not random strings. Prominent
copy should be organized by message intent, adjusted to Mood Context, and drawn
from copy families with clear tone rules and repetition control.

See `docs/HOMEKEEP_VOICE_SYSTEM.md`.

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
2. Smart Chore List
3. Active Chore Session
4. Done for now / Bonus Chore ending
5. Home Health and Areas
6. Plan / Scheduled Chores
7. Add Chore
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

Do not implement the frontend until the Ready Now / Ready-Now Mode, Smart Chore
List, Active Chore Session, and Done for now / Bonus Chore workflows have
approved MVP behavior.

## Questions To Answer Before Implementation

The design review should answer these questions before code starts:

- What is the first screen a person sees when they open Homekeep?
- Does Homekeep lead with a recommended session, a readiness launcher, or both?
- How much explanation should a recommendation show before the user asks for
  more?
- During an active Chore Session, is the experience guided one step at a time,
  or shown as a compact list?
- How should "Done for now" feel successful?
- How visible should Home Health be on the main screen?
- Should Home Health be a score, a status, or mostly area-level language?
- Where should Plan / Scheduled Chores live in the navigation?
- How lightweight should Add Chore be in the first app version?
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
- mocked Chore Bundle shuffle and chip-driven suggestion changes
- mocked active Chore Session state
- mocked timer, completion feedback, final summary, and Bonus Chore reveal
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
-> complete / skip / snooze / end-session service calls
```

Temporary identifiers such as `snapshot_id`, `recommendation_id`,
`session_id`, and `session_item_id` belong in frontend memory for the active
flow. Homekeep storage remains the source of truth.

## Why An App View Fits The Product

Homekeep's core interaction depends on short-lived service response data:

- `snapshot_id`
- `recommendation_id`
- `session_id`
- `session_item_id`
- planned Chore surfacing state
- Bonus Chore state

A Homekeep app view can own the temporary UI state while leaving durable state
inside Homekeep storage. That makes the main workflow clearer:

```text
choose context
-> generate Smart Chore List
-> inspect reasons and Projected Impact
-> start a Chore Session
-> complete / skip / snooze
-> Done for now / One more
```

## Primary Workflows

This section is the working review log. Each workflow starts with a draft
direction and should be updated as Steve answers design questions.

### Ready-Now Mode

Status: under review.

The main screen should make Ready-Now Mode immediate. Use a hybrid layout:
Mood-aware greeting first, then the best suggested Chore Session, with an
"I'm ready" customization path available without making the screen feel busy.

Decision: Ready Now layout order should be:

```text
Greeting
Context chips
Suggested Chore Bundle
Compact Home Health / Area Health lines inside the bundle
```

This lets the screen start human, gives the user quick control over context,
then presents the best suggested Chore Bundle with health context attached to
the recommendation.

Decision: When a Chore Session is active, Ready Now should become the active
session view.

The user should not have to navigate to a separate screen to continue a session.
While a Chore Session is active, Ready Now should show the active session state.
After `Done for now`, Ready Now should return to the normal greeting, context chips,
and suggested Chore Bundle layout.

Decision: Visually, Homekeep should show only one active Chore Session at a
time.

The UI should not present multiple active sessions, stacked session cards, or a
session switcher in the Ready Now experience. If a session is active, Ready Now is about
that session until it ends. This applies to the mocked prototype and should
remain the default expectation for the real app unless a later workflow
explicitly introduces multi-session behavior.

Decision: If Homekeep cannot generate a suggested Chore Bundle, Ready Now should
show a gentle no-suggestion state.

The user should keep the same context chips visible so they can adjust time,
energy, mood, goal, or area. Do not show a refresh button. If applicable, the
normal shuffle/regenerate affordance can remain available, but the main recovery
path should be changing visible context.

Example:

```text
Nothing fits this moment yet.
Try changing the time, energy, or area.
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
-> confirm Chore Bundle
-> mocked active Chore Session
-> start Chores in any order
-> complete Chores
-> completed Chores collapse into summary
-> final Done for now / One more ending
-> return to Ready Now
```

The mocked flow should include visible Keeps, Chore-level start/complete
actions, the active Chore timer state, the small completion effect, and the
Done for now / One more ending. Backend service wiring can come later.

Mock behavior should preserve real usage expectations:

- bundle confirmation starts a plausible active session state
- only one Chore can be ongoing at a time
- starting a Chore changes its state to ongoing
- completing a Chore moves it into the completed summary
- the timer appears only while a Chore is ongoing
- `Done for now` is available only at the appropriate ending point
- `One more` reveals a plausible Bonus Chore
- disabled/no-op controls should be limited to features intentionally not wired
  in the first mock, such as backend redraw logic

Decision: The main shuffle button in the first mocked Ready Now prototype should
swap to another mocked Chore Bundle.

The shuffle button should not be a dead control in the Ready Now mock. It should
visually exercise the real usage expectation by changing the suggested bundle to
a second plausible mocked option. The mock does not need backend recommendation
logic, but it should make the layout, fuzzy/refining state, and replacement
bundle feel testable.

Decision: Context chip changes in the first mocked Ready Now prototype should
change the mocked suggestion.

The chips should not be decorative. When the user changes time, energy, mood,
goal, or area, the mock should show the inline selector, run the fuzzy/refining
state, and then swap to a plausible mocked suggestion that reflects the changed
context.

Decision: The first mocked Ready Now prototype should include `4-5` mocked Chore
Bundle variants.

The variants should cover different time, energy, mood, and area contexts so
shuffle and chip changes feel meaningful. They should use synthetic household
data only.

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

Decision: In the mocked Ready Now prototype, `One more` should reveal a mocked
Bonus Chore.

The Bonus Chore reveal can use synthetic data, but it should visually exercise
the intended flow: `One more` reveals the option, the Bonus Chore shows its
Keeps, and accepting it remains a separate action. The mock does not need real
backend redraw or eligibility logic yet.

Decision: The mocked Bonus Chore should include the random/redraw button
visually, even if it is a no-op.

The button should occupy its intended final position so the layout and
interaction feel can be evaluated. It can be disabled, no-op, or show a small
not-wired-yet tooltip in the first mock.

Mock data decisions:

- Use `4-5` Chore Bundle variants.
- Use mostly single-area bundles so Area Health impact is easy to understand.
- Include one multi-area bundle to test bundle-level area display and mixed-area
  behavior.
- Use realistic synthetic areas: `Kitchen`, `Entryway`, `Bathroom`, `Laundry`,
  and `Living room`.
- Use realistic synthetic chores such as `Clear dishes`, `Wipe counters`,
  `Take out compost`, `Shake entry rug`, `Reset bathroom sink`, `Start a small
  laundry load`, and `Clear coffee table`.
- Include varied bundle sizes: one short `5 min` bundle, a couple of `10-15
  min` bundles, and one fuller `20 min` bundle.
- Include varied moods/energy contexts: calm, tired, focused, and energized.
- Include Keeps per Chore and visible bundle bonus opportunities.
- Include Home Health and Area Health mock numbers that line up with the
  suggested bundle, such as `Home 74`, `Kitchen 48`, and `Kitchen +24`.
- Include one no-suggestion mock state.
- Include one mocked Bonus Chore with Keeps and a visible redraw button.
- Keep all data synthetic and privacy-safe.
- Avoid generic labels, lorem ipsum, fake entity IDs, private household details,
  and real calendar text.

Mock interaction decisions:

- Main shuffle swaps to a different mocked Chore Bundle.
- Context chip changes swap to a plausible mocked Chore Bundle after the
  fuzzy/refining state.
- Bundle confirmation starts the mocked active session.
- The mocked active session uses real-feeling Chore states: ready, ongoing,
  completed.
- Only one Chore can be ongoing at a time.
- The timer appears only while a Chore is ongoing.
- Completed Chores collapse into a small completed summary.
- `Done for now` returns to Ready Now after the mocked final summary.
- `One more` reveals the mocked Bonus Chore; accepting it is separate.
- Bonus Chore redraw can remain disabled/no-op in the first mock.

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
- gently frame the kind of Chore Session that may fit the moment
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
-> choose energy
-> optionally accept or override Mood: Auto
-> choose goal
-> generate Smart Chore List
-> start a Chore Bundle or single Chore
```

The UI should show only a few recommendations and make the reason for each one
clear without becoming a report.

Suggested Chore Session display:

- Show the collapsed version by default.
- The collapsed view should include an evocative Chore Bundle title, estimated
  time, compact context, short reason, primary bundle-selection action, shuffle
  action, and expand affordance.
- Do not show the full Chore Bundle contents by default. Let the user expand
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
- The main action on the suggested Chore Session should confirm the bundle
  selection. It should not imply that the user has started doing the first
  Chore yet.
- After the user confirms a bundle, Homekeep should move into an active Chore
  Session where the user can start or complete individual Chores in the order
  they choose.
- Expanded Chore Bundle details should show each Chore with its estimated time.
  The time estimate should help the user trust the overall session fit without
  making the list feel dense or managerial.
- Expanded Chore Bundle details should show the Keeps available for each Chore.
  Keeps should be visible while suggesting bundles, not only after completion.
- Bundle-level bonus Keeps should be shown at the bundle level, such as
  `+4 Keeps bonus`.
- Area display should be conditional. If all Chores in the bundle share the
  same Home Assistant Area, show that area at the bundle level only. If the
  bundle spans multiple Home Assistant Areas, show the relevant area on each
  Chore row so the user understands where each step happens.
- Expanded Chore rows should include a small pre-start remove affordance. This
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
- Removing a Chore before starting should happen instantly with an undo affordance,
  not a confirmation dialog. This keeps tuning fast and reversible.
- Do not include per-Chore swap in the MVP. Use the shuffle action when the user
  wants a different suggestion.
- By default, removing a Chore before starting should affect only the current
  unsaved suggestion. It should not automatically train future recommendations.
- The UI may offer an optional explicit preference signal, such as
  `Suggest this less in short sessions`, when the user wants Homekeep to
  remember a context-specific pattern. This should be user-chosen, reversible,
  and phrased as a preference rather than a punishment.
- The optional context-specific preference should live in the undo toast after a
  pre-start remove action. The toast should offer Undo first and a secondary
  preference action only when Homekeep can describe the context clearly.
- Preference examples may include `less in short sessions`, `less when energy
  is low`, `less for evening resets`, or `less in this Home Assistant Area`.
  Do not offer a context-specific preference when the context would be vague or
  misleading.
- The undo toast should disappear automatically after a short time. It should
  remain visible long enough for Undo to be usable, and should not block bundle
  confirmation.

Projected Impact direction:

- Make the benefit of a suggested Chore Session easy to understand at a glance.
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

- area improvement, such as `Kitchen +24`
- Home Health improvement, such as `Home +7`
- simple projected before/after, such as `Kitchen 48 -> 72`
- friendly impact label, such as `Visible lift`, `Small win`, or
  `Big kitchen boost`
- soft celebration after completion when projected impact is realized

Chosen impact presentation:

- Use a combination of numbers and friendly labels.
- Numbers provide satisfying progress and explainability.
- Labels make the impact feel human and easy to choose.
- Pair concise metrics with plain-language benefit, such as
  `Kitchen +24 · Big kitchen boost`.
- Keep the presentation compact enough for mobile.

Chore Bundle title direction:

- Titles should be evocative, memorable, and inviting.
- A user should be able to remember the title later.
- A user should feel that choosing the bundle is pleasant, not like accepting a
  punishment list.
- Titles should sound like a small household mission, reset, or useful moment,
  not a raw list of chores.
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

- `Kitchen Reset`
- `Tiny Trash Run`
- `Countertop Comeback`
- `Entryway Fresh Start`
- `Laundry Launch`
- `Quiet Bathroom Refresh`
- `Five-Minute Floor Rescue`
- `Evening Reset`

Draft greeting directions:

- `calm`: steady, low-pressure, quietly capable
- `focused`: direct, crisp, momentum-oriented
- `tired`: gentle, permission-giving, small-scope
- `overwhelmed`: grounding, simplified, one-step-at-a-time
- `energized`: upbeat, action-ready, still practical
- `unknown` or `auto`: neutral, welcoming, easy to steer

Example greeting pattern:

```text
Good evening. Want a small reset that fits your energy?
```

The greeting should not replace the core action. It should frame the Ready Now
screen and help the user feel met before choosing or starting a Chore Session.

Chosen direction:

- Ready Now uses a hybrid layout.
- Top: substantial Mood Context greeting.
- Middle: best suggested Chore Session or helpful empty state.
- Primary action: confirm the suggested Chore Bundle when available.
- Homekeep should auto-generate the best suggested Chore Session when the app
  opens, using inferred or default context.
- Secondary action: "I'm ready" or equivalent customization path for changing
  time, energy, mood, and goal before generating a Smart Chore List.
- Include a light shuffle action that regenerates the Smart Chore List using the
  current visible context. It should feel easy and low-pressure, not like rejecting
  Homekeep's recommendation.
- Visual style should evoke a modern voice assistant rather than a card-heavy
  dashboard.
- Bundle-selection action copy should come from a small set of string
  variations instead of one fixed label. The tone should be inviting and may
  adapt to Mood Context.
- Inferred/default context should be shown as compact chips with icons and
  colors, such as time, energy, Mood Context, and goal. Chips should make the
  current context easy to scan and adjust without turning Ready Now into a form.
- Tapping a context chip should open a small inline selector in place, not a
  full edit screen. The selector should have large enough touch targets, keep
  the user anchored on Ready Now, and refresh the suggestion after the value
  changes.
- When the user changes a chip, Homekeep should wait briefly before refreshing
  so the user can change another chip. This should feel like refining a search,
  not submitting a form.

Auto-generation behavior:

- Use safe inferred/default context when the user has not explicitly chosen
  time, energy, mood, or goal.
- Make the inferred/default context visible enough to correct quickly.
- Do not make the user answer setup questions before seeing the first useful
  suggestion.
- Refresh the suggestion when the user changes time, energy, mood, goal, or
  relevant home context.
- Use a short debounce-style refresh after chip changes. During the wait and
  refresh, show a lightweight searching/refining state so the user understands
  Homekeep is finding a better fit.
- If no useful suggestion exists, show a calm empty state and a customization
  path rather than a blank dashboard.

Refining state direction:

- Keep the current suggestion visible until the new result is ready.
- During refinement, the current best suggested Chore Session may become softly
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
- Regenerate the Smart Chore List with the current chip context.
- Use the same fuzzy/refining state while the new list is generated.
- Avoid punitive wording such as `reject`, `dismiss`, or `not good`.
- Avoid making shuffle the dominant action over confirming the suggested
  bundle.
- Keep shuffle always visible on the suggested session surface, including when
  details are expanded.
- Shuffle should regenerate immediately, even if the user has removed Chores
  from the current suggestion. Do not ask for confirmation.
- Consider mood-aware microcopy such as `Try another fit`, `Shuffle`, or
  `Find another`.
- Do not make shuffle copy jokey or attention-seeking.

Bundle-selection action copy directions:

- Use varied, human labels so the app does not feel mechanical.
- Maintain a substantial set of available strings for each major mood.
- Keep labels short enough for mobile buttons.
- Avoid pressure, guilt, or fake cheerfulness.
- Prefer softer labels for `tired`, `overwhelmed`, `calm`, and `unknown`.
- Allow more direct labels for `focused` and `energized`.

Draft bundle-selection action strings:

- `Choose this reset`
- `Use this bundle`
- `This works`
- `Set this up`
- `Let's use this`
- `Pick this one`
- `Ready this reset`

The app should choose from this set based on context, with enough variation to
feel alive but not random or distracting.

### Active Chore Session

Status: under review.

Once a Chore Session starts, the app should switch into a focused active
session view.

The active session should show all selected Chores, but gently highlight the
best first Chore. The user can start or complete Chores in any order. Homekeep
may suggest the next best step, but it must not lock the user into a sequence.

Active sessions should feel more dynamic and rewarding than the selection
screen. Use positive gamification, Keeps/effects, encouraging action text, and
a dynamic timer/chrono treatment where it helps the session feel alive.

Gamification direction:

- make progress visible and satisfying
- show Keeps, impact, or reward effects for completed Chores
- award Keeps per completed Chore and for completed bundles
- keep rewards positive and non-punitive
- make small Chores feel worthwhile
- never punish stopping
- never imply failure for skipping, snoozing, or ending
- avoid competitive pressure or streak-loss mechanics
- avoid arcade-like effects or noisy celebration
- connect rewards to Home Health, Area Health, Projected Impact, or session
  progress
- make completing the originally suggested Chore Bundle intact more rewarding
  than completing an edited bundle, without making edits feel wrong

Keeps direction:

- Use `Keeps` as Homekeep's lightweight positive reward currency.
- Frame Keeps as a small sign of love the home gives back when it is cared for,
  not as productivity points.
- Frame Keeps as coming from the home as a whole, not from individual Home
  Assistant Areas.
- Award Keeps for each completed Chore.
- Show Keeps per Chore when suggesting a bundle and when the session is active.
- Award a bundle completion bonus when all Chores in the confirmed bundle are
  completed. Show that bonus at the bundle level, such as `+4 Keeps bonus`.
- Award an extra intact-bundle bonus when the user completes the suggested
  bundle as originally proposed, with no pre-start removals.
- Do not subtract Keeps for removing, skipping, snoozing, ending, or stopping.
- Edited bundles can still earn Chore Keeps and a smaller bundle completion
  bonus.
- Keep Keeps math simple enough to explain in one line.
- Do not show a persistent running total of Keeps received in the active session
  MVP. Show Keeps per Chore and bundle bonus opportunities instead.
- Use Keeps sparingly in prose and avoid transactional overuse of `earned`.
- Prefer quiet reciprocal language, such as `The home gives a little back`.
- Keep Keeps visuals soft; avoid coins, trophies, badges everywhere, or
  scoreboard metaphors.

Best-first highlight direction:

- gently highlight the recommended first Chore
- explain the highlight briefly, such as `good first step`
- allow any Chore to be started first
- update the suggested next Chore after completions, skips, snoozes, or manual
  starts
- keep the highlight helpful, not commanding

Dynamic session elements:

- encouraging Start button copy for individual Chores
- visible session progress
- dynamic chrono/timer treatment
- completion effects that are satisfying but not excessive
- Keeps or impact gain display
- a clear Done for now path

Completion feedback:

- Completing a Chore should trigger a quick reward effect.
- The effect should be immediate, satisfying, and lightweight.
- Do not interrupt the user with a full summary after every Chore.
- Show Keeps or impact gained briefly, then return focus to the remaining
  Chores and suggested next step.
- Respect reduced-motion preferences in the eventual implementation.
- Completed Chores should collapse into a small completed summary instead of
  staying as full checked-off rows. The summary should preserve progress and
  reward context without cluttering the active list.
- The completed summary should include completed Chore names and Keeps received,
  not only a count.
- The completed summary should be collapsed by default, showing a count with
  expandable details for completed Chore names and Keeps received.

Completed-bundle ending:

- After the final planned Chore is completed, keep the user in the active
  session ending state with `Done for now` and `One more` choices visible.
- Do not automatically exit the user from the flow.
- Make `Done for now` feel successful.
- Make `One more` inviting by showing the chance for the home to give a little
  more back, without
  making stopping feel like a loss.
- Use positive momentum language, not pressure.
- Tapping `One more` should immediately show the Bonus Chore and its Keeps.
  Do not add an extra confirmation step before revealing the option.
- Revealing a Bonus Chore and accepting it should be separate actions.
  `One more` reveals the option; the user must explicitly accept before it
  becomes active.
- Do not add a separate `No thanks` action for the Bonus Chore. `Done for now`
  remains the way to stop.
- The revealed Bonus Chore should include its own compact randomize/redraw
  button so the user can ask for a different Bonus Chore before accepting.
  This should feel lightweight and low-pressure, like the main shuffle action.
- Bonus Chore redraw should use the same fuzzy/refining state as the main
  suggestion shuffle, scoped to the Bonus Chore offer.
- Bonus Chore redraw is future product behavior that may require backend
  service/runtime support. Do not assume it already exists.
- Bonus Chore redraw should bias toward useful overdue Chores when they fit the
  current context, especially small tasks with high Projected Impact.
- Overdue bias must preserve the light `one more` feeling. Do not offer large
  overdue Chores that feel like a second session unless a tiny/light variant is
  available.
- Do not offer Chores the user just removed, skipped, snoozed, or dismissed.
- Do not use guilt-based overdue language. Phrase overdue Bonus Chores as
  positive opportunities, such as `one small overdue win`, not as obligations.

Done for now summary:

- Tapping `Done for now` should show a short final celebration/summary before
  returning to Ready Now.
- The summary should feel positive and complete, not like a report card.
- Include completed Chores, Keeps received, bundle bonus if received, and friendly
  Home/Area impact where available.
- Keep it brief enough to read at a glance.
- Make stopping feel like success.
- After a short moment, the summary should return the user to Ready Now
  automatically. It should not require a close/return tap.
- Do not include a share, log, or `View details` option in the MVP final
  summary. Keep it ephemeral. Detailed history can live later in Activity.

Timer behavior:

- The active session timer should run only when a Chore is `ongoing`.
- Confirming a bundle should not start the timer.
- Viewing, reordering mentally, choosing, pausing, or deciding what to do next
  should not count as active chore time.
- When no Chore is ongoing, show the session as ready or paused rather than
  timing the user.
- The timer should support the user, not pressure them.
- Pause should be combined with the Chore Session timer/chrono control. When
  the user pauses, Homekeep pauses the current ongoing Chore rather than
  presenting Pause as a separate primary action.
- The timer should clearly show paused state and offer a simple way to resume
  the same Chore.
- Completing a Chore should use a separate prominent Complete button. Stopping
  or pausing the timer should not be overloaded with completion choices.

Required actions:

- complete
- skip
- snooze
- pause
- end
- Done for now
- One more, when a Bonus Chore is available

Action visibility:

- Start and Complete should be the prominent Chore-level actions.
- Skip and Snooze should be tucked behind a secondary or overflow action.
- Skip and Snooze must remain available, but they should not dominate the active
  session UI.
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
- chores that are stale enough to matter
- Projected Impact from the offered Chore Session

Health should be presented as useful context, not a grade.

Decision: Home Health and Area Health should include visible numbers.

The number should provide clarity, progress, and quick comparison. It should not
feel like a grade on the user. Pair the number with friendly household language
so the meaning is obvious without making the screen clinical.

Decision: Home Health and Area Health use a `0-100` scale where higher is
healthier.

Area Health should communicate `how much would this area benefit from care
right now?` rather than `what percent of chores are done?` It is a household
status signal, not a personal score. In MVP, the score comes from the derived
health of enabled Chores in that Home Assistant Area, weighted by each Chore's
health impact and driven mostly by Staleness.

Preferred presentation:

- whole-home health number with a friendly status label
- area health numbers for the areas that matter most right now
- short area-level language beside the number, such as `Kitchen could use care`
  or `Entryway is holding steady`
- small area trends where useful
- projected improvement numbers when a suggested Chore Bundle would help an
  area, such as `Kitchen +24`

Suggested Area Health labels:

- `90-100`: `Fresh` or `Feeling good`
- `75-89`: `Holding steady`
- `60-74`: `Starting to build up`
- `40-59`: `Could use care`
- `0-39`: `Needs a reset`

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
Kitchen 48 · +24 with this reset
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

The whole-home number gives the satisfying sense that the home is being cared
for. The area number explains why the current Chore Bundle matters. The UI
should avoid turning this into a large dashboard section.

Recommended Ready Now treatment:

```text
Home 74 · Mostly steady
Kitchen 48 · This reset helps most
```

Recommended expanded-bundle treatment:

```text
Kitchen 48 -> 72 · Big kitchen boost
```

Decision: On Ready Now, the compact Home Health and Area Health treatment should
live inside the suggested Chore Bundle, visible in the collapsed bundle state.

This keeps health context directly attached to the recommendation it explains.
It also prevents Ready Now from becoming a dashboard made of separate health cards.
The treatment should read as a small support line inside the suggestion, not as
a standalone analytics section.

Recommended collapsed bundle structure:

```text
Evening Kitchen Reset
12 min · calm · Kitchen
Home 74 · Mostly steady
Kitchen 48 · This reset helps most
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

Decision: The `Home Health` view should be organized primarily as a
list of large Home Assistant Area cards.

Use a scannable card list rather than a home map, room diagram, or pure ranked
`needs care most` view. Each Home Assistant Area should have a large enough
card to show the area number, status, small trend, and useful detail without
feeling cramped. The list may still sort or highlight areas that need care, but
the user's mental model should remain `these are the areas of my home`.

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
- next upcoming Chore for healthy areas
- one main contributing Chore for areas below `70`, plus a compact `more ways
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
Clear dishes · +14
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
- hiding an Area should not delete existing Chores or change Home Assistant
  itself
- use safe neutral copy such as `Hide from Home Health`

Decision: Newly created Home Assistant Areas should be automatically taken in
charge by Homekeep.

Homekeep should not require a separate manual area import step. When a new Home
Assistant Area appears, Homekeep should include it in Home Health by default,
subject to the user's hidden-area configuration.

Decision: Hidden Areas should be considered unmanaged by Homekeep.

When an Area is hidden in Homekeep configuration, Homekeep should not use that
Area for Home Health, Area Health, Ready Now suggestions, Bonus Chores, or
Homekeep-managed direct care actions. The Area may still exist normally in Home
Assistant, but it is outside Homekeep's managed care surface.

Unmanaged Area rules:

- exclude from Home Health cards
- exclude from whole-home health calculations where practical
- exclude from recommendation and Bonus Chore eligibility
- exclude from Homekeep UI emphasis and area health summaries
- do not delete or modify the Home Assistant Area
- mark existing Homekeep Chores in that Area inactive, not deleted

Decision: Chores in hidden/unmanaged Areas should become inactive and
recoverable.

When a managed Area is hidden from Homekeep, existing Homekeep Chores assigned
to that Area should become inactive. They should not be suggested, shown as
active care opportunities, or counted toward Home Health while the Area is
unmanaged.

If the user re-includes the Area in Homekeep later, those inactive Chores should
be recoverable and can become active again. Homekeep should preserve enough
metadata to restore them without forcing the user to recreate their chore setup.

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
- reselecting an Area makes it managed again and can recover inactive Chores
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

Decision: Area cards below `70` should show one main contributing Chore plus a
small `more ways to help` line.

A contributing Chore is a Chore that is currently pulling the Area Health down
or would provide a clear Projected Impact if completed. It should be explainable
through Staleness, Area Health impact, Projected Impact, or a useful small
variant.

Show the top contributing Chore visibly so the card has a clear next action.
Represent the remaining contributors as a compact line, such as `2 more ways to
help`, rather than listing every Chore by default. This keeps the cards calm and
scannable while still indicating that the area has more useful care options.

Decision: Tapping `2 more ways to help` should expand the extra Chores inline
inside the Area Health card.

Do not open a separate Chore list view for this interaction. Inline expansion
keeps the user in the area context and makes the extra options feel like
supporting details, not a second workflow.

Inline expansion should show the remaining contributing Chores compactly:

```text
2 more ways to help
Wipe counters · +8
Take out compost · +6
```

Tapping any expanded Chore should open that Chore's details, with the same
direct single-Chore start rules as the main contributing Chore.

Decision: Inline extra Chores should collapse again when another Area card's
`more ways to help` section is expanded.

Only one Area card should show expanded extra Chores at a time. This keeps the
vertical Home Health view calm and prevents multiple area cards from growing
into a long chore list.

Decision: Area cards should be open by default with details visible.

The Home Health view should feel substantial and immediately useful, not like a
collapsed index that requires opening each area. Cards can still use visual
hierarchy to keep the page scannable.

Open card details:

- areas below `70` show one main contributing Chore and a compact `more ways to
  help` line
- healthy areas show recent care and next upcoming Chore
- all cards keep the number, status label, and small trend visible
- details should stay compact enough that the list remains easy to scan

Decision: Only areas below a certain health threshold should show contributing
Chore details.

Healthy areas should not be forced to expose contributing Chores because that
can make the whole home feel like a problem list. When an area is healthy, its
card can simply show the number, friendly status, and recent care or steady
state.

Decision: Show contributing Chore details for areas below `70`.

This keeps the area list calmer. Areas can show `Starting to build up` without
immediately exposing a chore breakdown, while lower-health areas show the
specific Chores that would help.

Contributor explanations should stay short and inspectable. Prefer reasons
that connect directly to derived Homekeep values:

- the Chore is stale enough to pull the area down
- the Chore has high Area Health impact
- the Chore offers clear Projected Impact for the area
- a small variant would provide useful care without turning the area into a
  problem list

Avoid explanations that sound like judgment, diagnosis, or a hidden model the
user cannot correct. `Kitchen could use care because counters are overdue` is
better than `Kitchen health is poor due to neglected maintenance`.

Decision: All areas should be expandable.

Areas at `70+` should still be expandable for context, but they should not show
contributing Chore details unless they drop below `70`. Healthy area expansion can
show steady-state information, recent care, or why the area is doing well.

Decision: Healthy expanded areas should show both recent care and the next
upcoming Chore.

Recent care explains why the area is healthy. The next upcoming Chore gives
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
Clear dishes · +14
Wipe counters · +8
Take out compost · +6
```

Decision: Tapping a contributing Chore should open Chore details only.

The Chore details view should include a button to start that Chore directly as
a single-Chore flow. This direct start should not generate a Chore Bundle, and
it should not offer a bundle bonus.

This keeps Area Health exploratory first. The user can understand why the Chore
matters before acting, but still has a clear direct path if they want to care
for that area immediately.

Direct Chore start from Area Health:

- starts only the selected Chore
- does not create a suggested bundle around it
- does not include bundle bonus Keeps
- can still show the Chore's own Keeps and Projected Impact
- should show a small `Done for now` / `One more` ending when finished
- should not interrupt an active Chore Session without a clear confirmation
  state

Direct Chore details should use a softer primary action label than
`Start this Chore`.

Preferred label direction:

- `Do this now`
- `Take care of this`
- `Care for this`
- `Help this area`

The label should still be clear that tapping it begins the selected Chore
directly. Avoid labels that imply a bundle, such as `Start reset` or
`Choose this bundle`.

Decision: Home Health should stay focused on Chore details and direct
single-Chore starts.

Do not add a primary action to generate a Chore Bundle from a selected area in
the Home Health view. Bundle generation should stay centered in Ready Now /
Ready-Now Mode and the Smart Chore List flow.

The Home Health view should help the user inspect areas, understand what is
affecting health, and optionally act on a single Chore. It should not become a
parallel recommendation builder.

Decision: Each Area Health card should have a primary visible action like
`Care for this area`.

The primary area action should make the card feel actionable at a glance. It
should help the user move from understanding an area's health to helping that
area.

Decision: Tapping `Care for this area` should open the top contributing Chore
details directly.

This gives the user one clear next step from an area card. The Chore details
view can explain why that Chore helps the area and offer the soft direct start
action. It must not silently create a Chore Bundle or imply bundle bonus Keeps.

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
opens the next upcoming Chore details.

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

Decision: After finishing a single Chore started from Area Health, Homekeep
should show a small `Done for now` / `One more` ending first.

This ending should be lighter than the full suggested-bundle ending because the
user completed a single direct Chore, not an intact Chore Bundle.

Single-Chore ending rules:

- show completion feedback for the Chore
- show the Chore's Keeps received
- show `Done for now` and `One more`
- do not show bundle bonus Keeps
- let `Done for now` return to the previous Area Health context or Ready Now
- let `One more` offer a small eligible Bonus Chore, using the same optional
  Bonus Chore model as other endings
- keep the copy low-pressure and clear that stopping is successful

Decision: `One more` after a single Area Health Chore may choose from any
eligible area, but should tilt toward the current area.

The current area should receive a preference boost because the user is already
thinking about that part of the home. This should not be a hard filter. If a
better small eligible Bonus Chore exists elsewhere, Homekeep may offer it.

Bonus Chore eligibility from Area Health should consider:

- current area preference
- low effort fit
- high Projected Impact
- overdue care when it still feels light
- recent skips, snoozes, removals, and dismissals
- whether the Chore was just completed

Avoid offering another Chore in the same area if it would make the flow feel
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

### Plan / Scheduled Chores

Status: draft.

Plan should feel like setting aside intentional future care, not generating a
Smart Chore List for later.

```text
Plan
-> choose a future time
-> choose or create set Chores
-> optionally group them into a planned care item
-> save the planned Chores
-> surface them on Ready Now when relevant
```

Decision: Users should not plan generated Smart Chore Bundles for the future.

Generated Chore Bundles belong to Ready Now / Ready-Now Mode, when the user is
actually ready to do household care. If the user wants a generated bundle, they
should wait until they are ready and use Ready Now.

Plan is for set Chores or planned household projects the user already knows
they want to do, such as painting the house Saturday morning.

Decision: Plan should support longer project-style Chores, while Ready Now
stays focused on short generated care bundles.

Ready Now answers `what can I do right now?` with generated, context-aware
Chore Bundles. Plan answers `what do I already know I need or want to do
later?` with intentional set Chores or projects. Plan may include longer work
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

Planned Chores should not silently start. When the planned time is near, Ready Now
can surface them as intentional planned work.

Decision: Planned Chores should appear on Ready Now only when they are relevant
soon, but creation and management should live in Plan.

Ready Now should surface saved planned Chores when they are close and actionable,
such as `Painting is planned for Saturday morning`. The full workflow for
creating, inspecting, editing, deleting, and managing planned Chores belongs in
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

### Add Chore

Status: draft.

Adding a Chore should be available from the Homekeep app, but it should not
interrupt an active Chore Session.

`homekeep.create_chore` creates a durable Chore definition. It must not rely on
Home Assistant To-do create write-through, and it must not create a Chore
Session by itself.

Questions to settle:

- Should Add Chore start as a quick capture field, a full structured form, or a
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
- reselecting an Area can recover inactive Chores for that Area
- changes affect Homekeep behavior only; they do not modify Home Assistant
  Areas

Decision: Managed Areas changes should require a `Save` button.

Selecting or unselecting Areas should update the pending settings state, but
Homekeep should not apply management changes until the user saves. This makes
the choice intentional, especially because unselecting an Area makes it
unmanaged and marks its Homekeep Chores inactive.

The Settings UI should clearly distinguish pending changes from saved Homekeep
behavior.

Decision: Saving Managed Areas changes that remove Areas should show a
confirmation message before applying.

The confirmation should explain the consequence plainly: removed Areas become
unmanaged by Homekeep, and existing Chores in those Areas become inactive but
recoverable if the Area is managed again later. The confirmation should not
sound alarming because the change is reversible.

Example confirmation:

```text
Remove 2 areas from Homekeep?
Their chores will become inactive, but they can come back if you manage those
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
- default time and energy preferences

Keep notifications, deeper privacy controls, and advanced planning behavior for
later unless they become necessary during implementation.

## Proposed Information Architecture

### Ready Now

The default view.

Purpose:
: Decide what to do now.

Contains:

- Ready-Now setup
- current Smart Chore List
- active Chore Session, when present
- Done for now / One more ending flow

### Home Health

Purpose:
: Check Area Health and see what can be done to help.

Contains:

- large whole-home health header
- one vertical column of large Home Assistant Area cards
- Area Health number, status, trend, and health-based tint
- Home Assistant configured Area icon
- one main contributing Chore for areas below `70`
- compact `more ways to help` inline expansion
- direct Chore details and single-Chore starts

Does not contain:

- bundle generation from an Area
- Ready Now health-line navigation
- refresh buttons
- Area management controls

### Plan

Purpose:
: Create and manage intentional future Chores and household projects.

Contains:

- target time window input
- planned set Chores
- planned household projects
- optional Home Assistant Area
- saved planned items
- Ready Now surfacing when relevant

Does not contain:

- generated Smart Chore Bundle planning
- Recommendation Engine bundle proposals for the future
- refresh buttons

### Activity

Purpose:
: Review recent household care without turning it into a scoreboard.

Contains:

- recent Chore completions
- recent Chore Sessions
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
- default time and energy preferences

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
- Make the active Chore Session visually distinct from planning and history.

The interface should feel more like a gentle operational panel than a decorative
landing page.

## MVP App View

The first app-view implementation should stay narrow:

1. Sidebar entry opens Homekeep.
2. Ready Now view supports Ready-Now Mode.
3. Ready Now view can render a Smart Chore List response.
4. Starting a recommendation switches to active Chore Session state.
5. Active Chore Session supports complete, skip, snooze, and end.
6. Done for now is always a valid success state.
7. One more uses Bonus Chore lifecycle and cannot chain indefinitely.
8. Overview sensors and To-do projections remain available to Home Assistant.

Plan / Scheduled Chores and Home Health can follow once the Ready Now flow is
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
- Render Smart Chore List results.
- Start a recommendation and store temporary UI identifiers only in the app
  view state.
- Switch into active Chore Session controls.

### Phase D: Home Assistant Projections

- Keep Home Assistant sensors and To-do entities useful as projections.
- Avoid duplicating complex session state outside the app view.

### Phase E: Expand Views

- Add Home Health view.
- Add Plan / Scheduled Chores view.
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
