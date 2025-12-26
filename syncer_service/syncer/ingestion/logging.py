from __future__ import annotations

import logging

from syncer_service.syncer.ingestion.types import IngestionSummary


def log_unit_summary(logger: logging.Logger, summary: IngestionSummary) -> None:
    """
    Emit a single, structured log line for one ingestion unit.

    This log line is the primary audit record for ingestion.
    All keys are intentionally fixed to allow grep / ELK parsing.
    """

    logger.info(
        "unit=%s:%s:%s:%s "
        "fetched=%d inserted=%d "
        "dropped_last=%d gap_warning=%d "
        "last_ts_db=%s min_ts_fetched=%s max_ts_fetched=%s",
        summary.exchange_name,
        summary.market_type,
        summary.canonical_symbol,
        summary.interval,
        summary.fetched_count,
        summary.inserted_count,
        int(summary.dropped_last_open_candle),
        int(summary.gap_warning),
        summary.last_ts_db,
        summary.min_ts_fetched,
        summary.max_ts_fetched,
    )
