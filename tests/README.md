# Tests

This directory contains the test suite for Phase 7 — Testing & QA.

---

## Structure

- `unit/`  
  Small isolated tests that do not require external services.

- `integration/`  
  Tests that verify interaction between application components, database, API routes, orchestration flow, and service layers.

- `e2e/`  
  End-to-end validation tests that verify the platform can run from a clean environment using Docker Compose.

---

## Phase 7 Goal

The goal of this phase is to verify that the platform can be:

- reproduced on a clean machine
- started successfully
- synchronized successfully
- queried successfully

without hidden setup steps or undocumented manual intervention.

---

## Current Test Coverage

### Unit Tests

- pytest sanity validation
- required project directory structure validation

### Integration Tests

#### Metadata Endpoint

- `/metadata` success response contract
- `/metadata` exchange and market structure validation

#### Candles Endpoint

- `/candles/...` response contract validation
- invalid exchange behavior validation
- unknown symbol behavior validation

#### Routing

- invalid route returns `404`

---

## Current Test Suite Status

Current suite result:

```text
8 passed
```

---

## Requirements

Integration tests currently require:

- PostgreSQL container running
- valid `.env`
- database schema available
- synchronized metadata
- accessible API dependencies

---

## Known Warnings

Current test runs produce deprecation warnings from:

```text
api_service/app/observability/logging_config.py
```

Specifically:

```python
datetime.utcfromtimestamp(...)
```

These warnings are currently accepted because:

- they do not affect runtime behavior
- they do not break the test suite
- previously completed phases are not modified unless necessary

---

## Policy / Rate Limit Note

The policy request limit was temporarily increased to prevent integration tests from being rate-limited by shared `testclient` attribution state during full suite execution.

A cleaner test-policy or policy-state reset mechanism may be added later.

---

## Initial Focus

The first priority of Phase 7 is end-to-end reproducibility based on `TEST_PLAN.md`.

Future expansion will include:

- additional unit tests
- adapter validation tests
- automated API validation
- end-to-end Docker Compose validation
- CI pipeline execution
- test isolation improvements
- policy mocking/reset support