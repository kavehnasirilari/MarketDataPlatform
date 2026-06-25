from __future__ import annotations

import logging
import time
from typing import Callable

from database.session import get_session

from .types import IngestionUnit, IngestionSummary
from .fetch import fetch_candles_for_unit
from .filter import run_filter_stage
from .persistence import persist_stage
from .logging import log_unit_summary


def ingest_unit(
    session_factory: Callable = get_session,
    unit: IngestionUnit = None,
    logger: logging.Logger = None,
    cycle_id: str | None = None
) -> IngestionSummary:
    """
    Run full ingestion pipeline for a single ingestion unit.

    Transaction scope:
    - Exactly ONE unit
    - Commit on success
    - Rollback on ANY exception
    """

    if unit is None:
        raise ValueError("IngestionUnit must be provided")

    if logger is None:
        logger = logging.getLogger(__name__)

    start = time.perf_counter()

    logger.info(
        "Ingestion unit started",
        extra={
            "service": "syncer-service",
            "event": "syncer.unit_started",
            "status": "started",
            "operation": "fetch_candles",
            "cycle_id": cycle_id,
            "exchange": unit.exchange_name,
            "market_type": unit.market_type,
            "symbol": unit.canonical_symbol,
            "interval": unit.interval,
        },
    )

    try:
        # -------------------------
        # fetch (no DB)
        # -------------------------
        fetch_result = fetch_candles_for_unit(unit)

        with session_factory() as session:
            # -------------------------
            # filter + sanity (DB read)
            # -------------------------
            filter_result = run_filter_stage(
                session=session,
                unit=unit,
                fetch_result=fetch_result,
            )

            # -------------------------
            # persistence (DB write)
            # -------------------------
            persist_result = persist_stage(
                session=session,
                unit=unit,
                filter_result=filter_result,
            )

        latency_ms = round((time.perf_counter() - start) * 1000, 2)

        # -------------------------
        # build summary (post-commit)
        # -------------------------
        summary = IngestionSummary(
            exchange_name=unit.exchange_name,
            market_type=unit.market_type,
            canonical_symbol=unit.canonical_symbol,
            interval=unit.interval,
            last_ts_db=filter_result.last_ts,
            min_ts_fetched=fetch_result.min_ts,
            max_ts_fetched=fetch_result.max_ts,
            fetched_count=fetch_result.fetched_count,
            inserted_count=persist_result.inserted,
            dropped_last_open_candle=filter_result.dropped_last_open_candle,
            gap_warning=filter_result.gap_warning,
        )

        # -------------------------
        # audit log
        # -------------------------
        log_unit_summary(
            logger = logger, 
            summary = summary,
            cycle_id = cycle_id,
            latency_ms = latency_ms
        )

        return summary
    
    except Exception:
        latency_ms = round((time.perf_counter() - start) * 1000, 2)

        logger.exception(
            "Ingestion unit failed",
            extra={
                "service": "syncer-service",
                "event": "syncer.unit_failed",
                "status": "error",
                "operation": "fetch_candles",
                "cycle_id": cycle_id,
                "exchange": unit.exchange_name,
                "market_type": unit.market_type,
                "symbol": unit.canonical_symbol,
                "interval": unit.interval,
                "latency_ms": latency_ms,
            },
        )
        raise    
