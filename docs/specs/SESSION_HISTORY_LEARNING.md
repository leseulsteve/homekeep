# Session-History Learning

Session-History Learning should improve recommendations without fragmenting
history into buckets too small to learn from.

## V1 Context Bucket

The v1 `context_bucket` must be deterministic and bounded.

`context_bucket` is not `context_fingerprint`. Use `context_bucket` for broad
learning lookup and `docs/specs/CONTEXT_FINGERPRINT.md` for exact recommendation
context provenance.

Use these dimensions:

```text
recommendation_mode
day_type
time_block
energy_level
goal
area_scope
mood
```

Dimension values:

```text
recommendation_mode:
- ready_now
- scheduled_suggestion

day_type:
- weekday
- weekend

time_block:
- morning
- midday
- afternoon
- evening
- night

energy_level:
- low
- normal
- high
- quiet
- any

goal:
- quick_wins
- overdue
- visible_impact
- prevent_future_mess
- full_reset
- any

area_scope:
- selected:<area_id>
- detected:<area_id>
- any

mood:
- calm
- focused
- tired
- overwhelmed
- energized
- unknown
- any
```

Format:

```text
mode=<mode>|day=<day_type>|time=<time_block>|energy=<energy>|goal=<goal>|area=<area_scope>|mood=<mood>
```

Example:

```text
mode=ready_now|day=weekday|time=afternoon|energy=normal|goal=quick_wins|area=selected:kitchen|mood=tired
```

## Time Blocks

Time blocks are based on Home Assistant local time, not raw UTC.

Before deriving `day_type` or `time_block`, convert Home Assistant datetimes to
local time:

```python
from homeassistant.util import dt as dt_util

local_dt = dt_util.as_local(value)
```

Use `local_dt` for weekday/weekend checks and the clock ranges below. Do not
bucket directly from UTC datetimes, because that will put evening, night, and
early morning sessions into the wrong learning context for many users.

```text
morning:   05:00-10:59
midday:    11:00-13:59
afternoon: 14:00-16:59
evening:   17:00-21:59
night:     22:00-04:59
```

Naive datetimes should be treated according to Home Assistant's datetime
helpers and converted through the same local-time path. During implementation,
verify exact helper behavior against the supported Home Assistant core version.

## Fallback Matching

History lookup must use fallback buckets to avoid sparse signals.

Lookup order:

```text
1. exact bucket + user + chore
2. exact bucket + household + chore
3. bucket without area + user + chore
4. bucket without area + household + chore
5. bucket with mood=any + household + chore
6. bucket with energy=any and goal=any + household + chore
7. area-level stats
8. neutral history score
```

If total observations for a match are below the minimum sample threshold, fall
through to the next broader bucket.

Recommended MVP threshold:

```text
minimum_observations = 3
```

## History Fit Score

Initial formula:

```text
attempts = accepted_count + completed_count + skipped_count + snoozed_count
positive = accepted_count + completed_count
negative = skipped_count + snoozed_count

raw_score = 50 + ((positive - negative) / max(attempts, 1)) * 50
history_fit_score = clamp(raw_score, 0, 100)
```

If there are too few observations after fallback matching:

```text
history_fit_score = 50
```

History is a weak recommendation signal in v1 and should not hide stale or
high-impact chores.

## Bounded Storage

Stats should be bounded.

Recommended MVP limits:

```text
max_buckets_per_user = 200
max_stats_per_bucket = 100
prune stats not updated in 180 days
```

## Updates

Update Session-History Learning on:

```text
recommendation accepted
chore completed
chore skipped
chore snoozed
recommendation dismissed
Bonus Chore accepted
```

Dismissals update history stats for future fit scoring, but the deterministic
score subtraction comes from `docs/specs/DISMISSAL_PENALTY.md`. Snoozes must not be
counted as dismissals for that penalty.

Dismissal context source:

```text
if dismiss_chore has session_id:
  use the ChoreSession context bucket
elif dismiss_chore has recommendation_snapshot_id:
  use the RecommendationSnapshot context bucket
else:
  update only chore-level dismissal penalty and skip history bucket update
```

Do not guess from "the active session" without a `session_id`; multiple users
or stale UI responses can make that ambiguous.
