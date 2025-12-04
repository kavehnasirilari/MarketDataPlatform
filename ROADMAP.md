📄 ROADMAP.md — MarketDataPlatform
Project Roadmap & Phase Plan

(هماهنگ با BLUEPRINT اصلی پروژه )

1. Purpose of This Document

این سند «نقشهٔ راه رسمی» پروژهٔ MarketDataPlatform است.
تمام فازهای توسعه، ترتیب اجرای آن‌ها، خروجی هر فاز و چت‌های توسعه‌ای مرتبط در اینجا تعریف می‌شوند.

هدف این سند این است که پس از اتمام برنامه‌ریزی، روند توسعه سریع، منظم و بدون اتلاف زمان انجام شود.

2. High-Level Structure of the System

پروژه از ۵ ستون اصلی تشکیل شده است:

Database Layer
Postgres + SQLAlchemy + Alembic

Core Layer
Canonical candle model + Exchange adapters + Mapping

Syncer Service
هماهنگ‌سازی symbolها، intervalها و متادیتای صرافی‌ها

API Service
FastAPI + JWT + HTTP Endpoints

DevOps Layer
Docker, docker-compose, env structure

3. Project Phases
🔷 Phase 0 — Bootstrap (Git + Repo Structure + Standards)

Goal: آماده‌سازی زیرساخت نسخه‌سازی پیش از هرگونه توسعه.

Deliverables:

ایجاد repo (MarketDataPlatform)

ساختار کلی فولدرها:

core/
api-service/
syncer-service/
database/
infra/


فایل‌های پایه:

README.md

ROADMAP.md

BLUEPRINT.md

.gitignore

سیاست branching:

main, dev, feature/*

🔷 Phase 1 — Docker Design (Architecture Only)

Goal: طراحی کامل زیرساخت Docker قبل از پیاده‌سازی.

Deliverables:

طراحی ساختار docker-compose.yml

تعیین سرویس‌ها (postgres, api-service, syncer-service)

تعیین شبکه داخلی docker

تعریف .env و .env.example

طراحی اسکلت Dockerfileهای سرویس‌ها
(غیر اجرایی — فقط design)

🔷 Phase 2 — Database Layer (Postgres + ORM + Alembic)

Goal: ساخت لایه دادهٔ پایدار و نسخه‌پذیر.

Deliverables:

مدل‌های SQLAlchemy

Alembic migrations

baseline

initial schema

ساختار پوشه database/

session factory و dependency

جداول:

exchanges

symbols

intervals

🔷 Phase 3 — Core Layer (Shared Logic)

Goal: ساخت هستهٔ منطقی پروژه — مستقل از API و Syncer.

Deliverables:

Canonical models:

Candle

Symbol

Exchange, MarketType, Interval enums

Adapters:

BaseAdapter

BinanceFuturesAdapter

HyperliquidPerpAdapter

CoinbaseSpotAdapter

mapping‌ها:

symbol_mapping.py

interval_mapping.py

utils:

time utilities

logging helper

🔷 Phase 4 — Syncer Service (Exchange Metadata Sync)

Goal: ساخت سرویس هماهنگ‌سازی صرافی‌ها با دیتابیس.

Deliverables:

ساختار syncer-service/

taskها:

sync_symbols.py

sync_intervals.py

ارتباط syncer با Core و Database Layer

یک entrypoint ساده برای اجرای sync

🔷 Phase 5 — API Service (FastAPI + JWT)

Goal: ساخت API استاندارد برای مصرف‌کنندگان داده.

Deliverables:

ساختار api-service/

JWT auth

routers:

/health

/meta/symbols

/meta/intervals

/candles/{...}

/latest/{...}

schemas (Pydantic)

dependency injection

error handling استاندارد

🔷 Phase 6 — Docker Implementation (Build & Run)

Goal: اجرای کامل پروژه در محیط Docker.

Deliverables:

Dockerfileهای api-service و syncer-service

compose نهایی:

build contexts

volumes

networks

اجرای تستی:

docker compose up

API روی پورت 8000 فعال شود

Syncer با DB تعامل کند

🔷 Phase 7 — Testing & QA

Goal: تضمین کیفیت و پایداری پروژه.

Deliverables:

راه‌اندازی pytest

تست واحد Core

تست Adapters

تست API

تست migrationها

تست end-to-end برای جریان کامل (adapter → DB → API)

(Optional) 🔷 Phase 8 — Documentation & Polish

Goal: آماده‌سازی پروژه برای رزومه و ارائهٔ حرفه‌ای.

Deliverables:

README کامل

معماری

روش اجرا

مثال API

اسکرین‌شات‌های OpenAPI UI

نمودار معماری

(اختیاری) GitHub Actions برای lint/test

4. Recommended Chat/Blueprint Order
Chat #1 — Phase 0 + Phase 1 (Bootstrap + Docker Design)
Chat #2 — Phase 2 (Database Layer)
Chat #3 — Phase 3 (Core Layer)
Chat #4 — Phase 4 (Syncer Service)
Chat #5 — Phase 5 (API Service)
Chat #6 — Phase 6 (Docker Implementation)
Chat #7 — Phase 7 (Testing & QA)
Chat #8 — Phase 8 (Documentation)

5. Project Execution Rules

هر فاز قبل از اجرای کد باید بلوپرینت مستقل داشته باشد.

هر چت → فقط یک فاز.

envها هرگز داخل repo ذخیره نمی‌شوند.

تمام سرویس‌ها از یک نسخه Python (3.12) استفاده می‌کنند.

توسعه اولیه در محیط لوکال (venv) و سپس docker انجام می‌شود.

هر مرحله پس از اتمام در این فایل ثبت و به‌روز می‌شود.

6. Final State of the Project

پس از تکمیل تمام فازها:

پروژه کاملاً کانتینری و قابل‌اجرا با یک دستور

API استاندارد، امن، و قابل‌اتکا

DB با مهاجرت‌های نسخه‌بندی‌شده

Core کاملاً reusable

ساختار حرفه‌ای برای رزومه و مصاحبه‌های سطح بالا

مسیر باز برای اضافه‌کردن:

caching

gap-fill

real-time streaming

multi-region deployment

7. End of Document

این سند باید همیشه در ریشهٔ پروژه قرار بگیرد و پس از اتمام هر فاز به‌روزرسانی شود.