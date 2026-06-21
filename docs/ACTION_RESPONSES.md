# Home Assistant Action Responses

## Goal

Homekeep services should be useful from Bubble Card, automations, scripts,
Assist, and developer tools without requiring callers to scrape entity state.

When a service naturally produces data, register it with Home Assistant action
response support and return a dictionary with the documented payload shape.

## Implementation Rule

During implementation, verify the exact import path and signature against the
supported Home Assistant core version. The intended pattern is:

```python
from homeassistant.core import SupportsResponse

hass.services.async_register(
    DOMAIN,
    "generate_smart_chore_list",
    handle_generate_smart_chore_list,
    schema=GENERATE_SMART_CHORE_LIST_SCHEMA,
    supports_response=SupportsResponse.ONLY,
)
```

Handlers registered with `SupportsResponse.ONLY` must return a dictionary.
Handlers registered with `SupportsResponse.OPTIONAL` may return a dictionary
when the caller requests a response.

Do not implement data-producing services as fire-and-forget state changes only.
Entity updates are still useful, but the service response is the primary return
path for generated recommendations and newly created sessions.

## Required Response Support

`homekeep.generate_smart_chore_list`
: Must use `SupportsResponse.ONLY`. It returns the Smart Chore List Result from
`docs/RECOMMENDATION_PAYLOADS.md`.

`homekeep.start_recommendation`
: Must use `SupportsResponse.ONLY`. It returns the created Chore Session
summary as `StartRecommendationResult` from `docs/SERVICE_SCHEMAS.md`.

`homekeep.start_chore_bundle`
: Must use `SupportsResponse.ONLY` if the compatibility alias is implemented.
It returns the same response shape as `homekeep.start_recommendation`.

`homekeep.accept_bonus_chore`
: Must use `SupportsResponse.ONLY`. It returns the updated session status and
active Bonus Chore item.

`homekeep.end_session`
: Must use `SupportsResponse.ONLY`. It returns the final session status and any
Bonus Chore offer when requested.

`homekeep.refresh_calendar_context`
: Should use `SupportsResponse.OPTIONAL`. It returns refreshed derived Calendar
Context when the caller requests a response.

Mutation services such as `complete_chore`, `skip_chore`, `snooze_chore`, and
`dismiss_chore` may use `SupportsResponse.OPTIONAL` to return a small
acknowledgement dictionary, but they do not need response-only behavior in MVP.

## Response Shape Rules

- Return plain JSON-serializable dictionaries.
- Use snake_case keys matching the docs.
- Do not return internal model objects.
- Do not include raw calendar text, secrets, tokens, or private identifiers.
- Include stable IDs needed by the next action, such as `snapshot_id`,
  `recommendation_id`, `session_id`, and `session_item_id`.
- Keep response payloads bounded.
- Service errors should still raise Home Assistant service exceptions instead
  of returning error dictionaries.

## Tests Required

Implementation must test:

- services that declare `SupportsResponse.ONLY` return dictionaries
- `generate_smart_chore_list` returns the documented Smart Chore List Result
- `start_recommendation` returns `session_id` and
  `source_recommendation_snapshot_id`
- `start_recommendation` returns materialized session items with concrete
  `session_item_id` values for subsequent actions
- response payloads are JSON-serializable
- service errors raise clear exceptions instead of returning error dictionaries
