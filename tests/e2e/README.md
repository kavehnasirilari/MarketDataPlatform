# E2E Validation

This directory contains end-to-end validation assets for Phase 7 — Testing & QA.

---

## Goal

Verify that the platform can be:

- reproduced from a clean environment
- started successfully
- synchronized successfully
- queried successfully

without hidden setup steps or undocumented manual intervention.

---

## E2E Scenario

### 1. Environment Bootstrap

Clone the repository.

Create the `.env` file from `.env.example`.

Run:

```bash
docker compose up --build
```

---

### 2. Infrastructure Validation

Verify the following:

- PostgreSQL container is running
- PostgreSQL container healthcheck passes
- API service starts successfully
- Syncer service starts successfully
- Syncer service can connect to PostgreSQL
- API service can connect to PostgreSQL

---

### 3. Functional Validation

Run metadata synchronization.

Then verify:

### Metadata Endpoint

```http
GET /metadata
```

Expected:

- HTTP 200
- valid JSON response
- non-empty exchange metadata

---

### Candles Endpoint

Example:

```http
GET /candles/binance/futures/BTC-USDT/1m
```

Expected:

- HTTP 200
- valid JSON response
- correct response contract

---

## Pass Criteria

The E2E validation is considered successful if:

- all containers start successfully
- PostgreSQL schema exists
- metadata synchronization completes successfully
- API endpoints return valid JSON responses
- no undocumented manual setup is required
- the platform can be reproduced on a clean machine

---

## Future Expansion

Future E2E validation may include:

- automated startup validation scripts
- Docker health verification scripts
- smoke-test automation
- CI pipeline execution
- container restart validation
- cold-start reproducibility checks
- database migration validation
- clean-environment validation