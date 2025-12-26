# syncer_service\syncer\ingestion\persistence.py

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from database.models import Candle as CandleORM

from core.models.candle import Candle

from .types import IngestionUnit, FilterResult, PersistResult


# -------------------------------------------------
# mapping
# -------------------------------------------------

def map_candle_to_row(
    unit: IngestionUnit,
    candle: Candle,
) -> CandleORM:
    """
    Map canonical Candle to ORM Candle row.

    Append-only.
    Timestamp source = open_timestamp.
    """
    return CandleORM(
        exchange_market_id=unit.exchange_market_id,
        interval_id=unit.interval_id,
        timestamp=candle.open_timestamp,
        open=candle.open,
        high=candle.high,
        low=candle.low,
        close=candle.close,
        volume=candle.volume,
    )


# -------------------------------------------------
# persistence helpers
# -------------------------------------------------

def bulk_insert_candles(
    session: Session,
    rows: List[CandleORM],
) -> int:
    """
    Bulk insert candle rows.

    NOTE:
    - Not idempotent yet (Phase 4B)
    - IntegrityError will rollback entire unit
    """
    if not rows:
        return 0

    session.bulk_save_objects(rows)
    return len(rows)


# -------------------------------------------------
# orchestration
# -------------------------------------------------

def persist_stage(
    session: Session,
    unit: IngestionUnit,
    filter_result: FilterResult,
) -> PersistResult:
    """
    Persist filtered candles for a single ingestion unit.
    """

    rows: List[CandleORM] = [
        map_candle_to_row(unit, candle)
        for candle in filter_result.new_candles
    ]

    inserted = bulk_insert_candles(session, rows)

    return PersistResult(
        inserted=inserted
    )
