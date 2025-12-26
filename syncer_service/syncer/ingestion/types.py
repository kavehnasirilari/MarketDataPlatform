from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Sequence

# NOTE:
# Candle is the canonical candle object produced by adapters (core layer)
# Do NOT import ORM models here.
from core.models.candle import Candle


# =========================
# Ingestion Unit
# =========================

@dataclass(frozen=True)
class IngestionUnit:
    """
    Represents a single independent ingestion unit:
    (supported market + interval)

    This object is the ONLY input to the ingestion pipeline.
    """
    supported_market_id: int
    exchange_market_id: int
    interval_id: int

    exchange_name: str
    market_type: str

    canonical_symbol: str
    interval: str  # canonical interval string from DB (e.g., "1m", "5m")
    interval_ms: int

    fetch_limit: int = 1000


# =========================
# Fetch Stage
# =========================

@dataclass
class FetchResult:
    candles: List[Candle]
    fetched_count: int
    min_ts: Optional[int]
    max_ts: Optional[int]


# =========================
# Filter Stage
# =========================

@dataclass
class FilterResult:
    new_candles: List[Candle]

    dropped_last_open_candle: bool
    gap_warning: bool

    last_ts: Optional[int]


# =========================
# Persistence Stage
# =========================

@dataclass
class PersistResult:
    inserted: int


# =========================
# Final Summary (Audit)
# =========================

@dataclass
class IngestionSummary:
    # unit identity
    exchange_name: str
    market_type: str
    canonical_symbol: str
    interval: str

    # timestamps
    last_ts_db: Optional[int]
    min_ts_fetched: Optional[int]
    max_ts_fetched: Optional[int]

    # counts
    fetched_count: int
    inserted_count: int

    # flags
    dropped_last_open_candle: bool
    gap_warning: bool
