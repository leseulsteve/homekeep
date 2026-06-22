# Target Time Window

## Goal

`target_time_window` lets callers ask for recommendations for a future or
specific time window. It must be parsed consistently so Scheduled-Suggestion,
Calendar Context, recommendation snapshots, and context fingerprints agree.

## Parser Choice

Use `python-dateutil` for flexible user-facing datetime parsing when a caller
passes natural-ish text or ISO-like strings.

Declare `python-dateutil` in the Home Assistant integration `manifest.json`
requirements during scaffolding.

Implementation guidance:

```python
from dateutil import parser as dateutil_parser
from homeassistant.util import dt as dt_util
```

After parsing, convert all datetimes through Home Assistant timezone helpers.
Do not compare or bucket raw naive or UTC datetimes directly.

Project-wide rule: use `python-dateutil` only at user-facing or config-facing
date/time input boundaries. Core Homekeep logic should receive normalized Home
Assistant local datetimes, timedeltas, or explicit internal values.

## Accepted MVP Inputs

MVP should support:

```text
null
today 17:00-18:00
tomorrow 09:00-10:00
next Friday 17:00-18:00
2026-07-03 17:00-18:00
2026-07-03T17:00:00-04:00/2026-07-03T18:00:00-04:00
```

For Ready-Now Mode, `target_time_window` may be null. Null means "now".

For Scheduled-Suggestion Mode, `target_time_window` is required in MVP.

## Normalized Shape

Parsing must produce:

```yaml
start: datetime
end: datetime
label: string
```

Rules:

- `start` and `end` must be timezone-aware Home Assistant local datetimes
- `end` must be after `start`
- if only a start time is provided, use the requested time budget when present
- if no time budget is present, default to a 60-minute window
- reject windows longer than 24 hours in MVP
- reject ambiguous text that `python-dateutil` cannot parse confidently

## Storage And Responses

Store and return `target_time_window` as a normalized string:

```text
<local ISO start>/<local ISO end>
```

Example:

```text
2026-07-03T17:00:00-04:00/2026-07-03T18:00:00-04:00
```

The original user text may be used transiently for parsing, but should not be
the durable value on RecommendationSnapshot or ChoreSession.

## Context Fingerprint

`context_fingerprint` must use the normalized `target_time_window` string, not
the raw user input. For example, these should fingerprint the same if they
resolve to the same local window:

```text
next Friday 17:00-18:00
2026-07-03T17:00:00-04:00/2026-07-03T18:00:00-04:00
```

## Tests Required

Implementation must test:

- ISO window parses to timezone-aware Home Assistant local datetimes
- natural text window parses through `python-dateutil` where supported
- parsed windows normalize to `<local ISO start>/<local ISO end>`
- null target window is accepted for Ready-Now Mode
- null target window is rejected for Scheduled-Suggestion Mode
- end before start is rejected
- windows longer than 24 hours are rejected
- context fingerprint uses normalized target window, not raw input text
