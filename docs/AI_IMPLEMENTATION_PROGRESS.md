# Implementation Progress

Codex must update this file at the end of every implementation phase.

Use it as the resume point for future sessions. Do not rely on chat memory.

## Current Status

```yaml
current_phase: 8
current_phase_name: Hardening and release readiness
last_updated: 2026-06-22
last_codex_summary: >
  Homekeep's main product vocabulary now uses Task project-wide for product,
  UX, and user-facing language. Chore remains legacy implementation/API
  vocabulary until a deliberate compatibility migration is designed. The mutual
  care model remains the north star: care by Area and care by source, with the
  home brokering non-scarce Keeps through Home Assistant signals.
```

## Phase Checklist

- [x] Phase 0: Scaffold
- [x] Phase 1: Models and storage
- [x] Phase 2: Health and adaptive intervals
- [x] Phase 3: Chore Session lifecycle
- [x] Phase 4: Recommendation Engine V1
- [x] Phase 5: Home Assistant services and entities
- [x] Phase 6: Calendar Context
- [x] Phase 7: Homekeep app MVP
- [x] Phase 8: Hardening and release readiness

## Phase Log

Add a new entry after each implementation pass.

Template:

```markdown
### YYYY-MM-DD - Phase N: Name

Status: not_started | in_progress | completed | blocked

Implemented:
- ...

Tests/checks run:
- ...

Docs updated:
- ...

Important decisions:
- ...

Known gaps / next prompt:
- ...
```

### 2026-06-22 - Project vocabulary moves from Chore to Task

Status: completed locally

Implemented:
- Made `Task` the project-wide product and user-facing term.
- Updated the project brief, app plan, voice guidance, and agent vocabulary for
  `Task`, `Task Bundle`, `Task Session`, `Smart Task List`, `Task Variant`,
  `Task Group`, and `Bonus Task`.
- Added a decision-log compatibility boundary: `Chore` remains legacy
  implementation/API vocabulary for existing Python classes, storage keys,
  Home Assistant service names, entity ids, tests, and older specs until a
  deliberate migration is designed.
- Added guardrails against blind code/API renames from Chore to Task.

Tests/checks run:
- `git diff --check -- AGENTS.md PROJECT_BRIEF.md docs/AI_DECISION_LOG.md docs/product/HOMEKEEP_APP_PLAN.md docs/product/HOMEKEEP_VOICE_SYSTEM.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- `rg -n "\bChore\b|\bChores\b|\bchore\b|\bchores\b" PROJECT_BRIEF.md docs/product/HOMEKEEP_APP_PLAN.md docs/product/HOMEKEEP_VOICE_SYSTEM.md`

Docs updated:
- `AGENTS.md`
- `PROJECT_BRIEF.md`
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- New UI and product language should use Task, not Chore.
- Existing `homekeep.create_chore`, `ChoreDefinition`, `ChoreState`, storage
  keys, and other API/code symbols must not be renamed without aliases,
  migrations, deprecation notes, and tests.

Known gaps / next prompt:
- Plan the technical Chore-to-Task compatibility migration separately if Steve
  wants API/code vocabulary to change too.

### 2026-06-22 - Mutual care documentation consolidation

Status: completed locally

Implemented:
- Added the canonical mutual-care model:
  `Care Source -> Care Contribution -> Keeps -> Area/Home Health context`.
- Clarified the distinction between Keeps and Area Health: Keeps show that care
  flowed through the home; Area Health shows where care helped, where care is
  drifting down, and what helps next.
- Replaced currency-flavored `infinite economy` wording with the non-scarce
  Keeps model.
- Replaced personal-name examples in new contribution copy with neutral
  `You` examples.
- Added a future `CareSource` / `CareContribution` data-shape note without
  expanding MVP scope.
- Added product-review recommendations for how the ideas should fit together:
  gradual introduction, Right Now first, Home Health contribution second,
  simple active-session Keeps, meaningful attribution only, and non-competitive
  reflection.
- Elevated care source contribution to a first-class product axis alongside
  Area care: Area care answers `where did care help?`, while source care answers
  `who or what carried care?`.
- Added the Keeps broker model: the home returns Keeps, Home Assistant provides
  local evidence, and Homekeep interprets that evidence into care
  contributions.

Tests/checks run:
- `git diff --check -- PROJECT_BRIEF.md docs/AI_DECISION_LOG.md docs/product/HOMEKEEP_APP_PLAN.md docs/product/HOMEKEEP_VOICE_SYSTEM.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `PROJECT_BRIEF.md`
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- The mutual-care ideas now have one canonical model for future implementation
  to follow.
- Non-scarce Keeps should be explained as abundance and recognition, not as an
  economy or currency.
- Homekeep should preserve both care perspectives: care by Area and care by
  source. Neither should be treated as a secondary detail of the other.
- Home Assistant is the signal layer for Keeps, not the emotional giver of
  Keeps. Not every Home Assistant event is care.

Known gaps / next prompt:
- Commit the unstaged documentation pass only after Steve confirms the product
  direction feels right.

### 2026-06-22 - Right Now as human contribution gateway

Status: completed locally

Implemented:
- Documented Right Now as the human contribution gateway into mutual care, not
  merely a chore screen.
- Added design implications for greeting, context controls, suggested bundle,
  primary action, active session feedback, ending summary, and Area Health
  connection.
- Added voice guidance so Right Now sounds like an invitation to contribute to
  the home's care flow rather than a task queue.

Tests/checks run:
- `git diff --check -- PROJECT_BRIEF.md docs/AI_DECISION_LOG.md docs/product/HOMEKEEP_APP_PLAN.md docs/product/HOMEKEEP_VOICE_SYSTEM.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `PROJECT_BRIEF.md`
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Time, Mood, and Area in Right Now are contribution-fit controls, not
  productivity filters.
- The suggested Chore Bundle is an invitation for a human to join care already
  happening in the home.

Known gaps / next prompt:
- Future Right Now design pass should check whether greeting, primary action,
  and ending summary communicate human contribution clearly.

### 2026-06-22 - Area Health contribution visibility

Status: completed locally

Implemented:
- Documented that Area Health should proudly show who and what helped an Area,
  not only what is pulling the Area Health down.
- Added the principle that Area Health naturally drifts down as care gets stale,
  and that this should be presented as a normal home rhythm rather than a
  failure.
- Added UI suggestions for `Helped lately`, `Care sources`, `Kept this area
  steady`, and separate `Could help next` treatment.
- Added contributor categories for humans, pets, plants, devices, air/comfort
  systems, and routines.

Tests/checks run:
- `git diff --check -- PROJECT_BRIEF.md docs/AI_DECISION_LOG.md docs/product/HOMEKEEP_APP_PLAN.md docs/product/HOMEKEEP_VOICE_SYSTEM.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `PROJECT_BRIEF.md`
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Area Health UI should preserve pride in contribution even when the area still
  needs care.
- Contribution display should be appreciative and prominent, not ranked or
  competitive.

Known gaps / next prompt:
- Future Home Health design pass should sketch Area cards with separate
  `Helped lately` and `Could help next` regions.

### 2026-06-22 - Non-scarce Keeps model

Status: completed locally

Implemented:
- Documented the explanation for a non-scarce Keeps model: Keeps are recognition
  of care, not currency.
- Added guardrails that Keeps are not spent, traded, stolen, depleted, exchanged,
  or competed for.
- Documented that more humans, pets, plants, devices, and routines contributing
  to the home means more care can be noticed.

Tests/checks run:
- `git diff --check -- PROJECT_BRIEF.md docs/AI_DECISION_LOG.md docs/product/HOMEKEEP_APP_PLAN.md docs/product/HOMEKEEP_VOICE_SYSTEM.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `PROJECT_BRIEF.md`
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- The product metaphor for Keeps is abundance, warmth, gratitude, and care
  recognition, not scarcity or money.
- One care source never takes Keeps from another.

Known gaps / next prompt:
- Future Keeps UI should explain the concept simply: `Keeps are the home
  noticing care. They are not a currency. They do not run out.`

### 2026-06-22 - Proud Keeps care-source totals

Status: completed locally

Implemented:
- Documented that future Keeps reflection surfaces should proudly display total
  Keeps by care source: humans, pets, plants, devices, air/comfort systems,
  quiet routines, and other meaningful contributors.
- Kept the non-competitive guardrail: care-source totals are appreciation for
  the home's care network, not leaderboards, rankings, currencies, or
  total-chasing surfaces.

Tests/checks run:
- `git diff --check -- docs/AI_DECISION_LOG.md docs/product/HOMEKEEP_APP_PLAN.md docs/product/HOMEKEEP_VOICE_SYSTEM.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Keeps source totals should be prominent in future reflection, not hidden.
- The presentation should be proud and appreciative, while avoiding comparison
  pressure between humans, pets, plants, devices, or routines.

Known gaps / next prompt:
- Future design pass should sketch a Keeps reflection surface that shows care
  source totals without feeling like a scoreboard.

### 2026-06-22 - Mutual care north star

Status: completed locally

Implemented:
- Promoted mutual care to Homekeep's main product goal: the home has needs, and
  the home also helps care for its humans, pets, and plants.
- Documented that every product, design, and implementation decision should move
  toward mutual care, even when the current MVP remains focused on chores.
- Added guardrails so future inhabitant-care features stay practical,
  environmental, and routine-aware rather than medical, psychological, or
  productivity-coach oriented.

Tests/checks run:
- `git diff --check -- PROJECT_BRIEF.md docs/product/HOMEKEEP_APP_PLAN.md docs/product/HOMEKEEP_VOICE_SYSTEM.md docs/AI_DECISION_LOG.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `PROJECT_BRIEF.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/AI_DECISION_LOG.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Mutual care is the north star, not a side theme or distant optional feature.
- Chore and Right Now work should be shaped as the first expression of a larger
  reciprocal-care product.

Known gaps / next prompt:
- After Live Test 2, review whether the Right Now flow already communicates
  mutual care or still feels only like chore optimization.

### 2026-06-22 - Version 0.0.4 private Live Test 2 publish prep

Status: completed locally, ready to push

Implemented:
- Bumped the Homekeep integration manifest version from `0.0.3` to `0.0.4`.
- Updated the private live-test checklist release notes for the Live Test 2
  candidate.
- Updated the mock adequacy review for the `0.0.4` private HACS publish scope.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `git diff --check`
- Fixed-string privacy/secret scan across changed files for tokens,
  credentials, cookies, webhooks, private endpoints, Wi-Fi details, and private
  entity ids. Hits were existing guardrail/checklist text or design-token
  wording only.

Docs updated:
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/live-test/MOCK_ADEQUACY_REVIEW.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Publish `0.0.4` as a private HACS/live-test candidate only. It does not claim
  public production readiness.
- No tag will be created because the repository still has no established tag
  convention.

Known gaps / next prompt:
- Push the `0.0.4` candidate to `main`, update Homekeep from HACS in the
  private Home Assistant test instance, restart Home Assistant, and run Gate 3B.

### 2026-06-22 - Live Test 2 readiness refresh

Status: completed locally, pending install into private Home Assistant test instance

Implemented:
- Rechecked the Gate 3B Live Test 2 runbook after the adaptive-duration pass.
- Added a Live Test 2 checkpoint to verify that displayed duration feels
  adaptive to Mood/Readiness and recent session momentum rather than rigidly
  tied to the user-entered Chore estimate.
- Confirmed Gate 3B still covers the Right Now component, mocked active-session
  loop, optional Chores, and basic Home Health visibility/navigation.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `git diff --check`
- Targeted privacy scan for obvious secret/private-detail terms in changed code,
  docs, and tests; results were expected synthetic calendar/testing references.

Docs updated:
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Live Test 2 remains a mocked Right Now review plus basic Home Health
  visibility/navigation; it still does not validate sidebar service wiring,
  full Home Health behavior, Plan, Add Chore, Activity, Settings, diagnostics,
  stale-state recovery, or full navigation.

Known gaps / next prompt:
- Install or update the private Home Assistant test instance to the current
  candidate, restart Home Assistant, then run Gate 3B from
  `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`.
- If using HACS from GitHub, commit and push the current candidate first so the
  private instance can install the exact reviewed code.

### 2026-06-22 - Adaptive recommendation durations

Status: completed locally

Implemented:
- Added a derived recommendation-duration helper that starts from learned
  completion duration when available and otherwise falls back to the Chore's
  entered estimate.
- Adapted recommendation item `estimated_minutes` for Mood/Readiness, Capacity,
  and recent session momentum so bundles can get smaller or fuller without
  mutating the stored Chore definition.
- Kept active work duration samples as the only training signal; skips,
  removals, snoozes, dismissals, and invalid timing remain excluded.
- Added recommendation tests for low Mood shortening learned duration and high
  readiness expanding it.

Tests/checks run:
- `python3 -m unittest tests.test_recommendations.RecommendationEngineTest.test_recommendations_use_learned_duration_samples -v`
- `python3 -m unittest tests.test_recommendations.RecommendationEngineTest.test_recommendations_shorten_learned_duration_for_low_mood -v`
- `python3 -m unittest tests.test_recommendations.RecommendationEngineTest.test_recommendations_can_expand_learned_duration_for_high_readiness -v`
- `python3 -m unittest tests.test_recommendations -v`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `python3 -m unittest tests.test_models tests.test_sessions -v`
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/architecture/DATA_MODEL.md`
- `docs/specs/RECOMMENDATION_ENGINE.md`
- `docs/specs/SERVICE_SCHEMAS.md`
- `docs/implementation/TEST_PLAN.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- User-entered Chore length is a fallback/base suggestion, not an authoritative
  recommendation duration.
- Current adaptation is derived and disposable; future storage can add
  Chore Variant or readiness-bucket samples without changing the source of
  truth.

Known gaps / next prompt:
- Live Test 2 should verify whether adaptive duration copy feels respectful and
  whether low-readiness recommendations actually feel lighter in the mocked UI.

### 2026-06-22 - Second Right Now live-test candidate

Status: completed locally, pending private Home Assistant live review

Implemented:
- Applied the second Right Now visual-system pass to the mocked sidebar panel:
  darker Home Assistant-theme-aware surfaces, translucent layering, softer
  borders, and less pale white/green treatment.
- Tightened typography and line-height rhythm across Right Now, active session,
  ending, Bonus Chore, toast, timer, and summary states.
- Kept randomize with the context chips and kept internal labels out of the
  visible Right Now surface.
- Made suggested Chores visible by default, quieter as selected/included rather
  than completed, and restorable in place after removal.
- Folded Projected Impact into the primary projected-benefit action and moved
  bundle bonus/Keeps into a quiet footer with lost-bonus treatment after Chore
  removal.
- Updated the mocked final summary so intact-bundle bonus Keeps are not awarded
  after pre-start Chore removal.
- Aligned Codex-facing UI implementation instructions with the second-candidate
  Right Now design.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md docs/implementation/AI_DASHBOARD_UI_STEVE_PROMPTS.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`

Important decisions:
- The second candidate remains mocked and visual-first.
- Sidebar service wiring still waits until Steve completes Gate 3B live review.

Known gaps / next prompt:
- Install/update the private Home Assistant test instance with this candidate
  and run Gate 3B from `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`.
- Continue to avoid treating this Right Now live test as validation for Home
  Health, Plan, Add Chore, Activity, Settings, diagnostics, full navigation, or
  stale-state recovery.

### 2026-06-22 - Remove duplicate removal undo toast

Status: completed locally

Implemented:
- Removed the pre-start Chore removal undo toast from the mocked Right Now
  panel.
- Kept row-level restore as the single visible recovery path for removed
  Chores.
- Updated product and Codex implementation docs so removal reversibility is
  handled in place instead of duplicated in a toast.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Do not show a temporary undo toast when the removed Chore remains visible with
  row-level restore.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Remove active-session Chore snooze

Status: completed locally

Implemented:
- Removed the Snooze button from active-session Chore rows in the mocked
  Homekeep panel.
- Updated app plan and Codex UI guidance so active-session Chores support
  start/complete, skip, pause, and end, but not snooze.
- Kept snooze as a recommendation/planning-level "later" concept rather than an
  in-session Chore control.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- `rg -n "Snooze" custom_components/homekeep/frontend/homekeep-panel.js`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Snooze is not needed on active-session Chores because the user has already
  accepted the Chore Session; use Skip, Pause, or End instead.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Allow skipping a started Chore

Status: completed locally

Implemented:
- Wired the active-session Skip button in the mocked Homekeep panel.
- Added skipped session-item state so skipped Chores leave the active list,
  do not award Keeps, and appear in a quiet skipped summary.
- Made Skip work for started/ongoing Chores by stopping the timer, clearing the
  active item, and moving the suggested-next highlight to the next pending
  Chore when available.
- Updated product and Codex UI guidance so started Chores can still be skipped.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- Targeted `rg` scan for skip wiring and started-Chore guidance.

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Skip is the in-session escape hatch even after a Chore starts; snooze remains
  outside the active-session Chore controls.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Keep completed Chores inline

Status: completed locally

Implemented:
- Removed the active-session completed Chore expand/collapse summary from the
  mocked Homekeep panel.
- Completed Chores now remain visible in their original session order as
  near-normal Chore rows with Area, duration, Keeps, a `Nice, done` signal, and
  a soft check badge.
- Removed completed-row active controls while keeping the completed item visible
  as part of the session history.
- Updated product and Codex UI guidance so completed Chores stay inline rather
  than hiding behind an expander.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- Targeted `rg` scan for old completed-summary/expander wording and code.

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Completed Chores should stay almost as-is in the active session, with a soft
  congratulatory done state instead of an expandable summary.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Inline optional Chores after planned completion

Status: completed locally

Implemented:
- Replaced the mocked active-session `Done for now` / `One more` ending choice
  with an inline optional Chore continuation.
- Completing the final planned Chore now appends three small optional Chores
  directly into the active session list under an `A few more that fit` divider.
- Optional Chores render as normal session rows with Start, Complete, and Skip;
  the first optional row is marked `Optional next`.
- Removed the old mocked Bonus Chore reveal/accept UI and frontend state.
- Updated product and Codex UI guidance so Live Test 2 reviews the inline
  optional list instead of the old ending button pair.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- Targeted `rg` scan confirmed the old frontend `Done for now` / `One more` /
  Bonus Chore reveal strings are gone.

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Optional Chores appear only when the last planned Chore is completed, not
  when the user skips out of the planned bundle.
- The optional list is bounded in the mock and does not chain indefinitely.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Progressive completion celebration

Status: completed locally

Implemented:
- Added completion flash levels to the mocked active session: regular Chore,
  completed suggested bundle, and progressively warmer optional Chore
  completions.
- The final planned Chore now shows a clearer bundle-complete message before
  optional Chores appear.
- Optional Chore completion feedback now ramps gently across the added optional
  list without adding plus signs, scores, or noisy arcade treatment.
- Updated product and Codex UI guidance so the suggested bundle completion is
  celebrated more clearly, and optional completions get gradually warmer.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- Targeted `rg` scan for progressive celebration copy and styling.

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Completing the suggested bundle deserves a stronger celebration than a single
  Chore.
- Optional Chore completions should get warmer as the user keeps going, while
  staying calm and non-scoreboard-like.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Recommendation-like optional Chore generation for Live Test 2

Status: completed locally

Implemented:
- Replaced the fixed optional Chore append list with a larger mocked candidate
  pool and local Recommendation Engine-like scoring.
- Optional Chores now score for small duration, mood/readiness fit, explicit or
  inferred Area fit, synthetic Home Health/Area Health usefulness, and
  Staleness-like usefulness.
- Optional Chores exclude Chores already in the current session, removed
  pre-start, or skipped in-session, and remain capped to one bounded inline
  list.
- Updated product, Codex UI guidance, and the Live Test 2 checklist so optional
  Chores are reviewed as stricter Recommendation Engine-like output.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- Targeted `rg` scan for optional-generation rules and stale Live Test 2 ending
  checks.

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- For Live Test 2, optional Chores are still synthetic and local, but they
  should feel generated from the same Recommendation Engine principles as the
  main suggestion, with stricter bounds.
- Optional generation must stay bounded and must not chain forever.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Active-session optional continuation refinements

Status: completed locally

Implemented:
- Added a subtle active-session progress line showing planned and optional
  progress.
- Added a persistent inline milestone row when the suggested reset is complete.
- Kept optional Chores visually quieter than planned rows and added a compact
  explanation for why they appeared.
- Kept an exit action visible once optional Chores appear so optional remains
  genuinely optional.
- Changed optional Chore skip copy to `Not now`.
- Shifted idle support copy after planned completion to a calmer continuation
  prompt.
- Kept the final summary reachable even when optional Chores make the list
  longer.
- Updated product, Codex UI guidance, and Live Test 2 checklist with the full
  accepted active-session recommendation set.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- Targeted `rg` scan for the new progress line, milestone row, optional
  explanation, exit action, and `Not now` copy.

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Active sessions should make planned completion visible as a milestone, while
  keeping optional continuation bounded, explained, and easy to leave.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Suggested Chore Engine rules and mock scoring

Status: completed locally

Implemented:
- Updated the mocked Right Now bundle picker to use hard rejection before
  scoring.
- Split mocked bundle scoring into Home need, user fit, bounded care nudge, and
  diversity/stability factors.
- Kept explicit Time and Area constraints stronger than high Home need.
- Kept optional Chore generation aligned with the stricter Recommendation
  Engine-like rules already used for Live Test 2.
- Added canonical Recommendation Engine guidance for two-stage selection,
  separate Home need/user fit, bounded nudging, Chore Variants, current-flow
  exclusions, optional continuation bounds, diversity, shuffle stability, and
  conservative learning.
- Updated the decision log, product plan, Codex UI guidance, and Live Test 2
  checklist so future service wiring follows the same engine shape.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/specs/RECOMMENDATION_ENGINE.md docs/AI_DECISION_LOG.md docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- Targeted `rg` scan for two-stage scoring, hard constraints, bounded care
  nudge, Chore Variant preference, shuffle stability, and mocked scoring code.

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/specs/RECOMMENDATION_ENGINE.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- The suggested Chore engine should be gently opinionated through a capped,
  explainable care nudge, not random, punitive, or purely easiest-first.
- Optional Chores share the same principles as the main suggestion but with
  stricter bounds and no unbounded chaining.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.
- Real service wiring still needs backend Recommendation Engine implementation
  that matches this documented shape.

### 2026-06-22 - Keeps gratitude model

Status: completed locally

Implemented:
- Reframed Keeps as care returned by the home, not points, money, wages,
  currency, or user performance scoring.
- Changed visible mocked bundle wording from `Keeps bonus` to
  `Keeps for the full reset` and changed inactive copy to `Full-reset Keeps not
  active`.
- Updated product, voice, Codex UI guidance, Live Test 2 checklist, and the
  decision log with rules for Keeps as gratitude, full-reset harmony, tiny-Chore
  acknowledgement, no reward chains, no plus signs, and quiet reflection
  instead of leaderboards.
- Replaced active planning language that implied lost/earned/bundle-bonus Keeps
  with received/full-reset Keeps language.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/AI_DECISION_LOG.md docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/product/HOMEKEEP_VOICE_SYSTEM.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- Targeted `rg` scan for full-reset Keeps language, care-returned framing, and
  stale `+ Keeps` / `Keeps bonus` wording.

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Keeps are gratitude/care texture from the home, not a spendable or
  leaderboard-like currency.
- Full-reset Keeps represent harmony in the suggested bundle, and optional
  Chores must not create a Keeps reward chain.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Positive gain values without plus signs

Status: completed locally

Implemented:
- Removed plus signs from visible Keeps values in the Right Now, active
  session, Bonus Chore, completion flash, completed summary, and final summary
  surfaces.
- Updated active implementation and product guidance so positive Keeps, health
  gain, impact gain, and other always-positive reward/gain values are shown
  without a `+` prefix.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- Targeted `rg` scan for old always-positive plus-sign examples in the Right
  Now UI and Live Test 2 guidance.

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Always-positive reward/gain values should read as positive by context rather
  than carrying a plus sign.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Live Test 2 final scope decisions

Status: completed locally

Implemented:
- Recorded that `Best fit` is final for automatic Time and Area in this pass.
- Recorded that the top-right projected-benefit action button stays as-is for
  Live Test 2.
- Expanded Live Test 2 scope to include basic Home Health visibility/navigation
  alongside Right Now and the mocked active-session loop.
- Updated the live-test checklist and product plan so future work does not
  treat Live Test 2 as Right Now-only.

Tests/checks run:
- `rg -n "Live Test 2 should focus only|Right Now-only|does not validate the full Home Health view|Home Health implementation remains planned but unvalidated until a later" docs/product/HOMEKEEP_APP_PLAN.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- `git diff --check -- docs/product/HOMEKEEP_APP_PLAN.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Live Test 2 should verify that Home Health is reachable and does not crowd
  Right Now, but it still does not validate Plan, Add Chore, Activity, Settings,
  diagnostics, service wiring, or the full Home Health behavior surface.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Selected Right Now pre-live polish

Status: completed locally

Implemented:
- Rendered internal `Auto` values as `Best fit` for Time and Area while keeping
  the internal value unchanged.
- Added subtle inferred/default versus explicit chip styling.
- Made explicit-Area fit copy acknowledge the user's choice.
- Added included-count text near the bundle bonus after removal.
- Added a filter-specific no-suggestion message for overconstrained explicit
  filters.
- Changed the shuffle tooltip/accessibility label to `Try another fit`.
- Tightened mobile vertical density around the hero, chips, suggestion card,
  metadata, bonus line, and Chore rows.
- Updated product, implementation, and live-test guidance for these selected
  pre-Live-Test-2 changes.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Keep the visible control set lean and make Homekeep's inferred choices
  understandable without adding Energy or Goal back to the top row.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Bundle bonus moved before Chore list

Status: completed locally

Implemented:
- Moved the bundle bonus/inactive-bonus line above the visible suggested Chore
  list.
- Preserved the inactive bonus treatment when Chores are removed before session
  start.
- Updated product, implementation, and live-test guidance.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Bundle bonus is part of the offer and should be visible before the user
  scans individual Chores.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Primary action moved to card header

Status: completed locally

Implemented:
- Moved the projected-benefit/start action from below the Chore list into the
  suggested bundle card header.
- Aligned the action to the top-right of the title/reason block on wider
  screens and stacked it cleanly on mobile.
- Removed the dependency between primary action placement and variable Chore
  list height.
- Updated product, implementation, and live-test guidance.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- The primary recommendation action belongs in a stable card-header position,
  not after content whose height changes with bundle composition.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Health metadata chip gain format

Status: completed locally

Implemented:
- Changed the Right Now health metadata chip from before/after notation to a
  scoped positive gain format, such as `Kitchen 24`.
- Kept the gain unprefixed because the chip always represents positive
  projected benefit.
- Updated active implementation guidance, product guidance, and the live-test
  checklist to avoid reintroducing `57 -> 74`-style notation in Right Now.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- `rg -n "healthLine|48 -> 72|74 -> 77|Kitchen 48 -> 72|Home 74 -> 77" custom_components/homekeep/frontend/homekeep-panel.js docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/product/HOMEKEEP_APP_PLAN.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Right Now should show the projected health gain compactly, not expose
  before/after health math in the metadata chip.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Filter relationship pass

Status: completed locally

Implemented:
- Kept the visible Right Now filter set to Time, Mood, Area, and shuffle, with
  Mood centered in the row.
- Added a compact fit explanation line to the suggested bundle card.
- Made explicit Area a stronger recommendation constraint.
- Updated shuffle so it respects visible filters; Mood `auto` can still vary
  hidden Goal/fit slightly.
- Used removed heavier/longer Chores as short-lived feedback that softens
  inferred Capacity on the next shuffle.
- Documented and checklisted the filter relationships, including the need to
  test whether `Auto` is clear for Time and Area.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Mood remains the primary visible readiness control. Time bounds length, Area
  constrains place, and hidden Capacity/Goal should follow Mood unless future
  review proves users need more visible controls.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Conservative Mood inference rules

Status: completed locally

Implemented:
- Updated `docs/specs/MOOD_CONTEXT.md` from the older emotion-style enum to
  the current readiness-context enum: `auto`, `low`, `quiet`, `focused`,
  `restless`, and `ready`.
- Documented conservative inference: default to `auto`, infer `low` only from
  clear constraints, infer `quiet` from late/quiet-hour contexts, infer
  `focused` from an open window with one clear high-need target, keep
  `restless` mostly explicit, and infer `ready` only from free block plus
  fuller-bundle completion history.
- Added safe practical signal categories: time/calendar pressure, recent
  behavior, current session context, Home Assistant context, and user
  correction.
- Clarified that Mood is readiness context, not a psychological claim, and user
  correction overrides inference for the moment.

Tests/checks run:
- `rg -n "unknown|calm|tired|overwhelmed|energized|low energy|explicit energy|Mood: Auto \\| Calm" docs/specs/MOOD_CONTEXT.md`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- docs/specs/MOOD_CONTEXT.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/specs/MOOD_CONTEXT.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Mood inference must remain lightweight, conservative, practical, and
  user-correctable. It must never diagnose or claim the user's emotional state.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Goal hidden and inferred from Mood

Status: completed locally

Implemented:
- Removed Goal from the visible Right Now context chips.
- Added internal Mood-to-Goal inference:
  `auto -> visible lift`, `low -> quick wins`, `quiet -> fresh start`,
  `focused -> overdue care`, `restless -> visible lift`, and
  `ready -> overdue care`.
- Updated Mood changes to infer both hidden Capacity and hidden Goal before
  rescoring the mocked recommendation.
- Updated active implementation guidance, product guidance, and the live-test
  checklist so Live Test 2 expects Time, Mood, Area, and shuffle as the visible
  Right Now controls.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Goal remains used internally to shape recommendation intent, but Mood is now
  the user-facing control that selects the default intent.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Capacity model replaces internal Energy

Status: completed locally

Implemented:
- Renamed the mocked internal recommendation field from `energy` to `capacity`.
- Renamed helper/scoring code from Energy wording to Capacity wording.
- Kept Mood-to-Capacity inference as the core relation:
  `auto -> auto`, `low/quiet -> low`, `focused -> steady`,
  `restless -> mobile`, and `ready -> strong`.
- Documented Capacity as the hidden physical-fit model evaluated against
  effort, movement, setup friction, duration, and interruption tolerance.
- Replaced user-facing and active planning examples that still framed the
  concept as Energy.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/specs/RECOMMENDATION_ENGINE.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/specs/RECOMMENDATION_ENGINE.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Capacity is now the preferred internal term. Energy should not return as a
  visible Right Now chip unless a later design review finds a real need for it.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Energy hidden and inferred from Mood

Status: completed locally

Implemented:
- Removed Energy from the visible Right Now context chips.
- Kept energy/capacity as an internal recommendation signal inferred from Mood:
  `auto -> auto`, `low/quiet -> low`, `focused -> steady`,
  `restless -> mobile`, and `ready -> strong`.
- Updated mock bundle scoring so inferred energy still affects fit.
- Updated no-suggestion copy, implementation instructions, the live-test
  checklist, product guidance, and Recommendation Engine spec language to make
  Mood the visible readiness control for Live Test 2.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/specs/RECOMMENDATION_ENGINE.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/specs/RECOMMENDATION_ENGINE.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Energy remains used by the app as an inferred capacity signal, but it should
  not ask the user for another top-level chip while Mood already expresses
  readiness.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Mood vocabulary and automatic time

Status: completed locally

Implemented:
- Replaced the Mood chip options with `auto`, `low`, `quiet`, `focused`,
  `restless`, and `ready`.
- Removed the explicit `all the time` time option from the UI.
- Made Time default to `Auto`, preserving it through shuffle unless the user
  explicitly chooses a duration.
- Updated automatic time scoring so mood/readiness drives bundle length when
  Time is inferred.
- Updated active implementation guidance and the live-test checklist so future
  work treats broad availability as an inferred/calendar-driven default rather
  than a user-selected chip option.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Time should usually be inferred from availability/context; Mood Context is
  the stronger user-facing driver for how small or ambitious the bundle feels.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Context chip visible labels removed

Status: completed locally

Implemented:
- Removed visible `Time`, `Energy`, `Mood`, `Goal`, and `Area` labels from
  Right Now context chips.
- Kept chip labels as `aria-label` and `title` text so icon-only labels remain
  accessible and understandable on hover.
- Documented the global chip pattern in implementation and live-test docs.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- For self-explanatory context chips, visible text should be icon plus current
  value only. The internal label stays available through accessible names and
  tooltips.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Shuffle chip optical sizing

Status: completed locally

Implemented:
- Kept the shuffle/randomize control with the context chips, but reduced its
  inner icon-slot and glyph size so the horizontal shuffle icon reads centered
  inside the round button.
- Preserved the 40px circular button size for touch comfort.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Round icon-only buttons can keep their touch target while tuning the glyph
  independently for optical balance.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Mood-aware time options

Status: completed locally

Implemented:
- Made the Right Now Time selector derive its options from current
  mood/readiness context instead of a static list.
- Added the expansive `I've got all the time. Let's do that.` selector option,
  displayed compactly as `all the time` in the chip.
- Updated mock recommendation scoring so `all the time` favors fuller bundles
  while still respecting explicit filters such as Area.
- Replaced fragile colon-split chip option handling with separate chip key and
  value data attributes.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Treat `all the time` as a readiness/willingness signal, not a literal
  duration or scheduled-session mode.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Non-punitive inactive bonus wording

Status: completed locally

Implemented:
- Changed the removed-Chore bundle bonus footer from a negative Keeps-style
  value to `Bundle bonus not active`.
- Updated product, implementation, and live-test docs to forbid negative-number
  treatment for unclaimed bundle bonuses after pre-start removal.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Pre-start removal can make a bundle bonus inactive, but it must not look like
  a penalty, negative score, or lost earned Keeps.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Right Now automatic Area context

Status: completed locally

Implemented:
- Changed the mocked Right Now Area chip default to `Auto` so it does not look
  like Homekeep preselected a user-chosen Area.
- Kept Recommendation Engine Area choice represented in the suggestion metadata,
  while treating a specific Area chip selection as an explicit filter.
- Documented the default automatic Area behavior in product and Codex
  implementation docs.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Right Now defaults to automatic Area selection. User-selected Areas are
  explicit filters.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Remove recommendation invite line

Status: completed locally

Implemented:
- Removed the separate recommendation/card invite line from the mocked Right Now
  suggestion card.
- Deleted the unused invite-copy generation code.
- Updated product, implementation, and live-test docs so the suggested bundle
  card leads directly with the Chore Bundle title after the page greeting and
  context chips.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- The page-level greeting sets tone; the suggestion card should not add a
  second invitation line above its title.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Chip icon-slot styling

Status: completed locally

Implemented:
- Added centered icon-slot backing treatment for icons inside context chips.
- Adjusted chip spacing so icon+text controls account for the icon background.
- Kept the projected-benefit action button's simpler right-side icon treatment.
- Documented the icon-slot rule in product and implementation docs.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Mixed icon+text chips should use a distinct centered icon slot instead of
  loose inline icons. Do not force that treatment onto action buttons when the
  simpler icon reads better.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Right Now greeting lifecycle

Status: completed locally

Implemented:
- Decoupled the mocked Right Now greeting from the selected Chore Bundle.
- Added mood/readiness-aware greeting families generated once on load.
- Regenerated the greeting only when time, energy, mood, or goal changes, while
  keeping it stable across shuffle and ordinary recommendation swaps.
- Updated product, implementation, and live-test docs for the greeting
  lifecycle.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- The page-level Right Now greeting is mood/readiness aware and stable across
  shuffle; the Chore Bundle card carries recommendation-specific details.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Right Now care bias principle

Status: completed locally

Implemented:
- Documented the Right Now product tension between the home's needs and the
  user's current readiness.
- Added Recommendation Engine guidance for a gentle, bounded care bias toward
  stale/high-impact Chores when they still fit user constraints.
- Updated voice guidance so Homekeep may nudge toward home care without guilt,
  pressure, or hidden manipulation.

Tests/checks run:
- `git diff --check -- docs/product/HOMEKEEP_APP_PLAN.md docs/specs/RECOMMENDATION_ENGINE.md docs/product/HOMEKEEP_VOICE_SYSTEM.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/specs/RECOMMENDATION_ENGINE.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Homekeep can have a small agenda to help the home get cared for, but it must
  be transparent, explainable, bounded, and easy for the user to correct.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Care bias operating rules

Status: completed locally

Implemented:
- Promoted the Right Now tension recommendations into ten important operating
  rules for product and recommendation behavior.
- Added `Homekeep is gently opinionated, never coercive` as the short design
  principle for this topic.
- Documented stretch-not-shove, light variants, visible nudges, escape hatches,
  non-punitive language, user correction, and successful stopping as core
  constraints.

Tests/checks run:
- `git diff --check -- docs/product/HOMEKEEP_APP_PLAN.md docs/specs/RECOMMENDATION_ENGINE.md docs/product/HOMEKEEP_VOICE_SYSTEM.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/specs/RECOMMENDATION_ENGINE.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Care bias is an important design and scoring principle, not a casual copy
  preference.

Known gaps / next prompt:
- Re-run Gate 3B after installing the updated candidate.

### 2026-06-22 - Live Test 2 checklist from recommendations

Status: completed

Implemented:
- Accepted Codex recommendations as provisional defaults for remaining
  pre-Live-Test-2 Home Health questions.
- Documented that the full Home Health view remains a top-level app destination.
  This Right Now-only scope was superseded by the later Live Test 2 final scope
  decision that includes basic Home Health visibility/navigation.
- Added Gate 3B as a concrete second Right Now live-test checklist.

Tests/checks run:
- `git diff --check -- docs/product/HOMEKEEP_APP_PLAN.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Stop broad app-question review before Live Test 2.
- Build the second Right Now candidate from Prompt 11, then verify it with Gate
  3B.

Known gaps / next prompt:
- Use `docs/implementation/AI_DASHBOARD_UI_STEVE_PROMPTS.md` Prompt 11 to build
  the second Right Now candidate.
- Use Gate 3B in `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md` for Steve's
  second live-test double-check.

### 2026-06-22 - Second Right Now live-test handoff

Status: completed

Implemented:
- Added a reusable Steve prompt for building the second mocked Right Now
  live-test candidate from the live visual review notes.
- Updated the private live-test checklist so Gate 3A reflects the current Right
  Now direction: visible included Chores, no expand/details control, randomize
  with filters, projected-benefit action, and removed-state restoration.
- Updated the current progress summary to point future sessions to Prompt 11
  before service wiring.

Tests/checks run:
- `git diff --check -- docs/implementation/AI_DASHBOARD_UI_STEVE_PROMPTS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/implementation/AI_DASHBOARD_UI_STEVE_PROMPTS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Steve now has a single copy-paste prompt to ask Codex for the second Right Now
  live-test candidate.
- The second candidate remains mocked and visual-first; Homekeep service wiring
  still waits.

Known gaps / next prompt:
- Use `docs/implementation/AI_DASHBOARD_UI_STEVE_PROMPTS.md` Prompt 11 to build
  the second Right Now live-test candidate.

### 2026-06-22 - First sidebar live design review planning

Status: completed

Implemented:
- Added a design-and-visual-first checklist for the first mocked Homekeep
  sidebar app live review.
- Made the next-build rule explicit: tune the mocked Ready Now visual feel
  before wiring Homekeep services if the live review finds friction.
- Updated the current progress summary so future sessions start with the
  design/visual review gate.

Tests/checks run:
- `git diff --check -- docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/product/HOMEKEEP_APP_PLAN.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- The first live sidebar app review starts with design and visuals before
  functional readiness.
- Service wiring waits until Ready Now visual feel, copy tone, and core flow are
  acceptable for private live review.

Known gaps / next prompt:
- Run Gate 3A in a private Home Assistant frontend and record Keep / Change
  before service wiring / Can wait / Open question findings.

### 2026-06-22 - Docs taxonomy and AI-prefix cleanup

Status: completed

Implemented:
- Reorganized docs by purpose into `product/`, `architecture/`, `specs/`,
  `implementation/`, and `live-test/`.
- Added `docs/README.md` as the documentation map and AI-development convention
  guide.
- Prefixed AI-agent operational docs with `AI_` so product and spec docs remain
  visually distinct from Codex runbooks and resume ledgers.
- Renamed the dashboard plan to `docs/product/HOMEKEEP_APP_PLAN.md` to match
  the sidebar app direction.
- Updated repository docs and internal markdown references to the new paths.

Tests/checks run:
- `python3` markdown docs-reference existence check
- `git diff --check`
- stale root-path scan for moved docs

Docs updated:
- `AGENTS.md`
- `ALL_DOCS.md`
- `PROJECT_BRIEF.md`
- `README.md`
- `docs/README.md`
- moved docs across the new docs folders

Important decisions:
- Keep `docs/AI_DECISION_LOG.md` and `docs/AI_IMPLEMENTATION_PROGRESS.md` at
  the docs root because they are the primary AI resume and conflict-resolution
  files.
- Prefix AI-agent operational docs with `AI_`; do not prefix product,
  architecture, or feature specs.

Known gaps / next prompt:
- Keep future docs in the purpose-based folder structure and update
  `docs/README.md` when adding a new source of truth.

### 2026-06-22 - Mocked Ready Now sidebar prototype

Status: completed

Implemented:
- Added Homekeep sidebar frontend registration using a non-iframe custom panel.
- Added a browser-native mocked Ready Now panel with synthetic Chore Bundle
  variants, context chips, shuffle/refining behavior, active Chore Session
  state, timer, completion feedback, final summary, and Bonus Chore reveal.
- Added focused tests for panel static-path registration and unload cleanup.

Tests/checks run:
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend.py custom_components/homekeep/frontend/homekeep-panel.js tests/test_frontend.py tests/test_reload_unload.py docs/AI_DECISION_LOG.md docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- Node REPL module import of `custom_components/homekeep/frontend/homekeep-panel.js`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components/homekeep tests/test_frontend.py tests/test_reload_unload.py`
- `python3 -m unittest discover -s tests -v`

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- The first frontend slice is explicitly mocked and local-only.
- The selected Home Assistant frontend path is a served local JS module plus a
  non-iframe custom panel registered with `frontend.async_register_built_in_panel`.

Known gaps / next prompt:
- Wire Ready Now to Homekeep services only after the mock feel is reviewed.
- Review the mocked Homekeep sidebar app in a real Home Assistant frontend and
  tune visual feel before service wiring.
- Continue dashboard planning after the live Ready Now review; do not treat
  the mocked prototype as full-dashboard approval.

### 2026-06-22 - Area Health documentation clarification

Status: completed

Implemented:
- Documented Area Health as a derived `0..100` health-weighted area score that
  answers how much a Home Assistant Area would benefit from care now.
- Clarified that Area Health is not a percent-of-chores-completed metric.
- Added contributor explanation guidance for stale, high-impact, and
  Projected Impact Chores.

Tests/checks run:
- `git diff --check -- docs/specs/DERIVED_HEALTH.md docs/product/HOMEKEEP_APP_PLAN.md docs/AI_DECISION_LOG.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/specs/DERIVED_HEALTH.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/AI_DECISION_LOG.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Mood Context, Ready-Now Mode, and Scheduled-Suggestion Mode may influence
  recommendations, but should not change the underlying Area Health score in
  MVP.
- Empty areas may calculate as `100` for stability, but UI should present them
  neutrally as having no tracked Chores yet.

Known gaps / next prompt:
- No code changes were needed because the current implementation already uses
  enabled-Chore, health-weighted Area Health derived from durable state.

### 2026-06-22 - Remove former dashboard example direction

Status: completed

Implemented:
- Removed the former dashboard examples and their dedicated tests.
- Removed the former dashboard UI doc and made `docs/product/HOMEKEEP_APP_PLAN.md`
  the UI direction document.
- Updated runtime completion sources from the UI-specific label to
  `dashboard`.
- Kept legacy `bubble_card` completion history migration, now normalizing it to
  `dashboard`.

Tests/checks run:
- `python3 -m unittest tests.test_frontend -v`
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `git diff --check -- PROJECT_BRIEF.md docs/AI_DECISION_LOG.md docs/specs/DERIVED_HEALTH.md docs/product/HOMEKEEP_APP_PLAN.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md custom_components/homekeep/frontend/homekeep-panel.js tests/test_frontend.py`

Docs updated:
- `AGENTS.md`
- `PROJECT_BRIEF.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/AI_DECISION_LOG.md`
- `docs/architecture/HOME_ASSISTANT_CONTRACT.md`
- `docs/implementation/IMPLEMENTATION_PLAN.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`
- Supporting checklist, test plan, mock review, readiness, and UX docs.

Important decisions:
- Homekeep's canonical UI should be a Home Assistant sidebar app, not a
  former dashboard example.
- The app should not be iframe-embedded.
- Lovelace is explicitly out of scope for Homekeep UI implementation.

Known gaps / next prompt:
- Verify the supported Home Assistant frontend extension path against the
  installed package or official developer docs, then implement the sidebar app
  shell in a small focused pass.

### 2026-06-22 - Dashboard UI handoff docs

Status: completed

Implemented:
- Added `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md` with current Codex-facing
  guardrails for future Homekeep sidebar app implementation.
- Added `docs/implementation/AI_DASHBOARD_UI_STEVE_PROMPTS.md` with phased prompts for continuing
  the human UI design review, translating approved decisions, verifying Home
  Assistant frontend assumptions, and starting the first app shell phase.
- Updated `AGENTS.md` planning-file references for the new dashboard UI handoff
  docs.

Tests/checks run:
- `git diff --check -- docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/implementation/AI_DASHBOARD_UI_STEVE_PROMPTS.md AGENTS.md`

Docs updated:
- `AGENTS.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/implementation/AI_DASHBOARD_UI_STEVE_PROMPTS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Future UI sessions should resume the human design review at Home Health and
  Areas before implementing frontend code.
- The last Steve prompt explicitly restarts from the current conversation state.
- A first frontend implementation may be limited to the Ready Now test slice;
  unresolved later workflows remain out of scope.

Known gaps / next prompt:
- For a fast prototype, use `docs/implementation/AI_DASHBOARD_UI_STEVE_PROMPTS.md` Prompt 9A.
- For design review, continue with Prompt 1.

### 2026-06-21 - Remove mock/dev-mode setup paths

Status: completed

Implemented:
- Removed the private `dev_mode` config/options toggle.
- Stopped config entry setup from seeding or repairing bundled synthetic
  Chores.
- Removed the `homekeep.load_sample_chores` service, service schema, service
  metadata, runtime handler, bundled integration sample YAML, and production
  sample YAML parser.
- Deleted the remaining example sample Chore YAML and converted tests that
  depended on sample loading to explicit synthetic in-test Chore definitions.

Tests/checks run:
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `AGENTS.md`
- `PROJECT_BRIEF.md`
- `ALL_DOCS.md`
- `docs/AI_DECISION_LOG.md`
- `docs/architecture/HOME_ASSISTANT_CONTRACT.md`
- `docs/specs/SERVICE_SCHEMAS.md`
- `docs/implementation/AI_SCAFFOLDING_TASKS.md`
- `docs/implementation/TEST_PLAN.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Homekeep setup now loads existing Homekeep storage only. It must not seed
  synthetic Chores, repair sample state, or clear durable test data.
- Test fixtures may still use synthetic in-test data, but production code no
  longer carries a sample Chore loader.

Known gaps / next prompt:
- Reinstall or reload the integration in the private Home Assistant instance
  and confirm the options UI no longer exposes dev mode and setup no longer
  auto-creates Chores.

### 2026-06-21 - Version 0.0.2 private publish prep

Status: completed

Implemented:
- Bumped Homekeep integration version to `0.0.2`.
- Updated mock adequacy and private live-test release notes for the removal of
  private dev mode, bundled sample Chore seeding, and `load_sample_chores`.

Tests/checks run:
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `custom_components/homekeep/manifest.json`
- `docs/live-test/MOCK_ADEQUACY_REVIEW.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- No tag will be created because the repository has no established tag
  convention.
- No deploy script exists in the workspace; this publish is a commit and push
  to `main` for private HACS consumption.

Known gaps / next prompt:
- Update Homekeep through HACS in the private Home Assistant instance and
  confirm version `0.0.2` loads without dev mode or automatic sample Chores.

### 2026-06-21 - Bubble Card to Homekeep app dashboard switch

Status: completed

Implemented:
- Replaced the Bubble Card dashboard target with the former dashboard example
  direction.
- That dashboard example direction has since been retired in favor of the
  sidebar app plan in `docs/product/HOMEKEEP_APP_PLAN.md`.
- Updated completion source validation so new dashboard calls use `dashboard`.
- Added storage normalization for legacy completion records that used
  `bubble_card` as their source.
- Added tests for the Homekeep app examples and legacy source normalization.

Tests/checks run:
- `python3 -m unittest tests.test_storage tests.test_models tests.test_services -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`
- `python3 -m unittest discover -s tests -v`

Docs updated:
- `AGENTS.md`
- `ALL_DOCS.md`
- `PROJECT_BRIEF.md`
- `docs/AI_DECISION_LOG.md`
- `docs/architecture/HOME_ASSISTANT_CONTRACT.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/specs/SERVICE_SCHEMAS.md`
- `docs/architecture/DATA_MODEL.md`
- `docs/implementation/IMPLEMENTATION_PLAN.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/live-test/PRIVATE_LIVE_TEST_RESULTS.md`
- Supporting planning and readiness docs that referenced the former dashboard
  target.

Important decisions:
- Homekeep app is the MVP dashboard layer. Bubble Card is no longer part of the MVP
  implementation target.
- The former helper/script bridge was necessary because dashboard cards did not
  persist Homekeep service response ids for later button calls.

Known gaps / next prompt:
- The former dashboard example had not been rendered in a live Home Assistant
  frontend yet.
- Homekeep app Skip and Snooze helper buttons still need separate live
  confirmation if full dashboard readiness becomes a release target.

### 2026-06-21 - Homekeep app assistant view and Add Chore service

Status: completed

Implemented:
- Added `homekeep.create_chore` as a consumer-facing chore-list mutation
  service. It creates an enabled Chore definition and initial ChoreState, and
  it does not create or schedule a Chore Session.
- Added idempotent `request_id` handling for `create_chore` so duplicate
  dashboard/script retries return the stored result.
- Added Home Assistant service schema and service metadata for
  `create_chore`.
- Reworked the former dashboard example into a single consumer-facing recipe
  with helper/script sections.
- Updated the main view to behave like a calm assistant surface: mood-colored
  greeting tiles, idle session setup, Add Chore controls, and active-session
  controls that appear when `input_text.homekeep_session_id` is populated.
- Removed the separate helper file.

Tests/checks run:
- `python3 -m unittest tests.test_services tests.test_homekeep_scaffold -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`
- `python3 -m unittest discover -s tests -v`

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/architecture/HOME_ASSISTANT_CONTRACT.md`
- `docs/specs/SERVICE_SCHEMAS.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`
- `PROJECT_BRIEF.md`
- `ALL_DOCS.md`

Important decisions:
- Add Chore is a Chore definition/list operation, not a Chore Session
  operation.
- To-do create remains rejected as write-through; the Homekeep app Add Chore
  button calls `homekeep.create_chore` through a script.
- The former consumer example used stock dashboard cards only, with no custom
  cards.

Known gaps / next prompt:
- Render the one-file Homekeep app recipe in a live Home Assistant frontend and
  verify conditional idle/active switching plus tile mood colors.
- Consider adding richer Chore Variant inputs later; MVP create uses a normal
  variant with credit `1.0`.

### 2026-06-21 - Phase 1: Models and storage

Status: completed

Implemented:
- Added `custom_components/homekeep/models.py` with typed dataclasses/enums for
  Chore definitions, Chore Variants, Chore State, and Chore Completions.
- Added validation helpers for finite positive intervals, interval ordering,
  estimated durations, health weights, allowed Chore Variant keys, Variant
  credit bounds, adaptive interval clamping, bounded dismissal/snooze event
  timestamps, and MVP participant attribution.
- Added `custom_components/homekeep/storage.py` with canonical empty storage,
  current storage version `2`, a v1-to-v2 migration hook, unsupported future
  version rejection, validation on load, JSON-safe dump helpers, and sample
  chore loading for tests.
- Added focused `unittest` coverage for invalid intervals, Chore Variant
  validation, participant attribution, v1-to-v2 migration behavior, future
  version rejection, sample chore loading, and storage round trip.

Tests/checks run:
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept Phase 1 pure Python because the requested deliverables do not require
  Home Assistant APIs. No Home Assistant API behavior was assumed.
- Used a tiny fixture-specific YAML parser for `examples/sample_chores.yaml`
  because PyYAML is not installed in the current environment.
- Treated Steve's Phase 1 request as an explicit override of the resume rule
  that would otherwise start with incomplete Phase 0 scaffold work.

Known gaps / next prompt:
- Phase 0 Home Assistant scaffold remains incomplete: no manifest, config
  flow, service registration, or Home Assistant storage wrapper exists yet.
- Health, completion credit application, adaptive interval training, and
  Home/Area Health derivation remain for the next bounded implementation pass.
- Pytest and PyYAML are not installed in this environment; current tests use
  standard-library `unittest`.

### 2026-06-21 - Phase 0: Scaffold

Status: completed

Implemented:
- Added the Home Assistant custom integration scaffold:
  `manifest.json`, `config_flow.py`, `services.yaml`, and `strings.json`.
- Expanded `const.py` with Homekeep domain metadata, platform list, service
  names, service attributes, and allowed enum values used by service schemas.
- Implemented `async_setup`, `async_setup_entry`, and `async_unload_entry` in
  `__init__.py` with empty Phase 0 handlers and schema-validated service
  registration.
- Registered data-producing services with `SupportsResponse.ONLY` and mutation
  or refresh services with `SupportsResponse.OPTIONAL`; no recommendation or
  session logic was implemented.
- Added `HomekeepStorage`, a Home Assistant storage adapter around the existing
  versioned core store, so load paths migrate, validate, repair, and save the
  canonical storage shape.
- Added `tests/test_homekeep_scaffold.py` for manifest, config flow, response
  support wiring, service metadata, and HA storage adapter checks.

Tests/checks run:
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Home Assistant and Voluptuous are not installed in this local environment, so
  Home Assistant APIs were verified against official Home Assistant developer
  docs instead of installed package source.
- Kept Home Assistant imports lazy in `__init__.py` and `storage.py` so the
  pure core tests remain runnable without a local Home Assistant install.
- Used the backed-up GitHub Phase 0 scaffold as historical reference only; the
  implementation was adapted to the current Homekeep service names and storage
  version `2`.

Known gaps / next prompt:
- The scaffold services intentionally return no-op scaffold responses and do
  not generate recommendations, create sessions, or mutate chore state.
- Full Home Assistant integration tests were not run because Home Assistant,
  Voluptuous, and pytest are not installed locally.
- Next recommended prompt: Implement Phase 2 health/adaptive interval helpers:
  completion credit application, adaptive interval training, derived Staleness,
  Home Health, Area Health, and focused tests.

### 2026-06-21 - Phase 2: Health and adaptive intervals

Status: completed

Implemented:
- Added `custom_components/homekeep/health.py` with pure derived functions for
  Staleness, display/priority Staleness, Chore Health, Home Health, Area
  Health, Area Health buckets, Area Health event threshold decisions, and
  Projected Impact.
- Added adaptive interval helpers using the documented v1 formula:
  `old * 0.70 + actual_gap * 0.30`, clamped to each Chore's
  `[min_interval_days, max_interval_days]`.
- Added completion scheduling helpers for Chore Variant credit and
  `next_due_at` derivation, including tiny completions that update schedule
  relief without training adaptive intervals.
- Added explicit non-completion action handling so skip, snooze, dismiss, and
  cancel preserve `adaptive_interval_days`.
- Kept health and staleness out of durable storage; the implementation derives
  values from durable Chore definitions and Chore state on read.
- Added `tests/test_health.py` covering cache loss/restart recomputation,
  completion-followed-by-restart recomputation, min/max interval clamping,
  first completion behavior, tiny/normal/deep completion effects, non-training
  actions, Projected Impact, and Area Health event thresholds.

Tests/checks run:
- `python3 -m unittest tests.test_health -v`
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Used deterministic MVP health formulas where planning docs were qualitative:
  Chore Health is `100 - capped_display_staleness`; Home Health and Area
  Health are enabled-Chore, health-weighted averages.
- Treated missing completion history as fully stale for derived display health,
  while never persisting that staleness result.
- Kept Phase 2 pure Python and independent from Home Assistant runtime APIs.

Known gaps / next prompt:
- Session services still do not create completions or mutate Chore State; Phase
  3 should wire Chore Session lifecycle and service behavior through the engine.
- Group Health is not yet exposed separately because the Phase 2 prompt asked
  for Home Health, Area Health, Staleness, and Projected Impact.
- Next recommended prompt: Implement Phase 3 Chore Session lifecycle with
  materialized Session Items, completion/skip/snooze/dismiss state changes,
  participant attribution, Bonus Chore lifecycle, and focused tests.

### 2026-06-21 - Phase 3: Chore Session lifecycle

Status: completed

Implemented:
- Added `custom_components/homekeep/sessions.py` with a pure core
  `SessionEngine` that serializes durable mutations through an `RLock`.
- Implemented Chore Session start, pause, completion, skip, snooze, dismiss,
  end, Bonus Chore acceptance, lazy Bonus Chore expiry, and terminal-state
  transition guards.
- Materialized Session Items at session start with stable `session_item_id`
  values and caller-facing session response dictionaries.
- Wired completions through the Phase 2 completion helpers so completions update
  durable `ChoreCompletion`, `ChoreState.last_completed_at`,
  `adaptive_interval_days`, and `next_due_at`.
- Added participant attribution validation: out-of-session participants are
  rejected; omitted `completed_by` defaults to `started_by` when available.
- Implemented skip/snooze/dismiss item handling without creating completions or
  training adaptive intervals; snooze and dismissal update bounded ChoreState
  event timestamps.
- Implemented bounded `bonus_pending` and `bonus_active` lifecycle with a
  15-minute pending offer TTL, one Bonus Chore per session, original
  `session_id` reuse, and completion of the accepted Bonus Chore ending the
  session.
- Added request-id idempotency records with 24-hour TTL and 1000-record cap;
  duplicate valid retries return the stored result.
- Added `tests/test_sessions.py` for allowed/disallowed transitions, duplicate
  completion calls, request-id idempotency, participant attribution, skip vs
  complete conflicts, snooze/dismiss side effects, Bonus Chore acceptance,
  expiry, paused-session Bonus Chore eligibility, and incomplete-session
  rejection.

Tests/checks run:
- `python3 -m unittest tests.test_sessions -v`
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept Phase 3 pure Python and storage-backed rather than wiring Home Assistant
  services yet; Phase 0 service handlers still return scaffold responses.
- Stored sessions as JSON-safe dictionaries inside the existing versioned store
  so later service/entity layers can persist them without a migration.
- Implemented a small explicit `start_session` helper for tests and future
  service wiring; RecommendationSnapshot materialization remains for the
  Recommendation Engine pass.

Known gaps / next prompt:
- Home Assistant service handlers still need to call `SessionEngine`; they
  remain no-op scaffold handlers until the service/entity wiring phase.
- RecommendationSnapshot freshness/materialization is not implemented yet and
  should be handled with the Recommendation Engine V1 work.
- Next recommended prompt: Implement Phase 4 Recommendation Engine V1 with
  deterministic scoring, Smart Chore List payloads, RecommendationSnapshots,
  context fingerprints, dismissal/snooze effects, and focused tests.

### 2026-06-21 - Phase 4: Recommendation Engine V1

Status: completed

Implemented:
- Added `custom_components/homekeep/recommendations.py` with deterministic,
  local Recommendation Engine V1 scoring. No LLM or network behavior is used.
- Added normalized component scoring for Staleness, Projected Impact, time fit,
  energy fit, area fit, neutral Calendar Context, Session-History fit, and
  bounded dismissal penalty.
- Added bounded Smart Chore List generation with best Chore Bundle, best single
  chore, easiest useful chore, up to 3 alternates, empty state handling, short
  explanations, projected impact payloads, and stable `recommendation_id`
  values within a RecommendationSnapshot.
- Added RecommendationSnapshot storage with `context_fingerprint`,
  `context_bucket`, candidate score breakdowns, selected recommendations,
  explanations, expiry, invalidation fields, and materialization tracking.
- Added fresh snapshot materialization through the existing `SessionEngine`;
  expired or invalidated snapshots are rejected and fresh sessions copy the
  snapshot `context_fingerprint`.
- Added `custom_components/homekeep/history.py` with deterministic v1
  `context_bucket` generation and sparse Session-History fallback scoring to
  neutral `50.0` when observations are insufficient.
- Added `tests/test_recommendations.py` covering payload shape, stable IDs,
  context fingerprint normalization, sparse history fallback, expired snapshot
  rejection, and fresh snapshot materialization.

Tests/checks run:
- `python3 -m unittest tests.test_recommendations -v`
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept the Recommendation Engine pure Python and deterministic; Home Assistant
  service handlers are still scaffold no-ops until Phase 5 wiring.
- Used a neutral `50.0` Calendar Context score until Calendar Context snapshots
  are implemented.
- Used a deterministic `ctx:v1:<sha256>` context fingerprint from normalized
  non-secret context fields, ignoring volatile timestamps like `created_at`.

Known gaps / next prompt:
- Home Assistant services still need to call `RecommendationEngine` and
  `SessionEngine`, persist changed stores, and return action-response payloads.
- Calendar Context, Mood Context inference, and richer dismissal cooldown logic
  remain future phases or hardening work.
- Next recommended prompt: Implement Phase 5 Home Assistant service wiring and
  initial entities/to-do projections around the existing core engine.

### 2026-06-21 - Phase 5: Home Assistant services and entities

Status: completed

Implemented:
- Replaced the Phase 0 scaffold service handler with real Homekeep service
  handlers that load the active integration store, call a small
  `HomekeepServiceRuntime`, persist successful mutations, and translate core
  validation errors to Home Assistant service validation errors when Home
  Assistant is installed.
- Added `custom_components/homekeep/runtime.py` as a testable adapter over
  `RecommendationEngine` and `SessionEngine` for Smart Chore List generation,
  recommendation/session starts, complete/skip/snooze/dismiss, pause, accept
  Bonus Chore, end session, and a minimized calendar-context refresh stub.
- Enabled Phase 5 platforms: `sensor`, `binary_sensor`, and `todo`.
- Added initial sensors for Home Health, due Chore count, best next Chore, and
  minimized calendar context.
- Added per-Chore due binary sensors.
- Added To-do projections for latest recommendations and the active Chore
  Session. Active-session projected completions write through with Homekeep
  metadata; create/delete/edit/rename/move/reorder attempts refresh the
  projection and raise a Homekeep mutation error.
- Added tests for malformed service payloads, unknown IDs, service
  idempotency, valid projected To-do completion, invalid projection completion,
  and To-do mutation traps.

Home Assistant API verification:
- Home Assistant is not installed in the local test environment, so Phase 5 API
  assumptions were verified against official Home Assistant developer docs.
- Verified service action registration/response support expectations from the
  Home Assistant service developer docs.
- Verified `TodoListEntity`, `TodoItem`, `TodoItemStatus`, supported feature
  flags, and async create/delete/update/move handlers from the official To-do
  entity developer docs.
- Verified the basic sensor and binary sensor entity patterns from the official
  entity developer docs.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components/homekeep`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept service behavior small and local: Home Assistant handlers adapt payloads
  and persistence, while existing Homekeep engines remain authoritative for
  durable mutations and recommendation behavior.
- To-do projections advertise update support only so Home Assistant can send
  completion updates; updates that are actually edits/renames are rejected and
  refreshed from storage.
- Recommendation To-do items remain non-completable suggestions until a
  recommendation is materialized into a session; active-session To-do items are
  the write-through completion surface.
- Calendar refresh remains a minimized Phase 5 stub with no raw calendar event
  details; the full Calendar Context phase still owns real calendar snapshot
  behavior.

Known gaps / next prompt:
- Home Assistant package is not installed locally, so Phase 5 was verified with
  unit tests plus official docs rather than an in-process Home Assistant test
  harness.
- Entity coverage is intentionally MVP-minimal; unload/reload behavior,
  dynamic entity additions after chore import, and richer action response
  payloads should be hardened in the Phase 9 test/reload pass.
- Calendar Context, Homekeep app dashboard wiring, and To-do area projections
  remain later phases.
- Next recommended prompt: Implement Phase 6 Calendar Context with minimized
  durable snapshots, freshness checks, entity invalidation, and tests.

### 2026-06-21 - Mood Context Post-Prototype Planning

Status: completed

Implemented:
- Added a post-prototype improvement note to `docs/specs/MOOD_CONTEXT.md` for
  evolving Mood Context into broader Readiness Context after the MVP prototype.
- Captured the future direction in `docs/AI_DECISION_LOG.md` so future
  implementation keeps mood optional, explainable, and subordinate to practical
  planning signals.

Tests/checks run:
- Not run; documentation-only update.

Docs updated:
- `docs/specs/MOOD_CONTEXT.md`
- `docs/AI_DECISION_LOG.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- The MVP Mood Context rules remain unchanged.
- Post-prototype improvements should focus on chore friction, safer
  explanations, explicit session modes, and user correction rather than deeper
  emotional inference.

Known gaps / next prompt:
- Next implementation work remains Phase 5 Home Assistant service wiring unless
  Steve asks to revise Mood/Readiness Context docs further.

### 2026-06-21 - Mood And Readiness Feature Plan

Status: completed

Implemented:
- Added `docs/product/MOOD_READINESS_FEATURE_PLAN.md` as the coherent
  post-prototype plan for evolving Mood Context into Readiness Context.
- Consolidated session modes, chore-friction learning, safer explanation
  wording, Home Assistant signals, opt-in wearable signals, open-source/local
  source options, storage/privacy rules, implementation phases, and tests.
- Replaced the long post-prototype note in `docs/specs/MOOD_CONTEXT.md` with a
  pointer to the dedicated feature plan.
- Updated `docs/AI_DECISION_LOG.md` to reference the new plan.

Tests/checks run:
- `git diff --check -- docs/product/MOOD_READINESS_FEATURE_PLAN.md docs/specs/MOOD_CONTEXT.md docs/AI_DECISION_LOG.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/product/MOOD_READINESS_FEATURE_PLAN.md`
- `docs/specs/MOOD_CONTEXT.md`
- `docs/AI_DECISION_LOG.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- MVP Mood Context remains unchanged.
- Post-prototype Readiness Context should expose session posture to users
  rather than claiming to know the user's mood.
- Wearable and Home Assistant signals must be opt-in, derived, short-lived, and
  subordinate to explicit user choices.

Known gaps / next prompt:
- Next implementation work remains Phase 6 Calendar Context unless Steve asks
  for further Mood/Readiness planning.

### 2026-06-21 - Phase 6: Calendar Context

Status: completed

Implemented:
- Added `custom_components/homekeep/calendar_context.py` with selected calendar
  entity normalization, source version tracking, freshness checks, derived
  signal extraction, max-age expiry, context version hashes, and invalidation
  helpers.
- Added Home Assistant options for selecting calendar entities with a calendar
  entity selector.
- Wired `homekeep.refresh_calendar_context` to build minimized snapshots from
  selected or caller-provided calendar entities.
- Added lazy Calendar Context freshness refresh before Smart Chore List
  generation when selected calendars are configured.
- Added automatic invalidation listeners for selected calendar entity state
  changes during config entry setup, including dependent RecommendationSnapshot
  invalidation.
- Updated the Recommendation Engine to include fresh Calendar Context id/version
  in context fingerprints and RecommendationSnapshots, and to use a bounded
  derived calendar context score instead of a permanently neutral score.
- Updated the next-calendar-context sensor to report stale derived context when
  a snapshot has been invalidated.
- Added tests for derived snapshots, raw-detail minimization, max-age
  freshness, source version changes, target-window changes, calendar state
  invalidation, dependent recommendation invalidation, and runtime service
  wiring.

Home Assistant API verification:
- Home Assistant is not installed locally, so Phase 6 calendar assumptions were
  verified against official Home Assistant developer docs and current Home
  Assistant core source.
- Verified Calendar entities expose timezone-aware `async_get_events(hass,
  start_date, end_date)` patterns and `CalendarEvent` fields.
- Verified the built-in `calendar.get_events` service supports response data
  for event fetching.
- Verified `homeassistant.helpers.event.async_track_state_change_event` is the
  current state-change helper and that older `async_track_state_change` is
  deprecated.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_calendar_context -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Calendar Context stores only minimized derived signals and source version
  metadata; raw summary, description, and location text are used transiently
  during refresh and are not stored in durable snapshots.
- Recommendation generation refreshes stale selected Calendar Context lazily
  rather than doing unbounded background recommendation work on every calendar
  state change.
- The Phase 6 event fetch path uses Home Assistant's `calendar.get_events`
  service response instead of trying to reach into calendar entity internals.
- Calendar scoring remains bounded and explainable, with neutral behavior when
  there is no fresh context.

Known gaps / next prompt:
- Full in-process Home Assistant tests are still deferred because Home
  Assistant is not installed locally.
- Calendar signal extraction is MVP keyword-based and intentionally minimal;
  richer source-specific semantics can be hardened later.
- Existing uncommitted Mood/Readiness planning docs remain separate from Phase
  6 implementation work.
- Next recommended prompt: Implement Phase 7 Homekeep sidebar app MVP
  and service wiring around the completed Homekeep services.

### 2026-06-21 - Phase 7: Former dashboard example

Status: completed

Implemented:
- Added the former dashboard example with a Homekeep dashboard view,
  Ready-Now launcher, time/energy/goal/mood controls, recommendation display,
  active-session controls, Done for now, One more, and Accept one more flow.
- Used stock dashboard sections, tile, entities, grid, button, and To-do list
  cards for the dashboard surface.
- Used Home Assistant helpers/scripts where dashboard cards need durable bridge
  state for Homekeep response ids.
- Documented required companion helper entities and scripts in the example
  YAML so scripts can read local selections, call Homekeep services, and store
  returned response ids.
- Updated `docs/product/HOMEKEEP_APP_PLAN.md` with the Phase 7 capability gap and helper
  script bridge.

Homekeep app capability verification:
- Verified the example uses stock Home Assistant frontend and Home Assistant tap actions
  with `call-service`.
- Identified a gap: Homekeep app dashboard YAML should not be relied on to
  capture Home Assistant service response payloads and bind returned ids into
  later service calls.

Tests/checks run:
- `python3 - <<'PY' ...` dashboard example content check
- `git diff --check`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/AI_DECISION_LOG.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept the dashboard as an MVP example surface; Homekeep storage, sensors, and
  To-do projections remain authoritative.
- Used helper/script bridging for `snapshot_id`, `recommendation_id`,
  `session_id`, `session_item_id`, and Bonus Chore ids because those values
  come from Homekeep service responses or current session context.
- Did not add runtime code for scripts or helpers in Phase 7 because the prompt
  requested the dashboard example and not a Home Assistant package blueprint.

Known gaps / next prompt:
- The example assumes companion helpers and scripts exist. A future hardening
  pass can add packaged helper/script examples or native Homekeep entities that
  expose current recommendation/session ids directly.
- The dashboard YAML was syntax/content checked locally but not rendered in a
  live Home Assistant frontend.
- Next recommended prompt: Implement Phase 8 hardening and release readiness:
  reload/unload behavior, migration edge cases, entity refresh behavior,
  service response polish, packaged helper/script examples, and focused Home
  Assistant integration tests where dependencies are available.

### 2026-06-21 - Phase 8: Hardening and release readiness

Status: completed

Implemented:
- Hardened `HomekeepServiceRuntime` so missing required service fields raise
  `HomekeepValidationError` instead of raw `KeyError`.
- Added malformed service payload tests for missing `chore_id`,
  `snooze_minutes`, `recommendation_snapshot_id`, `session_id`, and `status`.
- Added stale session response coverage: a stale completion attempt after
  session cancellation is rejected and does not create a completion or mutate
  terminal session state.
- Expanded storage migration tests for version `2` loading, missing optional
  sections, stale unknown-Chore state cleanup, and invalid stored values.
- Added config entry unload/reload mock coverage for platform unload success,
  failed platform unload preservation, and calendar listener cleanup.
- Added `docs/live-test/MOCK_ADEQUACY_REVIEW.md` for pre-`1.0` version-bump readiness.
- Updated `docs/implementation/IMPLEMENTATION_READINESS_REVIEW.md` with Phase 8 hardening
  notes and remaining public-release test gaps.

Deploy workflow status:
- Reviewed the working tree before changes.
- No version bump was requested or performed.
- No deploy, publish, tag, or release command was run.
- Pre-`1.0` mock adequacy was reviewed. Current mocks are adequate for local
  developer readiness, but not enough to claim public release readiness without
  Home Assistant package-backed tests or an approved live synthetic candidate.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_services tests.test_storage tests.test_reload_unload -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `git diff --check`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`
- `docs/implementation/IMPLEMENTATION_READINESS_REVIEW.md`
- `docs/live-test/MOCK_ADEQUACY_REVIEW.md`

Important decisions:
- Kept Phase 8 scoped to local hardening and release readiness review. No
  deploy or version bump was performed because Steve explicitly said not to
  deploy unless asked.
- Used local fakes for Home Assistant lifecycle behavior because Home Assistant
  is not installed in the local environment.
- Treated Home Assistant package-backed integration tests as a remaining
  release-readiness gap rather than pretending source checks are equivalent.

Known gaps / next prompt:
- Add Home Assistant package-backed tests for config flow, service
  registration/action responses, sensors, binary sensors, To-do projections,
  calendar services, reload/unload, and entity refresh behavior.
- Add packaged helper/script examples for the former dashboard example
  if the dashboard should be one-copy deployable.
- Next recommended prompt: Add Home Assistant package-backed integration tests
  and release checklist automation, or ask explicitly for a version bump/release
  pass when ready.

### 2026-06-21 - Private HACS live-test seeding helper

Status: completed

Implemented:
- Added bundled synthetic Chore fixtures to the installed integration package
  for private HACS testing.
- Added a private `dev_mode` config/options toggle, defaulting to true, so a
  new config entry seeds bundled sample Chores automatically when storage is
  empty. The options flow reloads Homekeep when the toggle changes.
- Added `homekeep.load_sample_chores` with a `replace_existing` guard so the
  private test instance can explicitly reset synthetic Homekeep data from
  Developer Tools > Actions.
- Expanded the bundled fixture to 22 synthetic Chores across kitchen,
  bathroom, living room, entryway, laundry, bedroom, plants, office, hallway,
  and admin groups.
- Updated the private live-test checklist to use the bundled seed service.
- Adjusted README language so it describes Steve's private test status without
  public-user expectations.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_homekeep_scaffold tests.test_reload_unload tests.test_services tests.test_storage -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_services tests.test_storage -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `README.md`
- `docs/AI_DECISION_LOG.md`
- `docs/architecture/HOME_ASSISTANT_CONTRACT.md`
- `docs/specs/SERVICE_SCHEMAS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept sample loading as a private test seed helper, not a general Chore import
  API.
- Automatic setup seeding is gated by private dev mode and only runs when
  Homekeep storage has no Chores, so install/reload does not overwrite existing
  live-test data.
- The helper refuses to overwrite existing stored Chores unless
  `replace_existing=true`, and replacement intentionally resets other durable
  Homekeep test state to avoid mixed old/new synthetic data.

Known gaps / next prompt:
- Push the private dev-mode seeding update, then update/re-download Homekeep
  through HACS and run Gate 3 by confirming automatic synthetic Chore setup.

### 2026-06-21 - Private HACS live-test due-state repair

Status: completed and live-confirmed

Implemented:
- Updated bundled sample Chore seeding so synthetic Chore states are
  immediately due for private live testing instead of having `next_due_at=null`.
- Added a dev-mode setup repair for existing previously seeded sample Chores:
  if a bundled sample Chore exists, has no completion history, and has no
  `next_due_at`, setup marks it due without replacing Chore definitions or
  touching completed/scheduled Chores.
- Added regression coverage using the actual due-count sensor and per-Chore
  binary sensor classes.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_reload_unload tests.test_services tests.test_storage -v`

Important decisions:
- Kept normal `ChoreState.new_for_chore` unchanged. Only private bundled sample
  seed/repair behavior marks chores immediately due.
- Existing live-test stores from the first seed pass can be repaired by
  updating through HACS and restarting with dev mode enabled.

Known gaps / next prompt:
- Gate 3 synthetic data setup is live-confirmed on the private HACS install.
- Next prompt: run Gate 4 service smoke tests from Developer Tools > Actions,
  starting with `homekeep.generate_smart_chore_list`.

### 2026-06-21 - Calendar Context live-test hardening

Status: completed locally, pending private HACS live retest

Implemented:
- Added `source_calendar_event_fingerprint` to Calendar Context snapshots.
- Built the fingerprint from minimized event facts: event start/end times and
  derived guest, travel, trash, and evening flags. Raw event summary,
  description, and location text are not stored.
- Updated Calendar Context freshness checks so recommendation generation can
  detect added or modified selected calendar events even when the Home
  Assistant calendar entity state metadata remains unchanged.
- Changed Calendar Context refresh to invalidate dependent
  RecommendationSnapshots when the refreshed minimized calendar context version
  changes.

Tests/checks run:
- `python3 -m unittest tests.test_calendar_context -v`
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/specs/CALENDAR_CONTEXT.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/live-test/PRIVATE_LIVE_TEST_RESULTS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept the durable calendar data minimized by storing only a hash of reduced
  event facts and derived category flags.
- Treated event additions/modifications as enough to refresh Calendar Context
  before recommendation reuse, because some Home Assistant calendar providers
  may keep the calendar entity state as `off` after an event edit.

Known gaps / next prompt:
- Update Homekeep through HACS, restart/reload, then retest Gate 6 by adding or
  modifying a synthetic event on the selected test calendar and generating a
  fresh Smart Chore List. Confirm the Calendar Context snapshot changes and the
  old dependent RecommendationSnapshot is not reused.
- Homekeep app dashboard Gate 8 still needs private live testing.
- Home Assistant package-backed automated tests remain a public-release
  blocker.

### 2026-06-21 - Calendar Context French keyword support

Status: completed locally, pending private HACS live retest

Implemented:
- Added basic French Calendar Context keywords alongside the existing English
  terms for guest/visit, travel/departure, and trash/recycling/compost signals.
- Centralized keyword checks so derived Calendar Context signals and minimized
  event fingerprints classify events consistently.
- Added regression coverage using synthetic French calendar event titles.

Tests/checks run:
- `python3 -m unittest tests.test_calendar_context -v`

Docs updated:
- `docs/specs/CALENDAR_CONTEXT.md`
- `docs/AI_DECISION_LOG.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept this as simple local keyword matching for private live testing, not a
  language model or broad localization system.
- Included accented and unaccented French forms for common live-test calendar
  phrases.

Known gaps / next prompt:
- Commit and push, update through HACS, then retest with a synthetic French
  event title such as `Visite d'invités pour souper`.

### 2026-06-21 - Gate 6 Calendar Context live confirmation

Status: completed and live-confirmed

Implemented:
- No code change in this pass; recorded private HACS live-test evidence for
  Calendar Context event-fingerprint and French keyword behavior.

Tests/checks run:
- Private HACS live test on Home Assistant Core `2026.6.3`.
- `homekeep.refresh_calendar_context` with selected calendar entity
  `calendar.activites`.
- `homekeep.generate_smart_chore_list` after refreshed Calendar Context.
- `sensor.homekeep_next_calendar_context` state check.

Docs updated:
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/live-test/PRIVATE_LIVE_TEST_RESULTS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Treated Gate 6 as live-confirmed after Homekeep detected a synthetic French
  event, derived `has_guests_soon: true`, stored only
  `source_calendar_event_fingerprint`, generated a fresh Smart Chore List, and
  exposed `guests` through `sensor.homekeep_next_calendar_context`.

Known gaps / next prompt:
- Calendar listener behavior after reload is still not separately
  live-confirmed.
- Homekeep app dashboard Gate 8 remains the next private live-test gate.
- Home Assistant package-backed automated tests remain a public-release
  blocker.

### 2026-06-21 - Bilingual string-signal guessing

Status: completed locally

Implemented:
- Added a shared `text_signals` helper for local English/basic-French keyword
  matching with case and accent normalization.
- Moved Calendar Context keyword classification onto the shared helper so
  derived signals and event fingerprints continue to treat French calendar text
  consistently.
- Updated Recommendation Engine calendar-fit guesses from Chore names, Chore
  groups, and Home Assistant Area ids so French terms such as `salle de bain`,
  `poubelles`, and `recyclage` can influence guest-prep and trash-day scoring.
- Added focused recommendation coverage for French Chore string guesses.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_recommendations tests.test_calendar_context -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `git diff --check`

Docs updated:
- `docs/specs/CALENDAR_CONTEXT.md`
- `docs/AI_DECISION_LOG.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`
- `docs/specs/RECOMMENDATION_ENGINE.md`

Important decisions:
- Kept this as bounded local keyword matching, not a broad localization system
  or language model.
- Treated French support as a shared rule for all current string-based signal
  guesses rather than only Calendar Context event text.

Known gaps / next prompt:
- Full Home Assistant package-backed automated tests remain a public-release
  blocker.
- Homekeep app dashboard Gate 8 remains the next private live-test gate.

### 2026-06-21 - Homekeep app companion helper example

Status: completed locally, pending private HACS live retest

Implemented:
- Added helper and bridge script sections for the dashboard recipe.
- Updated `accept_bonus_chore` responses to include the materialized bonus
  `session_item_id`, so the Homekeep app bridge can continue after accepting
  One more without scraping To-do internals.
- Updated Homekeep app and service docs to point at the companion helper file
  and document the bonus accept response.

Tests/checks run:
- `python3 -m unittest tests.test_sessions -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `python3 -m unittest discover -s tests -v`
- `git diff --check`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/specs/SERVICE_SCHEMAS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept helper state in Home Assistant helper entities only as dashboard bridge
  state. Homekeep storage remains authoritative for Chores, sessions, and
  projections.
- The dashboard bridge stores the best single recommendation by default, with
  bundle/easiest fallback, because Home Assistant frontend cannot comfortably capture
  arbitrary service response choices without scripts.

Known gaps / next prompt:
- Run focused tests, commit, push, update through HACS, then paste/create the
  helpers/scripts and dashboard YAML in Home Assistant for Gate 8 live testing.

### 2026-06-21 - Homekeep app start helper template fix

Status: completed locally, pending private HACS live retest

Implemented:
- Fixed the Homekeep app helper script to reference the
  `start_recommendation` response `items` key with bracket notation. Home
  Assistant Jinja treats `homekeep_start.items` as the dictionary method, so
  the bridge must use `homekeep_start['items']`.
- Recorded the partial Gate 8 live result: Generate succeeded, Start created a
  session, and helper storage failed only at the script template layer.

Tests/checks run:
- `python3 -m unittest tests.test_frontend -v`
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `git diff --check -- PROJECT_BRIEF.md docs/AI_DECISION_LOG.md docs/specs/DERIVED_HEALTH.md docs/product/HOMEKEEP_APP_PLAN.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md custom_components/homekeep/frontend/homekeep-panel.js tests/test_frontend.py`

Docs updated:
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept using service response data instead of scraping To-do projection
  internals. The fix is purely the Jinja access form for a response key named
  `items`.

Known gaps / next prompt:
- Commit and push the helper fix, update/reload scripts in Home Assistant, then
  continue Gate 8 with Done, Skip/Snooze, Done for now, and One more actions.

### 2026-06-21 - Homekeep app end-session helper response fix

Status: completed locally, pending private HACS live retest

Implemented:
- Added `response_variable: homekeep_end` to
  `script.homekeep_end_session_completed` in
  Homekeep app helper script, because `homekeep.end_session` is a
  response-only Home Assistant action.
- Recorded that the Homekeep app complete helper successfully completed the
  active item after helper ids were restored from the Start trace.

Tests/checks run:
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`
- Secret/private-detail scan over changed files with `rg`; hits were limited
  to benign documented field names and checklist text.

Docs updated:
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept `homekeep.end_session` response-only and fixed the dashboard bridge
  script to follow the Home Assistant service contract.

Known gaps / next prompt:
- Commit and push this helper fix, reload scripts in Home Assistant, then
  retest Done for now and continue One more / Accept one more.

### 2026-06-21 - Gate 8 Homekeep app main flow confirmation

Status: completed for private MVP main flow

Implemented:
- No code change in this pass; recorded private HACS live-test evidence for
  the Homekeep app companion helper/scripts.

Tests/checks run:
- Private HACS live test on Home Assistant Core `2026.6.3`.
- `script.homekeep_generate_ready_now`
- `script.homekeep_start_selected_recommendation`
- `script.homekeep_complete_selected_session_item`
- `script.homekeep_end_session_completed`
- `script.homekeep_offer_bonus_chore`
- `script.homekeep_accept_bonus_chore`
- Bonus Chore completion and active-session To-do check.

Docs updated:
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/live-test/PRIVATE_LIVE_TEST_RESULTS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Treated a second completion failure with `session cannot accept completions`
  as expected after `todo.homekeep_active_session` reached `0`, because the
  session was already terminal.

Known gaps / next prompt:
- Homekeep app Skip and Snooze helper buttons still need separate live
  confirmation if full dashboard readiness becomes a release target.
- Calendar listener behavior after reload remains not separately
  live-confirmed.
- Home Assistant package-backed automated tests remain a public-release
  blocker.

### 2026-06-21 - Homekeep Not Loaded startup fix

Status: completed locally, pending private HACS live retest

Implemented:
- Investigated Steve's Home Assistant log export after the UI showed
  `Hubs > Homekeep > Not loaded`.
- Fixed Homekeep setup failing during service schema registration by importing
  `ATTR_VISIBILITY` in `custom_components/homekeep/__init__.py`.
- Added a scaffold test that actually builds Homekeep's service schemas with
  lightweight Home Assistant and voluptuous stand-ins, so missing schema
  constants fail in unit tests before a live Home Assistant restart.

Tests/checks run:
- `python3 -m unittest tests.test_homekeep_scaffold tests.test_services -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Treated the log's `NameError: name 'ATTR_VISIBILITY' is not defined` as the
  direct cause of the Homekeep "Not loaded" state.
- Kept the fix limited to startup/schema registration and test coverage; no
  service contract changes were needed.

Known gaps / next prompt:
- Commit/push or reinstall this local fix, then reload or restart the private
  Home Assistant instance and confirm Homekeep loads.

### 2026-06-21 - Version 0.0.3 private publish prep

Status: completed locally, pending push and private HACS live retest

Implemented:
- Bumped Homekeep integration version to `0.0.3`.
- Updated mock adequacy and private live-test release notes for the Homekeep
  startup schema import fix.

Tests/checks run:
- `python3 -m unittest` for the former dashboard example tests
- `ruby -e "require 'yaml'; ..."` over the former dashboard example files
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`
- `python3` YAML parse check was attempted but skipped because PyYAML is not
  installed locally.

Docs updated:
- `custom_components/homekeep/manifest.json`
- `docs/live-test/MOCK_ADEQUACY_REVIEW.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- No tag will be created because the repository has no established tag
  convention.
- No deploy script exists in the workspace; this publish is a commit and push
  to `main` for private HACS consumption.

Known gaps / next prompt:
- Update Homekeep through HACS in the private Home Assistant instance and
  confirm version `0.0.3` loads.

### 2026-06-21 - Split Homekeep app example files

Status: completed locally

Implemented:
- Split the former Homekeep dashboard example into separate paste targets:
  a helper file for package helpers/scripts and a raw dashboard editor file.
- Replaced the old combined dashboard example with a short
  index pointing to the two target-specific files.
- Updated Homekeep app docs, private live-test checklist text, mock adequacy text,
  and tests to reference the split examples.

Tests/checks run:
- `python3 -m unittest tests.test_frontend -v`
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `git diff --check -- PROJECT_BRIEF.md docs/AI_DECISION_LOG.md docs/specs/DERIVED_HEALTH.md docs/product/HOMEKEEP_APP_PLAN.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md custom_components/homekeep/frontend/homekeep-panel.js tests/test_frontend.py`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/live-test/MOCK_ADEQUACY_REVIEW.md`
- `docs/implementation/AI_SCAFFOLDING_TASKS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`
- `PROJECT_BRIEF.md`
- `ALL_DOCS.md`

Important decisions:
- The raw dashboard file intentionally starts at `title: Homekeep`; there is no
  wrapper key to strip before pasting into Homekeep app.

Known gaps / next prompt:
- Reload packages/scripts in Home Assistant, paste the raw dashboard file, and
  run the dashboard smoke flow.

### 2026-06-22 - Learned Chore duration and lower-friction session start

Status: completed locally

Implemented:
- Added storage version `3` with `ChoreState.duration_samples_minutes` for
  bounded learned Chore duration samples.
- Trained duration samples from real timed Chore Session item completions when
  `started_at` precedes `completed_at`; skips, snoozes, dismissals,
  cancellations, direct non-session completions, and invalid timing do not
  train duration.
- Made the first session item active at session start and automatically
  activates the next pending item when the current item is completed, so timing
  can be learned without an extra form/action step.
- Used the learned median duration for recommendation `estimated_minutes`,
  time-fit scoring, and materialized session item display, falling back to the
  user-entered Chore estimate when no samples exist.
- Stored the generation request context on RecommendationSnapshots and made
  `start_recommendation` infer session mode, time budget, energy level, target
  time window, and area preference from that context and the selected
  recommendation.

Tests/checks run:
- `python3 -m unittest tests.test_storage tests.test_sessions tests.test_recommendations tests.test_services -v`
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`
- Stale-reference scan for old storage/source/dashboard wording.

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/architecture/DATA_MODEL.md`
- `docs/architecture/STORAGE_MIGRATIONS.md`
- `docs/specs/SERVICE_SCHEMAS.md`
- `docs/specs/RECOMMENDATION_PAYLOADS.md`
- `docs/architecture/HOME_ASSISTANT_CONTRACT.md`
- `docs/implementation/TEST_PLAN.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept `ChoreDefinition.estimated_minutes` as the user-correctable fallback
  instead of mutating it directly.
- Did not add a separate `start_chore_session` path; the canonical
  `start_recommendation` service remains the only MVP session materialization
  path.
- Did not fabricate learned duration from historical completions or static
  estimates, because those records do not prove active work time.

Known gaps / next prompt:
- Private Home Assistant retest should confirm storage migration from version
  `2` to `3` and that session forms no longer ask for fields inferred from the
  selected recommendation.

### 2026-06-22 - Right Now language moves away from reset

Status: completed locally

Implemented:
- Replaced visible Right Now mock copy that framed the recommendation as a
  `reset` with Task Bundle, lift, or useful-pass language.
- Changed the projected-benefit action accessible label from `Choose this reset`
  to `Start this bundle`.
- Renamed visible mock bundle titles such as `Kitchen Reset` and
  `Evening Reset` to `Kitchen Lift` and `Evening Lift`.
- Reframed full-reset Keeps as Bundle Keeps in the product plan, voice system,
  Codex UI instructions, decision log, and mocked frontend copy.
- Kept internal ids, method names, and legacy values containing `reset`
  untouched when they are compatibility or implementation details rather than
  user-facing copy.

Tests/checks run:
- `git diff --check -- AGENTS.md PROJECT_BRIEF.md custom_components/homekeep/frontend/homekeep-panel.js docs/AI_DECISION_LOG.md docs/AI_IMPLEMENTATION_PROGRESS.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/product/HOMEKEEP_APP_PLAN.md docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- Targeted `rg` scan for old Right Now reset phrases such as
  `Choose this reset`, `full-reset Keeps`, `Kitchen Reset`, and `small reset`.
- Targeted `rg` scan for visible `Chore`/`Chores` in product/UI files; only
  the intentional `Legacy Chore` compatibility note remains in
  `PROJECT_BRIEF.md`.

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`
- `PROJECT_BRIEF.md`

Important decisions:
- `Reset` is no longer the main Right Now concept. It sounds like clearing a
  productivity slate instead of contributing care to the home.
- The preferred main action label is `Start this bundle`.
- `Bundle Keeps` is the preferred user-facing phrase for intact-bundle harmony
  Keeps.

Known gaps / next prompt:
- Continue preserving internal/API compatibility names until a deliberate
  migration plan covers aliases, storage compatibility, services, and tests.

### 2026-06-23 - Add While You're There compatible Tasks to bundles

Status: completed locally

Implemented:
- Replaced hard-coded `While you're there` Tasks with a small candidate selector
  that pre-includes at most one compatible Task per mocked Right Now Task
  Bundle.
- The mock selector filters for same Area/context compatibility, tiny duration,
  Mood/Capacity fit, useful health/staleness value, and recent removal
  avoidance.
- Rendered compatible Tasks as subtle included Tasks visible from the start of
  the suggested bundle rather than post-completion optional continuation Tasks.
- Included compatible Tasks in the active Task Session when the bundle starts,
  so they can be started before the core bundle is complete.
- Added mocked post-completion momentum Task candidates that can be larger than
  the default optional continuation Tasks when Mood/Capacity suggests the user
  may want to keep going.
- Kept low/quiet contexts biased toward small optional continuation Tasks.
- Kept compatible add-ons removable before session start.
- Made Bundle Keeps depend only on core Tasks, so removing a `While you're
  there` Task does not deactivate Bundle Keeps.
- Documented the distinction between pre-start compatible add-ons and
  post-completion optional Tasks.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/AI_DECISION_LOG.md docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/AI_IMPLEMENTATION_PROGRESS.md`
- Targeted `rg` scan for `While you're there`, `while you are there`,
  `whileThere`, and `momentum` across the changed frontend and planning docs.
- Targeted `rg` scan for `WHILE_THERE_CANDIDATES`, `scoreWhileThereTask`,
  `pickWhileThereTask`, `rejectedWhileThere`, compatibility-context terms, and
  generated `whileThere: true` usage.

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- `While you're there` Tasks are pre-included opportunistic compatible Tasks
  inside a suggested Task Bundle.
- They should be small and explainable by same Area, route, setup, or device
  context.
- They are not required for Bundle Keeps and should not make the core bundle
  feel punitive if removed.
- Post-completion momentum Tasks are a separate concept: they may be larger,
  appear only after the planned bundle is complete, and must be framed as an
  optional way to use momentum rather than a new finish line.
- The planned bundle must complete cleanly before Momentum Tasks appear; the app
  should not move the finish line after the user succeeds.
- Momentum Tasks should feel special and bounded, not like every bundle always
  asks for more.
- Future recommendation payloads should distinguish `core`, `while_there`, and
  `momentum` roles instead of overloading `optional`.
- While You're There selection should be hard-compatibility first, then scoring;
  omit it when no candidate clearly fits.

Known gaps / next prompt:
- Backend Recommendation Engine payloads do not yet have a dedicated
  `while_you_are_there` role; add that deliberately when moving this from mock
  UI behavior to durable recommendation payloads.

### 2026-06-23 - Live Test 3 Home Health visual entry

Status: completed locally

Implemented:
- Added a panel-level `Right Now` / `Home Health` tab treatment to the mocked
  Homekeep sidebar app.
- Kept Right Now as the default opening surface.
- Added a mocked synthetic Home Health visual surface with a whole-home header,
  supportive status copy, and Area Health cards.
- Area cards separate `Helped lately` from `Could help next` so contribution
  stays visible even while health naturally drifts down.
- Kept the Home Health surface visual-only and synthetic for private live-test
  review; no Homekeep services are called from the sidebar app yet.
- Added a Gate 3C private live-test checklist for today's closest-to-production
  mocked sidebar candidate.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_frontend -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js tests/test_frontend.py docs/AI_DECISION_LOG.md docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Tests updated:
- `tests/test_frontend.py`

Important decisions:
- Live Test 3 may visually test Home Health from inside the panel through a
  dedicated tab.
- This does not validate backend Home Health wiring, Area action flows, Area
  configuration behavior, stale-state recovery, or the broader dashboard.
- Home Health visual copy should stay supportive and contextual, not grade-like.

Known gaps / next prompt:
- Run Gate 3C in the private Home Assistant instance and record visual findings
  before wiring Homekeep services into the sidebar app.

### 2026-06-23 - Version 0.0.5 private Live Test 3 publish prep

Status: completed locally

Implemented:
- Bumped the Homekeep integration manifest version from `0.0.4` to `0.0.5`.
- Updated the private live-test checklist release notes for the Live Test 3
  sidebar visual candidate.
- Updated the mock adequacy review for the `0.0.5` private HACS publish scope.

Tests/checks run:
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `git diff --check`

Docs updated:
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/live-test/MOCK_ADEQUACY_REVIEW.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Publish `0.0.5` as a private HACS/live-test candidate only. It does not claim
  public release readiness.
- No tag will be created because the repository still has no established tag
  convention for these private HACS candidates.
- No deploy script exists in the workspace; this publish remains a commit and
  push to `main` for HACS update.

Known gaps / next prompt:
- Commit `50242e4` was pushed to `main` for the private HACS candidate.
- Update Homekeep from HACS in the private Home Assistant instance, restart
  Home Assistant, and run Gate 3C.

### 2026-06-23 - Label-first Home Health direction

Status: completed locally

Implemented:
- Changed the product direction so user-facing Home Health and Area Health use
  labels, qualitative trends, and care-focused explanations instead of raw
  numeric health values.
- Kept numeric health as an internal calculation/integration value for sorting,
  thresholds, events, and Projected Impact.
- Updated the mocked Home Health panel to remove the whole-home number, Area
  health numbers, and percent-like bars.
- Added frontend source checks to guard against reintroducing numeric Home
  Health display in the mocked panel.

Tests/checks run:
- `git diff --check -- PROJECT_BRIEF.md docs/AI_DECISION_LOG.md docs/product/HOMEKEEP_APP_PLAN.md docs/product/HOMEKEEP_VOICE_SYSTEM.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `PROJECT_BRIEF.md`
- `docs/AI_DECISION_LOG.md`
- `docs/specs/DERIVED_HEALTH.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Tests updated:
- `tests/test_frontend.py`

Important decisions:
- Because Home Health is not expected to realistically reach a perfect state,
  the app should not teach users to interpret health as a percent-like score.
- Raw health values may still exist for internal Homekeep and Home Assistant
  integration behavior until a later entity/API compatibility pass decides
  whether to add label-based companion entities.

Known gaps / next prompt:
- Review whether `sensor.homekeep_home_health` should gain a label-first
  companion sensor or be hidden from the primary user experience in a future
  Home Assistant entity contract pass.

### 2026-06-23 - Contribution vocabulary and health communication guidance

Status: completed locally

Implemented:
- Documented that `Task` remains the individual user-facing item.
- Documented that a suggested or completed `Task Bundle` should be framed as a
  `Contribution` in user-facing app copy.
- Added guardrails that Contribution language must feel optional,
  appreciative, fitting, and mutual rather than obligatory.
- Expanded the mutual-care model to include humans, animals, pets, plants,
  objects, devices, routines, home systems, and the home itself as possible
  contributors when signals are meaningful.
- Added a thorough ten-point derived health communication guide covering
  labels, reasons, `Helped lately`, `Could help next`, trend language,
  recommendations, completion feedback, appreciation/action separation, and
  keeping raw numbers internal.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`
- `git diff --check -- custom_components/homekeep/frontend/homekeep-panel.js docs/product/HOMEKEEP_APP_PLAN.md docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md docs/AI_IMPLEMENTATION_PROGRESS.md`

Docs updated:
- `PROJECT_BRIEF.md`
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/product/HOMEKEEP_VOICE_SYSTEM.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Do not rename individual Tasks to Contributions.
- Use Contribution as the humane, user-facing frame for the bundled care offer.
- Contribution copy must never suggest duty, debt, pressure, or disappointment.

Known gaps / next prompt:
- Future UI copy pass should replace visible `Suggested Task Bundle` phrasing
  with Contribution-oriented copy while keeping Task rows clear.

### 2026-06-23 - Mixed chip icon segment correction

Status: completed locally

Implemented:
- Reformatted mixed icon+text chips so the icon background fills a full-height
  left segment up to the chip border.
- Applied the same segment pattern to the proposed Task Bundle metadata chips.
- Introduced a shared `icon-chip` class for mixed icon+text chip styling.
- Removed the floating icon-slot background treatment from mixed chips.
- Kept the boundary between icon and text as the color edge where the segment
  meets the plain chip body, without adding a separate divider stroke.
- Kept the shuffle icon-only chip on its separate compact treatment.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `python3 -m unittest tests.test_frontend tests.test_reload_unload -v`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Mixed icon+text chips should use a full-height icon segment. The segment's
  background color change is the divider; do not add an extra line or border
  between icon and text.
- Icon-only chips, such as the shuffle button, should not add a separate icon
  background inside the button.

Known gaps / next prompt:
- Re-run the visual review in the Home Assistant panel after installing the
  updated candidate.

### 2026-06-23 - Right Now greeting refresh reset

Status: completed locally

Implemented:
- Reset the Right Now greeting generation rule so it now considers task-time,
  Mood Context, Area, and time of day.
- Regenerated the greeting on page load, task-time changes, Mood Context
  changes, Area changes, returning to Right Now from another tab, and returning
  to Ready Now after the summary flow.
- Added a lightweight once-per-minute day-part check so the greeting can refresh
  when the open panel crosses morning, afternoon, evening, or night.
- Kept shuffle from regenerating the greeting by itself.
- Added a retry when refreshing the greeting so visible trigger changes are less
  likely to land on the same phrase.
- Reserved a consistent two-line-height greeting area in the Ready Now hero.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_frontend -v`

Docs updated:
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- The greeting is contextual to the moment and top-level filters, not to the
  selected Task Bundle title.
- The greeting should not create layout jump when the phrase changes.

Known gaps / next prompt:
- Re-run the visual review in the Home Assistant panel after installing the
  updated candidate.

### 2026-06-23 - Home Health area help handoff

Status: completed locally

Implemented:
- Added gentle mocked Area Health actions for `Short help` and `Care nudge`.
- Kept Right Now as the main task giver: Home Health requests now hand off to
  the Right Now surface instead of becoming a parallel task builder.
- Added synthetic quick Area tasks for short time-budget help.
- Softened the Home Health header and Area action copy so the home's needs are
  felt without becoming harsh or punitive.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_frontend -v`

Docs updated:
- `docs/AI_DECISION_LOG.md`
- `docs/product/HOMEKEEP_APP_PLAN.md`
- `docs/implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`
- `docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Tests updated:
- `tests/test_frontend.py`

Important decisions:
- Area Health can make a gentle request for help, but Right Now remains the
  central place that gives the task.
- `Critical care` language is too sharp for this surface; use gentler language
  such as `Care nudge`.

Known gaps / next prompt:
- Re-run the Home Assistant panel visual review and decide whether the handoff
  should become a real service-backed behavior or remain a mocked review affordance.

### 2026-06-23 - Suggested bundle card redundancy trim

Status: completed locally

Implemented:
- Removed duplicate Area Health lift copy from the suggested bundle start
  button.
- Kept health context in the metadata chip and made the start button a compact
  action-only CTA.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_frontend -v`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- The suggested bundle card should not repeat the same health lift in both the
  chip row and primary action. The CTA starts the flow; the chip explains why.

Known gaps / next prompt:
- Re-review the card visually in Home Assistant to confirm the CTA now reads as
  an action rather than another status surface.

### 2026-06-23 - Suggested bundle chip richness

Status: completed locally

Implemented:
- Added additional icon chips to the suggested bundle card for goal, mood fit,
  and bonus Keeps.
- Kept the compact start CTA action-only and left Area Health lift in the chip
  row to avoid the previous redundancy.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_frontend -v`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Tests updated:
- `tests/test_frontend.py`

Important decisions:
- More chips are welcome when each chip carries a distinct part of the care
  context: size, health lift, goal, mood fit, or Keeps.

Known gaps / next prompt:
- Review the suggested bundle card at mobile width to make sure the richer chip
  row still scans cleanly.

### 2026-06-23 - Home Health chip richness

Status: completed locally

Implemented:
- Added icon chip rows to Home Health Area cards for status, trend, available
  lift, and recent helped-lately signals.
- Removed the separate Area lift meter so Area facts live in the same chip
  language as the suggested bundle card.
- Kept Area help buttons visually distinct as actions rather than status chips.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_frontend -v`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Tests updated:
- `tests/test_frontend.py`

Important decisions:
- Home Health can use lots of chips as long as they are small, icon-led, and
  descriptive rather than numeric or grade-like.

Known gaps / next prompt:
- Review Home Health on mobile to ensure the denser chip rows wrap cleanly.

### 2026-06-23 - Task Session header stability

Status: completed locally

Implemented:
- Reserved stable vertical space for the running-session support/timer line.
- Moved completion feedback into an always-present flash slot inside the Task
  Session header.
- Removed sticky flash insertion above the task list so completing or starting
  a Task does not bounce the list up and down.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_frontend -v`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Tests updated:
- `tests/test_frontend.py`

Important decisions:
- The running Task Session header should reserve space for changing state so
  the task list stays visually anchored during start, pause, complete, and
  flash-feedback transitions.

Known gaps / next prompt:
- Visually review active-session transitions in the Home Assistant panel,
  especially first start, completion flash, optional-task offer, and mobile
  width.

### 2026-06-23 - Session summary explicit dismiss

Status: completed locally

Implemented:
- Removed the automatic return from the completed Task Session summary.
- Added an explicit `Dismiss` button to the session-complete summary page.
- Wired the dismiss action to return to Right Now only when the user taps it.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Tests updated:
- `tests/test_frontend.py`

Important decisions:
- Completion feedback should stay visible until dismissed in the live session
  review flow; it should not disappear automatically.

Known gaps / next prompt:
- Confirm in the Home Assistant panel that the completed summary remains open
  long enough for live review and dismisses cleanly.

### 2026-06-23 - Remote live-test build update without version bump

Status: completed locally

Implemented:
- Prepared the current Live Test 3 UI/documentation changes for a remote build
  update without changing the integration manifest version.
- Kept `custom_components/homekeep/manifest.json` at `0.0.5` per Steve's
  explicit instruction not to bump.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`
- Targeted privacy/secret scan across changed files; hits were guardrail/spec
  terms such as `session_id`, `tokens`, and checklist language, not secrets.

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Important decisions:
- This remote build update is a private live-test candidate update only. No
  version bump, tag, or public release claim is included.

Known gaps / next prompt:
- After the push, update the private Home Assistant instance from the remote
  source and run the current Live Test 3 visual checklist.

### 2026-06-23 - Live Test 3 card chip and greeting polish

Status: completed locally

Implemented:
- Fixed suggested-card and Home Health card chips so the icon segment reaches
  the left chip border like the Today filter chips.
- Removed the redundant mood/fit chip from the suggested card because the Mood
  filter already carries that information.
- Clamped the Right Now greeting block to two lines to prevent vertical jumping
  from longer generated greetings.
- Fixed restore/undo for proposed extra Tasks so restoring a removed
  `while-there` Task clears the rejection and brings it back instead of making
  it disappear.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_frontend -v`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Tests updated:
- `tests/test_frontend.py`

Important decisions:
- Repeated information should be removed from chip rows even when chips are
  visually appealing. Chips should each carry a distinct job.
- Right Now greetings must fit the reserved two-line hero area.

Known gaps / next prompt:
- Rebuild/push the remote live-test candidate again after these final UI polish
  fixes.

### 2026-06-23 - Live Test 3 care wording and session ordering polish

Status: completed locally

Implemented:
- Changed the visible Home Health tab/surface language toward `Home Care` and
  care-oriented stats to avoid medical-feeling language and pulse icons.
- Replaced less reliable/medical-looking Material Design icons with simpler
  care/home icons.
- Moved Home Care stats to the surface header instead of showing confusing
  per-Area stat chips.
- Sorted active Task Session rows so open/new Tasks, including offered extra
  Tasks, appear before completed Tasks.
- Removed bottom-of-list session controls; finish/done controls now appear in
  the stable header action area where they are visible.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_frontend -v`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest discover -s tests -v`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`
- `git diff --check`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Tests updated:
- `tests/test_frontend.py`

Important decisions:
- Visible UI copy should prefer care/home wording over medical-feeling health
  language when showing the mocked sidebar surface.
- Task Session lists should keep actionable work at the top and move completed
  work down.

Known gaps / next prompt:
- Run visual QA on the Home Assistant panel for the Home Care surface and live
  session list ordering, then push the next no-version-bump live-test update.

### 2026-06-23 - Home Care card label reduction

Status: completed locally

Implemented:
- Removed repeated `Helped lately` and `Could help next` labels from every Home
  Care Area card.
- Kept the information self-explanatory through recent-care chips, concrete
  next-care copy, and accessible labels.

Tests/checks run:
- `/Users/steve/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check custom_components/homekeep/frontend/homekeep-panel.js`
- `env PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m unittest tests.test_frontend -v`
- `git diff --check`

Docs updated:
- `docs/AI_IMPLEMENTATION_PROGRESS.md`

Tests updated:
- `tests/test_frontend.py`

Important decisions:
- Repeated column labels should be avoided on repeated cards when the content
  itself can carry the meaning.

Known gaps / next prompt:
- Re-run Home Care visual QA on mobile and desktop to confirm the cards scan
  cleanly without repeated labels.

## Resume Instructions

When resuming implementation:

1. Read `AGENTS.md`.
2. Read this file.
3. Read the docs for the next incomplete phase.
4. Check `git status --short`.
5. Continue from the first unchecked phase unless Steve asks otherwise.
