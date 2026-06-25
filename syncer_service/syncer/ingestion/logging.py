from __future__ import annotations

import logging

from syncer_service.syncer.ingestion.types import IngestionSummary


def log_unit_summary(
        logger: logging.Logger, 
        summary: IngestionSummary,
        cycle_id: str | None = None,
        latency_ms: float | None = None,
        ) -> None:

    logger.info(
        "Ingestion unit completed",
        extra={
            "service": "syncer-service",
            "event": "syncer.unit_completed",
            "status": "success",
            "operation": "fetch_candles",
            "cycle_id": cycle_id,

            "exchange": summary.exchange_name,
            "market_type": summary.market_type,
            "symbol": summary.canonical_symbol,
            "interval": summary.interval,

            "fetched_count": summary.fetched_count,
            "inserted_count": summary.inserted_count,

            "dropped_last_open_candle": summary.dropped_last_open_candle,
            "gap_warning": summary.gap_warning,

            "last_ts_db": summary.last_ts_db,
            "min_ts_fetched": summary.min_ts_fetched,
            "max_ts_fetched": summary.max_ts_fetched,

            "latency_ms": latency_ms,
        },
    )
