# Project Instructions — Order Service (Project-Wide)

## Migration context (read this first)
This service was migrated off the Fair Penny POS API. Class, method, and
variable names still say "Fair Penny" everywhere (`FairPennyOrder`,
`add_fair_penny_item`, `get_fair_penny_order_stats`, `FAIR_PENNY_API_KEY`), but no code
in this repository talks to Fair Penny. This is legacy naming, not live
integration. Do not propose fixes that assume a working Fair Penny connection
exists — there isn't one. When refactoring, treat "Fair Penny" naming as
migration debt to be cleaned up.

## Language and Style
- Python 3.10+. Add type hints to any function you touch, even if the
  surrounding code doesn't have them yet.
- Follow PEP 8.

## Documentation
- Every public function and class needs a docstring: what it does, and any
  non-obvious behavior (e.g. what happens on invalid input).

## Testing
- Use pytest.
- Any bug fix must ship with a regression test that fails before the fix
  and passes after it.
- Test the boundary values explicitly, not just the middle of the range.

## Error Handling
- Raise specific exceptions (`ValueError`, `TypeError`) with a message that
  says what was invalid and why — never a bare `Exception`.
- Validate inputs before mutating any order's state (items, discount,
  status).
