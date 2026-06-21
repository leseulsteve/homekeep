# Mise en Place Assistant — Agent Guide

Keep this file short, practical, and local-only.

## Working standards

- Prefer small, readable changes with explicit error handling. Avoid duplicate
  logic, dead code, silent failures, and unbounded work or memory use.
- Review changes for correctness, clear failure modes, input validation,
  least-privilege access, and compatibility or performance regressions.
- Use reputable, actively maintained libraries when they cleanly fit; keep
  project code focused on Mise en Place Assistant-specific policy and
  integration boundaries.
- Add or update focused tests when behaviour changes. Before calling a fix
  complete, cover the reported problem with a test or reproducible check.

## Home Assistant and M5Dial safety

For any integration or M5Dial change, review the Home Assistant ↔ ESPHome
contract end to end before committing:

- Event and service/action names, payload field names and types, tag identity,
  state transitions, and cancellation/timeout paths must agree on both sides.
- Treat inventory as durable data: preserve storage migrations and backwards
  compatibility; validate quantities and units, including non-finite values.
- A malformed event or unknown tag must never crash a service handler.
- Keep Home Assistant APIs compatible with the supported core version,
  including config flows, manifests, services, translations, entities, panel
  APIs, and unload/reload behaviour.
- Run focused Python syntax/tests/lint checks as available, and validate
  ESPHome YAML whenever either side changes.
- Keep device behaviour safe: no blocking loops; stale NFC or Home Assistant
  responses must not mutate inventory; BLE/radio controls must reach a known
  state after boot, cancellation, timeout, or restart.

## Secrets and documentation

- Never put secrets or private details in tracked files, logs, commits, tags,
  or releases. This includes Gmail addresses, credentials, tokens, Wi-Fi
  details, API encryption keys, OTA passwords, device identifiers, and private
  endpoints.

## Commits and changelog

- Always provide a commit message.
- When continuing existing changelog or commit-message wording, keep its
  sarcastic tone and mock a specific technical thing—not a person.

## Publishing the integration

When Steve asks to publish, follow this exact order:

1. Complete a full review of the changes to be released.
2. Summarize code changes, user-facing behaviour, and likely Home Assistant /
   Mise en Place Assistant impact.
3. Draft a short, developer-oriented release note for Steve to approve or
   adjust. It should describe implementation and integration impact, not
   marketing or end-user instructions.
4. Commit the release changes and push the commit.
5. Run the publish script; it owns the remaining release workflow.

```bash
python3 scripts/publish_integration.py VERSION "Short release note"
```

Use the most credit-efficient workflow that still meets this review, testing,
and quality bar; avoid redundant analysis and checks.
