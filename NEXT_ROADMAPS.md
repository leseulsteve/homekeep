# Mise en Place Assistant Roadmap

## Direction

Mise en Place Assistant should consolidate, not expand into another project.
The integration already has enough moving parts: provider data, local
containers, Home Assistant entities and services, panel views, logbook history,
and M5Dial workflows. The next roadmap should make those pieces easier to
trust, easier to understand, and more useful in daily kitchen use.

Provider ownership stays fixed:

- Mealie owns recipes, foods, and meal-planning context.
- Grocy owns durable stock, products, quantity units, storage locations,
  expiry, and minimum-stock policy.
- KitchenOwl owns household shopping-list execution.
- Home Assistant owns automations, entities, devices, and environmental
  signals.
- Mise owns physical containers, NFC/M5Dial workflows, local prep state,
  Home Assistant location health, logbook history, and the next useful kitchen
  action.

The rule for this phase: no new product surface unless it simplifies an
existing workflow. Prefer enrichment, clearer contracts, better feedback, and
removal of duplicate concepts.

## What Is Already In Place

The current system has the main platform pieces:

- Dashboard readiness, suggested actions, provider status, and storage
  attention.
- Inventory rows that connect Grocy stock, Mise containers, locations, dates,
  and recent stock writes.
- Planning views for Mealie recipe containers, prepared components, recipe
  classifications, and Grocy comparison.
- Shopping actions for empty containers, explicit products, and Grocy minimum
  stock with provider-specific notes.
- Storage health metadata and a storage-attention sensor for automations.
- Request-scoped M5Dial scan/create/update flows with provider-aware results.

Future work should mostly refine these pieces, reduce duplicated decisions, and
make the user experience feel coherent across panel, services, sensors, and the
Dial.

## Priority 1: Consolidate The Daily Workflow

The panel should tell one story: what exists, what needs attention, and what the
next useful action is. Avoid adding tabs, dashboards, or parallel views.

- Re-audit Dashboard, Inventory, Planning, Storage, and Dev for duplicate
  information, repeated labels, and conflicting action language.
- Keep each tab's job narrow:
  - Dashboard: what needs attention now.
  - Inventory: what physically exists.
  - Storage: where things are and whether conditions look safe.
  - Planning: what is prepared and what meals or components it supports.
  - Dev: diagnostics and provider testing only.
- Move repeated display logic into shared helpers when it reduces real
  duplication in panel payloads or frontend rendering.
- Make dashboard suggestions link directly to the existing review surface or
  service action that resolves the issue.
- Remove stale roadmap-era language from the UI when the workflow has become
  self-explanatory.

Definition of done:

- No new tab or standalone workflow is introduced.
- Important kitchen actions are reachable from the current panel structure.
- Panel smoke coverage still checks dashboard, inventory, planning, storage,
  and shopping language.

## Priority 2: Enrich Existing Recommendations

Recommendations should become more useful without becoming mysterious. They
must remain explainable summaries of data Mise already has.

- Improve ordering so safety, freshness, stale physical inventory, and failed
  provider writes appear before nice-to-have shopping prompts.
- Strengthen every "because" line with the specific container, location,
  provider, date, or logbook entry that caused the recommendation.
- Make source chips consistent across recommendation, inventory, planning, and
  storage rows.
- Add freshness context for opened, best-before, purchased, stale, and missing
  location cases using existing fields only.
- Add a way to define low-content thresholds per container, so the panel can
  stop treating every container as low at the same hard-coded quantity.
- Keep action recommendations backed by existing Home Assistant services; keep
  judgment recommendations pointed at existing review views.
- Keep payloads small enough to audit from the panel overview JSON.

Definition of done:

- Every suggestion has a short reason and a visible source.
- Suggestions never mutate inventory without an explicit user or service
  action.
- Enrichment uses existing provider reads and local data; no new provider
  project starts here.

## Priority 3: Tighten Provider Boundaries

The strongest product decision is knowing which system owns each fact. This
phase should make those boundaries obvious in code, UI, tests, and docs.

- Review service schemas, store methods, panel payloads, and M5Dial events for
  field-name and type drift.
- Make provider-owned values visibly provider-owned in the UI instead of
  copying them into Mise-owned concepts.
- Keep Grocy quantities, units, storage locations, and minimum stock policy out
  of new Mise data models.
- Keep Mealie recipe and meal semantics as references, not duplicated local
  recipe data.
- Keep KitchenOwl as a shopping execution target, not a second inventory or
  planning source.
- Add focused contract tests when a boundary is clarified or a malformed input
  path is found.

Definition of done:

- A future contributor can tell where each field comes from and where it should
  be changed.
- Malformed provider, service, or Dial payloads fail clearly without crashing
  handlers.
- No durable provider data is silently forked into Mise state.

## Priority 4: Polish Physical UX

The M5Dial should remain the fast physical workflow surface. It should not grow
into a tiny version of the whole panel.

- Review the scan, known-container, create-container, update-quantity,
  choose-location, save, cancel, timeout, and provider-failure paths as one
  end-to-end contract.
- Keep each Dial screen focused on one decision.
- Ensure stale Home Assistant replies, canceled flows, timeouts, and restarts
  leave the Dial and inventory in a known safe state.
- Make result copy match the panel and logbook language for the same outcome.
- Keep durable decisions in Home Assistant; the Dial should only hold transient
  selection state.

Definition of done:

- ESPHome YAML validates after any Dial change.
- No blocking loops or device-side durable inventory assumptions are added.
- Physical behavior is checked with the existing real-device checklist when the
  workflow changes.

## Priority 5: Improve Feedback And Recovery

The user should always know what happened, what did not happen, and where to
look next.

- Make provider failures visible without turning the dashboard into an error
  wall.
- Give shopping actions consistent "queued where" and "last queued" feedback.
- Make storage attention explain whether the issue is environmental,
  missing-location, stale-date, or empty-container related.
- Keep logbook entries consistent: action, message, provider, target IDs,
  reason, and item count where relevant.
- Review service errors for clear Home Assistant messages instead of generic
  tracebacks.

Definition of done:

- A failed provider write does not mutate local inventory.
- The panel, sensor attributes, and logbook describe the same event in
  compatible terms.
- Important failures are actionable without requiring source-code inspection.

## Priority 6: Documentation For The Existing System

Documentation should help Steve and future contributors avoid rebuilding
concepts the integration already has.

- Add or refresh a concise "What Mise owns" section.
- Document the provider boundary in practical terms: Mealie recipes, Grocy
  stock, KitchenOwl shopping, Home Assistant automation, Mise physical prep.
- Document the M5Dial request-scoped event contract at the level needed to
  safely change it later.
- Add screenshots or short descriptions only for stable panel workflows.
- Keep release notes implementation-oriented and honest about provider impact.

Definition of done:

- A new reader can understand the integration without reading the source.
- A contributor can avoid adding duplicate provider models.
- Local planning docs remain local unless intentionally promoted.

## Not Now

These may be useful later, but they are explicitly outside this roadmap unless
an existing workflow cannot be completed without them:

- New provider integrations.
- A second meal-planning product surface.
- A general recipe parser or scoring engine.
- KitchenOwl read-side synchronization.
- Deeper Mealie meal-plan reads beyond enriching the existing Planning view.
- Grocy stock-entry detail unless current totals and date fields cannot answer
  the freshness question.
- New Home Assistant entities that duplicate existing panel or sensor
  attributes.

## Priority Order

1. Consolidate the daily workflow.
2. Enrich existing recommendations.
3. Tighten provider boundaries.
4. Polish physical UX.
5. Improve feedback and recovery.
6. Document the existing system.

North star: Mealie knows what the household wants to cook. Grocy knows what
stock exists. KitchenOwl knows what to buy. Home Assistant knows what the home
is sensing. Mise knows what is physically prepped, where it is, whether it is
safe, and what the next useful action should be.
