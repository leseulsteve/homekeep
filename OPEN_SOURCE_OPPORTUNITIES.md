# Open Source And Self-Hosted Opportunities

## Purpose

This file identifies other self-hosted or open-source tools that could enrich Mise en Place Assistant later. These are not immediate roadmap commitments. The main roadmap should still prioritize the APIs and Home Assistant services already used by the project.

The best external tools for this integration are the ones that answer a kitchen workflow question without making Mise duplicate another app:

- What product is this?
- What should be cooked or prepped soon?
- What needs to be bought?
- Where is the physical item?
- Is the food safe?
- What evidence or history should be attached to this container or workflow?

## Best-Fit Opportunities

### Open Food Facts

Open Food Facts is a strong candidate for barcode/product enrichment.

Possible value:

- Resolve barcodes scanned by phone, NFC companion flow, or future camera workflow.
- Enrich local products with brand, package size, categories, allergens, ingredients, nutrition, and images.
- Help create a product when Mealie/Grocy does not already know it.
- Improve M5Dial/container creation by allowing "scan package barcode, then bind to container tag."
- Provide a fallback product catalog that is not a grocery-stock owner.

Integration shape:

- Read-only enrichment provider.
- Store only selected Mise-specific metadata locally.
- Prefer Grocy or Mealie identity when already available.
- Use barcode/GTIN as the external identity.

Risk:

- Crowdsourced data quality varies.
- Package quantities and units need careful normalization.
- Should not become the authoritative inventory source.

Priority: High once current Grocy/Mealie catalog workflows are stable.

### Tandoor Recipes

Tandoor overlaps with Mealie, so it should be considered as an alternate recipe provider, not a parallel feature set.

Possible value:

- Support households that use Tandoor instead of Mealie.
- Pull recipes, tags, units, meal plans, and shopping context.
- Reuse the same recipe-container model already built for Mealie.
- Allow prepared batches, freezer meals, sauces, bases, and ready meals to be created from Tandoor recipes.

Integration shape:

- Add a provider interface similar to Mealie's current catalog/recipe path.
- Keep recipe editing, meal planning, cookbooks, and shopping list ownership in Tandoor.
- Map Tandoor recipes into the same internal `recipe_items()` structure.

Risk:

- It duplicates Mealie provider scope if added too early.
- Only worthwhile after the provider abstraction is stable and recipe-container workflows are polished.

Priority: Medium. Good as a second recipe provider after Mealie workflows prove the model.

### Node-RED

Node-RED is a good companion for event-driven kitchen automation, especially for users who already wire Home Assistant automations visually.

Possible value:

- Provide example flows for Mise events: scan, fill, empty, move, unsafe location, shopping queued.
- Let advanced users route Mise events to notifications, dashboards, MQTT, printers, or external APIs.
- Prototype workflows before they become native HA services.

Integration shape:

- Do not add a hard dependency.
- Publish clean events and service examples.
- Document a few recipes: "container emptied -> shopping prompt", "freezer unhealthy -> alert", "scan unknown tag -> create flow."

Risk:

- Complex flows can hide business logic outside the integration.
- Keep the integration itself authoritative for durable inventory changes.

Priority: Medium-high for documentation/examples, low for direct integration.

### Homebox

Homebox is interesting for non-food physical inventory and kitchen equipment.

Possible value:

- Track durable kitchen objects: containers, jars, labels, sensors, M5Dial devices, spare NFC tags, appliances, manuals, warranties.
- Link a Mise location or container type to Homebox item records.
- Use QR labels and Homebox locations for household organization outside food inventory.

Integration shape:

- Optional link-out or reference fields only.
- Avoid syncing consumable food stock into Homebox.
- Use it for durable assets, not pantry quantities.

Risk:

- Homebox is home inventory, not food inventory.
- It could distract from the core prep/container workflow.

Priority: Low-medium. Useful later for asset/documentation management.

## Useful But Later

### Paperless-ngx

Paperless-ngx could support receipts, manuals, appliance documents, and food safety records.

Possible value:

- Attach receipt/document references to Grocy purchases or container batches.
- Archive appliance manuals and warranty documents for storage locations.
- Keep food safety logs or printed prep sheets searchable.

Integration shape:

- Store document links or IDs in Mise logbook/location metadata.
- Do not upload or manage documents directly at first.

Priority: Low. Useful for documentation-heavy households, not core workflow.

### Vikunja

Vikunja could be a general task/project target for chores and kitchen maintenance.

Possible value:

- Create tasks for "clean fridge", "rotate freezer stock", "replace NFC tag", "review expired prep."
- Turn Mise warnings into household tasks rather than one-off notifications.

Integration shape:

- Optional outbound task target.
- Keep shopping in Grocy/KitchenOwl, not Vikunja.

Priority: Low-medium if household task workflows become important.

### Immich

Immich could store photos of containers, labels, prep batches, pantry shelves, or product packages.

Possible value:

- Attach photos to containers or locations.
- Use images for visual audit of pantry/fridge state.
- Store package photos when Open Food Facts lacks a product.

Integration shape:

- Link to uploaded assets only.
- Avoid building image management into Mise.

Priority: Low. Nice for visual workflows, but not required for core inventory correctness.

### Nextcloud Cookbook

Nextcloud Cookbook is another recipe source candidate.

Possible value:

- Support users already using Nextcloud for household data.
- Use recipe JSON/metadata as another recipe provider.

Integration shape:

- Treat like Tandoor: alternate recipe provider only.
- Do not duplicate cookbook UI.

Priority: Low-medium. Consider after Mealie/Tandoor-style provider abstraction is clean.

## Automation Platforms To Treat Carefully

### n8n

n8n can connect many APIs and offers workflow automation, but it should be treated as an external automation companion rather than a core dependency.

Possible value:

- Prototype cross-app workflows.
- Send Mise events to chat, email, calendars, or reporting tools.
- Build user-specific integrations without adding all of them to Mise.

Risk:

- It is not strictly the same kind of open-source dependency as smaller community projects; check license and deployment fit before recommending it as "open source."
- Public webhook exposure and credential handling need care.
- Workflow logic can become invisible to the integration and hard to support.

Priority: Low for native support. Better as docs/examples for advanced users.

## Integration Ideas By Workflow

### Product Identification

Best tools:

- Open Food Facts.
- Grocy.
- Mealie or Tandoor as curated recipe/product context.

Feature idea:

- Scan package barcode, enrich from Open Food Facts, then create or map a Grocy/Mealie product before binding it to an NFC container.

### Prep Planning

Best tools:

- Mealie first.
- Tandoor or Nextcloud Cookbook later.
- Grocy for stock readiness.

Feature idea:

- Show "prep readiness" by comparing upcoming recipes, prepared containers, empty containers, and Grocy stock.

### Shopping

Best tools:

- KitchenOwl.
- Grocy shopping list.
- Tandoor or Mealie shopping context later, only if configured as the user's recipe owner.

Feature idea:

- Add missing prep items to the user's preferred shopping target, with a reason attached to each item.

### Household Operations

Best tools:

- Home Assistant automations.
- Node-RED examples.
- Vikunja tasks.

Feature idea:

- Turn Mise location health problems into actionable tasks or automations: clean, inspect, move food, or replace sensor batteries.

### Evidence And Attachments

Best tools:

- Paperless-ngx.
- Immich.
- Homebox.

Feature idea:

- Attach receipts, product photos, container photos, appliance manuals, or prep logs to Mise locations and logbook entries by external URL/ID.

## Recommended Order

1. Add no new external tools until the current Mealie, Grocy, KitchenOwl, panel, services, and sensor surfaces are fully exploited.
2. Add Open Food Facts first if product/barcode creation becomes the next clear pain point.
3. Add Tandoor or Nextcloud Cookbook only after recipe provider boundaries are clean.
4. Add Node-RED examples before adding any direct automation-platform integration.
5. Add Paperless-ngx, Immich, Homebox, or Vikunja only as optional link-outs or outbound actions.
6. Avoid making any new tool a required dependency.

## Source Links

- Open Food Facts: https://world.openfoodfacts.org/
- Open Food Facts API/docs: https://docs.openfoodfacts.org/
- Tandoor Recipes: https://docs.tandoor.dev/
- Node-RED: https://nodered.org/
- Homebox: https://hay-kot.github.io/homebox/
- Paperless-ngx: https://docs.paperless-ngx.com/
- Vikunja: https://vikunja.io/docs/
- Immich: https://docs.immich.app/
- Nextcloud Cookbook: https://apps.nextcloud.com/apps/cookbook
- n8n: https://docs.n8n.io/
