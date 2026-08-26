---
applyTo: /tests/**
---

# Test Standards

Scoped to any code under `/tests`.

## Framework
- pytest only. Never `unittest`.
- Test file naming: `test_<module_name>.py`, mirroring the module under
  test.

## Coverage Expectations
- Every public method on `FairPennyOrder` needs at least one happy-path test.
- Every documented bug fix (see `AGENTS.md` → "Known issues") needs a test
  that reproduces the original bug and asserts the fixed behavior.
- Status transitions: test every entry in `STATUS_TRANSITIONS` as a valid
  case, and at least three invalid transitions (e.g. `completed` →
  `pending`, `cancelled` → `preparing`, skipping a step like `pending` →
  `ready`).
- Discounts: test 0%, 100%, a normal mid-range value, and both
  out-of-range directions (negative, > 100).
- Aggregation functions (`get_fair_penny_order_stats`): test empty input,
  normal input, and mixed-type input (e.g. one order with an integer
  quantity, another with a string quantity).

## Style
- One logical behavior per test. If a test name needs "and" to describe
  it, split it into two tests.
- Use `pytest.raises` for exception testing — don't catch-and-assert
  manually.
- Prefer fixtures for constructing a baseline `FairPennyOrder` over repeating
  setup code in every test.
