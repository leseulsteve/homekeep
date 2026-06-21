# M5Dial Physical UX Checklist

Use this on the actual Dial before treating a firmware or HA contract change as
done. The Dial owns only transient selection state; Home Assistant owns every
durable inventory decision.

## Controls

- Short press advances one screen or acknowledges result/error.
- Long press opens the Mise listening view and clears the active request.
- Side Hold Button cancels any active flow and returns to idle.
- Encoder changes only the current visible choice or quantity.
- NFC scan starts a new request and invalidates any older request.

## Real-Device Pass

- Scan unknown tag: loading view appears, create flow opens, item selection is
  usable, quantity changes with the encoder, location selection is clear, save
  shows success, and the new container exists in Home Assistant.
- Scan known tag: current inventory appears, quantity and location can be
  changed, save shows success, and the existing container updates in Home
  Assistant.
- Stale response: scan tag A, scan tag B before tag A response returns, and
  confirm tag A response is ignored without mutating inventory.
- Cancel: start create/update, press the side Hold Button, and confirm the Dial
  returns to idle and a later HA response does not mutate inventory.
- Timeout: block or delay the HA response and confirm the Dial shows a clear
  no-reply/error view with the attention tone.
- Provider failure: force a Grocy/Mealie/HA write failure and confirm the Dial
  shows the failure result, plays the attention tone, and leaves inventory
  unchanged.
- Listening view: long press from idle and from an active flow; confirm the
  simple Mise view appears, says how to exit, and exits with a short press.

## Screen Questions

- Idle asks: scan a tag?
- Loading asks: wait while HA identifies this tag?
- New container asks: which item?
- Inventory count asks: how many?
- Location asks: where does it live?
- Saving asks: wait for HA confirmation?
- Result asks: continue or scan another tag?
- Error asks: retry or cancel?
- Mise listening asks: stay in the ambient listening view or exit?
