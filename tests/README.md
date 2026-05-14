# MarketDataPlatform Testing Guide

## Purpose

This directory contains the Phase 7 Testing & QA suite for MarketDataPlatform.

The goal of this phase is to validate API behavior, internal execution flow, data contracts, Docker warm-start behavior, and basic end-to-end platform readiness.

---

## Test Structure

```text
tests/
├── unit/
├── integration/
│   └── internal/
└── e2e/
```

---

## Unit Tests

Unit tests validate small, isolated project assumptions.

Current coverage includes:

- pytest sanity check
- required project directory structure

Run:

```bash
pytest tests/unit -v
```

---

## Integration Tests

Integration tests validate API behavior and internal service contracts without requiring full remote deployment.

Covered areas:

- `/metadata` response contract
- `/candles` response contract
- invalid route behavior
- metadata filtering
- metadata no-data behavior
- candle data integrity
- orchestrator semantics
- internal endpoint wiring
- attribution resolver
- policy engine
- consumption state
- data accessor behavior
- policy + consumption integration
- logging / observability contract

Run:

```bash
pytest tests/integration -v
```

---

## E2E Tests

E2E tests validate the platform from the outside, usually through HTTP calls and Docker-based runtime checks.

Covered areas:

- API response contracts
- invalid request contracts
- no-data contracts
- metadata filters
- candle data integrity
- metadata data integrity
- Docker warm-start validation
- health endpoint availability
- remote deployment validation

Run:

```bash
pytest tests/e2e -v
```

---

## Full Test Suite

Run all tests:

```bash
pytest -v
```

Expected current result:

```text
98 passed, 2 skipped
```

---

## Skipped Tests

Some tests are intentionally skipped because they require external or isolated environments.

### Cold Start Validation

Skipped because it requires:

- isolated Docker project execution
- database bootstrap / migration support
- reliable image availability

### Remote Deployment Validation

Skipped unless `PUBLIC_API_BASE_URL` is set.

Example:

```bash
PUBLIC_API_BASE_URL=https://example.com pytest tests/e2e/test_remote_deployment_validation.py -v
```

---

## Important Contracts

### HTTP Status Codes

Business/API-level invalid requests usually return:

```text
HTTP 200
body.type = "error"
```

Unknown FastAPI routes must return:

```text
HTTP 404
```

### Metadata Query Parameters

Current public metadata filter uses:

```text
market
```

not:

```text
market_type
```

### Candle Route Name

Current internal orchestrator route name is:

```text
gat_candle
```

This is a known typo and is tracked for future cleanup.

### Metadata No-Data Behavior

Metadata no-data cases must not return HTTP 500.

Current expected behavior:

```text
HTTP 200
body.type = "error"
body.data = null
```

### Health Endpoint

The health endpoint is intentionally simple and does not pass through the full orchestrator.

Expected response:

```json
{
  "type": "success",
  "message": null,
  "data": {
    "status": "ok"
  }
}
```

### Syncer Service Behavior

The syncer service is treated as a job-style one-shot service.

In warm-start validation, both states are acceptable:

```text
running
```

or:

```text
exited with exit code 0
```

---

## Known Deferred Cleanup Items

The following items are intentionally deferred and tracked separately:

- decide public query parameter naming: `market` vs `market_type`
- fix `gat_candle` typo in orchestrator route naming
- define explicit orchestrator behavior for unknown internal routes
- standardize semantic result typing: `SemanticType` enum vs raw string values
- review inconsistent result models: `DataResault` vs `MetadataResult`
- review typo / inconsistent messages like `not find` and `Interval not find`