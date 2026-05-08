# Test Plan

## Purpose

The purpose of this test plan is to verify that a new developer can:

- clone the repository
- configure the environment
- start the platform using Docker Compose
- synchronize metadata successfully
- query the API endpoints successfully

without requiring hidden setup steps or undocumented manual intervention.

---

## Critical End-to-End Scenario

### Environment Bootstrap

1. Clone repository
2. Create `.env` from `.env.example`
3. Run:

```bash
docker compose up --build
```

---

### Infrastructure Validation

4. Verify PostgreSQL container is healthy
5. Verify API service is running
6. Verify syncer service can connect to PostgreSQL

---

### Functional Validation

7. Run metadata synchronization
8. Call `/metadata` endpoint
9. Call `/candles/...` endpoint

---

## Pass Criteria

The test is considered successful if:

- all containers start successfully
- PostgreSQL schema exists
- metadata synchronization completes successfully
- API endpoints return valid JSON responses
- no undocumented manual setup is required
- the platform can be reproduced on a clean machine

---

## Future Expansion

This test plan will later include:

- unit tests
- integration tests
- adapter validation tests
- automated API tests
- CI pipeline validation


