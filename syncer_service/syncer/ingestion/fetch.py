from __future__ import annotations

from typing import List

from core.models.candle import Candle
from core.models.enums import MarketType, Interval

from syncer_service.syncer.adapters.registry import ADAPTER_REGISTRY

from .types import IngestionUnit, FetchResult


def build_adapter_for_unit(unit: IngestionUnit):
    """
    Build adapter instance for a single ingestion unit (Phase 4B).

    Rules:
    - Adapter class is resolved via Phase registry
    - Adapter is instantiated per unit
    """
    adapter_cls = ADAPTER_REGISTRY.get(unit.exchange_name)
    if adapter_cls is None:
        raise ValueError(f"No adapter registered for exchange '{unit.exchange_name}'")

    # unit.market_type is a string from DB (e.g. "spot", "futures")
    market_type = MarketType(unit.market_type)

    return adapter_cls(market_type=market_type)


def fetch_candles_for_unit(unit: IngestionUnit) -> FetchResult:
    """
    Fetch latest candles for a single ingestion unit.

    Responsibilities:
    - Call adapter.fetch_candles (BaseAdapter standard pipeline)
    - Defensive explicit sort
    - Produce FetchResult

    No DB access.
    No incremental logic.
    """
    adapter = build_adapter_for_unit(unit)

    # unit.interval is canonical string from DB (e.g. "1m", "5m")
    interval_enum = Interval(unit.interval)

    candles: List[Candle] = adapter.fetch_candles(
        symbol=unit.canonical_symbol,
        interval=interval_enum,
        limit=unit.fetch_limit,
    )

    if not candles:
        return FetchResult(
            candles=[],
            fetched_count=0,
            min_ts=None,
            max_ts=None,
        )

    # Canonical Candle has open_timestamp/close_timestamp
    candles = sorted(candles, key=lambda c: c.open_timestamp)

    return FetchResult(
        candles=candles,
        fetched_count=len(candles),
        min_ts=candles[0].open_timestamp,
        max_ts=candles[-1].open_timestamp,
    )
