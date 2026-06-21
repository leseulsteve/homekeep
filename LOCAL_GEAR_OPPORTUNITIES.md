# Local Gear And ESPHome Opportunities

## Purpose

This file captures opportunities for Mise en Place Assistant using local-first hardware: ESPHome devices, BLE sensors, kitchen scales, thermometers, buttons, displays, lights, and other physical gear. The goal is not to add gadget noise. The goal is to make the kitchen feel responsive, safe, and a little bit magical while keeping durable inventory state in Home Assistant.

Good hardware additions should answer one of these questions:

- What container or ingredient is physically here?
- How much is in it?
- Is it safe?
- What step should happen next?
- Can the user confirm the action without touching a phone?
- Can Home Assistant react locally even if the cloud is unavailable?

## Design Principles

- Prefer ESPHome, BLE, MQTT, local APIs, and Home Assistant-native entities.
- Keep Home Assistant as the durable state and policy owner.
- Keep devices simple: read sensors, display context, collect confirmation, and report events.
- Avoid blocking loops, cloud-only dependencies, and device-side business logic.
- Every physical action should be idempotent or confirmable: stale sensor readings must not mutate inventory.
- Treat scales and thermometers as evidence until the user or workflow confirms the inventory change.

## Highest-Value Gear

### Kitchen Scale

A connected scale is probably the highest-impact hardware addition after NFC.

Possible value:

- Fill a container by weight instead of typing quantity.
- Remove items by weight when cooking.
- Tare a container, scan NFC, pour ingredient, then save the measured amount.
- Detect refill, portioning, batching, or consumption events.
- Support recipe batch creation: "This sauce batch produced 1,240 g across 4 containers."

ESPHome/local shape:

- ESP32 + HX711 load-cell amplifier + load cells.
- Expose weight sensor, tare button/service, stable-reading binary sensor, and calibration controls.
- Home Assistant service flow owns the inventory write after scan + stable weight + user confirmation.

Wow feature:

- Put a container on the scale, scan its NFC tag, and the panel/M5Dial says: "Tare? Fill? Remove?" Then Mise records the measured delta automatically after confirmation.

Safety notes:

- Require stable readings for a short window before proposing a quantity.
- Never auto-save a weight change without context.
- Store raw measured quantity and normalized inventory quantity separately.

Priority: Very high.

### BLE Fridge And Freezer Thermometers

Temperature sensors make the location-health model immediately useful.

Possible value:

- Monitor fridge, freezer, pantry, cellar, or fermentation locations.
- Detect temperature excursions and attach them to affected containers.
- Warn when prepared food is in a risky location.
- Turn "location health" into useful HA automations.

ESPHome/local shape:

- ESPHome Bluetooth proxy or direct BLE parsing.
- Map thermometer entities to Mise locations through existing location metadata.
- Use existing `location_health` style checks rather than inventing new storage logic.

Wow feature:

- If a freezer warms above threshold, Mise can show exactly which prepared meals or containers are at risk and offer a "move/inspect/discard" workflow.

Safety notes:

- Missing sensor should degrade to unknown, not unsafe mutation.
- Use thresholds and duration windows to avoid false alarms.

Priority: Very high.

### Probe Or Meat Thermometer

A connected probe can bridge cooking and prep inventory.

Possible value:

- Track cook temperature for batch prep.
- Record food-safety evidence in the logbook.
- Trigger "ready to portion" when target temperature is reached.
- Help with cooling workflows: cooked food should move from hot to safe storage quickly.

ESPHome/local shape:

- ESPHome temperature probe using supported sensors, or BLE thermometer through HA.
- Expose current temperature, target state, and maybe a cooking session entity.
- Use Home Assistant automations to trigger Mise prompts.

Wow feature:

- When a batch reaches temperature, the kitchen display prompts: "Chicken stock ready. Place container on scale to portion."

Safety notes:

- Mise should not certify food safety. It can record readings and prompt workflows.
- Avoid medical/food-safety claims; keep messages practical and conservative.

Priority: High.

### Door Sensors

Door sensors are simple but make storage health feel alive.

Possible value:

- Detect fridge/freezer door left open.
- Correlate temperature rise with door activity.
- Improve alerts: "freezer door open, stock at risk" is more useful than "temperature high."

ESPHome/local shape:

- Zigbee, BLE, ESPHome reed switch, or existing HA binary sensor.
- Map entity ID to Mise location metadata.

Wow feature:

- If the fridge door stays open while an M5Dial prep flow is active, show a local reminder instead of just a phone notification.

Priority: High.

### M5Dial / Touch Display / E-Paper Label Station

The M5Dial is already in the project; expanding its role could make the integration feel like a real appliance.

Possible value:

- Fast scan/create/update without phone.
- Show container identity, quantity, location, and next action.
- Confirm scale measurements.
- Choose location or content type.
- Print or show temporary prep labels.

ESPHome/local shape:

- Keep device payloads bounded and explicit.
- HA sends catalog/options; device returns chosen action and correlation ID.
- Cancellation, timeout, and restart must always return the device to a known state.

Wow feature:

- Scan a blank container tag, put it on the scale, choose product on M5Dial, pour until target weight, and save.

Priority: High because the project already has this path.

## Strong Supporting Gear

### NFC Tags And Readers

NFC remains the identity backbone.

Possible value:

- Permanent reusable container identity.
- Prep station check-in.
- Location check-in: scan shelf/fridge/freezer tag to move a container.
- Batch workflow identity: scan recipe card, then scan containers.

ESPHome/local shape:

- PN532 or compatible reader through ESPHome where possible.
- Existing HA tag events or custom ESPHome events.

Wow feature:

- Scan a freezer shelf tag, then scan multiple containers to bulk-move them into that location.

Priority: High.

### Barcode Scanner

Barcode scanning complements NFC: barcode identifies product package, NFC identifies reusable container.

Possible value:

- Create products faster.
- Link packaged goods to Grocy/Open Food Facts later.
- Refill a container from a package with less typing.

Local shape:

- USB HID scanner connected to kiosk/tablet/HA companion device.
- Camera barcode scan from phone or browser later.
- Optional future Open Food Facts lookup.

Wow feature:

- Scan product barcode, scan container tag, place container on scale, pour, save.

Priority: Medium-high.

### Presence Or Motion Sensors

Useful for making the prep station wake up when someone is working.

Possible value:

- Wake display when someone approaches.
- Start prep-station mode.
- Keep dashboards local and glanceable.
- Avoid always-on screens.

ESPHome/local shape:

- PIR or mmWave sensor feeding HA.
- Automations switch the panel/device into active mode.

Wow feature:

- The prep station wakes to the current recipe/prep queue when someone walks up.

Priority: Medium.

### LED Status Indicators

Small lights can make state visible without opening a dashboard.

Possible value:

- Location warning light: freezer attention, fridge door open, prep complete.
- Scale state: waiting, stable, saving, error.
- M5Dial or station status.

ESPHome/local shape:

- ESPHome RGB LED, WLED, or addressable strip.
- HA owns the state mapping.

Wow feature:

- The scale glows green when weight is stable and red when the selected container/product is unsafe or unknown.

Priority: Medium.

### Label Printer

Labels are a natural bridge between digital inventory and physical containers.

Possible value:

- Print prep labels with name, quantity, date, location, QR/NFC tag ID, best-before/opened date.
- Print freezer labels after recipe-container creation.
- Print shelf labels with location IDs.

Local shape:

- Network label printer if available.
- Home Assistant shell/REST bridge later, or external print service.
- Start with label payload generation before direct printer support.

Wow feature:

- Create a recipe batch, portion it across containers, then print labels with exact weight and date for each one.

Priority: Medium.

## Advanced / Experimental Gear

### Camera At Prep Station

Camera can help with barcode scanning, label OCR, or visual audit.

Possible value:

- Scan product barcode.
- Capture container photo.
- Compare shelf/fridge state over time.
- Attach images to logbook entries.

Local shape:

- ESP32-CAM for simple snapshots, local IP camera, or tablet camera.
- Keep image processing optional and local where possible.

Risk:

- Privacy and reliability concerns.
- Computer vision can become a distraction.

Priority: Low until scale/NFC/temperature workflows are strong.

### Smart Plugs And Appliance Power Monitoring

Useful for dehydrators, rice cookers, freezers, fermentation chambers, and sous-vide setups.

Possible value:

- Detect appliance running state.
- Confirm freezer/fridge power availability.
- Track batch cooking sessions.
- Warn if an expected appliance is off.

ESPHome/local shape:

- Existing HA plug/switch/sensor entities mapped into location metadata.
- Power threshold rules in location health or prep session logic.

Wow feature:

- Mise knows the dehydrator is still running and delays "store batch" prompts until power drops.

Priority: Medium.

### Fermentation / Proofing Sensors

Useful for dough, kombucha, yogurt, curing, or fermentation projects.

Possible value:

- Track ambient temperature and humidity.
- Log fermentation start/end.
- Prompt next action.
- Link prepared container state to a time/temperature process.

ESPHome/local shape:

- Temperature/humidity sensor, timer, optional display.
- HA automation triggers Mise logbook/session updates.

Wow feature:

- A sourdough container can have a live "proofing" state and prompt when the window is likely right.

Priority: Low-medium, depending on cooking habits.

## Workflow Concepts

### Scan, Weigh, Save

1. Scan NFC container.
2. Place container on scale.
3. Tare or read current weight.
4. Add/remove ingredient.
5. Wait for stable weight.
6. Confirm on M5Dial/panel.
7. Mise updates inventory and logs the evidence.

### Package To Container

1. Scan package barcode.
2. Resolve product from Grocy/Mealie/Open Food Facts later.
3. Scan reusable container NFC tag.
4. Weigh transfer.
5. Save product identity, quantity, unit, location, and date.

### Cook, Portion, Store

1. Probe thermometer reaches target.
2. Mise prompts "ready to portion."
3. User places each container on scale and scans NFC.
4. Mise records portions/weight per container.
5. User selects fridge/freezer/pantry location.
6. Optional label print.

### Storage Risk Response

1. BLE thermometer detects fridge/freezer excursion.
2. Door/power sensors add context.
3. Mise marks location health degraded.
4. Panel lists affected containers.
5. User can move, inspect, discard, or log recovery.

### Prep Station Mode

1. Motion sensor wakes station.
2. Display shows current prep queue, empty containers, and suggested actions.
3. NFC and scale drive the workflow.
4. LED status confirms stable readings, errors, and successful saves.

## Recommended Implementation Order

1. Build scale support as a measurement source, not an inventory writer.
2. Tighten location-health mapping for BLE temperature, door, and power sensors.
3. Add panel/M5Dial flows that combine NFC identity with scale readings.
4. Add cooking/probe thermometer session prompts.
5. Add barcode-to-container refill workflow.
6. Add label payload generation, then optional printer support.
7. Add LED/display/presence polish for wow factor.
8. Explore cameras and advanced food-process sensors only after the core physical loop is reliable.

## Entity And Service Ideas

Potential Home Assistant surfaces:

- Sensor: prep station scale weight.
- Binary sensor: scale stable.
- Button/service: tare prep scale.
- Event: measured container delta proposed.
- Service: confirm measured container update.
- Sensor: storage temperature health.
- Binary sensor: storage attention needed.
- Event: cooking target reached.
- Service: start prep session.
- Service: finish prep session.
- Service: generate label payload.

The key distinction: sensor readings propose actions; HA services commit actions.

## Wow Factor Features

- A container remembers what it is, and the scale knows how much changed.
- The freezer warning names the actual meals at risk.
- The prep station wakes up when someone approaches.
- A cooked batch reaching temperature triggers a guided portioning flow.
- A label prints with exact weight, date, and storage destination.
- LEDs show whether the kitchen is waiting, measuring, saving, or warning.
- A shelf tag can bulk-move scanned containers to that location.
- The M5Dial becomes a physical kitchen console instead of a novelty controller.

## Guardrails

- No automatic inventory mutation from a single sensor reading.
- Every mutation needs identity, quantity, unit, and freshness validation.
- Stale device responses must be ignored.
- Unknown tags, malformed sensor data, and unavailable devices must fail safely.
- Calibration state belongs to the scale/device, but inventory policy belongs to HA.
- Keep all flows usable without cloud services.
