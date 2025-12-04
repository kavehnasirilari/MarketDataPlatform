# Market Data Platform - Multi-exchange candle & Metadata Service

## 🧭 Overview

The **Market Data Platform** is a modular backend system designed to provide a
**unified market-data layer** across multiple cryptocurrency exchanges.

Its purpose is to take fragmented, exchange-specific market data and transform
it into a **clean, consistent, canonical format** that any application or trading
system can rely on.

The platform exposes this standardized data through a **secure, high-performance
HTTP API**, making it suitable for:

- automated trading systems  
- research pipelines  
- market-data dashboards  
- multi-exchange analytics tools  

### 🎯 Why This Project Exists

Current exchange APIs are inconsistent — symbols differ, intervals differ, and
each exchange structures data in its own proprietary format.  
This platform provides a **single source of truth** by offering:

- a unified **Canonical Candle Model**  
- centralized metadata for symbols & intervals  
- pluggable **exchange adapters**  
- Dockerized microservices for clean scalability  

This makes the system both a solid **production-ready component** and a strong
**portfolio asset** demonstrating backend architecture, API design, and
multi-service orchestration.

### 🔧 What the Platform Aims to Deliver (v1)

- Multi-exchange candle ingestion (Binance Futures, Hyperliquid, Coinbase)  
- A reusable **Core Layer** containing canonical models & adapters  
- A **Syncer Service** for keeping exchange metadata up-to-date  
- A public-facing **FastAPI service** with JWT authentication  
- A structured PostgreSQL schema for symbols, intervals, and future extensions  
- Fully isolated development & deployment using **Docker Compose**  

---

## 🚫 Non-Goals (v1)

The first version of the platform focuses on building a clean, minimal, and stable foundation.  
To keep the scope controlled, the following items are **explicitly out of scope** for v1:

- **Real-time streaming (WebSocket feeds)**  
  No live tick or candle streaming will be implemented in the initial release.

- **Gap-filling or interval reconstruction**  
  The platform will not generate synthetic candles or rebuild missing intervals.

- **Aggregated intervals (e.g., building 15m from 1m)**  
  All intervals in v1 must come directly from the exchange APIs.

- **Multi-exchange price merging or synthetic “global price”**  
  Each exchange is treated independently; no consolidation layer is planned for v1.

- **Historical backfill beyond basic metadata sync**  
  The syncer focuses only on symbols and intervals in v1, not full historical candle ingestion.

- **Advanced monitoring / alerting stack**  
  Tools like Prometheus, Grafana, or centralized logging will be added only in later versions.

- **High-availability or distributed deployment**  
  v1 runs as a simple Docker Compose environment, not a production cluster.

These constraints help maintain a lean, manageable foundation while enabling clean expansion in future phases.

---

## 🛠️ Tech Stack

The platform is built using a clean, modular backend architecture.  
The following technologies form the foundation of the system:

### **Core Technologies**
- **Python 3.12** — primary language for all services  
- **FastAPI** — high-performance HTTP API for serving market data  
- **SQLAlchemy 2.x** — ORM layer for database interaction  
- **PostgreSQL 16** — main storage for symbols, intervals, and future candle data  

### **Service Architecture**
- **Docker + Docker Compose** — isolated, reproducible multi-service environment  
- **Modular Microservices**  
  - `api-service` (public-facing API)  
  - `syncer-service` (exchange metadata sync)  
  - shared `core` module for models, adapters, and mappings  

### **Authentication**
- **JWT (JSON Web Tokens)** — secure access to API endpoints  

### **Networking & Integrations**
- **HTTPX / Requests** — communication with exchange APIs  
- **pydantic** — data validation and serialization  

### **Development & Tooling**
- **black + isort** — code formatting  
- **pytest** — testing framework  
- **.env-based configuration** — environment-variable-driven setup  

This minimal tech foundation is intentionally simple in v1, yet scalable enough to support upcoming phases such as historical ingestion, caching, and real-time extensions.

---

## 🗺️ Roadmap

The project is being developed in well-defined phases to ensure clarity,
scalability, and clean architectural progression.

### **Phase 0 — Project Bootstrap**
- Repository initialization  
- Folder structure layout  
- Base documentation (README, BLUEPRINT, ROADMAP)

### **Phase 1 — Docker Architecture Design**
- Designing service boundaries  
- Planning Docker Compose structure  
- Defining environment variables

### **Phase 2 — Database Layer (PostgreSQL + ORM)**
- Core schema design  
- SQLAlchemy models  
- Migration setup (Alembic)

### **Phase 3 — Core Layer**
- Canonical Candle & Symbol models  
- Exchange adapters (Binance, Hyperliquid, Coinbase)  
- Mapping & utilities

### **Phase 4 — Syncer Service**
- Metadata synchronization (symbols, intervals)  
- Integration with Core layer and DB

### **Phase 5 — API Service**
- FastAPI implementation  
- JWT-secured endpoints for metadata & candles

### **Phase 6 — Docker Implementation**
- Full multi-service build  
- Local deployment via Docker Compose

### **Phase 7 — Testing & QA**
- Unit tests  
- Adapter tests  
- API tests  
- End-to-end validation

---

These phases will be expanded as the system grows, and the README will evolve
to reflect the project’s real implementation and capabilities.

---

## 📌 Development Progress

A phase-based checklist showing the current state of the project:

- [x] Phase 0 — Project Bootstrap  
- [x] Phase 1 — Docker Architecture Design  
- [ ] Phase 2 — Database Layer (in progress)  
- [ ] Phase 3 — Core Layer  
- [ ] Phase 4 — Syncer Service  
- [ ] Phase 5 — API Service  
- [ ] Phase 6 — Docker Implementation  
- [ ] Phase 7 — Testing & QA 