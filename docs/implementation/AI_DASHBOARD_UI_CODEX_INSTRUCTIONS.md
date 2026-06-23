# Dashboard UI Codex Instructions

This file translates the current Homekeep app design state into future Codex
implementation instructions. It is intentionally stricter and more operational
than `docs/product/HOMEKEEP_APP_PLAN.md`.

This file is currently scoped for a Ready Now-only test implementation. The first
frontend pass may use mocked Ready Now data so Steve can quickly evaluate the app
feel before backend wiring is complete. Do not implement the full dashboard app
from this file. Later workflow decisions are still intentionally undocumented.

Treat `docs/product/HOMEKEEP_APP_PLAN.md` and `docs/product/HOMEKEEP_VOICE_SYSTEM.md` as the
human product source.

## Non-Negotiables

- Lovelace is not part of the plan.
- Do not create, restore, ship, test, or document Lovelace dashboard templates.
- Do not implement the Homekeep app as an iframe.
- Homekeep storage remains the source of truth.
- Home Assistant To-do entities remain projections.
- The frontend may hold temporary action-response identifiers, but it must not
  become durable state.
- The app must feel like a modern assistant-style Home Assistant sidebar app,
  not a card-heavy admin dashboard.
- The app must be warm, varied, and quiet by default. Avoid chatty, jokey, or
  attention-seeking copy.
- The app voice should act like a care companion for the home, not a coach for
  the person.
- Keep gamification positive and non-punitive.
- Follow `docs/product/HOMEKEEP_VOICE_SYSTEM.md` for all user-facing text.

## Required Pre-Implementation Checks

Before coding the frontend, Codex must:

1. Verify the supported Home Assistant sidebar/custom panel/frontend extension
   approach against the installed Home Assistant package or official developer
   docs.
2. Record the chosen frontend approach in `docs/product/HOMEKEEP_APP_PLAN.md` or a
   follow-up implementation note.
3. Confirm the app is not iframe-embedded.
4. Identify how the frontend calls Homekeep services and receives action
   responses.
5. Identify how the frontend refreshes entity/projection state after service
   calls.
6. Identify how temporary UI identifiers are stored in the app during a flow:
   `snapshot_id`, `recommendation_id`, `session_id`, and `session_item_id`.
7. Identify tests or source checks for the selected frontend registration
   approach.

If the Home Assistant frontend API conflicts with this plan, stop and document
the conflict before coding.

Verification note:

- On 2026-06-22, the local Python environment did not include an importable
  `homeassistant` package.
- The first mocked Ready Now prototype therefore verified the sidebar panel path
  against official Home Assistant source for
  `frontend.async_register_built_in_panel`, `panel_custom`, and
  `http.StaticPathConfig`.
- The selected path serves
  `custom_components/homekeep/frontend/homekeep-panel.js` through
  `hass.http.async_register_static_paths(...)` and registers a non-iframe
  custom panel through `frontend.async_register_built_in_panel(...)`.

## Current Product State

The current approved design work covers enough to prototype and test:

- Ready Now / Ready-Now Mode
- Smart Chore List presentation
- suggested Chore Bundle selection
- active Chore Session behavior
- inline optional Chores after planned session completion
- Homekeep Voice System

It does not mean the whole dashboard is planned. The current implementation is
ready for a live-feel test of the mocked Ready Now slice only.

Implementation boundary:

- Implement only the Ready Now test slice first.
- A fast mocked Ready Now prototype is acceptable before real service wiring.
- Do not implement Home Health and Areas beyond what Ready Now needs to display
  Projected Impact or a small context hint.
- Do not implement Plan / Scheduled Chores.
- Do not implement Add Chore.
- Do not implement Activity.
- Do not implement Settings or diagnostics.
- Do not implement the full navigation model.
- Do not treat unresolved workflow placeholders as permission to invent
  behavior.
- Treat live-test feedback as input for the Ready Now prototype and future
  planning, not as approval to wire or build unplanned dashboard areas.

Later workflow decisions are partially documented, but they are not part of the
first implementation slice. The next workflow review should continue from:

```text
Plan / Scheduled Chores
```

Current Plan decision:

```text
Plan is for intentional future Chores and household projects, not generated
Smart Chore Bundles.
```

## Ready Now Test Slice Requirements

The Ready Now screen is the default Homekeep app surface.

Fast mock prototype scope:

- Use mocked Ready Now suggestion data.
- Use mocked Chore Bundle contents.
- Use mocked Keeps values.
- Use mocked Projected Impact.
- Use mocked Mood Context and chip values.
- Buttons should be visible and feel clickable.
- The mocked live session must correspond to realistic live usage, using
  synthetic data but real-feeling state transitions.
- Bundle confirmation must transition into a full mocked active session.
- Visually show only one active Chore Session at a time.
- Chore Start and Complete must update local mock UI state.
- Completed Chores must stay visible as near-normal Chore rows with a soft
  congratulatory done state.
- The mocked session must include the active Chore timer state.
- The mocked session must include a quick completion effect.
- Completing the final planned Chore must add a short list of optional Chores
  directly into the active session list.
- The old `Done for now` / `One more` choice pair must not appear immediately
  after the planned Chores are completed.
- The optional Chores can use mocked synthetic data; backend eligibility/redraw
  behavior does not need to be wired yet.
- The main shuffle button must swap to another mocked Chore Bundle in the first
  mock prototype.
- Shuffle should visually exercise the fuzzy/refining state, even with mocked
  data.
- Context chip changes must update the mocked suggestion after the
  fuzzy/refining state, using plausible synthetic variants.
- Include `4-5` mocked Chore Bundle variants covering different time, inferred
  Capacity, mood, and area contexts.
- Always use realistic synthetic household mocks, never placeholders such as
  `Area 1`, `Task 1`, or lorem ipsum.
- Use mostly single-area mocked bundles, plus one multi-area bundle to test
  mixed-area display behavior.
- Include varied mocked bundle durations: one short `5 min`, a couple of
  `10-15 min`, and one fuller `20-25 min` option.
- Include realistic synthetic areas such as `Kitchen`, `Entryway`, `Bathroom`,
  `Laundry`, and `Living room`.
- Include realistic synthetic chores such as `Clear dishes`, `Wipe counters`,
  `Take out compost`, `Shake entry rug`, `Reset bathroom sink`, `Start a small
  laundry load`, and `Clear coffee table`.
- Include mocked Home Health and Area Health numbers that align with the
  selected suggestion and Projected Impact.
- Include one mocked no-suggestion state.
- Use realistic synthetic copy and no private household/calendar details.
- Clearly document what is mocked versus wired to Homekeep services.

It must:

- use a hybrid layout
- show a substantial Mood Context greeting first
- generate the Right Now greeting from top-level readiness context, not from the
  selected Chore Bundle title
- keep the greeting stable through shuffle unless time or mood changes
  meaningfully
- auto-generate the best suggested Chore Session on open
- use inferred/default context when the user has not chosen values
- show context as compact colored chips with icons and the current value; avoid
  visible labels when the icon is self-explanatory, but keep accessible labels
  and tooltips
- keep internal `Auto` values, but render them as `Best fit` in the Time and
  Area chips/selectors
- visually distinguish inferred/default chip values from explicit user-selected
  chip values without adding visible labels
- keep the visible filter row lean and ordered as Time, Mood, Area, then
  shuffle; this keeps Mood visually central without adding another label
- default Time to automatic availability when the user has not chosen a
  duration; do not expose an explicit `all the time` option
- make Mood Context/readiness drive bundle length when Time is automatic:
  `low`/`quiet` bias shorter, `focused`/`restless` bias mid-sized useful
  resets, and `ready` can bias fuller bundles
- do not show Energy as a top-level Right Now chip for Live Test 2; keep
  Capacity internal and infer it from Mood Context as
  `auto -> auto`, `low/quiet -> low`, `focused -> steady`,
  `restless -> mobile`, and `ready -> strong`
- score Capacity against effort, movement, setup friction, duration, and
  interruption tolerance; `low` should stay short and contained, `mobile` can
  include movement/light carrying, and `strong` can include fuller physical care
- do not show Goal as a top-level Right Now chip for Live Test 2; keep Goal
  internal and infer it from Mood Context as `auto -> visible lift`,
  `low -> quick wins`, `quiet -> fresh start`, `focused -> overdue care`,
  `restless -> visible lift`, and `ready -> overdue care`
- show Area as automatic by default, not as a user-selected Area
- treat a specific user-selected Area as an explicit recommendation filter that
  strongly constrains the recommendation
- add a compact fit explanation line in the suggested bundle card, such as
  `Picked for a quiet 10-minute reset in the Bathroom`
- when Area is explicit, make the fit line acknowledge the user choice, such as
  `Kept to Bathroom because you picked it.`
- let shuffle respect the visible filters; when Mood is `auto`, shuffle may
  vary hidden Goal/fit slightly, but explicit Time/Area choices must remain
  intact
- title the shuffle control as `Try another fit`
- use removed physical Chores as short-lived feedback: if a heavier/longer
  Chore is removed before session start, soften inferred Capacity for the next
  shuffle
- include a filter-specific no-suggestion state when explicit filters overconstrain
  the result, such as `Nothing fits Bathroom with this mood right now.`
- during live review, check whether `Best fit` for Time and Area is understood
  and whether mobile vertical density remains comfortable
- let each chip open a small inline selector
- center chip icons inside a distinct icon-slot background, with spacing
  adjusted for that layout; do not force this treatment onto action buttons
  where the simpler icon reads better
- wait briefly after chip changes before refreshing, so multiple changes can
  settle together
- keep the current suggestion visible while refining
- use a fuzzy/blurred suggestion state plus a small status line while refining
- avoid an assistant orb/pulse in MVP
- include one always-visible shuffle button
- in the final wired version, regenerate immediately on shuffle without
  confirmation

For the first mocked prototype, the main shuffle button must work visually by
swapping to a second mocked Chore Bundle. It does not need backend
recommendation logic, but it should use the intended final position and exercise
the fuzzy/refining state.

The Ready Now screen must not:

- make the user answer setup questions before seeing a suggestion
- show a grid of dashboard cards as the first impression
- duplicate the shuffle button
- use an iframe
- use Lovelace

For the first implementation, Ready Now may be the only meaningful app screen.
Stub, hide, or defer navigation to later workflows.

## Suggested Chore Bundle Requirements

The suggested Chore Bundle shows its core Chores by default.

Default display must include:

- evocative Chore Bundle title
- compact bundle count and estimated total time
- scoped health context when it explains the recommendation
- short reason
- included Chores
- removed Chores, if any, with removed styling and restore
- full-reset Keeps footer
- compact projected-benefit action

Do not hide the core Chores behind an expand/details control. A Chore Bundle is
the set of Chores the user is choosing, so the list should be visible by
default. Expansion can be used later for deeper explanations, but not for
revealing the core bundle contents.

The randomize/shuffle control belongs with the context chips, not inside the
suggestion card.

The main action confirms bundle selection. It must not imply the user has
started doing the first Chore. Visible button text should emphasize Projected
Impact, with an action icon on the right and an accessible action label.

Avoid labels like a hard `Start now` here. Use bundle-selection language such
as:

- `Choose this reset`
- `Use this bundle`
- `This works`
- `Set this up`
- `Let's use this`
- `Pick this one`
- `Ready this reset`

## Chore Bundle Titles

Chore Bundle titles must be:

- evocative
- memorable
- inviting
- restrained
- truthful
- short
- easy to say out loud

Titles should sound like a small household mission, reset, or useful moment,
not a raw chore list.

Example directions:

- `Kitchen Reset`
- `Tiny Trash Run`
- `Countertop Comeback`
- `Entryway Fresh Start`
- `Laundry Launch`
- `Quiet Bathroom Refresh`
- `Five-Minute Floor Rescue`
- `Evening Reset`

## Bundle Detail Requirements

Bundle details live inside the suggestion.

Bundle details must:

- keep the user anchored on Ready Now
- show only the selected suggested bundle
- not show alternate suggestions underneath
- fold Projected Impact into the primary projected-benefit action
- place the projected-benefit/start action in the suggestion card header,
  aligned to the top-right of the title/reason block on wider screens, so it
  does not move below a variable-height Chore list
- show each Chore with estimated time
- show Keeps per Chore
- show full-reset Keeps, such as `4 Keeps for the full reset`, before the Chore
  list so the offer is visible before scanning individual Chores
- include an included-count indicator near the full-reset Keeps after removal, such
  as `2 of 3 included`
- conditionally show Home Assistant Area

Area display rule:

- if all Chores share one Home Assistant Area, combine area and health gain in
  one scoped metadata chip, such as `Kitchen 24`
- do not use before/after notation such as `57 -> 74` in the Right Now metadata
  chip, and do not prefix the gain with `+`; the gain is always positive
- if the bundle spans multiple areas, show each Chore row's area

## Pre-Start Editing

Suggested Chore rows may include remove only.

Do:

- make remove secondary
- use icons with accessible labels
- remove instantly with row-level restore
- keep removed Chores visible with removed styling
- provide row-level restore
- recalculate time and Projected Impact after removal
- show full-reset Keeps or projected-benefit no-longer-active treatment when
  applicable, without negative numbers
- keep the original recommendation recoverable through shuffle or visible
  context changes
- do not show an undo toast when row-level restore is already visible

Do not:

- add per-Chore swap in MVP
- ask for confirmation before removal
- automatically train recommendation learning from removal
- allow edits that break service/session validity

Row-level restore:

- remains visible as long as the removed Chore remains in the suggested bundle
- should be visually secondary but easy to find
- should not be duplicated by a temporary undo toast

Example preference actions:

- `Suggest this less in short sessions`
- `Suggest this less when Capacity is low`
- `Suggest this less for evening resets`
- `Suggest this less in this area`

Do not offer vague or misleading context-specific preferences.

## Projected Impact And Keeps

Projected Impact should be folded into the primary recommendation action and
should be simple, encouraging, lightly gamified, and non-punitive.

Use a combination of numbers and friendly labels:

```text
Kitchen 24 · Big kitchen boost
```

Keeps are Homekeep's lightweight signal of care returned by the home.
They should be framed as gratitude from the home, not a score on the user,
money, a wage, or a productivity measure.
Keeps should always be framed as coming from the home as a whole, not from
individual Home Assistant Areas.

Keeps rules:

- show Keeps per Chore when suggesting a bundle
- show Keeps per Chore in active sessions
- award Keeps for care completed, not for speed, optimization, streaks, or
  performance
- show full-reset Keeps as harmony for a coherent suggested bundle, not as a
  pressure reward for obeying the app
- allow optional Chores to add Keeps, but never create a reward chain
- do not prefix positive Keeps, health gain, impact gain, or other always-positive
  reward/gain values with `+`
- do not subtract Keeps for removing, skipping, snoozing, ending, or stopping
- showing full-reset Keeps changes during pre-start removal is allowed, but it must
  communicate an inactive/unclaimed opportunity, not a negative number, penalty,
  or subtraction from received Keeps
- do not show a persistent running Keeps total in MVP
- keep Keeps math explainable in one line
- use Keeps more as care texture than as a currency; do not add spend, bank,
  shop, redeem, upgrade, or exchange-rate mechanics
- keep Keeps feedback restrained; avoid arcade-like celebration
- celebrate the completed suggested bundle more clearly than an individual
  Chore, because it is the main recommendation loop completing
- when optional Chores are completed after the suggested bundle, make each
  additional completion feel gradually warmer while staying calm and
  non-scoreboard-like
- use Keeps sparingly in prose
- avoid transactional language such as `earn`, `earned`, `spend`, `bank`, or
  `redeem`
- prefer quiet reciprocal language, such as `The home gives a little back`
- avoid coin, trophy, badge-heavy, or scoreboard-like visual metaphors
- use Keeps to help tiny Chores feel like they count
- let Home Health say where care helps and Keeps say care happened; do not make
  them compete

## Recommendation Engine Fit Rules For The Mock

The mocked Right Now suggestions should behave like Recommendation Engine
output, even before service wiring:

- filter hard constraints before scoring
- keep home need and user fit separate internally
- allow a bounded care nudge toward useful Home Health/Staleness work
- prefer smaller Chore Variants over rejecting useful care when the user context
  is light
- exclude Chores just removed, skipped, dismissed, snoozed, or completed in the
  current flow
- make optional Chores stricter than the planned bundle: smaller, better-fit,
  bounded, and non-chaining
- explain one human reason rather than exposing score math
- avoid repetitive bundles and incoherent mixed-area bundles
- keep shuffle stable within a family of good fits, not random
- learn conservatively from correction signals; soften or retime before
  suppressing useful care
- treat user-entered Chore length as a starting estimate; learned active-session
  duration and current readiness should shape displayed/scored duration
- use adaptive duration to resize care with tiny/light variants or shorter
  passes when the user context is light

## Active Chore Session Requirements

After bundle confirmation, Homekeep enters an active Chore Session. This is in
scope for the Ready Now test slice because it validates the primary Ready Now loop.

The active session must:

- show all selected Chores
- gently highlight the best first Chore
- allow the user to start or complete Chores in any order
- update the suggested next Chore after completions, skips, or manual starts
- keep the highlight helpful, not commanding
- feel more dynamic and rewarding than the selection screen

Prominent Chore-level actions:

- Start
- Complete

Secondary/overflow actions:

- Skip

Skip must remain available for both pending and started/ongoing Chores inside
an active Chore Session. If the user skips the ongoing Chore, stop that Chore's
timer, mark it skipped rather than completed, and move the suggested-next
highlight to the next pending Chore when one exists.

Pause belongs to the timer/chrono control, not as a separate main action.
Do not offer Snooze on active-session Chores. Snooze is a recommendation or
planning-level "later" action, not a control for a Chore the user already
accepted into an active session.

## Timer Requirements

The timer/chrono runs only when a Chore is `ongoing`.

Rules:

- confirming a bundle does not start the timer
- choosing what to do next does not count as active chore time
- no timer runs when no Chore is ongoing
- pause pauses the current ongoing Chore
- paused state must be clear
- resume returns to the same Chore
- Complete is a separate prominent button
- timer behavior must support the user, not pressure them

## Completion Feedback

Completing a Chore should trigger a quick reward effect.

Do:

- show quick Keeps or impact gained
- keep feedback immediate and lightweight
- return focus to remaining Chores and suggested next step
- respect reduced-motion preferences in the eventual implementation

Do not:

- interrupt with a full summary after every Chore
- hide completed Chores behind an expand/collapse control

Completed Chores stay inline in the active session list.

The completed row treatment:

- preserves the Chore name, Area, duration, and Keeps line
- removes Start/Complete/Skip actions
- adds a quiet congratulatory signal such as `Nice, done`
- uses a soft done badge or check treatment without turning the row into a
  separate summary component

## Optional Chores After Planned Completion

After the final planned Chore is completed:

- keep the user in the active Chore Session
- append a short list of new optional Chores directly to the session list
- keep completed planned Chores visible above the optional Chores
- show a subtle session progress line, such as `2 of 3 planned done · optional
  care available`
- add a persistent inline milestone row when the suggested reset is complete,
  such as `Suggested reset complete · The home feels lighter`
- visually separate the optional list with a compact inline divider
- include a tiny `why these?` explanation for optional Chores, such as `Picked
  for small effort, current fit, and useful home lift`
- do not automatically exit the user from the flow
- keep an exit action available once optional Chores appear so optional really
  means optional
- make stopping feel already successful, not like rejecting more work
- shift the idle support text after planned completion toward `Stop here, or
  pick one more small thing`
- make optional Chores inviting without pressure
- show a clear completion flash when the suggested bundle is done before the
  optional Chores appear

Optional Chore behavior:

- use `2-3` small Chores in the first mock
- generate the mocked optional Chores from Recommendation Engine-like scoring,
  not from a fixed always-visible list
- score optional Chores with stricter bounds than the main suggestion: small
  duration, mood/time fit, current Area/Home Health usefulness, Staleness or
  Projected Impact, and session-history exclusions
- render optional Chores as normal actionable session rows with Start, Complete,
  and Skip
- label the first optional Chore as `Optional next`
- label the skip action on optional Chores as `Not now`
- use progressively warmer completion feedback as optional Chores are completed
- do not require a separate reveal or accept action before optional Chores
  become visible
- bias toward useful overdue Chores when they fit context
- prefer small overdue tasks with high Projected Impact
- preserve the light optional feeling
- avoid large overdue Chores unless a tiny/light variant exists
- avoid Chores just removed, skipped, snoozed, or dismissed
- keep optional generation bounded; do not chain new optional lists after the
  first inline optional list is shown
- avoid guilt-based overdue language

## Final Summary

When the user exits the completed session, show a short final
celebration/summary before returning to Ready Now.

The summary:

- is brief
- feels positive and complete
- is not a report card
- includes completed Chores
- includes Keeps received
- includes full-reset Keeps if received
- includes friendly Home/Area impact where available
- auto-returns to Ready Now after a short moment
- has no share/log/details option in MVP

Detailed history belongs later in Activity.

## Critical Risks

- Do not let gamification become punitive.
- Do not let gamification become noisy or annoying.
- Do not make Home Health feel like a grade on the user.
- Do not let UI state become durable source of truth.
- Do not make the app feel like an admin console.
- Do not make recommendations feel like obligations.
- Do not overbuild optional Chore redraw until backend support is verified.
- Do not implement frontend APIs from memory; verify Home Assistant behavior.
- Do not implement later workflows that still lack Steve-approved decisions.

## Minimum Docs To Read Before Implementation

Read these before any frontend implementation pass:

- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/AI_DECISION_LOG.md`
- `docs/architecture/HOME_ASSISTANT_CONTRACT.md`
- `docs/specs/SERVICE_SCHEMAS.md`
- `docs/specs/RECOMMENDATION_PAYLOADS.md`
- `docs/specs/SESSION_STATE_MACHINE.md`
- `docs/specs/BONUS_CHORE_LIFECYCLE.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`
