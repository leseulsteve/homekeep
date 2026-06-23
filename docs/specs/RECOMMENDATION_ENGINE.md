# Recommendation Engine

## Goal

Generate Smart Chore Lists that are useful, light, explainable, and bounded.

Homekeep should rank chores by usefulness in context, not only by due date.

The engine should balance household need against user readiness. Staleness and
Projected Impact represent what the home would benefit from; time, inferred
Capacity, Mood Context, explicit filters, and history fit represent what is
likely reasonable for the user now.

Homekeep may apply a gentle care bias toward stale or high-impact Chores when
they still fit the user's stated constraints. This bias must remain
explainable, bounded, and correctable. It must not override explicit user time,
capacity, area, snooze, dismissal, or safety constraints, and it must not use
guilt, penalties, or hidden manipulation.

Important care-bias rules:

1. `Stretch, do not shove`: prefer meaningful care only when it still fits the
   user's stated time, inferred capacity, and context.
2. Prefer tiny/light variants of high-need Chores when user capacity is low.
3. Recommendation explanations should expose the nudge in plain language.
4. The UI must keep correction paths available: context changes, shuffle,
   removal, restore, snooze/dismiss where applicable, and Done for now.
5. Urgent stale Chores should remain eligible, but the recommended variant
   should be resized when possible.
6. Internal care-debt-like signals must not surface as debt language.
7. Do not use punitive color, warning, streak, or penalty mechanics for normal
   household care.
8. User correction should adjust timing, tone, variant, or fit; it should not
   permanently suppress useful stale care by itself.
9. A bundle may include one small high-need item balanced by easier fit items.
10. Stopping must remain valid. Recommendation state must support `Done for now`
   as a successful outcome.

## Recommendation Modes

Ready-Now Mode:
: User is ready now. Recommend an immediate Light Session.

Scheduled-Suggestion Mode:
: User or calendar context asks for a future window. Recommend a planned Chore
Session for that time.

## V1 Scoring Formula

Every component is normalized to `0-100`.

```text
recommendation_score =
  staleness_score * 0.30
+ health_impact_score * 0.25
+ time_fit_score * 0.15
+ capacity_fit_score * 0.10
+ area_fit_score * 0.10
+ calendar_context_score * 0.05
+ history_fit_score * 0.05
- dismissal_penalty
```

## Component Definitions

`staleness_score`
: How much the chore needs attention now or by the target time window.

`health_impact_score`
: Estimated Home Health, Area Health, or Group Health improvement.

`time_fit_score`
: How well the chore fits the user's available time.

Time fit must use adaptive recommendation duration rather than treating the
user-entered Chore estimate as authoritative. `ChoreDefinition.estimated_minutes`
is the fallback/base suggestion. Once real active-session timing samples exist,
use the learned median as the base, then lightly adapt the recommended duration
to Mood/Readiness, inferred Capacity, and current-session momentum:

- `low` and `quiet` bias toward shorter/light variants or shorter displayed
  duration
- `focused` uses the normal learned/base duration
- `ready` or strong Capacity may allow a fuller duration
- `restless` prefers movement-friendly, not necessarily longer, care
- after several completed Chores in the current session, optional or additional
  Chores should assume lower remaining capacity unless the user explicitly keeps
  choosing more

Duration adaptation must be used to resize care, not shame the user. If a useful
Chore is too large for the current context, prefer a smaller Chore Variant or a
shorter pass before excluding it.

Only actual active work time can train learned duration. Paused time, reading,
deciding, skips, removals, snoozes, dismissals, cancellations, direct
non-session completions, and invalid timing must not train duration.

`capacity_fit_score`
: How well the chore fits the selected or inferred Capacity level. Capacity is
an internal Recommendation Engine concept, not a top-level Ready-Now question.
Use `auto`, `low`, `steady`, `mobile`, and `strong`.

Mood Context can infer a default Capacity for Ready-Now Mode:
`auto -> auto`, `low/quiet -> low`, `focused -> steady`,
`restless -> mobile`, and `ready -> strong`. Explicit low-capacity context must
still win over inferred ambition.

Capacity should be evaluated against Chore metadata such as effort, movement,
setup friction, duration, and interruption tolerance. For example, `low`
prefers short, low-effort, low-transition chores; `mobile` can include
multi-room movement and light carrying; `strong` can include heavier, longer,
or more physically involved overdue care.

`area_fit_score`
: Whether the chore matches the selected or detected Home Assistant Area.

`calendar_context_score`
: Whether the chore helps prepare for or recover from Calendar Context.
Calendar Context must be fresh. If the snapshot is expired or a source calendar
entity changed, refresh before scoring or score without Calendar Context.
  When this component guesses from Chore names, groups, or Home Assistant Area
  ids, it uses the shared English/basic-French text-signal matcher rather than
  English-only keywords.

`history_fit_score`
: Whether similar users or sessions historically accept or complete this chore.
Uses the bounded context bucket strategy in
`docs/specs/SESSION_HISTORY_LEARNING.md`. If matching history is sparse, fall back to
broader buckets and then to a neutral score.

`Mood Context`
: A lightweight inferred or explicit context from `docs/specs/MOOD_CONTEXT.md`.
Mood Context may influence inferred Capacity, session length, recommendation
wording, and how many choices Homekeep shows. It must not hide urgent stale
chores by itself.

`dismissal_penalty`
: Bounded, decaying penalty from recent dismissals. It uses the formula in
`docs/specs/DISMISSAL_PENALTY.md`. Snoozes do not add to this penalty in MVP; they
only hide a chore until the explicit snooze target time.

Snoozed chores with a future `snoozed_until` are excluded from normal
recommendations before scoring, following `docs/specs/SNOOZE_POLICY.md`.

The scoring implementation must compute:

```text
base_score =
  staleness_score * 0.30
+ health_impact_score * 0.25
+ time_fit_score * 0.15
+ capacity_fit_score * 0.10
+ area_fit_score * 0.10
+ calendar_context_score * 0.05
+ history_fit_score * 0.05

recommendation_score = clamp(base_score - effective_dismissal_penalty, 0, 100)
```

Dismissals may temporarily lower or cool down recommendations. They must not
permanently suppress stale chores.

## Selection Pipeline

The Recommendation Engine should use a two-stage selection pipeline:

1. Apply hard constraints before scoring.
2. Score and rank the remaining candidates.

Hard constraints include hidden or unmanaged Areas, future snoozes, explicit
Area filters, explicit time limits, invalid Chore metadata, active-session
exclusions, and service safety/validation rules. A hard constraint must not be
overridden by a high score.

Scoring should keep `home_need` and `user_fit` separate internally:

```text
home_need = staleness + health/projected_impact + relevant calendar need
user_fit = time_fit + capacity_fit + area_fit + mood/readiness + history_fit
```

The final score may combine them, but implementation should retain both values
for explanation, debugging, and future UI copy. Homekeep's "secret agenda" is a
bounded care nudge: it may gently prefer a higher-need Chore when it still fits
the user's current constraints, but it must not hide the tradeoff or override
explicit user choices.

Care nudge rules:

- cap the care nudge so it cannot dominate user fit
- allow at most one slightly harder/high-need Chore in a small bundle
- balance that Chore with easier, better-fit Chores
- explain the nudge in plain language when it matters
- never frame the nudge as guilt, debt, failure, or urgency unless a future
  true urgent state is explicitly designed

Prefer Chore Variants over rejection. If a useful Chore is too large for the
moment, the engine should consider a smaller or lighter Chore Variant before
dropping it. For example, recommend `Start a small laundry load` instead of a
full laundry catch-up when readiness is low or time is tight.

Session-level exclusions must be applied before scoring optional continuation
Chores and future suggestions in the same session. Do not offer Chores that
were just completed, skipped, removed, dismissed, or snoozed in the current
flow. Exclusions should be local and bounded unless the user explicitly creates
a lasting preference.

Optional continuation Chores after a completed planned bundle use the same
engine principles with stricter bounds:

- shorter duration than the main suggestion
- stronger mood/time fit
- useful Home Health, Area Health, Staleness, or Projected Impact
- no current-session repeats
- no unbounded chaining
- softer copy and lower visual emphasis than the planned bundle

Bundle diversity rules:

- avoid bundles made of near-duplicate actions unless that is the purpose
- avoid all low-value filler Chores
- avoid too many unrelated Areas unless the bundle is intentionally mixed-area
- prefer a coherent mix of one meaningful care item plus supporting fit items

Stability rules:

- shuffle should vary within a small family of good fits, not feel random
- the same context should not produce wildly different suggestions without a
  meaningful context change
- explicit Time, Area, and Mood choices should remain stable through shuffle
- when the user removes or skips a Chore, use that as short-lived context
  feedback before changing durable preference state

Learning must stay conservative. Skips, removals, dismissals, and snoozes can
soften, defer, resize, or retime future suggestions in similar contexts. They
must not permanently suppress useful care by themselves and must not train
adaptive intervals.

## Smart Chore List Shape

The first Smart Chore List should include at most:

```text
1 best Chore Bundle
1 best single chore
1 easiest useful chore
up to 3 alternates
```

Each recommendation must include:

- stable `recommendation_id`
- kind
- title
- chore items
- estimated minutes
- Projected Impact
- short explanation
- suggested action

If Mood Context influenced the recommendation, the explanation should say so in
practical language without claiming to know the user's inner state.

Use the payload shape in `docs/specs/RECOMMENDATION_PAYLOADS.md`.

## Explanation Examples

```text
Reason: high Kitchen Health impact, fits 5 minutes, and you often choose
kitchen tasks after work.
```

```text
Reason: guests are on the calendar tomorrow, and this improves Bathroom Health
quickly.
```

## Empty State

If no good recommendation exists:

```text
No useful chore fits this session.
Options:
- loosen filters
- show all due chores
- schedule a session for later
- end for now
```

## Light Session Rules

- Prefer short sessions.
- Finishing the planned session is always a success.
- After completion, offer only a bounded inline optional Chore list when useful.
- Optional continuation Chores are optional and bounded.
- Accepting optional Chores is positive history, not permission for an
  unbounded queue.
- Optional continuation Chores use the original Chore Session context; they do
  not create an implicit new session in MVP.
