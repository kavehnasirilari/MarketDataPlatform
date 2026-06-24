# Market Data Platform

A backend platform for collecting, normalizing, storing, and serving cryptocurrency market data through a unified API.

---

## Overview

Market Data Platform collects market data from multiple cryptocurrency exchanges, converts exchange-specific formats into canonical models, stores them in PostgreSQL, and exposes them through a unified FastAPI interface.

The project is designed as a production-oriented backend system with a strong focus on architecture, maintainability, and extensibility.

---

## Quick Start

### Clone Repository

```bash
git clone https://github.com/kavehnasirilari/MarketDataPlatform.git
cd MarketDataPlatform
```

### Configure Environment

Create a local environment file:
```bash
cp .env.example .env
```

Review and update the values inside `.env` if necessary.

### Start The Platform

```bash
docker compose up -d --build
```

### Verify Services

```bash
docker compose ps
```
Expected services:
- postgres
- migration-service
- api-service
- syncer-service

### Access API

By default the API is available at:

```text
http://localhost:8000
```

### Test API

```bash
curl http://localhost:8000/health
```

```bash
curl http://localhost:8000/metadata
```

```bash
curl http://localhost:8000/candles/hyperliquid/futures/ETH-USDC/1m
```

---

## Architecture

```text
Exchange APIs
      │
      ▼
Syncer Service
      │
      ▼
 PostgreSQL
      │
      ▼
 FastAPI API
      │
      ▼
 API Consumers
```

### Components

**Syncer Service**
- Exchange communication
- Metadata synchronization
- Candle ingestion

**API Service**
- Market data delivery
- Consumer attribution
- Rate limiting

**Database Module**
- SQLAlchemy models
- Session management
- Database configuration
- Alembic migrations

**Shared Core**
- Canonical models
- Exchange adapters
- Shared contracts

---

## Current Status

### Completed

- Multi-exchange adapter architecture
- Metadata synchronization
- Candle ingestion pipeline
- PostgreSQL persistence layer
- FastAPI service
- Dockerized deployment
- VPS deployment
- Integration testing
- End-to-end validation

### Next Development Phase

- Observability
- Redis integration
- Async ingestion pipeline
- API key management
- Historical backfill

---

## License

MIT License