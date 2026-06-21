# Homekeep Combined Documentation

Generated from Markdown files in this project. Original files are unchanged.

## Table Of Contents

- [AGENTS.md](#agentsmd)
- [PROJECT_BRIEF.md](#project-briefmd)
- [README.md](#readmemd)


---

## AGENTS.md

# Homekeep Agent Guide

Keep the product brief human-readable. Put implementation details in `docs/`.

## Canonical Terms

- Homekeep
- Chore
- Home Assistant Area
- Chore Bundle
- Chore Session
- Ready-Now Mode
- Scheduled-Suggestion Mode
- Smart Chore List
- Recommendation Engine
- Staleness
- Home Health

## Supporting Vocabulary

Use these when they make implementation clearer, but do not treat them as
top-level product vocabulary:

- Chore Variant
- Chore Group
- Area Health
- Group Health
- Projected Impact
- Calendar Context
- Session-History Learning
- Mood Context
- Light Session
- Bonus Chore

## Engineering Standards

- Homekeep storage is the source of truth.
- Home Assistant To-do entities are projections.
- To-do completion may write through only for projected items with valid
  Homekeep metadata; reject or revert To-do create/delete/rename/edit/reorder.
- Keep recommendation logic local-first, bounded, and explainable.
- Treat Home Health, Area Health, Group Health, Staleness, and Projected Impact
  as derived values. Cached values must be disposable and rebuildable.
- Serialize durable mutations through the engine and make retries idempotent
  where `request_id` is available.
- Validate all service payloads.
- Reject non-finite intervals, weights, durations, and credits.
- Clamp adaptive interval writes to each Chore's min/max interval.
- Never train adaptive intervals from skips, snoozes, dismissals, swaps, or
  cancellations.
- Unknown chore IDs must not crash handlers.
- For session completions, validate `completed_by` against session
  participants when participants are present.
- Bonus Chores use the original session through `bonus_pending` and
  `bonus_active`; they must not create an unbounded chain.
- Skips, snoozes, dismissals, and cancellations must not count as completions.
- Calendar details should be minimized in durable storage.
- Mood Context must be lightweight, explainable, user-correctable, and never a
  medical or mental-health claim.
- Use `python-dateutil` only at user-facing or config-facing date/time input
  boundaries. Core Homekeep logic should receive normalized Home Assistant
  local datetimes, timedeltas, or explicit internal values.
- Gamification must be positive and non-punitive.
- When Codex repeats a regular operation flow and the sequence is stable enough
  to reuse, prefer turning it into a script or documented command on disk
  instead of relying on chat memory. Keep scripts small, explicit, and safe to
  run again.

## Security And Privacy

- Never commit secrets, credentials, tokens, API keys, passwords, cookies,
  session IDs, private endpoints, Wi-Fi details, encryption keys, webhook URLs,
  or Home Assistant long-lived access tokens.
- Never put Steve's personal email address or private contact details in git
  commits, README files, docs, examples, logs, fixtures, manifests, release
  notes, screenshots, or generated output.
- Use safe placeholder values in docs and examples, such as
  `user@example.com`, `calendar.family`, `person.steve`, `REDACTED`, or
  `YOUR_TOKEN_HERE`.
- Do not copy real calendar event text, household routines, private addresses,
  device identifiers, entity IDs that reveal private details, or personal
  schedules into tracked files.
- Test fixtures and mocks must use synthetic data only.
- Logs and diagnostics should avoid raw calendar descriptions and sensitive
  Home Assistant state. Prefer derived context such as `has_guests_soon`.
- Before commits, releases, or deploys, scan changed files for secrets and
  private details.
- If a secret or private detail is discovered in tracked files, stop and ask
  Steve how to rotate/remove it. Do not bury it in follow-up commits.

## Version Bump Testing

- Until Homekeep reaches version `1.0`, every version bump must include a check
  that mocks are present and adequate for the changed behavior.
- Mock coverage should be reviewed alongside tests, especially for Home
  Assistant entities, services, To-do projections, calendar changes,
  recommendation snapshots, adaptive intervals, and session history.
- Do not treat a pre-`1.0` version bump as ready if the tests rely on missing,
  stale, or unrealistic mocks.
- At version `1.0`, ask Steve how to proceed with real live candidates before
  replacing or supplementing the mock-first release workflow.

## Implementation Mode

When Steve asks to implement part of Homekeep, work in small bounded phases.
Read the relevant planning docs before editing, but treat them as guidance, not
executable truth.

Before implementing, read `docs/IMPLEMENTATION_PROGRESS.md` and continue from
the first incomplete phase unless Steve asks for a different phase. At the end
of every implementation pass, update `docs/IMPLEMENTATION_PROGRESS.md` with the
phase status, summary, tests/checks run, docs updated, important decisions, and
next recommended prompt.

Codex must:

- verify Home Assistant API assumptions against the installed Home Assistant
  package or official developer docs before relying on them
- call out contradictions between docs, Home Assistant APIs, and existing code
  before choosing an implementation path
- keep each implementation pass small enough to finish with focused tests
- stay inside MVP scope unless Steve explicitly expands it
- update docs when implementation reality differs from the plan
- keep `docs/IMPLEMENTATION_PROGRESS.md` current so future sessions can resume
  without chat history
- for every new feature, update `docs/DECISION_LOG.md`, relevant spec docs,
  tests, and `docs/IMPLEMENTATION_PROGRESS.md` before or alongside code so
  production behavior and planning docs do not drift
- end each phase with what changed, what was verified, tests run, and remaining
  risks

Codex must not:

- blindly trust old planning text
- invent Home Assistant APIs
- implement broad future scope during MVP work
- treat To-do projections, health caches, calendar snapshots, or recommendation
  snapshots as source of truth
- skip tests for lifecycle, storage, service handlers, or Home Assistant entity
  behavior touched by the change

Recommended build order:

1. Scaffold the Home Assistant integration.
2. Implement models and versioned storage.
3. Implement derived Staleness, Home Health, and adaptive intervals.
4. Implement Chore Session lifecycle and service validation.
5. Implement Recommendation Engine V1.
6. Wire Home Assistant services, sensors, and To-do projections.
7. Implement Calendar Context.
8. Add the Lovelace MVP dashboard example.
9. Harden tests, reload/unload behavior, migrations, and release checks.

Ask Steve before proceeding when:

- Home Assistant API behavior conflicts with the plan
- a required product decision is not covered by docs
- live household data, live calendar data, or a real deployment candidate is
  needed
- version `1.0` release workflow needs real live candidates
- a scope choice would materially change the MVP

## Deploy Workflow

When Steve asks to deploy, publish, or release Homekeep, follow this sequence:

1. Inspect the working tree with `git status --short`.
2. Review the changes intended for the release. Do not include unrelated user
   work.
3. Confirm the target version with Steve if it was not stated explicitly.
4. Check version-bump requirements:
   - pre-`1.0`: verify mocks are present and adequate for the changed behavior
   - `1.0`: ask Steve how to proceed with real live candidates before changing
     the mock-first workflow
   - post-`1.0`: follow the live-candidate policy Steve approved
5. Run the focused test/lint/syntax checks relevant to changed files.
6. Fix release-blocking failures before continuing.
7. Bump the version in all required project files.
8. Update changelog or release notes with developer-oriented implementation
   impact and Home Assistant behavior changes.
9. Re-run the focused checks that cover the version bump and release notes.
10. Summarize for Steve:
    - code changes
    - user-facing behavior
    - Home Assistant impact
    - tests/checks run
    - mock adequacy status
    - release note draft
11. Get Steve approval before final publish if the deploy command is destructive,
    public, irreversible, or uses live candidates.
12. Stage only intended files.
13. Create a git commit with a clear release commit message.
14. Create a version tag when the project has an established tag convention.
15. Push the commit and tag only after checks pass and approval requirements are
    satisfied.
16. Run the project deploy/publish command if one exists.
17. Report the final commit, tag, push, deploy result, and any residual risk.

Git rules:

- Never revert user changes unless Steve explicitly asks.
- Never use destructive git commands for deploy cleanup.
- Prefer non-interactive git commands.
- If unrelated files are dirty, leave them alone and stage only release files.
- If no deploy script or tag convention exists yet, document that gap instead
  of inventing a release mechanism silently.

## Planning Files

- `PROJECT_BRIEF.md`: human product brief.
- `docs/DECISION_LOG.md`: authoritative conflict resolver for implementation.
- `docs/ARCHITECTURE.md`: integration architecture and module boundaries.
- `docs/HOME_ASSISTANT_CONTRACT.md`: entities, services, events, To-do behavior.
- `docs/ACTION_RESPONSES.md`: Home Assistant service response rules.
- `docs/TODO_PROJECTIONS.md`: supported and rejected To-do mutations.
- `docs/PARTICIPANT_ATTRIBUTION.md`: completion attribution rules.
- `docs/BONUS_CHORE_LIFECYCLE.md`: one-more chore session lifecycle.
- `docs/SESSION_STATE_MACHINE.md`: allowed session transitions.
- `docs/DATA_MODEL.md`: stored objects and validation rules.
- `docs/STORAGE_MIGRATIONS.md`: storage versions and migration rules.
- `docs/COMPLETION_CREDIT.md`: variant credit and next due behavior.
- `docs/RECOMMENDATION_ENGINE.md`: deterministic v1 scoring.
- `docs/DISMISSAL_PENALTY.md`: dismissal score formula, decay, and cooldown.
- `docs/SNOOZE_POLICY.md`: snooze bounds and recommendation behavior.
- `docs/RECOMMENDATION_PAYLOADS.md`: Smart Chore List payload shape.
- `docs/RECOMMENDATION_SNAPSHOTS.md`: recommendation snapshot lifecycle.
- `docs/CONTEXT_FINGERPRINT.md`: exact recommendation context fingerprinting.
- `docs/TARGET_TIME_WINDOW.md`: target time window parsing and normalization.
- `docs/SCHEDULED_SUGGESTION_UX.md`: future-session proposal UX.
- `docs/SESSION_HISTORY_LEARNING.md`: context buckets and history fit scoring.
- `docs/MOOD_CONTEXT.md`: inferred mood/readiness context rules.
- `docs/SERVICE_SCHEMAS.md`: draft Home Assistant service payloads.
- `docs/TEST_PLAN.md`: unit and integration test plan.
- `docs/SCAFFOLDING_TASKS.md`: file-by-file first implementation checklist.
- `docs/LOVELACE_MVP.md`: dashboard flow and service wiring.
- `docs/CALENDAR_CONTEXT.md`: calendar freshness and invalidation rules.
- `docs/ADAPTIVE_INTERVALS.md`: adaptive cadence bounds and update rules.
- `docs/DERIVED_HEALTH.md`: health/staleness derivation and cache rules.
- `docs/CONCURRENCY_AND_IDEMPOTENCY.md`: mutation locking and retry behavior.
- `docs/IMPLEMENTATION_READINESS_REVIEW.md`: pre-scaffold risk review.
- `docs/IMPLEMENTATION_PROGRESS.md`: phase status and resume ledger.
- `docs/IMPLEMENTATION_PLAN.md`: build phases.
- `docs/MVP_ACCEPTANCE_CRITERIA.md`: definition of done.
- `examples/sample_chores.yaml`: sample chore definitions for tests and demos.

## Before Implementing

Read `docs/DECISION_LOG.md` first. It is the conflict resolver when older docs
or chat-derived planning disagree. If implementation discovers a conflict,
pause code changes for that decision, update `docs/DECISION_LOG.md` first with
the winning interpretation, then update the stale doc, then write code. Record
the decision and affected docs in `docs/IMPLEMENTATION_PROGRESS.md`.

Then read the docs relevant to the current phase. For a broad scaffold pass,
read:

1. `PROJECT_BRIEF.md`
2. `docs/DECISION_LOG.md`
3. `docs/IMPLEMENTATION_PROGRESS.md`
4. `docs/IMPLEMENTATION_PLAN.md`
5. `docs/SCAFFOLDING_TASKS.md`
6. `docs/MVP_ACCEPTANCE_CRITERIA.md`
7. `docs/ARCHITECTURE.md`
8. `docs/HOME_ASSISTANT_CONTRACT.md`
9. `docs/SERVICE_SCHEMAS.md`
10. `docs/DATA_MODEL.md`
11. `docs/STORAGE_MIGRATIONS.md`
12. `docs/RECOMMENDATION_PAYLOADS.md`
13. `docs/CONTEXT_FINGERPRINT.md`
14. `docs/TARGET_TIME_WINDOW.md`
15. `docs/TEST_PLAN.md`

For focused implementation phases, read `docs/DECISION_LOG.md`,
`docs/IMPLEMENTATION_PROGRESS.md`, and only the phase-specific docs needed for
the files being changed.


---

## PROJECT_BRIEF.md

# Homekeep Product Brief

## Summary

Homekeep is a Home Assistant integration for adaptive household chores. It helps
people decide what to do next by learning the care patterns of the home, the
current context, and what users historically choose to complete.

Homekeep is not a static chore checklist. It is a light Chore Session planner.
When a user is ready to do chores, they tell Home Assistant, answer a few simple
context questions, review a short Smart Chore List or Chore Bundle, choose what
they want to do, and start a tracked Chore Session.

## Product Promise

Homekeep should answer:

```text
Given who is ready, how much time they have, how they feel, and what the home
needs, what is the most useful Chore Session to offer right now?
```

The system should feel helpful, gentle, and practical. It should avoid a giant
guilt-inducing list of overdue tasks.

## Core Terms

Chore
: A durable recurring household task that Homekeep tracks over time.

Home Assistant Area
: A room or location from Home Assistant that Homekeep can use to group and
prioritize chores.

Chore Bundle
: A recommended set of chores that work well together.

Chore Session
: A tracked work session where one or more users complete selected chores.

Ready-Now Mode
: The user says they are ready now, and Homekeep proposes an immediate Light
Session.

Scheduled-Suggestion Mode
: Homekeep proposes a saved Chore Session plan for a future window, such as
next Friday or before guests arrive. It is not an active Chore Session until
the user starts a fresh recommendation.

Smart Chore List
: A short curated list of recommended chores or bundles generated for the user,
moment, goal, and home state.

Recommendation Engine
: The local decision engine that scores, groups, explains, and offers chores.

Home Health
: A high-level score that summarizes how much care the home needs. Homekeep may
also calculate area-level health internally.

Staleness
: How much a chore needs attention based on elapsed time, adaptive interval,
and context.

Supporting concepts used in the implementation docs include Chore Variant,
Chore Group, Projected Impact, Calendar Context, Session-History Learning,
Light Session, and Bonus Chore.

## Main User Flow

1. User tells Home Assistant: "I am ready to do chores."
2. Homekeep asks only the context it needs.
3. User provides time, energy, and goal.
4. Homekeep generates a Smart Chore List.
5. User chooses a chore or Chore Bundle.
6. Homekeep starts a Chore Session.
7. User completes, skips, snoozes, or ends the session.
8. Homekeep updates chore history, adaptive intervals, Staleness, and health
scores.
9. Homekeep may offer an optional Bonus Chore.

## Smart Recommendations

Homekeep recommendations should consider:

```text
Staleness
Home Health and Area Health impact
available time
energy level
Mood Context
Home Assistant Area
Calendar Context
sensor context
Session-History Learning
recent dismissals
```

Mood Context should feel like a gentle planning aid. Homekeep may infer that a
shorter, quieter, or quick-win session fits the moment, but the user can always
override it.

The first Smart Chore List should stay small:

```text
1 best Chore Bundle
1 best single chore
1 easiest useful chore
up to 3 alternates
```

Every recommendation should include a short reason.

Example:

```text
Kitchen Reset · 13 min
- Empty compost
- Wipe counters
- Start dishwasher

Projected: Kitchen 48 -> 72, Home 63 -> 70
Reason: high Kitchen Health impact, fits your time, and you often choose kitchen
tasks on Friday afternoons.
```

## Calendar-Aware Planning

Homekeep should analyze Home Assistant calendar context and suggest chores that
help with real life.

Examples:

```text
Guests tomorrow:
- bathroom refresh
- entryway reset
- trash
- dishes

Vacation Friday:
- clear fridge leftovers
- empty trash
- start dishwasher
- move laundry

Busy evening:
- offer short low-energy chores
```

Calendar data should be minimized. Homekeep should store derived context when
possible, not raw event descriptions.

## Area-Aware Grouping

Homekeep should use Home Assistant Areas when they help users scan and act.

Example:

```text
Kitchen
- Empty compost
- Wipe counters
- Start dishwasher
```

Area grouping is not mandatory. Some sessions should group chores by purpose.

Example:

```text
Trash Run
- Empty kitchen trash
- Empty bathroom bin
- Collect recycling
- Clear fridge leftovers
```

## Light Rewards

Chore Sessions should stay light by default.

```text
2 minutes: one tiny chore
5 minutes: one or two quick chores
15 minutes: a small Chore Bundle
30 minutes: a focused reset
```

After a session, Homekeep should make stopping feel successful:

```text
Done for now
One more
Plan later
```

If the user asks for "one more", Homekeep should offer a small Bonus Chore and
treat that as positive momentum. It should never punish stopping after the
planned session.

## MVP Scope

The MVP should include:

- Chore definitions and completion history
- adaptive intervals
- Staleness
- Home Health and Area Health
- Ready-Now Chore Sessions
- Scheduled-Suggestion saved proposals
- Smart Chore Lists
- Chore Bundles
- Projected Impact
- Home Assistant services and sensors
- Home Assistant To-do projections
- Lovelace dashboard flow
- Calendar Context
- Session-History Learning
- Light Sessions and Bonus Chores

## How To Build This Project

Use these prompts one at a time. Codex must follow `AGENTS.md` Implementation
Mode and update `docs/IMPLEMENTATION_PROGRESS.md` after every phase so the next
session can resume without chat history.

Before implementation, Codex should read `docs/DECISION_LOG.md`. It records the
winning interpretation when older planning docs conflict.

### Phase 0 Prompt

```text
Implement Homekeep Phase 0: Scaffold.

Follow AGENTS.md Implementation Mode.

Before coding:
- read docs/IMPLEMENTATION_PROGRESS.md
- read docs/IMPLEMENTATION_PLAN.md Phase 0
- read docs/ARCHITECTURE.md
- read docs/HOME_ASSISTANT_CONTRACT.md
- verify current Home Assistant custom integration, config flow, service
  registration, and storage APIs

Deliver:
- Home Assistant custom integration skeleton
- manifest, constants, config flow, init
- versioned storage helper with empty store
- empty service registration with schemas
- initial pytest structure

Keep changes small and testable. Do not implement recommendation logic yet.
Run focused syntax/tests if available.

Before finishing:
- update docs/IMPLEMENTATION_PROGRESS.md
- summarize what changed, what was verified, tests run, and next recommended
  prompt
```

### Phase 1 Prompt

```text
Implement Homekeep Phase 1: Models and storage.

Follow AGENTS.md Implementation Mode. Resume from docs/IMPLEMENTATION_PROGRESS.md.

Read:
- docs/DATA_MODEL.md
- docs/ADAPTIVE_INTERVALS.md
- docs/DERIVED_HEALTH.md
- docs/PARTICIPANT_ATTRIBUTION.md
- examples/sample_chores.yaml

Deliver:
- typed models or dataclasses
- validation helpers
- storage migration hook
- sample chore loading for tests
- tests for invalid intervals, ChoreVariant validation, and storage round trip

Update docs/IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 2 Prompt

```text
Implement Homekeep Phase 2: Derived health and adaptive intervals.

Follow AGENTS.md Implementation Mode. Resume from docs/IMPLEMENTATION_PROGRESS.md.

Read:
- docs/DERIVED_HEALTH.md
- docs/ADAPTIVE_INTERVALS.md
- docs/TEST_PLAN.md

Deliver:
- derived Staleness, Home Health, Area Health, and Projected Impact functions
- clamped adaptive interval update helper
- tests for cache loss, restart recomputation, min/max interval clamping, and
  skip/snooze/dismiss not training intervals

Do not store health or staleness as authoritative durable state.
Update docs/IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 3 Prompt

```text
Implement Homekeep Phase 3: Chore Session lifecycle.

Follow AGENTS.md Implementation Mode. Resume from docs/IMPLEMENTATION_PROGRESS.md.

Read:
- docs/SESSION_STATE_MACHINE.md
- docs/BONUS_CHORE_LIFECYCLE.md
- docs/PARTICIPANT_ATTRIBUTION.md
- docs/CONCURRENCY_AND_IDEMPOTENCY.md
- docs/SERVICE_SCHEMAS.md

Deliver:
- session start/pause/end
- complete/skip/snooze/dismiss item handling
- participant attribution validation
- bonus_pending and bonus_active lifecycle
- accept_bonus_chore
- mutation lock and request_id idempotency where practical
- tests for allowed/disallowed transitions and duplicate calls

Update docs/IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 4 Prompt

```text
Implement Homekeep Phase 4: Recommendation Engine V1.

Follow AGENTS.md Implementation Mode. Resume from docs/IMPLEMENTATION_PROGRESS.md.

Read:
- docs/RECOMMENDATION_ENGINE.md
- docs/RECOMMENDATION_PAYLOADS.md
- docs/RECOMMENDATION_SNAPSHOTS.md
- docs/SESSION_HISTORY_LEARNING.md

Deliver:
- deterministic normalized scoring
- best Chore Bundle, best single chore, easiest useful chore
- stable recommendation_id values
- recommendation explanations
- RecommendationSnapshot lifecycle
- context bucket generation and fallback history scoring
- tests for payload shape, sparse history fallback, and expired snapshots

Do not use an LLM.
Update docs/IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 5 Prompt

```text
Implement Homekeep Phase 5: Home Assistant services and entities.

Follow AGENTS.md Implementation Mode. Resume from docs/IMPLEMENTATION_PROGRESS.md.

Read:
- docs/HOME_ASSISTANT_CONTRACT.md
- docs/SERVICE_SCHEMAS.md
- docs/TODO_PROJECTIONS.md
- docs/CONCURRENCY_AND_IDEMPOTENCY.md

Verify current Home Assistant service response and To-do entity APIs before
coding.

Deliver:
- service handlers
- sensors
- binary sensors if still appropriate
- To-do projections
- rejection/revert behavior for To-do create/delete/rename/edit/reorder
- tests for malformed payloads, unknown IDs, To-do mutation traps, and service
  idempotency

Update docs/IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 6 Prompt

```text
Implement Homekeep Phase 6: Calendar Context.

Follow AGENTS.md Implementation Mode. Resume from docs/IMPLEMENTATION_PROGRESS.md.

Read:
- docs/CALENDAR_CONTEXT.md
- docs/HOME_ASSISTANT_CONTRACT.md
- docs/RECOMMENDATION_ENGINE.md

Verify current Home Assistant calendar entity APIs and event-fetching patterns.

Deliver:
- selected calendar entity options
- derived Calendar Context snapshots
- source calendar version tracking
- automatic invalidation on calendar entity state changes
- max-age freshness checks
- tests for added/modified events invalidating context

Do not store raw calendar details in long-lived history unless no safe
alternative exists.
Update docs/IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 7 Prompt

```text
Implement Homekeep Phase 7: Lovelace MVP dashboard example.

Follow AGENTS.md Implementation Mode. Resume from docs/IMPLEMENTATION_PROGRESS.md.

Read:
- docs/LOVELACE_MVP.md
- docs/SERVICE_SCHEMAS.md
- docs/TODO_PROJECTIONS.md

Use stock Lovelace cards for the final YAML.

Deliver:
- examples/lovelace_dashboard.yaml
- Ready-Now launcher
- time/energy/goal controls
- recommendation display
- Add Chore flow
- active session controls
- Done for now / One more flow

Use Home Assistant native controls, helpers, scripts, and entities for the MVP.
Update docs/IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 8 Prompt

```text
Implement Homekeep Phase 8: Hardening and release readiness.

Follow AGENTS.md Implementation Mode and Deploy Workflow. Resume from
docs/IMPLEMENTATION_PROGRESS.md.

Read:
- docs/TEST_PLAN.md
- docs/MVP_ACCEPTANCE_CRITERIA.md
- docs/IMPLEMENTATION_READINESS_REVIEW.md
- AGENTS.md Version Bump Testing and Deploy Workflow

Deliver:
- storage migration tests
- malformed service payload tests
- stale session response tests
- reload/unload behavior
- mock adequacy review for pre-1.0 version bump readiness
- documentation updates for any implementation differences

Do not deploy unless Steve explicitly asks for deploy/release.
Update docs/IMPLEMENTATION_PROGRESS.md before finishing.
```

## Product Principle

Homekeep should not ask, "What chores are due?"

It should ask, "What useful, achievable care can we offer at this moment?"


---

## README.md

# Homekeep

Homekeep is a planned Home Assistant integration for adaptive chores, light
Chore Sessions, Smart Chore Lists, and Home Health.

Start here:

- `PROJECT_BRIEF.md` for the human product brief.
- `AGENTS.md` for Codex instructions.
- `docs/IMPLEMENTATION_PLAN.md` for the build sequence.
- `docs/MVP_ACCEPTANCE_CRITERIA.md` for the definition of done.



---
