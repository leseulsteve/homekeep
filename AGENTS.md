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
8. Add the Homekeep sidebar app MVP.
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
- `docs/HOMEKEEP_VOICE_SYSTEM.md`: user-facing tone, copy families, and
  Mood Context voice rules.
- `docs/SERVICE_SCHEMAS.md`: draft Home Assistant service payloads.
- `docs/TEST_PLAN.md`: unit and integration test plan.
- `docs/SCAFFOLDING_TASKS.md`: file-by-file first implementation checklist.
- `docs/DASHBOARD_UI_PLAN.md`: dashboard UI direction and app-view plan.
- `docs/DASHBOARD_UI_CODEX_INSTRUCTIONS.md`: Codex-facing app UI implementation
  guardrails translated from the current design state.
- `docs/DASHBOARD_UI_STEVE_PROMPTS.md`: phased prompts for continuing app UI
  design review and implementation planning.
- `docs/CALENDAR_CONTEXT.md`: calendar freshness and invalidation rules.
- `docs/ADAPTIVE_INTERVALS.md`: adaptive cadence bounds and update rules.
- `docs/DERIVED_HEALTH.md`: health/staleness derivation and cache rules.
- `docs/CONCURRENCY_AND_IDEMPOTENCY.md`: mutation locking and retry behavior.
- `docs/IMPLEMENTATION_READINESS_REVIEW.md`: pre-scaffold risk review.
- `docs/IMPLEMENTATION_PROGRESS.md`: phase status and resume ledger.
- `docs/IMPLEMENTATION_PLAN.md`: build phases.
- `docs/MVP_ACCEPTANCE_CRITERIA.md`: definition of done.

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
