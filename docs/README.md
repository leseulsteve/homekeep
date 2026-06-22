# Homekeep Docs Map

This directory is organized by the job each document does.

Use this map before adding new docs. Prefer updating an existing source of truth
over creating another planning file with overlapping authority.

## AI Development Rules

Files prefixed with `AI_` are operational context for Codex and other AI agents.
They are written to make future implementation sessions resumable without chat
history.

AI-facing docs may contain:

- current resume state
- implementation guardrails
- phase checklists
- prompts for future AI sessions
- private live-test runbooks with synthetic-data boundaries

AI-facing docs must not become product source of truth when a product or spec
document already exists. If an AI doc discovers a product or implementation
decision, record the decision in the correct source document and reference it
from the AI doc.

Conflict order:

1. `docs/AI_DECISION_LOG.md`
2. product and spec docs in the relevant folder
3. `docs/AI_IMPLEMENTATION_PROGRESS.md`
4. older planning notes and historical phase entries

When implementing, read `docs/AI_DECISION_LOG.md` first, then
`docs/AI_IMPLEMENTATION_PROGRESS.md`, then only the product/spec docs relevant
to the current task.

## Root Docs

- `AI_DECISION_LOG.md`: authoritative conflict resolver for implementation.
- `AI_IMPLEMENTATION_PROGRESS.md`: current phase status and resume ledger.
- `README.md`: this map.

## Product Docs

Human-facing product direction and UX choices.

- `product/HOMEKEEP_APP_PLAN.md`: Homekeep sidebar app plan and workflow design.
- `product/HOMEKEEP_VOICE_SYSTEM.md`: user-facing voice and copy rules.
- `product/MOOD_READINESS_FEATURE_PLAN.md`: future Mood/Readiness direction.
- `product/MVP_ACCEPTANCE_CRITERIA.md`: definition of done.

## Architecture Docs

System boundaries, durable model, storage, and Home Assistant contract.

- `architecture/ARCHITECTURE.md`: integration architecture and module boundaries.
- `architecture/DATA_MODEL.md`: stored objects and validation rules.
- `architecture/STORAGE_MIGRATIONS.md`: storage versions and migrations.
- `architecture/CONCURRENCY_AND_IDEMPOTENCY.md`: mutation locking and retries.
- `architecture/HOME_ASSISTANT_CONTRACT.md`: entities, services, events, and To-do behavior.

## Specs

Feature-level implementation contracts.

- `specs/ACTION_RESPONSES.md`
- `specs/ADAPTIVE_INTERVALS.md`
- `specs/BONUS_CHORE_LIFECYCLE.md`
- `specs/CALENDAR_CONTEXT.md`
- `specs/COMPLETION_CREDIT.md`
- `specs/CONTEXT_FINGERPRINT.md`
- `specs/DERIVED_HEALTH.md`
- `specs/DISMISSAL_PENALTY.md`
- `specs/MOOD_CONTEXT.md`
- `specs/PARTICIPANT_ATTRIBUTION.md`
- `specs/RECOMMENDATION_ENGINE.md`
- `specs/RECOMMENDATION_PAYLOADS.md`
- `specs/RECOMMENDATION_SNAPSHOTS.md`
- `specs/SCHEDULED_SUGGESTION_UX.md`
- `specs/SERVICE_SCHEMAS.md`
- `specs/SESSION_HISTORY_LEARNING.md`
- `specs/SESSION_STATE_MACHINE.md`
- `specs/SNOOZE_POLICY.md`
- `specs/TARGET_TIME_WINDOW.md`
- `specs/TODO_PROJECTIONS.md`

## Implementation Docs

Build sequencing, readiness, tests, and AI-facing implementation prompts.

- `implementation/IMPLEMENTATION_PLAN.md`: build phases.
- `implementation/IMPLEMENTATION_READINESS_REVIEW.md`: pre-scaffold risk review.
- `implementation/TEST_PLAN.md`: unit and integration test plan.
- `implementation/AI_SCAFFOLDING_TASKS.md`: AI implementation checklist.
- `implementation/AI_DASHBOARD_UI_CODEX_INSTRUCTIONS.md`: AI guardrails for app UI implementation.
- `implementation/AI_DASHBOARD_UI_STEVE_PROMPTS.md`: AI prompts for continuing UI planning.

## Live-Test Docs

Private validation runbooks and results. Keep these synthetic-data safe.

- `live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`: AI runbook for private live tests.
- `live-test/PRIVATE_LIVE_TEST_RESULTS.md`: private live-test observations.
- `live-test/MOCK_ADEQUACY_REVIEW.md`: pre-`1.0` mock adequacy review.

## Naming Rules

- Prefix AI-agent operational docs with `AI_`.
- Do not prefix product, architecture, or feature specs with `AI_`.
- Keep filenames stable after implementation starts; update all references in
  `AGENTS.md`, `ALL_DOCS.md`, `PROJECT_BRIEF.md`, and this map when moving docs.
- Avoid duplicate authority. If two docs conflict, update
  `AI_DECISION_LOG.md` with the winning interpretation, then fix the stale doc.
