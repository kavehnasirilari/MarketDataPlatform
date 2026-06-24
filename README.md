# Market Data Platform

**A production-oriented backend platform for collecting, normalizing, storing, and serving cryptocurrency market data from multiple exchanges through a unified API.**

---

## Overview

Market Data Platform is a Python-based backend system designed to solve a common problem in cryptocurrency infrastructure: every exchange exposes market data differently.

Symbols, intervals, endpoints, response formats, and market structures vary between exchanges, making it difficult to build reliable multi-exchange applications.

This platform provides a unified market data layer by:

* Collecting data from multiple exchanges
* Converting exchange-specific formats into canonical models
* Validating and storing market data
* Exposing a consistent API to consumers
* Providing a foundation for trading systems, research tools, and analytics platforms

The project was built with a strong focus on backend architecture, maintainability, extensibility, and operational reliability.

---

## Key Features

### Multi-Exchange Support

Currently integrated exchanges include:

* Binance Futures
* Hyperliquid Futures
* Additional exchanges can be added through the adapter system

### Canonical Data Model

Exchange-specific formats are normalized into a consistent internal representation:

* Canonical Symbols
* Canonical Intervals
* Unified Candle Model

This allows consumers to work with a single data structure regardless of data source.

### Metadata Synchronization

A dedicated Syncer Service is responsible for:

* Exchange discovery
* Symbol synchronization
* Market synchronization
* Interval synchronization

### Historical Candle Storage

Market data is persisted in PostgreSQL with:

* Data validation
* Duplicate protection
* Timestamp consistency checks
* Exchange-specific normalization

### Unified API

The platform exposes market data through FastAPI endpoints including:

```http
GET /metadata
GET /candles/{exchange}/{market}/{symbol}/{interval}
GET /health
```

### Consumer Attribution & Rate Limiting

The API tracks consumer usage through:

* IP attribution
* Consumer identification
* Usage accounting
* Rate limiting policies

This provides a foundation for future API key management and usage-based access control.

---

## Architecture

```text
+------------------+
| Exchange APIs    |
+--------+---------+
         |
         v
+------------------+
| Syncer Service   |
+--------+---------+
         |
         v
+------------------+
| PostgreSQL       |
+--------+---------+
         |
         v
+------------------+
| FastAPI Service  |
+--------+---------+
         |
         v
+------------------+
| API Consumers    |
+------------------+
```

### Services

#### Syncer Service

Responsible for:

* Exchange communication
* Metadata synchronization
* Market data ingestion
* Data validation

#### API Service

Responsible for:

* Serving market data
* Request validation
* Attribution
* Rate limiting
* API responses

#### Shared Core Module

Contains:

* Canonical models
* Exchange adapters
* Mappings
* Shared contracts
* Domain logic

---

## Engineering Challenges Solved

### Data Integrity

The platform performs multiple validation steps before persisting data:

* Open candles are excluded
* Duplicate candles are detected
* Timestamp continuity is validated
* Exchange anomalies are filtered
* Invalid records are rejected

### Extensible Exchange Integration

The adapter architecture allows new exchanges to be added without changing consumer-facing APIs.

Consumers interact with a unified contract while exchange-specific complexity remains isolated inside adapters.

### API Protection

The platform includes:

* Consumer attribution
* Usage tracking
* Rate limiting
* Request accounting

allowing abusive consumers to be identified and restricted independently.

### Clean Separation of Concerns

The project separates responsibilities between:

* Data ingestion
* Storage
* Business logic
* API delivery

making the system easier to maintain and extend.

---

## Technology Stack

### Backend

* Python 3.12
* FastAPI
* SQLAlchemy 2.x
* Pydantic

### Database

* PostgreSQL 16
* Alembic

### Infrastructure

* Docker
* Docker Compose

### Testing

* Pytest
* Integration Testing
* End-to-End Testing

---

## Current Status

### Functional MVP Completed

Implemented:

* Multi-exchange adapter architecture
* Metadata synchronization
* Candle ingestion pipeline
* Canonical market data models
* PostgreSQL persistence layer
* FastAPI service
* Dockerized deployment
* Consumer attribution
* Rate limiting foundation
* Integration tests
* End-to-end validation tests

### In Progress

* Production hardening
* Async ingestion pipeline
* Background workers
* Caching layer
* Monitoring and observability

---

## Design Goals

The project prioritizes:

* Simplicity
* Reliability
* Extensibility
* Clear architecture
* Production-oriented design

rather than maximizing features in early versions.

---

## Future Improvements

Planned future work includes:

* Redis caching layer
* Async ingestion workers
* WebSocket streaming
* Monitoring and alerting
* Advanced rate limiting
* API key management
* Historical backfill services
* Multi-region deployment support

---

## Project Goal

Beyond solving a real technical problem, this project serves as an exploration of backend engineering practices including:

* Service-oriented architecture
* Data modeling
* API design
* Exchange integrations
* Data quality validation
* Operational reliability

The goal is to build a maintainable system that can evolve from a learning project into a production-grade market data platform.
