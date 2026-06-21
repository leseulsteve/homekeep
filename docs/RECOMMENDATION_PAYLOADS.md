# Recommendation Payloads

Smart Chore List output must use a stable payload shape. Do not leave
recommendations as arbitrary dictionaries.

`homekeep.generate_smart_chore_list` must return the Smart Chore List Result as
a Home Assistant action response. See `docs/ACTION_RESPONSES.md`.

## Recommendation

```yaml
recommendation_id: string
kind: bundle | single | easiest | alternate | bonus
title: string
estimated_minutes: int
chore_items: list[RecommendationItem]
projected_impact:
  home_health_delta: float
  area_health_delta: dict[string, float]
reason: string
score: float
source_snapshot_id: string
expires_at: datetime | null
```

Validation:

- `recommendation_id` must be stable within a RecommendationSnapshot.
- `kind` determines how UI labels and `start_recommendation` behave.
- `estimated_minutes` must be positive and finite.
- `score` must be finite and bounded.
- `reason` must be short and user-readable.

## RecommendationItem

```yaml
chore_id: string
variant: tiny | normal | deep
estimated_minutes: int
area_id: string | null
session_item_id: string | null
```

`session_item_id` is null before materialization. It is assigned when a
recommendation becomes a Chore Session.

Callers must not cache or reuse `RecommendationItem.session_item_id` for
session actions. Before materialization it is always null, and after
materialization the authoritative item identities come from the
`StartRecommendationResult.items` response.

## Smart Chore List Result

```yaml
snapshot_id: string
recommendation_mode: ready_now | scheduled_suggestion
target_time_window: string | null
expires_at: datetime
mood_context: MoodContext | null
best_bundle: Recommendation | null
best_single_chore: Recommendation | null
easiest_chore: Recommendation | null
alternates: list[Recommendation]
empty_state: EmptyState | null
```

This shape is the response dictionary for
`homekeep.generate_smart_chore_list`.

By default, `alternates` contains up to 3 recommendations. If the caller passes
`include_alternates=false`, `alternates` must be an empty list.

`mood_context` is included when Homekeep uses explicit or inferred Mood Context
for defaults, wording, or recommendation shaping. It must follow
`docs/MOOD_CONTEXT.md`.

For Scheduled-Suggestion Mode, `target_time_window` must be set and `expires_at`
must be shown by the UI so the user understands that the plan may need refresh
before starting.

## EmptyState

```yaml
message: string
actions: list[loosen_filters | show_due | schedule_later | end_now]
```

## ScoreBreakdown

```yaml
recommendation_id: string
total_score: float
components:
  staleness_score: float
  health_impact_score: float
  time_fit_score: float
  energy_fit_score: float
  area_fit_score: float
  calendar_context_score: float
  history_fit_score: float
  dismissal_penalty: float
```

`dismissal_penalty` is the effective penalty after decay, caps, cooldown, and
staleness override from `docs/DISMISSAL_PENALTY.md`. It is the value subtracted
from the recommendation base score, not the raw count of dismissal events.

## Materialization

`homekeep.start_recommendation` takes:

```yaml
recommendation_snapshot_id: string
recommendation_id: string
```

It must copy `Recommendation.chore_items` into concrete `SessionItem` records
with new `session_item_id` values.

Result shape:

```yaml
session_id: string
source_recommendation_snapshot_id: string
status: active
items: list[MaterializedSessionItem]
```

## MaterializedSessionItem

```yaml
session_item_id: string
chore_id: string
variant: tiny | normal | deep
status: pending | active
estimated_minutes: int
area_id: string | null
```

After `start_recommendation`, callers must use this materialized item list for
`complete_chore`, `skip_chore`, `snooze_chore`, and display of the active
session. Cached Recommendation payloads are proposal data only.
