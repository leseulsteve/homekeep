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
- Chore creation from the Homekeep dashboard
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
