from __future__ import annotations

from typing import List, Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import Candle as CandleORM

from core.models.candle import Candle

from syncer_service.syncer.ingestion.types import IngestionUnit, FetchResult, FilterResult


# -------------------------------------------------
# helpers
# -------------------------------------------------

def drop_last_candle(candles: List[Candle]) -> Tuple[List[Candle], bool]:
    """
    Always drop the last fetched candle to avoid open candle ingestion.
    """
    if not candles:
        return candles, False

    return candles[:-1], True


def get_last_timestamp(
    session: Session,
    unit: IngestionUnit,
) -> Optional[int]:
    """
    Get last ingested candle timestamp for this unit.
    """
    return session.query(
        func.max(CandleORM.timestamp)
    ).filter(
        CandleORM.exchange_market_id == unit.exchange_market_id,
        CandleORM.interval_id == unit.interval_id,
    ).scalar()


def filter_new_candles(
    candles: List[Candle],
    last_ts: Optional[int],
) -> List[Candle]:
    """
    Keep only candles with open_timestamp > last_ts.
    """
    if last_ts is None:
        return candles

    return [
        c for c in candles
        if c.open_timestamp > last_ts
    ]


def sanity_check_gap(
    candles: List[Candle],
    last_ts: Optional[int],
    interval_ms: int,
) -> bool:
    """
    Detect potential candle gap.
    Only emits a boolean warning.
    """
    if last_ts is None or not candles:
        return False

    min_ts = candles[0].open_timestamp
    return min_ts > last_ts + interval_ms


# -------------------------------------------------
# orchestration
# -------------------------------------------------

def run_filter_stage(
    session: Session,
    unit: IngestionUnit,
    fetch_result: FetchResult,
) -> FilterResult:
    """
    Run filter + sanity stage for one ingestion unit.
    """

    # 1) drop last candle
    candles, dropped = drop_last_candle(fetch_result.candles)

    # 2) get last timestamp from DB
    last_ts = get_last_timestamp(session, unit)

    # 3) gap detection (before incremental filter)
    gap_warning = sanity_check_gap(
        candles=candles,
        last_ts=last_ts,
        interval_ms=unit.interval_ms,
    )

    # 4) incremental filtering
    new_candles = filter_new_candles(
        candles=candles,
        last_ts=last_ts,
    )

    return FilterResult(
        new_candles=new_candles,
        dropped_last_open_candle=dropped,
        gap_warning=gap_warning,
        last_ts=last_ts,
    )
