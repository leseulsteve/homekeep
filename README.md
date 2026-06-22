# Homekeep

Homekeep is a planned Home Assistant integration for adaptive chores, light
Chore Sessions, Smart Chore Lists, and Home Health.

## Private Test Status

Homekeep is experimental pre-release software for Steve's private testing. It
is not production-ready and should not be connected to private calendar data,
real routines, or household-critical automations until the private live-test
checklist and release-readiness work are complete.

The integration is still missing Home Assistant package-backed integration
tests, live validation of the mocked Homekeep sidebar app, service wiring for
that app, and a release process.

## Private HACS Test Install

Homekeep can be installed through HACS as a custom repository for the private
MVP test.

Requirements:

- the GitHub repository must be public; HACS cannot install private GitHub
  repositories
- HACS must be installed and configured in Home Assistant
- Home Assistant Core `2026.6.0` or newer

Private test install:

1. In Home Assistant, open HACS.
2. Open the custom repositories menu.
3. Add `https://github.com/leseulsteve/homekeep`.
4. Select repository type `Integration`.
5. Download Homekeep.
6. Restart Home Assistant.
7. Add the Homekeep integration from Settings > Devices & services.

For live-test preparation, follow
`docs/live-test/AI_PRIVATE_LIVE_TEST_CHECKLIST.md`.

Start here:

- `PROJECT_BRIEF.md` for the human product brief.
- `AGENTS.md` for Codex instructions.
- `docs/README.md` for the documentation map.
- `docs/implementation/IMPLEMENTATION_PLAN.md` for the build sequence.
- `docs/product/MVP_ACCEPTANCE_CRITERIA.md` for the definition of done.
