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
- Done for now / Bonus Chore ending flow
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
- Completed Chores must collapse into a small mocked summary.
- The mocked session must include the active Chore timer state.
- The mocked session must include a quick completion effect.
- `Done for now` must show a mocked final summary and return to Ready Now.
- `One more` must reveal a mocked Bonus Chore in the ending flow.
- Revealing the mocked Bonus Chore and accepting it must be separate actions.
- The mocked Bonus Chore must include the random/redraw button visually, even
  if it is disabled or no-op.
- Bonus Chore backend eligibility/redraw behavior does not need to be wired yet.
- The main shuffle button must swap to another mocked Chore Bundle in the first
  mock prototype.
- Shuffle should visually exercise the fuzzy/refining state, even with mocked
  data.
- Context chip changes must update the mocked suggestion after the
  fuzzy/refining state, using plausible synthetic variants.
- Include `4-5` mocked Chore Bundle variants covering different time, energy,
  mood, and area contexts.
- Always use realistic synthetic household mocks, never placeholders such as
  `Area 1`, `Task 1`, or lorem ipsum.
- Use mostly single-area mocked bundles, plus one multi-area bundle to test
  mixed-area display behavior.
- Include varied mocked bundle durations: one short `5 min`, a couple of
  `10-15 min`, and one fuller `20 min` option.
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
- auto-generate the best suggested Chore Session on open
- use inferred/default context when the user has not chosen values
- show context as compact colored chips with icons
- let each chip open a small inline selector
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

- stable invite line
- evocative Chore Bundle title
- compact bundle count and estimated total time
- scoped health context when it explains the recommendation
- short reason
- included Chores
- removed Chores, if any, with removed styling and restore
- bundle bonus/Keeps footer
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
- show each Chore with estimated time
- show Keeps per Chore
- show bundle-level bonus Keeps, such as `+4 Keeps bonus`, in a quiet footer
- conditionally show Home Assistant Area

Area display rule:

- if all Chores share one Home Assistant Area, combine area and health change in
  one scoped metadata chip
- if the bundle spans multiple areas, show each Chore row's area

## Pre-Start Editing

Suggested Chore rows may include remove only.

Do:

- make remove secondary
- use icons with accessible labels
- remove instantly with undo
- keep removed Chores visible with removed styling
- provide row-level restore
- recalculate time and Projected Impact after removal
- show lost bundle bonus or projected-benefit treatment when applicable
- keep the original recommendation recoverable through shuffle or visible
  context changes
- offer optional context-specific preference learning in the undo toast

Do not:

- add per-Chore swap in MVP
- ask for confirmation before removal
- automatically train recommendation learning from removal
- allow edits that break service/session validity

Undo toast:

- auto-dismisses after a short time
- remains visible long enough for Undo
- does not block bundle confirmation
- may include a context-specific preference action when honest and clear

Example preference actions:

- `Suggest this less in short sessions`
- `Suggest this less when energy is low`
- `Suggest this less for evening resets`
- `Suggest this less in this area`

Do not offer vague or misleading context-specific preferences.

## Projected Impact And Keeps

Projected Impact should be folded into the primary recommendation action and
should be simple, encouraging, lightly gamified, and non-punitive.

Use a combination of numbers and friendly labels:

```text
Kitchen +24 · Big kitchen boost
```

Keeps are Homekeep's lightweight positive reward currency.
They should be framed as a small sign of love the home gives back when it is
cared for, not as productivity points or a scoreboard.
Keeps should always be framed as coming from the home as a whole, not from
individual Home Assistant Areas.

Keeps rules:

- show Keeps per Chore when suggesting a bundle
- show Keeps per Chore in active sessions
- award Keeps for each completed Chore
- award bundle bonus Keeps when the confirmed bundle is completed
- award extra intact-bundle bonus when the originally suggested bundle is
  completed with no pre-start removals
- do not subtract Keeps for removing, skipping, snoozing, ending, or stopping
- showing a lost bundle bonus during pre-start removal is allowed, but it must
  communicate an unclaimed opportunity, not a penalty or subtraction from earned
  Keeps
- do not show a persistent running Keeps total in MVP
- keep Keeps math explainable in one line
- keep Keeps feedback restrained; avoid arcade-like celebration
- use Keeps sparingly in prose
- avoid transactional overuse of `earned`
- prefer quiet reciprocal language, such as `The home gives a little back`
- avoid coin, trophy, badge-heavy, or scoreboard-like visual metaphors

## Active Chore Session Requirements

After bundle confirmation, Homekeep enters an active Chore Session. This is in
scope for the Ready Now test slice because it validates the primary Ready Now loop.

The active session must:

- show all selected Chores
- gently highlight the best first Chore
- allow the user to start or complete Chores in any order
- update the suggested next Chore after completions, skips, snoozes, or manual
  starts
- keep the highlight helpful, not commanding
- feel more dynamic and rewarding than the selection screen

Prominent Chore-level actions:

- Start
- Complete

Secondary/overflow actions:

- Skip
- Snooze

Pause belongs to the timer/chrono control, not as a separate main action.

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
- leave completed Chores as full checked-off rows

Completed Chores collapse into a small completed summary.

The completed summary:

- is collapsed by default
- shows a count
- expands to show completed Chore names and Keeps received

## Done For Now And Bonus Chore

After the final planned Chore is completed:

- keep the user in the active session ending state
- show `Done for now`
- show `One more`
- do not automatically exit the user from the flow
- make `Done for now` feel successful
- make `One more` inviting without pressure

`One more` behavior:

- tapping `One more` immediately reveals the Bonus Chore and Keeps
- revealing and accepting are separate actions
- no separate `No thanks`; `Done for now` remains the stop action
- revealed Bonus Chore has a compact randomize/redraw button
- Bonus Chore redraw uses the same fuzzy/refining state as main shuffle
- Bonus Chore redraw is future behavior and may need backend support

Bonus Chore redraw should:

- bias toward useful overdue Chores when they fit context
- prefer small overdue tasks with high Projected Impact
- preserve the light `one more` feeling
- avoid large overdue Chores unless a tiny/light variant exists
- avoid Chores just removed, skipped, snoozed, or dismissed
- avoid guilt-based overdue language

## Final Summary

Tapping `Done for now` shows a short final celebration/summary before returning
to Ready Now.

The summary:

- is brief
- feels positive and complete
- is not a report card
- includes completed Chores
- includes Keeps received
- includes bundle bonus if received
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
- Do not overbuild Bonus Chore redraw until backend support is verified.
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
