# Implementation Progress

Codex must update this file at the end of every implementation phase.

Use it as the resume point for future sessions. Do not rely on chat memory.

## Current Status

```yaml
current_phase: 2
current_phase_name: Health and adaptive intervals
last_updated: 2026-06-21
last_codex_summary: >
  Phase 0 scaffold has been restored/applied on top of the Phase 1 core
  models/storage work. Homekeep now has a Home Assistant integration skeleton,
  config flow, manifest, service metadata, empty schema-validated service
  handlers, a Home Assistant storage adapter around the versioned core store,
  and focused scaffold tests. The next incomplete implementation area is
  derived health and adaptive interval behavior.
```

## Phase Checklist

- [x] Phase 0: Scaffold
- [x] Phase 1: Models and storage
- [ ] Phase 2: Health and adaptive intervals
- [ ] Phase 3: Chore Session lifecycle
- [ ] Phase 4: Recommendation Engine V1
- [ ] Phase 5: Home Assistant services and entities
- [ ] Phase 6: Calendar Context
- [ ] Phase 7: Bubble Card MVP
- [ ] Phase 8: Hardening and release readiness

## Phase Log

Add a new entry after each implementation pass.

Template:

```markdown
### YYYY-MM-DD - Phase N: Name

Status: not_started | in_progress | completed | blocked

Implemented:
- ...

Tests/checks run:
- ...

Docs updated:
- ...

Important decisions:
- ...

Known gaps / next prompt:
- ...
```

### 2026-06-21 - Phase 1: Models and storage

Status: completed

Implemented:
- Added `custom_components/homekeep/models.py` with typed dataclasses/enums for
  Chore definitions, Chore Variants, Chore State, and Chore Completions.
- Added validation helpers for finite positive intervals, interval ordering,
  estimated durations, health weights, allowed Chore Variant keys, Variant
  credit bounds, adaptive interval clamping, bounded dismissal/snooze event
  timestamps, and MVP participant attribution.
- Added `custom_components/homekeep/storage.py` with canonical empty storage,
  current storage version `2`, a v1-to-v2 migration hook, unsupported future
  version rejection, validation on load, JSON-safe dump helpers, and sample
  chore loading for tests.
- Added focused `unittest` coverage for invalid intervals, Chore Variant
  validation, participant attribution, v1-to-v2 migration behavior, future
  version rejection, sample chore loading, and storage round trip.

Tests/checks run:
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`

Docs updated:
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Kept Phase 1 pure Python because the requested deliverables do not require
  Home Assistant APIs. No Home Assistant API behavior was assumed.
- Used a tiny fixture-specific YAML parser for `examples/sample_chores.yaml`
  because PyYAML is not installed in the current environment.
- Treated Steve's Phase 1 request as an explicit override of the resume rule
  that would otherwise start with incomplete Phase 0 scaffold work.

Known gaps / next prompt:
- Phase 0 Home Assistant scaffold remains incomplete: no manifest, config
  flow, service registration, or Home Assistant storage wrapper exists yet.
- Health, completion credit application, adaptive interval training, and
  Home/Area Health derivation remain for the next bounded implementation pass.
- Pytest and PyYAML are not installed in this environment; current tests use
  standard-library `unittest`.

### 2026-06-21 - Phase 0: Scaffold

Status: completed

Implemented:
- Added the Home Assistant custom integration scaffold:
  `manifest.json`, `config_flow.py`, `services.yaml`, and `strings.json`.
- Expanded `const.py` with Homekeep domain metadata, platform list, service
  names, service attributes, and allowed enum values used by service schemas.
- Implemented `async_setup`, `async_setup_entry`, and `async_unload_entry` in
  `__init__.py` with empty Phase 0 handlers and schema-validated service
  registration.
- Registered data-producing services with `SupportsResponse.ONLY` and mutation
  or refresh services with `SupportsResponse.OPTIONAL`; no recommendation or
  session logic was implemented.
- Added `HomekeepStorage`, a Home Assistant storage adapter around the existing
  versioned core store, so load paths migrate, validate, repair, and save the
  canonical storage shape.
- Added `tests/test_homekeep_scaffold.py` for manifest, config flow, response
  support wiring, service metadata, and HA storage adapter checks.

Tests/checks run:
- `python3 -m unittest discover -s tests -v`
- `PYTHONPYCACHEPREFIX=/private/tmp/homekeep-pycache python3 -m compileall -q custom_components tests`

Docs updated:
- `docs/IMPLEMENTATION_PROGRESS.md`

Important decisions:
- Home Assistant and Voluptuous are not installed in this local environment, so
  Home Assistant APIs were verified against official Home Assistant developer
  docs instead of installed package source.
- Kept Home Assistant imports lazy in `__init__.py` and `storage.py` so the
  pure core tests remain runnable without a local Home Assistant install.
- Used the backed-up GitHub Phase 0 scaffold as historical reference only; the
  implementation was adapted to the current Homekeep service names and storage
  version `2`.

Known gaps / next prompt:
- The scaffold services intentionally return no-op scaffold responses and do
  not generate recommendations, create sessions, or mutate chore state.
- Full Home Assistant integration tests were not run because Home Assistant,
  Voluptuous, and pytest are not installed locally.
- Next recommended prompt: Implement Phase 2 health/adaptive interval helpers:
  completion credit application, adaptive interval training, derived Staleness,
  Home Health, Area Health, and focused tests.

## Resume Instructions

When resuming implementation:

1. Read `AGENTS.md`.
2. Read this file.
3. Read the docs for the next incomplete phase.
4. Check `git status --short`.
5. Continue from the first unchecked phase unless Steve asks otherwise.
