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
