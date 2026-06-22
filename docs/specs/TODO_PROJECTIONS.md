# To-do Projection Contract

Home Assistant To-do entities are projections of Homekeep state. They are not a
source of truth.

## Supported Write-Through Operation

The only supported write-through operation in the MVP is completion of an
existing projected item.

```text
To-do complete item
-> validate projected item token
-> call Homekeep completion/session logic
-> refresh To-do projection from Homekeep state
```

## Unsupported Mutations

These To-do mutations must not modify Homekeep durable state:

```text
create item
delete item
rename item
change description
change due date
move/reorder item
manually create arbitrary completed item
```

Preferred behavior:

```text
1. Reject unsupported mutation with a clear Home Assistant error if the To-do
   platform method allows rejection.
2. If Home Assistant UI requires accepting the call shape, ignore the mutation
   and immediately refresh the projection from Homekeep state.
3. Log a diagnostic warning for unsupported write attempts.
```

## Reverting Optimistic UI Mutations

Home Assistant's To-do UI may optimistically assume that add, delete, rename,
edit, or reorder operations succeeded. Homekeep must make unsupported
operations visibly snap back to the projection from internal storage.

In `todo.py`, every unsupported To-do platform mutation handler must:

```text
1. avoid mutating Homekeep storage
2. log the unsupported mutation attempt at diagnostic/debug level
3. rebuild or keep the projected item list from Homekeep storage
4. call self.async_write_ha_state() before returning when the entity instance
   can do so
```

This applies to Home Assistant handlers for adding, deleting, updating,
renaming, moving, or reordering To-do items. Use the exact method names required
by the supported Home Assistant core version, but the behavior must be the
same.

The result should be:

```text
user adds/deletes/edits item in HA UI
-> HA frontend briefly shows optimistic change
-> Homekeep handler rejects or ignores unsupported mutation
-> Homekeep calls async_write_ha_state()
-> HA frontend refreshes from Homekeep projection
-> unsupported change disappears
```

If a handler can raise a clear Home Assistant validation error and still causes
the frontend to refresh correctly, that is acceptable. If the frontend remains
stale after the error, Homekeep must still force a projection refresh.

## Projection Identity

Projected To-do items must include stable Homekeep metadata sufficient to map a
completion back to Homekeep state.

Recommended metadata:

```yaml
homekeep_projection_id: string
chore_id: string
session_item_id: string | null
session_id: string | null
recommendation_snapshot_id: string | null
variant: tiny | normal | deep
projection_kind: recommendation | active_session | area
```

If a To-do completion lacks valid Homekeep metadata, reject it. Do not infer by
name.

## Entity-Specific Rules

`todo.homekeep_recommendations`

- Completing a projected recommendation may start or complete only through the
defined Homekeep flow.
- If the recommendation item maps to a Chore that is already pending in an
active Chore Session, completion may write through to that active session item.
Recommendation-only completion without a matching active session remains
rejected.
- When such an active-session match exists, the recommendation projection should
  expose the resolved active-session metadata so the Home Assistant frontend can
  send back `session_id` and `session_item_id`.
- Creating, deleting, renaming, moving, or editing recommendations is rejected
or reverted.
- Regeneration replaces the projection from Homekeep recommendations.

`todo.homekeep_active_session`

- Completing a projected active session item calls Homekeep session completion.
- Creating, deleting, renaming, moving, or editing session items is rejected or
reverted.
- Session item order comes from Homekeep session state.

`todo.homekeep_<area>`

- Area To-do lists are read-mostly projections.
- Completion may call Homekeep completion logic if the item has valid metadata.
- All other mutations are rejected or reverted.

## Tests Required

- completing a projected item calls Homekeep completion logic
- adding a To-do item is rejected or reverted and does not create a Chore
- deleting a To-do item is rejected or reverted and does not remove a Chore
- renaming/editing a To-do item is rejected or reverted and does not mutate
Homekeep state
- reordering a To-do item is rejected or reverted unless Homekeep later supports
session ordering explicitly
- completing an item without valid Homekeep metadata is rejected
