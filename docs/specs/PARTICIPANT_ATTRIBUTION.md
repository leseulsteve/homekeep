# Participant Attribution

Homekeep supports a `participants` list on Chore Sessions. MVP behavior should
be simple and explicit so shared Home Assistant instances do not create
ambiguous history.

## MVP Rules

For session-based completions:

```text
if completed_by is provided:
  completed_by must be in ChoreSession.participants
elif ChoreSession.started_by is set:
  completed_by may default to started_by
else:
  completed_by remains null
```

For non-session completions:

```text
completed_by may be null or a known Home Assistant user/person identifier.
```

The MVP should not attempt complex fairness or contribution scoring.

## Session Item Attribution

Each session item should store completion attribution:

```yaml
completed_by: string | null
```

When a chore is completed inside a session, the resulting `ChoreCompletion` and
the session item should use the same `completed_by` value.

## Validation

Reject session-based completion when:

```text
session_id is provided
completed_by is provided
completed_by is not in session.participants
```

If `participants` is empty, no participant validation is possible. In that case,
Homekeep may accept `completed_by` but should not use it for fairness logic.

## Tests Required

- `completed_by` in participants is accepted
- omitted `completed_by` defaults to `started_by` when available
- `completed_by` outside participants is rejected
- session item and ChoreCompletion store the same `completed_by`
- non-session completion may use null `completed_by`
