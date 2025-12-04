# Market Data Platform — Multi-Exchange Candle Service

## 1. Overview

هدف این پروژه ساخت یک **لایهٔ دادهٔ مارکت** برای چند صرافی است که:

- دادهٔ کندل (OHLCV) را از صرافی‌های مختلف می‌گیرد
- آن‌ها را به یک **مدل استاندارد واحد (Canonical Candle Model)** تبدیل می‌کند
- از طریق یک API امن (JWT-based) در اختیار کلاینت‌ها قرار می‌دهد
- ساختار **میکروسرویسی + Docker + Postgres** دارد

این سرویس قرار است:

- هم برای رزومه قابل‌دفاع باشد
- هم بعدها واقعاً در پروژه‌های دیگر استفاده شود (asset بلندمدت)

---

## 2. Goals

- طراحی و پیاده‌سازی یک **canonical data model** برای کندل‌ها و symbolها
- پشتیبانی از **چند صرافی** در فاز اول:  
  - `binance` (futures perp)  
  - `hyperliquid` (perp)  
  - `coinbase` (spot)
- فراهم کردن یک **HTTP API** برای دریافت:
  - کندل‌های تاریخی
  - آخرین کندل
  - متادیتا (symbolها، تایم‌فریم‌ها)
- معماری **microservices** شامل:
  - `api-service` (public-facing API)
  - `syncer-service` (jobهای هماهنگی/آپدیت)
  - `postgres` (ذخیرهٔ دیتا و متادیتا)
- استفاده از:
  - Docker / docker-compose
  - PostgreSQL 16
  - Python + FastAPI + SQLAlchemy

---

## 3. Non-Goals (v1)

در نسخهٔ اول، عمداً **این کارها را انجام نمی‌دهیم**:

- پر کردن گپ‌های کندل (no gap filling)
- aggregate کردن intervalها (مثلاً ساخت 15m از 1m)
- merge کردن دادهٔ چند صرافی برای ساخت قیمت «global»
- سیستم real-time streaming با WebSocket
- سیستم full-blown monitoring (Prometheus, Grafana)
- high-availability / multi-region deployment

Assumption v1:

- صرافی دیتای درست و کامل می‌دهد
- اگر symbol/interval پشتیبانی نشود → خطای واضح می‌دهیم
- اگر timestamp/دیتا مشکل داشته باشد → خطای واضح می‌دهیم

---

## 4. High-Level Architecture

### 4.1 Components

1. **Postgres (market_data DB)**
   - ذخیره:
     - `exchanges`
     - `symbols`
     - `supported_intervals`
     - (در صورت نیاز) cache کندل‌ها
   - پایگاه داده مشترک بین `api` و `syncer`

2. **API Service (`api-service`)**
   - FastAPI
   - JWT authentication
   - Endpoints:
     - `GET /candles/{exchange}/{market_type}/{symbol}/{interval}`
     - `GET /latest/{exchange}/{market_type}/{symbol}/{interval}`
     - `GET /meta/symbols`
     - `GET /meta/intervals`
     - `GET /health`
   - از DB و adapters استفاده می‌کند

3. **Syncer Service (`syncer-service`)**
   - اسکریپت/سرویس پایتونی که:
     - symbolها و intervalهای پشتیبانی‌شده را از صرافی‌ها می‌گیرد
     - آن‌ها را در DB به‌روز می‌کند
   - ممکن است بعداً:
     - pre-fetch کندل‌ها
     - jobهای دوره‌ای دیگر داشته باشد

4. **Exchange Adapters**
   - ماژول‌های پایتونی جدا برای هر صرافی:
     - `BinanceFuturesAdapter`
     - `HyperliquidPerpAdapter`
     - `CoinbaseSpotAdapter`
   - مسئول:
     - تماس با API صرافی
     - map کردن symbol/interval
     - تبدیل خروجی خام به `Candle` استاندارد

---

## 5. Tech Stack

- **Language:** Python 3.12
- **Framework (API):** FastAPI
- **DB:** PostgreSQL 16 (در Docker)
- **ORM:** SQLAlchemy 2.x (+ Alembic در صورت نیاز)
- **Auth:** JWT (PyJWT یا FastAPI JWT)
- **Containerization:** Docker, docker-compose
- **Testing:** pytest
- **Styling/Lint:** black, isort, flake8 (optional but recommended)
- **Git hosting:** GitHub (Repo: `MarketDataPlatform` یا اسم مشابه)

---

## 6. Repository & Directory Structure

ریپو گیت (ریoot):

```txt
MarketDataPlatform/
├── api-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   ├── routers/
│   │   │   ├── candles.py
│   │   │   ├── meta.py
│   │   │   └── health.py
│   │   ├── schemas/
│   │   │   ├── candle.py
│   │   │   └── symbol.py
│   │   ├── auth/
│   │   │   └── jwt.py
│   │   └── db/
│   │       ├── models.py
│   │       └── session.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── syncer-service/
│   ├── syncer/
│   │   ├── main.py
│   │   ├── tasks/
│   │   │   ├── sync_symbols.py
│   │   │   └── sync_intervals.py
│   │   └── db/
│   │       ├── models.py      # می‌تواند shared باشد یا جدا
│   │       └── session.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── core/
│   ├── models/
│   │   ├── candle.py          # Canonical Candle Model
│   │   ├── symbol.py
│   │   └── enums.py
│   ├── adapters/
│   │   ├── base.py            # ExchangeAdapter ABC
│   │   ├── binance.py
│   │   ├── hyperliquid.py
│   │   └── coinbase.py
│   ├── mapping/
│   │   ├── symbol_mapping.py
│   │   └── interval_mapping.py
│   └── utils/
│       ├── time.py
│       └── logging.py
│
├── database/
│   ├── schema.sql             # نسخه اولیه اسکیمای Postgres
│   └── alembic/               # در صورت استفاده از Alembic
│
├── docker-compose.yml
├── .env.example
├── BLUEPRINT.md
└── README.md



Docker Architecture — Final (Phase 1)

Network:

mdp_network (bridge)

Containers:

postgres

api-service

syncer-service

Rules:

همه سرویس‌ها داخل یک شبکه هستند

Postgres healthcheck تعیین‌کننده شروع سرویس‌هاست

env variables از .env تزریق می‌شوند

volume داده پایدار فراهم می‌کند

imageها از python:3.12-slim ساخته می‌شوند

Container Interaction:

api-service → read/write → Postgres

syncer-service → write → Postgres

postgres → provider for both services

Secrets Model:

.env به‌صورت untracked

شامل creds DB + JWT_SECRET

secretهای صرافی در همین فایل اضافه می‌شود