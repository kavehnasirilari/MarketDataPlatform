# E2E Smoke Checklist

## 1. Clone Repository

```bash
git clone <repo-url>
cd MarketDataPlatform
```

---

## 2. Configure Environment

Create `.env` from `.env.example`.

Verify:

- PostgreSQL credentials
- ports
- service names

---

## 3. Start Platform

```bash
docker compose up --build
```

Expected:

- postgres container becomes healthy
- api-service starts successfully
- syncer-service starts successfully

---

## 4. Verify PostgreSQL

Verify PostgreSQL accepts connections.

Expected:

- schema exists
- no startup crash

---

## 5. Verify API Service

Call:

```http
GET /metadata
```

Expected:

- HTTP 200
- valid JSON response

---

## 6. Verify Candles Endpoint

Call:

```http
GET /candles/binance/futures/BTC-USDT/1m
```

Expected:

- HTTP 200
- valid JSON response

---

## 7. Pass Criteria

The smoke validation passes if:

- all containers start successfully
- database is reachable
- metadata endpoint works
- candles endpoint works
- no undocumented manual setup is required