# Redis Infrastructure

## Purpose

Redis is added as an infrastructure dependency to support:

- Metadata caching
- Request rate limit state
- Distributed sync locks

Redis is not the source of truth. PostgreSQL remains the source of truth for persistent market data and metadata.

---

## Redis Responsibilities

Redis is responsible for:

- Temporary cached metadata responses
- Short-lived rate limit counters
- Short-lived sync locks

Redis is not responsible for:

- Permanent candle storage
- Permanent metadata storage
- Audit logs
- Business-critical historical state

---

## Failure Philosophy

If Redis is unavailable:

- Metadata endpoints should fall back to PostgreSQL when possible
- Rate limiting may fail closed or fail open depending on policy
- Sync locks should fail safely to avoid duplicate dangerous work

---

## Key Naming

```text
metadata:exchanges
metadata:intervals
metadata:supported_markets
metadata:canonical_symbols

rate_limit:ip:{ip_address}
rate_limit:api_key:{api_key_id}

lock:syncer:candles:{exchange}:{symbol}:{interval}