# Bonus Chore Lifecycle

Bonus Chores are optional extensions to a completed Light Session. They should
not create an unbounded queue or an ambiguous session state.

## MVP Model

The MVP keeps the original Chore Session open in a bounded post-completion
state while a Bonus Chore is pending.

Session status values:

```text
active
paused
bonus_pending
bonus_active
completed
cancelled
```

## Flow

```text
1. User finishes planned session items.
2. `homekeep.end_session` is called with:
   status=completed
   offer_bonus_chore=true
3. If the session is `active` or `paused`, Homekeep marks it `bonus_pending`.
4. Homekeep sets `bonus_chore_expires_at` and returns at most one Bonus Chore.
5. User accepts the Bonus Chore with `homekeep.accept_bonus_chore`.
6. Homekeep marks the session `bonus_active`.
7. User completes the Bonus Chore with the original `session_id`.
8. Homekeep marks the Bonus Chore done and the session `completed`.
```

If the user declines:

```text
session status = completed
bonus_chore_accepted = false
```

If the Bonus Chore expires or is cancelled:

```text
session status = completed
bonus_chore_accepted = false
ended_at = expiry handling time
```

## Expiry Policy

MVP Bonus Chore offer TTL:

```text
bonus_chore_offer_ttl_minutes = 15
```

When Homekeep moves a session to `bonus_pending`:

```text
bonus_chore_expires_at = now + 15 minutes
```

Expiry checks are lazy. Homekeep does not need a background timer in MVP.

Check expiry:

- before `accept_bonus_chore`
- before `complete_chore` for a `bonus_pending` or `bonus_active` session
- before returning active session state to Home Assistant entities
- before `end_session`
- during startup/reload cleanup

If a session is `bonus_pending` and `now >= bonus_chore_expires_at`:

```text
status = completed
ended_at = now
bonus_chore_accepted = false
bonus_chore_offered remains stored for audit
bonus_chore_expires_at remains stored for audit
```

If a session is `bonus_active`, `bonus_chore_expires_at` no longer controls
completion. Accepting the Bonus Chore consumes the offer before expiry, and the
user may finish that accepted Bonus Chore normally.

Late `homekeep.accept_bonus_chore` calls must reject with a clear service error:

```text
bonus_chore_expired
```

The error should include the expired `session_id` when possible, but must not
reopen the session or silently create a new Bonus Chore.

## Service Rules

`homekeep.end_session`

- With `offer_bonus_chore=false`, complete or cancel the session normally.
- With `offer_bonus_chore=true`, `status=completed`, and current status
  `active` or `paused`, move to `bonus_pending` if all planned items are done
  and a Bonus Chore is available.
- Return the Bonus Chore and keep the original `session_id`.
- Set `bonus_chore_expires_at = now + 15 minutes` when moving to
  `bonus_pending`.

`homekeep.complete_chore`

- May accept the original `session_id` when session status is `bonus_active`.
- Must reject completing arbitrary chores against a `bonus_pending` session.
- Must reject completing more than the one accepted Bonus Chore.

`homekeep.accept_bonus_chore`

- Moves `bonus_pending` to `bonus_active`.
- Must reject if the requested chore does not match `bonus_chore_offered`.
- Must check `bonus_chore_expires_at` before accepting.
- If expired, mark the session `completed` and raise `bonus_chore_expired`.

## Boundedness Rules

- A session may offer at most one Bonus Chore in MVP.
- A pending Bonus Chore offer expires after 15 minutes.
- Completing a Bonus Chore must not trigger another Bonus Chore automatically.
- The original planned session counts as successful even if Bonus Chore is
declined, expired, skipped, or cancelled.

## Tests Required

- `end_session(..., offer_bonus_chore=true)` moves to `bonus_pending`
- `bonus_pending` sets `bonus_chore_expires_at` to 15 minutes after offer
- paused sessions can move to `bonus_pending` when planned items are complete
- expired `bonus_pending` session becomes `completed`
- late `accept_bonus_chore` after expiry raises `bonus_chore_expired`
- accepting Bonus Chore moves to `bonus_active`
- completing Bonus Chore uses original `session_id`
- completing Bonus Chore ends session as `completed`
- completing an unrelated chore in `bonus_active` is rejected
- declining Bonus Chore ends session as `completed`
- Bonus Chore completion does not offer another Bonus Chore
