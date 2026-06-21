# M5Dial Use-Case Roadmap

## North Star

The M5Dial should be the fridge-mounted controller for the physical kitchen.
When there is nothing important to say, it is a calm clock. When something
needs attention, it becomes the fastest way to understand, confirm, and recover
without opening the Home Assistant panel.

The web panel remains the review and configuration surface. The Dial owns the
moment at the fridge: glance, scan, rotate, swipe, confirm, cancel, and move on.

Provider ownership stays fixed:

- Mealie owns recipes, foods, and meal-planning context.
- Grocy owns stock, products, units, storage locations, expiry, and minimum
  stock policy.
- KitchenOwl owns shopping-list execution.
- Home Assistant owns automations, entities, devices, and environmental
  signals.
- Mise owns NFC containers, physical prep state, storage attention, local
  logbook history, and the next useful kitchen action.

## Interaction Grammar

The Dial should feel predictable before it feels clever.

- Idle: clock first, unless an action, alert, timer, or attention card exists.
- Rotate: change the highlighted choice, card, quantity, timer, or location.
- Short press: confirm the highlighted thing or advance one step.
- Long press: open Mise listening / command mode from anywhere.
- Hold button: cancel the current transient flow and return to idle.
- Swipe left/right: move between major contexts.
- Swipe up: reveal detail, reason, source, or supporting data.
- Swipe down: return to summary or dismiss detail.
- NFC scan: jump directly into the scanned container workflow.
- Audio: progress, saved, attention, cancel, timer done.

The user should not have to remember mode names. The screen should answer:

- What is happening?
- Why does it matter?
- What can I do now?

## Use Case: I Walk Up To The Fridge

User need: know whether the kitchen needs attention before deciding what to do.

Default workflow:

1. Dial shows the clock if everything is quiet.
2. If something matters, the clock yields to the top priority card.
3. Rotate moves through other cards.
4. Swipe up shows why the card exists.
5. Short press opens the safest action.

Useful cards:

- "Fridge warm"
- "Use curry today"
- "Milk opened 6 days ago"
- "Queue empty containers"
- "Grocy write failed"
- "Mealie unavailable"
- "Rice timer 08:32"

Dial fit:

- The round screen is perfect for one status and one reason.
- The rotary encoder makes priority cards feel physical and fast.
- The clock fallback keeps the device useful without becoming noisy.

Home Assistant contract:

- Home Assistant sends a bounded priority feed ranked by safety, freshness,
  failed writes, shopping, and planning.
- Each card includes id, severity, title, reason, source, action, request_id.
- The Dial never invents severity or mutates from a passive card.

First useful implementation:

- Reuse dashboard suggested actions and storage attention.
- Add a `show_priority_cards` ESPHome action.
- Make idle show clock when the card list is empty.

## Use Case: I Scan A Container

User need: identify or update the physical thing in hand.

Known container workflow:

1. User scans NFC.
2. Dial shows item, quantity, location, and freshness/status.
3. Rotate adjusts quantity.
4. Swipe up shows provider, dates, last log entry, and source.
5. Short press advances to location/action.
6. Rotate chooses location or action.
7. Short press confirms save.

Unknown tag workflow:

1. User scans NFC.
2. Dial shows likely item list.
3. Rotate selects item.
4. Short press confirms item.
5. Rotate sets quantity.
6. Swipe/press selects location.
7. Short press saves.

Dial fit:

- NFC makes physical identity instant.
- Rotary quantity adjustment is better than touch typing.
- Hold button gives confidence because cancel is always available.

Safety contract:

- Every scan starts a request_id.
- Home Assistant tracks active requests and consumes mutating events once.
- Stale, canceled, duplicate, timed-out, or restarted flows cannot mutate
  inventory.
- Location must be explicit and cannot be The Void.

Wow later:

- Show a tiny "confidence ring" around the screen: green for known, amber for
  missing location, red for unsafe storage.
- Suggest location based on item metadata and recent behavior.

## Use Case: I Am Putting Food Away

User need: save food in the right place with enough context to find it later.

Basic workflow:

1. Scan the container.
2. Dial asks what is inside or shows the known contents.
3. Rotate sets quantity.
4. Swipe to location.
5. Rotate selects fridge, freezer, pantry, or another valid location.
6. Short press saves.

With scale:

1. Scan the container.
2. Put it on the scale.
3. Dial shows stable gross weight.
4. Home Assistant subtracts known tare if available.
5. Dial shows net quantity.
6. Short press confirms.

With thermometer: (wow later)

1. Probe reading arrives while the container flow is active.
2. Dial shows "Cooling", "Warm", or "In range" based on HA policy.
3. Press logs the reading.
4. If storage is risky, Dial suggests a safer location or warning.

Dial fit:

- The fridge location makes this workflow natural.
- Scale and thermometer readings remove manual entry.
- Rotary remains available for small corrections.

Data needed:

- Optional container tare metadata.
- Last stable scale reading and unit.
- Optional temperature reading and freshness.
- Home Assistant location health.

Safety contract:

- No automatic save from scale or thermometer alone.
- Stable readings can prefill a confirmation card.
- Home Assistant owns unit validation, tare math, and safety classification.

Wow later:

- "Put-away composer": scan tag, weigh, probe, choose location, save in one
  guided flow.
- "Cooling timer": if food is too warm for storage, Dial starts a timer and
  returns to the container when it expires.

## Use Case: I Want To Know What To Eat Or Use First

User need: make a fridge-side decision without opening Mealie or the panel.

Workflow:

1. Dial shows "Use first" card when there is freshness pressure.
2. Rotate through prepared meals, opened products, and at-risk containers.
3. Swipe up shows why: opened date, best-before date, location health, or low
  quantity.
4. Press opens the scanned/selected container or starts a use/update flow.

Dial fit:

- This is a small ranked list, not a recipe browser.
- The Dial can show one concrete option at a time.
- The fridge location makes "what should I use?" immediate.

Home Assistant contract:

- Home Assistant builds use-first cards from Mise containers, Grocy dates, and
  Mealie planning context.
- Cards include source chips and reason text.
- The Dial never queries providers directly.

Wow later:

- "Dinner radar": ring segments for ready protein, starch, vegetable, sauce.
- "Use-up pairing": show "Use curry with cooked rice" when both are ready.
- "Presence-aware nudge": if the user is in the kitchen after work, show a
  dinner-use card instead of a generic status.

## Use Case: I Am Cooking Or Prepping A Batch

User need: turn cooking into tracked prepared food without paperwork.

Workflow:

1. User opens Cook context or says a short command.
2. Dial shows recent/planned recipes and prep components.
3. Rotate selects recipe or component.
4. Short press starts a batch flow.
5. User chooses portions or weighs output.
6. User scans one or more containers.
7. Dial saves prepared containers with quantity and location.

Dial fit:

- Rotary is good for portions.
- NFC is good for assigning batch output to real containers.
- Scale is good for splitting uneven leftovers.

Home Assistant contract:

- Mealie recipe remains a reference.
- Mise creates physical recipe/meal containers.
- Grocy stock changes happen through existing provider-safe paths.

Wow later:

- "Batch split": after weighing total output, scan containers one by one and
  the Dial tracks remaining weight.
- "Prep station mode": display timer, current recipe batch, next container to
  fill, and remaining portions.
- "Smart label handoff": send a short label to an e-ink shelf/bin tag.

## Use Case: I Notice Something Is Empty

User need: make shopping happen from the place the empty container is found.

Workflow:

1. Scan empty or low container.
2. Dial shows item and current quantity.
3. Rotate to "Queue shopping" or "Mark empty".
4. Press opens confirmation.
5. Second press queues through Grocy/KitchenOwl.
6. Result shows target and item count.

Dial fit:

- Empty container is physically in the user's hand.
- Two-press confirmation prevents accidental shopping spam.
- Result feedback avoids "did that do anything?" uncertainty.

Home Assistant contract:

- Use existing shopping services:
  - `add_empty_containers_to_shopping_list`;
  - `add_missing_products_to_shopping_list`;
  - `add_to_shopping_list`.
- Result copy mirrors panel/logbook.
- Provider failures show "Not queued", not "Saved".

Wow later:

- "Scan-to-shop pile": scan several empty containers, then press once to queue
  a grouped shopping request.
- "Shopping confidence": show Grocy vs KitchenOwl target before confirmation.

## Use Case: I Need To Move Food

User need: move a physical container because storage changed or food is at risk.

Workflow:

1. Dial shows storage attention or user scans a container.
2. Rotate to "Move".
3. Rotate through valid locations.
4. Swipe up shows location health.
5. Press saves move.

Dial fit:

- Fridge-mounted controller is the natural place to choose fridge/freezer.
- Rotary location choice is faster than opening the panel.
- Storage health can influence the decision at the exact moment.

Home Assistant contract:

- Home Assistant provides valid active locations.
- Protected locations are never selectable.
- Location health is advisory unless a policy later blocks a move.

Wow later:

- "Safe move suggestion": if fridge is warm, suggest freezer or pantry based on
  product behavior.
- "Door-aware move": if freezer door is open, put freezer option first while
  the user is standing there.

## Use Case: Storage Conditions Are Bad

User need: understand whether food is at risk and what can be done.

Workflow:

1. Home Assistant detects storage warning or critical state.
2. Dial priority card replaces idle clock.
3. Rotate through affected locations.
4. Swipe up shows sensor readings and affected containers.
5. Press opens action: acknowledge, move, review, or start timer.

Dial fit:

- The fridge is the right place for fridge/freezer warnings.
- The small screen can show one problem at a time.
- Audio can make critical attention noticeable without becoming a siren.

Home Assistant contract:

- Home Assistant owns thresholds and classification.
- Dial receives status, problems, affected count, and top affected containers.
- Dial does not claim food is safe. It says "check", "warm", "out of range",
  "in range", or "attention".

Wow later:

- "Risk map": ring segments around the display for fridge/freezer/pantry.
- "Rescue workflow": one press opens a guided move list for at-risk prep.

## Use Case: I Need A Timer While Cooking

User need: start and notice kitchen timers without touching a phone.

Workflow:

1. User long-presses and says "rice timer 18 minutes" or rotates in Timer.
2. Dial shows timer card.
3. Idle clock includes active timer when relevant.
4. Audio alerts when done.
5. Press acknowledges; hold cancels.

Dial fit:

- The Dial is visible from the kitchen.
- Rotary is good for duration.
- Timers naturally coexist with clock idle.

Home Assistant contract:

- Home Assistant owns timer entities/helpers.
- Dial sends timer actions and displays current timer state.

Wow later:

- Appliance smart-plug detection suggests timers when rice cooker or slow
  cooker power changes.
- Timers can attach to containers or recipe batches.

## Use Case: My Hands Are Busy

User need: operate common flows with minimal touch.

Workflow options:

- Long press opens voice.
- Nearby button puck confirms/cancels with wet hands.
- Presence detects the kitchen user and wakes relevant cards.
- Speaker/buzzer confirms without requiring visual attention.

Dial fit:

- Long press is deliberate and easy.
- Voice is useful for intent, not final mutation.
- External button can sit closer to the prep area.

Safety contract:

- Voice can propose actions but cannot save inventory alone.
- Mutations require press, button, scan context, or explicit HA-approved
  confirmation.
- Ambiguous voice results show choices.

Wow later:

- "Mise, what needs using?" opens a ranked use-first card.
- "I made four portions of curry" creates a draft batch flow waiting for scan.
- "Where is the tofu?" shows location if known and optionally beeps near a
  tagged shelf/peripheral later.

## Use Case: I Have A Packaged Product

User need: handle store packaging without pretending it is a reusable
container.

Workflow:

1. Scan barcode.
2. Dial shows Grocy product match or unknown barcode.
3. Rotate actions: add stock, open package, transfer to NFC container, queue
   shopping.
4. If transferring, scan NFC container.
5. Optionally weigh the transferred amount.
6. Press confirms.

Dial fit:

- Barcode is product identity.
- NFC is container identity.
- The Dial can coordinate both without confusing them.

Home Assistant contract:

- Barcode never becomes a container tag.
- Linking product to container requires explicit confirmation.
- Provider identity comes from Home Assistant.

Wow later:

- "Open package assistant": barcode + scale + NFC creates a tracked container
  and updates remaining packaged stock.

## Use Case: I Am Setting Up Or Pairing Kitchen Peripherals

User need: add useful local devices without turning YAML into a secret pile.

Workflow:

1. Dial shows nearby peripheral candidates.
2. Rotate through devices: scale, thermometer, beacon, button, barcode scanner.
3. Press requests Home Assistant enrollment or opens a pairing prompt.
4. Home Assistant owns registry, credentials, and entity mapping.

Dial fit:

- BLE scanning and screen make discovery visible.
- Fridge location is central enough for storage sensors and kitchen presence.

Home Assistant contract:

- Dial may discover and display candidates.
- Home Assistant owns pairing, registry, secrets, and storage-location
  assignment.

Wow later:

- "Tap to assign": scan a shelf/location tag, then pair a thermometer or door
  sensor to that location.
- "Peripheral health card": scale battery low, probe missing, fridge sensor
  stale.

## Cross-Workflow Peripheral Ideas

Scale:

- Learn empty container tare.
- Weigh filled containers.
- Split batches across scanned containers.
- Measure remaining quantity after serving.

Thermometer:

- Log cooked/reheated/cooling temperature.
- Surface unsafe storage risk.
- Attach a reading to a container log entry.

Microphone:

- Capture intent.
- Start timers.
- Prepare draft inventory actions.
- Ask location/use-first questions.

Barcode scanner:

- Match packaged goods to Grocy.
- Transfer packaged food into NFC containers.
- Queue packaged product shopping.

Door and ambient sensors:

- Prioritize storage cards.
- Detect stale open-door events.
- Suggest rescue/move workflows.

BLE presence:

- Wake kitchen-relevant cards when the user is nearby.
- Suppress noisy cards when nobody is around.
- Distinguish passive clock from active kitchen mode.

## Wow Features To Consider

These are deliberately ambitious. They should be prototyped only after the
core scan/update/storage flows are safe and boring.

- Fridge command clock: idle clock with a subtle ring showing active timer,
  storage health, and top attention severity.
- Mise radar: a rotating one-screen answer to "what should I do next?"
- Batch split wizard: weigh a cooked batch, scan containers, and watch the
  Dial track remaining portions.
- Use-first carousel: one-card-at-a-time recommendations that combine
  freshness, storage risk, and meal context.
- Rescue mode: when storage goes critical, guide the user through moving the
  highest-risk prepared food first.
- Voice-to-draft: voice creates a draft action, but press confirms it.
- Barcode-to-container handoff: scan package, scan NFC container, weigh, save.
- Cooling coach: probe temperature plus timer helps decide when prepared food
  can be stored.
- Shelf/location tags: scan a fridge shelf tag to choose location instantly.
- Peripheral orchestration: Dial shows "scale stable", "probe ready", "door
  open", and "container scanned" as one composed workflow.
- Ambient kitchen mode: when someone is present, show kitchen-relevant cards;
  otherwise stay a quiet clock.
- One-knob meal prep: rotate through suggested prep tasks and press to start a
  guided batch/container flow.

## Implementation Roadmap

Phase 1: make current flows dependable

- Keep request-scoped scan/create/update.
- Keep stale replies, duplicates, cancel, timeout, and restart safe.
- Extend known-container payload with freshness, provider, location health, and
  last-log summary.
- Ensure idle is clock-first when there are no cards.

Phase 2: add priority cards

- Build a bounded Home Assistant priority payload from existing dashboard,
  storage, shopping, and logbook data.
- Add `show_priority_cards`.
- Let idle yield to the top card only when severity or action justifies it.
- Add swipe up/down for reason/detail.

Phase 3: add fridge workflows

- Add use-first, put-away, storage attention, and shopping confirmations.
- Keep every mutating action two-step unless it is inside an active NFC scan
  save flow.
- Match Dial result language to panel and logbook.

Phase 4: add peripheral contracts

- Define generic peripheral reading events:
  - source;
  - reading type;
  - value;
  - unit;
  - stable/fresh flag;
  - optional tag_id;
  - optional location_id;
  - request_id.
- Start with scale and thermometer because they directly improve inventory
  accuracy and food safety context.
- Add voice only as intent/draft, not final mutation.

Phase 5: add wow prototypes

- Batch split wizard.
- Cooling coach.
- Barcode-to-container handoff.
- Rescue mode.
- Fridge command clock.

## API And Event Sketch

Home Assistant to Dial:

- `show_priority_cards`
- `show_container_summary`
- `show_put_away_flow`
- `show_cook_cards`
- `show_storage_cards`
- `show_shopping_cards`
- `show_timer_cards`
- `show_confirmation_card`
- `show_dial_status`

Dial to Home Assistant:

- `esphome.mise_en_place_assistant_scan`
- `esphome.mise_en_place_assistant_create_container`
- `esphome.mise_en_place_assistant_update_container`
- `esphome.mise_en_place_assistant_card_action`
- `esphome.mise_en_place_assistant_voice_intent`
- `esphome.mise_en_place_assistant_scale_reading`
- `esphome.mise_en_place_assistant_temperature_reading`
- `esphome.mise_en_place_assistant_barcode_scan`
- `esphome.mise_en_place_assistant_timer_action`
- `esphome.mise_en_place_assistant_peripheral_candidate`

Every mutating event should be request-scoped or tied to a Home
Assistant-issued confirmation card.

## Safety Rules

- The Dial holds transient selection state only.
- Home Assistant owns validation, ranking, provider writes, and durable
  inventory mutation.
- No stale, duplicate, canceled, timed-out, or restarted flow may save.
- No empty or protected location may be saved.
- No voice-only inventory mutation.
- No scale-only inventory mutation.
- No thermometer reading should claim food is safe without explicit HA policy.
- Barcode identifies product; NFC identifies container.
- Provider failures must show as failed results.
- The clock is the fallback, not an alert surface.

## Definition Of Done

The M5Dial is the main controller when:

- a user can walk to the fridge and know whether anything needs attention;
- the clock is calm when nothing matters;
- scan/create/update/move/queue workflows can be completed safely on-device;
- scale and thermometer readings can enrich flows without silent mutation;
- storage health and prepared-food risk are visible from the fridge;
- shopping requests show their target and result;
- the panel remains useful for review/configuration but is not required for
  daily physical kitchen work.
