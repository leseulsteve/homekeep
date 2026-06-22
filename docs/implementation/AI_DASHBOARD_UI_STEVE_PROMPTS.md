# Dashboard UI Steve Prompts

Use these prompts one at a time. They are written for Steve to give Codex in
future sessions. The goal is to continue the human design review first, then
translate the approved design into implementation instructions.

Do not skip ahead to frontend implementation until the required workflow
decisions are documented.

## Prompt 1: Continue Human UI Review From Current Point

```text
Continue the Homekeep app UI design review.

Read:
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/product/HOMEKEEP_VOICE_SYSTEM.md
- docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md

Do not implement code.
Ask me one question at a time.
Document every answer in docs/product/HOMEKEEP_APP_PLAN.md.

Resume exactly where we left off:
Home Health and Areas.

Ask:
Should Home Health be shown mostly as a numeric score, a friendly status label,
or area-level language like "Kitchen could use attention"?
```

## Prompt 2: Finish Home Health And Areas Review

```text
Continue the Homekeep app UI design review for Home Health and Areas.

Read:
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/product/HOMEKEEP_VOICE_SYSTEM.md

Do not implement code.
Ask one question at a time.
Document every answer in docs/product/HOMEKEEP_APP_PLAN.md.

Cover:
- how Home Health appears on Ready Now
- whether Home Health is numeric, label-based, area-based, or a combination
- how Area Health is shown
- how stale or attention-worthy areas are surfaced
- how Projected Impact connects to Home Health and Area Health
- how to avoid making health feel like a grade
- mobile and desktop priorities
```

## Prompt 3: Review Plan / Scheduled Chores

```text
Continue the Homekeep app UI design review for Plan / Scheduled Chores.

Read:
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/specs/TARGET_TIME_WINDOW.md
- docs/product/HOMEKEEP_VOICE_SYSTEM.md

Do not implement code.
Ask one question at a time.
Document every answer in docs/product/HOMEKEEP_APP_PLAN.md.

Cover:
- where planned sessions live in navigation
- how future windows are selected
- how proposals show target time and expiry
- how stale or expired proposals refresh
- how the app avoids pretending a proposal is an active session
- how voice/tone changes for planning versus doing
```

## Prompt 4: Review Add Chore

```text
Continue the Homekeep app UI design review for Add Chore.

Read:
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/architecture/DATA_MODEL.md
- docs/specs/SERVICE_SCHEMAS.md
- docs/product/HOMEKEEP_VOICE_SYSTEM.md

Do not implement code.
Ask one question at a time.
Document every answer in docs/product/HOMEKEEP_APP_PLAN.md.

Cover:
- quick capture versus structured form
- required fields in MVP
- Home Assistant Area selection
- interval and duration inputs
- Chore Variant handling
- how Add Chore behaves during an active Chore Session
- validation and empty/error states in human language
```

## Prompt 5: Review Activity

```text
Continue the Homekeep app UI design review for Activity.

Read:
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/product/HOMEKEEP_VOICE_SYSTEM.md
- docs/specs/SESSION_HISTORY_LEARNING.md

Do not implement code.
Ask one question at a time.
Document every answer in docs/product/HOMEKEEP_APP_PLAN.md.

Cover:
- what recent activity should show
- how completed sessions appear
- how Keeps and impact history appear
- whether skipped/snoozed/dismissed items appear
- how to avoid scoreboard or blame language
- what belongs in MVP versus later
```

## Prompt 6: Review Settings And Diagnostics

```text
Continue the Homekeep app UI design review for Settings and diagnostics.

Read:
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/product/HOMEKEEP_VOICE_SYSTEM.md
- docs/specs/CALENDAR_CONTEXT.md
- docs/specs/MOOD_CONTEXT.md

Do not implement code.
Ask one question at a time.
Document every answer in docs/product/HOMEKEEP_APP_PLAN.md.

Cover:
- selected calendars
- Mood Context correction and defaults
- default time, energy, and goal preferences
- diagnostic visibility
- privacy-sensitive state
- what should be hidden from normal users
- what belongs in MVP
```

## Prompt 7: Translate Approved Design To Codex Instructions

```text
Translate the approved Homekeep app design into implementation instructions.

Read:
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/product/HOMEKEEP_VOICE_SYSTEM.md
- docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md
- docs/AI_DECISION_LOG.md
- docs/architecture/HOME_ASSISTANT_CONTRACT.md
- docs/specs/SERVICE_SCHEMAS.md
- docs/specs/RECOMMENDATION_PAYLOADS.md
- docs/specs/SESSION_STATE_MACHINE.md
- docs/specs/BONUS_CHORE_LIFECYCLE.md
- docs/AI_IMPLEMENTATION_PROGRESS.md

Do not implement frontend code yet.

Update docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md so it reflects every approved
workflow decision. Be critical:
- identify missing backend support
- identify Home Assistant API assumptions that must be verified
- identify test/source-check requirements
- identify MVP scope boundaries
- identify risks where the UI could become punitive, cluttered, or stateful in
  the wrong place

End with a proposed small first implementation phase.
```

## Prompt 8: Verify Home Assistant Frontend Approach

```text
Verify the Home Assistant frontend approach for the Homekeep sidebar app.

Read:
- docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/AI_DECISION_LOG.md
- custom_components/homekeep/manifest.json
- custom_components/homekeep/__init__.py

Use the installed Home Assistant package if available. If not available, use
official Home Assistant developer docs. Do not rely on memory.

Do not implement the app yet.

Document:
- supported sidebar/custom panel approach
- whether the app can avoid iframe embedding
- required files and registration points
- how frontend assets are loaded
- how services/action responses can be called
- how entity/projection refresh should work
- tests or source checks that can verify registration
- risks or contradictions with the current plan
```

## Prompt 9: Implement First App Shell Phase

```text
Implement the first Homekeep Ready Now test slice.

Before coding, read:
- docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/product/HOMEKEEP_VOICE_SYSTEM.md
- docs/AI_DECISION_LOG.md
- docs/AI_IMPLEMENTATION_PROGRESS.md

Scope:
- sidebar app registration only
- no iframe
- no Lovelace
- Ready Now / Ready-Now test slice only
- no full dashboard workflow implementation yet
- no Home Health and Areas implementation beyond Ready Now hints already approved
- no Plan / Scheduled Chores
- no Add Chore
- no Activity
- no Settings or diagnostics
- do not invent later workflow behavior
- implement enough of the Ready Now loop to test the approved design direction:
  mood-aware greeting, compact chips, auto-suggestion, shuffle/refining state,
  collapsed/expanded suggested bundle, bundle confirmation, active session,
  Chore start/complete, Keeps display, Done for now, and Bonus Chore reveal
  only where backend support already exists or can be safely stubbed

Run focused checks.
Update docs/AI_IMPLEMENTATION_PROGRESS.md before finishing.
End with what changed, what was verified, tests run, and remaining risks.
```

## Prompt 9A: Implement Fast Mocked Ready Now Prototype

```text
Implement a fast mocked Homekeep Ready Now prototype.

Before coding, read:
- docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/product/HOMEKEEP_VOICE_SYSTEM.md
- docs/AI_DECISION_LOG.md
- docs/AI_IMPLEMENTATION_PROGRESS.md

Scope:
- Ready Now / Ready-Now prototype only
- mocked data is allowed and expected
- no Lovelace
- no iframe
- no full navigation
- no Home Health and Areas workflow
- no Plan / Scheduled Chores
- no Add Chore
- no Activity
- no Settings or diagnostics
- do not invent later workflow behavior

Build:
- Homekeep sidebar app shell if not already present
- assistant-style Ready Now surface
- mood-aware greeting using mock Mood Context
- compact colored context chips with icons
- inline chip selectors that can update local mock state
- mocked best suggested Chore Bundle
- collapsed suggestion by default
- inline expanded details
- evocative bundle title
- mocked time estimate
- mocked short reason
- mocked Projected Impact
- mocked Keeps per Chore
- mocked bundle bonus Keeps
- one always-visible shuffle button in the intended final location
- shuffle button does not need to work yet
- bundle-selection button that transitions into a mocked active session
- active session with all Chores visible
- gentle best-first highlight
- Chore Start button
- timer/chrono visual for an ongoing mocked Chore
- Complete button that updates local mock state
- quick reward effect or simple reward state
- completed summary collapsed by default
- Done for now ending summary that auto-returns to Ready Now

Clearly document what is mocked, what is nonfunctional, and what remains to wire
to Homekeep services. Run focused checks. Update docs/AI_IMPLEMENTATION_PROGRESS.md
before finishing.
```

## Prompt 10: Current Conversation Resume Prompt

```text
We were doing the human Homekeep app UI design review.

Do not implement code.
Ask one question at a time.
Document every answer in docs/product/HOMEKEEP_APP_PLAN.md.

Read:
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/product/HOMEKEEP_VOICE_SYSTEM.md
- docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md

Current state:
- Lovelace is out of scope.
- The app is a non-iframe Home Assistant sidebar app.
- Ready Now auto-generates a suggested Chore Bundle.
- Ready Now uses mood-aware assistant-style greeting.
- Context is shown as compact colored icon chips with inline selectors.
- Chip changes debounce and use fuzzy/refining state.
- Main shuffle is always visible and regenerates immediately.
- Suggested bundles are collapsed by default and expand inline.
- Bundle titles must be evocative, memorable, fun, inviting, and truthful.
- Expanded details show Projected Impact, Chores, time estimates, Keeps per
  Chore, and bundle bonus Keeps.
- Pre-start remove is instant with undo; no swap in MVP.
- Active session highlights the best first Chore but allows any order.
- Timer runs only while a Chore is ongoing.
- Complete is separate from timer pause/resume.
- Completing a Chore gives a quick reward effect.
- Keeps are shown per Chore and as bundle bonus opportunities, not as a running
  total.
- Completed Chores collapse into a summary with count and expandable names /
  earned Keeps.
- Done for now shows a short celebration summary and auto-returns to Ready Now.
- One more reveals a Bonus Chore and Keeps; accepting is separate.
- Bonus Chore redraw uses fuzzy/refining state and should bias toward small,
  useful overdue Chores when appropriate.

Resume at Home Health and Areas.

Ask me:
Should Home Health be shown mostly as a numeric score, a friendly status label,
or area-level language like "Kitchen could use attention"?
```

## Prompt 11: Build Second Right Now Live-Test Candidate

```text
Build the second Homekeep Right Now live-test candidate from the live visual
review notes.

Before coding, read:
- docs/AI_DECISION_LOG.md
- docs/AI_IMPLEMENTATION_PROGRESS.md
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/product/HOMEKEEP_VOICE_SYSTEM.md
- docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md
- docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md
- custom_components/homekeep/frontend/homekeep-panel.js

Scope:
- Right Now mocked sidebar component only.
- Keep the app non-iframe and non-Lovelace.
- Do not wire Homekeep services yet.
- Do not build Home Health, Plan, Add Chore, Activity, Settings, diagnostics,
  full navigation, or real stale-state recovery.
- Use only synthetic data.
- Treat live visual review notes in docs/product/HOMEKEEP_APP_PLAN.md as global
  design-system direction unless explicitly scoped.

Implement the second-test polish:
- Make the visual system fit Home Assistant dark theme: darker translucent
  surfaces, theme tokens where practical, softer borders, less pale white/green
  treatment, and more transparent layering.
- Apply a consistent typography and line-height scale across the mocked Right
  Now, active session, ending, Bonus Chore, toast, and summary states.
- Keep `Ready Now` and `Suggested Chore Bundle` out of visible user-facing
  labels.
- Keep greeting/invitation copy from repeating the Chore Bundle name.
- Keep the recommendation invite line stable during the page session but able
  to vary on reload using lightly contextual mood/energy copy families.
- Keep randomize/shuffle with the filter/context chips.
- Show Chores in the suggested bundle by default. Do not hide them behind an
  expand/details control.
- Show suggested Chores as included/selected by default, not completed.
- Keep removed Chores visible with removed styling and row-level restore.
- Use one scoped metadata chip for bundle count/time and one for area health
  scope, for example `3 chores · 15 min` and `Kitchen 48 -> 72`.
- Fold Projected Impact into the compact primary action button: projected
  benefit on the left, action icon on the right, accessible action label.
- Move bundle bonus/Keeps information into a quieter footer near the Chore list
  or primary action. When a Chore is deselected, show the lost bundle bonus or
  lost projected benefit.
- Tighten reason text so it answers `why this now?` without repeating area,
  impact, or bundle title content.
- Recheck mobile scan order: invite, title/reason, bundle size, included
  Chores, projected-benefit action.

Run:
- bundled Node syntax check for custom_components/homekeep/frontend/homekeep-panel.js
- `git diff --check`
- focused Python tests that cover frontend registration/reload if touched

Update:
- docs/AI_IMPLEMENTATION_PROGRESS.md with the second Right Now candidate status,
  summary, checks run, remaining risks, and next recommended live-test prompt.
- docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md if the live-test steps need
  to change.

End with:
- what changed
- what was verified
- exact checks run
- what Steve should test in the private Home Assistant sidebar next
```
