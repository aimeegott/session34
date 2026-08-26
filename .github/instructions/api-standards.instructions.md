---
applyTo: /api/**
---

# API Standards

Scoped to any code under `/api` — the request/response layer that sits in
front of the order logic (not written yet in this exercise repo, but
anticipated here so participants can see folder-specific instructions in
action).

## Validation
- Validate every field in an incoming request before it reaches
  `FairPennyOrder` or `get_fair_penny_order_stats`. The order-logic layer should
  never have to defend against malformed external input — that's this
  layer's job.
- Reject requests with a clear 4xx error and a message naming the invalid
  field. Never silently coerce a bad value to something "close enough."

## Response Shape
- Every endpoint returns a consistent envelope: `{ "data": ..., "error":
  null }` on success, `{ "data": null, "error": { "code", "message" } }` on
  failure.
- Never leak internal exception messages or stack traces into an API
  response.

## Status Codes
- 400 for malformed input, 404 for an order ID that doesn't exist, 409 for
  an invalid status transition attempt, 500 only for genuinely unexpected
  failures.

## Testing
- Every endpoint needs a test for: valid input, missing required field,
  wrong type, and (where relevant) an invalid status transition attempt.
