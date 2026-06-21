# Homekeep

Homekeep is a planned Home Assistant integration for adaptive chores, light
Chore Sessions, Smart Chore Lists, and Home Health.

## Do Not Use Yet

Homekeep is experimental pre-release software for private testing only. Do not
use it in a production Home Assistant instance, do not rely on it for household
operations, and do not connect it to private calendar data or real routines
until the live-test checklist and release-readiness work are complete.

The integration is still missing Home Assistant package-backed integration
tests, live validation, packaged helper/script examples for the dashboard, and
a public release process. Expect breaking changes, incomplete behavior, and
rough edges.

## Private HACS Test Install

Homekeep can be tested as a HACS custom repository while it is still private
MVP software.

Requirements:

- the GitHub repository must be public; HACS cannot install private GitHub
  repositories
- HACS must be installed and configured in Home Assistant
- Home Assistant Core `2026.6.0` or newer

Install:

1. In Home Assistant, open HACS.
2. Open the custom repositories menu.
3. Add `https://github.com/leseulsteve/homekeep`.
4. Select repository type `Integration`.
5. Download Homekeep.
6. Restart Home Assistant.
7. Add the Homekeep integration from Settings > Devices & services.

For live-test preparation, follow
`docs/PRIVATE_LIVE_TEST_CHECKLIST.md`.

Start here:

- `PROJECT_BRIEF.md` for the human product brief.
- `AGENTS.md` for Codex instructions.
- `docs/IMPLEMENTATION_PLAN.md` for the build sequence.
- `docs/MVP_ACCEPTANCE_CRITERIA.md` for the definition of done.
