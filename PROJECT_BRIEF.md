# Homekeep Product Brief

## Summary

Homekeep is a Home Assistant integration for adaptive household tasks. It helps
people decide what to do next by learning the care patterns of the home, the
current context, and what users historically choose to complete.

Homekeep is not a static task checklist. It is a light Task Session planner.
When a user is ready to contribute, they tell Home Assistant, answer a few
simple context questions, review a short Smart Task List or Task Bundle, choose
what they want to do, and start a tracked Task Session.

Homekeep's main goal is mutual care: the home has needs, and the home also helps
care for the humans, pets, and plants who live inside it. Every product,
design, and implementation decision should move in that direction, even when the
current MVP work is focused on tasks. The practical center remains household
care, comfort, readiness, and small environmental support, not wellness coaching
or medical/psychological claims.

## Product Promise

Homekeep should answer:

```text
Given who is ready, how much time they have, how they feel, and what the home
needs, what is the most useful Task Session to offer right now?
```

The system should feel helpful, gentle, and practical. It should avoid a giant
guilt-inducing list of overdue tasks.

Homekeep's promise is broader than tasks alone: help the home and its
inhabitants keep each other well. Sometimes that means nudging care for a stale
area; sometimes it means protecting quiet, keeping a plant, animal, or pet
routine visible, or suggesting that enough has been done for now.

Keeps are part of that promise. Over time, Keeps should represent care
circulating through the home: humans caring for rooms and routines, plants
helping air and presence, purifiers keeping air steady, and comfort routines
protecting rest. A coffee machine can also return Keeps through comfort and
ritual: good coffee is a small way the home takes care of its inhabitants.
Keeps are not points for people; they are the soft trace of mutual care
happening.

Because Homekeep lives in Home Assistant, connected devices can also participate
in that trace. A Task like laundry can acknowledge shared care between the
human doing the gathering, loading, moving, and folding, and the washing machine
doing the machine work. This should feel collaborative, not transactional.

Keeps are non-scarce because care is abundant. They are recognition, not
currency: they are not spent, stolen, traded, or depleted. More humans, animals,
pets, plants, objects, devices, routines, and home systems contributing to the
home means more care can be noticed.

Care source contribution should be treated as a first-class product axis, at
the same level as caring for an Area. Homekeep should help users see both
`where care helped` and `who or what carried care`: a human changing filters, a
pet routine like emptying litter, a purifier improving air, a coffee machine
making the morning kinder, or a washer carrying part of laundry.

The home is the broker of Keeps, with help from Home Assistant. Home Assistant
provides signals from Areas, entities, devices, sensors, automations, and
service events. Homekeep interprets those signals as care contributions. The
home returns Keeps as recognition. This keeps Keeps emotional and home-centered,
while Home Assistant remains the trusted local signal layer.

Homekeep's user-facing language should follow `docs/product/HOMEKEEP_VOICE_SYSTEM.md`.
The app should use structured, mood-aware copy families rather than random
string variation.

## Core Terms

Task
: A durable recurring household contribution that Homekeep tracks over time.
Task is the project-wide product and user-facing term.

Legacy Chore
: Existing code, storage, service names, and older specs may still use Chore
until a deliberate compatibility migration is implemented. Do not expose Chore
in new user-facing UI unless showing a legacy API or diagnostic name.

Home Assistant Area
: A room or location from Home Assistant that Homekeep can use to group and
prioritize tasks.

Task Bundle
: A recommended set of tasks that work well together. In user-facing app copy,
a selected Task Bundle should usually be framed as a Contribution.

Contribution
: The user-facing name for a fitting Task Bundle once Homekeep is inviting the
user to do it or recognizing that it was done. Contribution language should feel
optional, appreciative, and mutual, not obligatory.

Task Session
: A tracked contribution session where one or more users complete selected
tasks.

Ready-Now Mode
: The human contribution gateway into mutual care. The user says they are ready
now, and Homekeep proposes an immediate Light Session that helps them join the
home's care flow at the scale that fits the moment.

Scheduled-Suggestion Mode
: Homekeep proposes a saved Task Session plan for a future window, such as
next Friday or before guests arrive. It is not an active Task Session until
the user starts a fresh recommendation.

Smart Task List
: A short curated list of recommended tasks or bundles generated for the user,
moment, goal, and home state.

Recommendation Engine
: The local decision engine that scores, groups, explains, and offers tasks.

Home Health
: A high-level household status that summarizes where care would help. Homekeep
may calculate numeric health values internally, but user-facing Home Health and
Area Health should use labels, trends, and care-focused language rather than
numbers. Area Health should eventually show both what would help next and who
or what helped lately, because health naturally drifts down as care gets stale
and contribution should remain visible.

Staleness
: How much a task needs attention based on elapsed time, adaptive interval,
and context.

Supporting concepts used in the implementation docs include Task Variant,
Task Group, Projected Impact, Calendar Context, Session-History Learning,
Light Session, and Bonus Task.

## Main User Flow

1. User tells Home Assistant: "I am ready to contribute."
2. Homekeep asks only the context it needs.
3. User provides time, energy, and goal.
4. Homekeep generates a Smart Task List.
5. User chooses a task or Task Bundle.
6. Homekeep starts a Task Session.
7. User completes, skips, snoozes, or ends the session.
8. Homekeep updates task history, adaptive intervals, Staleness, and health
scores.
9. Homekeep may offer an optional Bonus Task.

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

The first Smart Task List should stay small:

```text
1 best Task Bundle
1 best single task
1 easiest useful task
up to 3 alternates
```

Every recommendation should include a short reason.

Example:

```text
Kitchen Lift · 13 min
- Empty compost
- Wipe counters
- Start dishwasher

Projected: Big kitchen lift
Reason: high Kitchen Health impact, fits your time, and you often choose kitchen
tasks on Friday afternoons.
```

## Calendar-Aware Planning

Homekeep should analyze Home Assistant calendar context and suggest tasks that
help with real life.

Examples:

```text
Guests tomorrow:
- bathroom refresh
- entryway lift
- trash
- dishes

Vacation Friday:
- clear fridge leftovers
- empty trash
- start dishwasher
- move laundry

Busy evening:
- offer short low-energy tasks
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

Area grouping is not mandatory. Some sessions should group tasks by purpose.

Example:

```text
Trash Run
- Empty kitchen trash
- Empty bathroom bin
- Collect recycling
- Clear fridge leftovers
```

## Light Rewards

Task Sessions should stay light by default.

```text
2 minutes: one tiny task
5 minutes: one or two quick tasks
15 minutes: a small Task Bundle
30 minutes: a focused Task Bundle
```

After a session, Homekeep should make stopping feel successful:

```text
Done for now
One more
Plan later
```

If the user asks for "one more", Homekeep should offer a small Bonus Task and
treat that as positive momentum. It should never punish stopping after the
planned session.

## MVP Scope

The MVP should include:

- Task definitions and completion history
- adaptive intervals
- Staleness
- Home Health and Area Health
- Ready-Now Task Sessions
- Scheduled-Suggestion saved proposals
- Smart Task Lists
- Task Bundles
- Projected Impact
- Home Assistant services and sensors
- Home Assistant To-do projections
- Task creation from the Homekeep dashboard
- Homekeep sidebar app flow
- Calendar Context
- Session-History Learning
- Light Sessions and Bonus Tasks

## How To Build This Project

Use these prompts one at a time. Codex must follow `AGENTS.md` Implementation
Mode and update `docs/AI_IMPLEMENTATION_PROGRESS.md` after every phase so the next
session can resume without chat history.

Before implementation, Codex should read `docs/AI_DECISION_LOG.md`. It records the
winning interpretation when older planning docs conflict.

### Phase 0 Prompt

```text
Implement Homekeep Phase 0: Scaffold.

Follow AGENTS.md Implementation Mode.

Before coding:
- read docs/AI_IMPLEMENTATION_PROGRESS.md
- read docs/implementation/IMPLEMENTATION_PLAN.md Phase 0
- read docs/architecture/ARCHITECTURE.md
- read docs/architecture/HOME_ASSISTANT_CONTRACT.md
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
- update docs/AI_IMPLEMENTATION_PROGRESS.md
- summarize what changed, what was verified, tests run, and next recommended
  prompt
```

### Phase 1 Prompt

```text
Implement Homekeep Phase 1: Models and storage.

Follow AGENTS.md Implementation Mode. Resume from docs/AI_IMPLEMENTATION_PROGRESS.md.

Read:
- docs/architecture/DATA_MODEL.md
- docs/specs/ADAPTIVE_INTERVALS.md
- docs/specs/DERIVED_HEALTH.md
- docs/specs/PARTICIPANT_ATTRIBUTION.md

Deliver:
- typed models or dataclasses
- validation helpers
- storage migration hook
- tests for invalid intervals, ChoreVariant validation, and storage round trip

Update docs/AI_IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 2 Prompt

```text
Implement Homekeep Phase 2: Derived health and adaptive intervals.

Follow AGENTS.md Implementation Mode. Resume from docs/AI_IMPLEMENTATION_PROGRESS.md.

Read:
- docs/specs/DERIVED_HEALTH.md
- docs/specs/ADAPTIVE_INTERVALS.md
- docs/implementation/TEST_PLAN.md

Deliver:
- derived Staleness, Home Health, Area Health, and Projected Impact functions
- clamped adaptive interval update helper
- tests for cache loss, restart recomputation, min/max interval clamping, and
  skip/snooze/dismiss not training intervals

Do not store health or staleness as authoritative durable state.
Update docs/AI_IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 3 Prompt

```text
Implement Homekeep Phase 3: Task Session lifecycle.

Follow AGENTS.md Implementation Mode. Resume from docs/AI_IMPLEMENTATION_PROGRESS.md.

Read:
- docs/specs/SESSION_STATE_MACHINE.md
- docs/specs/BONUS_CHORE_LIFECYCLE.md
- docs/specs/PARTICIPANT_ATTRIBUTION.md
- docs/architecture/CONCURRENCY_AND_IDEMPOTENCY.md
- docs/specs/SERVICE_SCHEMAS.md

Deliver:
- session start/pause/end
- complete/skip/snooze/dismiss item handling
- participant attribution validation
- bonus_pending and bonus_active lifecycle
- accept_bonus_chore
- mutation lock and request_id idempotency where practical
- tests for allowed/disallowed transitions and duplicate calls

Update docs/AI_IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 4 Prompt

```text
Implement Homekeep Phase 4: Recommendation Engine V1.

Follow AGENTS.md Implementation Mode. Resume from docs/AI_IMPLEMENTATION_PROGRESS.md.

Read:
- docs/specs/RECOMMENDATION_ENGINE.md
- docs/specs/RECOMMENDATION_PAYLOADS.md
- docs/specs/RECOMMENDATION_SNAPSHOTS.md
- docs/specs/SESSION_HISTORY_LEARNING.md

Deliver:
- deterministic normalized scoring
- best Task Bundle, best single task, easiest useful task
- stable recommendation_id values
- recommendation explanations
- RecommendationSnapshot lifecycle
- context bucket generation and fallback history scoring
- tests for payload shape, sparse history fallback, and expired snapshots

Do not use an LLM.
Update docs/AI_IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 5 Prompt

```text
Implement Homekeep Phase 5: Home Assistant services and entities.

Follow AGENTS.md Implementation Mode. Resume from docs/AI_IMPLEMENTATION_PROGRESS.md.

Read:
- docs/architecture/HOME_ASSISTANT_CONTRACT.md
- docs/specs/SERVICE_SCHEMAS.md
- docs/specs/TODO_PROJECTIONS.md
- docs/architecture/CONCURRENCY_AND_IDEMPOTENCY.md

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

Update docs/AI_IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 6 Prompt

```text
Implement Homekeep Phase 6: Calendar Context.

Follow AGENTS.md Implementation Mode. Resume from docs/AI_IMPLEMENTATION_PROGRESS.md.

Read:
- docs/specs/CALENDAR_CONTEXT.md
- docs/architecture/HOME_ASSISTANT_CONTRACT.md
- docs/specs/RECOMMENDATION_ENGINE.md

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
Update docs/AI_IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 7 Prompt

```text
Implement Homekeep Phase 7: Homekeep sidebar app MVP.

Follow AGENTS.md Implementation Mode. Resume from docs/AI_IMPLEMENTATION_PROGRESS.md.

Read:
- docs/product/HOMEKEEP_APP_PLAN.md
- docs/specs/SERVICE_SCHEMAS.md
- docs/specs/TODO_PROJECTIONS.md

Deliver:
- Home Assistant sidebar entry
- Homekeep app shell
- Ready-Now launcher
- time/energy/goal controls
- recommendation display
- Add Task flow
- active session controls
- Done for now / One more flow

Use Home Assistant native controls, helpers, scripts, and entities for the MVP.
Update docs/AI_IMPLEMENTATION_PROGRESS.md before finishing.
```

### Phase 8 Prompt

```text
Implement Homekeep Phase 8: Hardening and release readiness.

Follow AGENTS.md Implementation Mode and Deploy Workflow. Resume from
docs/AI_IMPLEMENTATION_PROGRESS.md.

Read:
- docs/implementation/TEST_PLAN.md
- docs/product/MVP_ACCEPTANCE_CRITERIA.md
- docs/implementation/IMPLEMENTATION_READINESS_REVIEW.md
- AGENTS.md Version Bump Testing and Deploy Workflow

Deliver:
- storage migration tests
- malformed service payload tests
- stale session response tests
- reload/unload behavior
- mock adequacy review for pre-1.0 version bump readiness
- documentation updates for any implementation differences

Do not deploy unless Steve explicitly asks for deploy/release.
Update docs/AI_IMPLEMENTATION_PROGRESS.md before finishing.
```

## Product Principle

Homekeep should not ask, "What tasks are due?"

It should ask, "What useful, achievable care can we offer at this moment?"
