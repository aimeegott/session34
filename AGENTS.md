# AGENTS.md

Onboarding notes for any AI tool (Copilot, Claude, Cursor, etc.) opening
this repository for the first time.

## What this repo is
An in-house restaurant order management service. It handles order
creation, line items, discounts, status transitions (pending → confirmed →
preparing → ready → completed, with cancellation possible up to "ready"),
and basic reporting stats across orders.

## Critical context: this is NOT a Fair Penny integration
This codebase was migrated OFF the Fair Penny POS API. The migration was never
finished at the naming level, so you will see `FairPennyOrder`,
`add_fair_penny_item`, `get_fair_penny_order_stats`, `FAIR_PENNY_API_KEY`, and a
`FairPennyWebhookPayload` class throughout the code. **None of this talks to
Fair Penny.** Treat every "Fair Penny"-prefixed name as a leftover naming artifact,
not a signal that this code integrates with Fair Penny's API.

Do not:
- Suggest updating Fair Penny API credentials or rotating `FAIR_PENNY_API_KEY`.
- Suggest fixing "broken" Fair Penny webhook handling — there are no live
  webhooks; `FairPennyWebhookPayload` is unused dead code.
- Assume `_sync_to_fair_penny_terminal` is called anywhere. It isn't.

Do:
- Treat "Fair Penny" naming as legacy cruft to flag or clean up when asked to
  refactor.
- Analyze what the code actually does (reads/writes local Python objects)
  rather than what the names suggest it does.

## Where to look
- `order_service.py` — all order logic lives here for now (not yet split
  into `/api` and `/tests`, which is intentional for this exercise; the
  folder-specific instruction files below anticipate that split).
- `.github/copilot-instructions.md` — project-wide standards.
- `.github/instructions/api-standards.md` — applies once order-facing
  endpoint code lands under `/api`.
- `.github/instructions/test-standards.md` — applies to everything under
  `/tests`.
- `.github/agents/migration-reviewer.agent.md` — a specialist agent for
  catching leftover Fair Penny-migration artifacts.

## Known issues (for humans and agents to fix, not to work around)
- `apply_discount` does not validate that `percent` is between 0 and 100.
- `update_status` does not enforce `STATUS_TRANSITIONS` — it will accept
  any string as a new status, including invalid transitions.
- `get_fair_penny_order_stats` assumes every `item["quantity"]` is numeric; it
  breaks on mixed int/string input from inconsistent callers.
- `add_fair_penny_item` performs no validation on `quantity` (e.g. negative or
  zero) or item availability.
