from __future__ import annotations

import logging

from database.session import get_session
from database.models import Exchange

from syncer_service.syncer.ingestion.targets import load_ingestion_units
from syncer_service.syncer.ingestion.pipeline import ingest_unit


def preflight_validation() -> None:
    """
    Validate minimal required metadata before ingestion starts.
    Fail fast if system is not ready.
    """
    with get_session() as session:
        exchange_count = session.query(Exchange).count()
        if exchange_count == 0:
            raise RuntimeError(
                "Preflight failed: no exchanges found in database"
            )


def main(cycle_id: str) -> None:
    # -------------------------
    # bootstrap
    # -------------------------
    logger = logging.getLogger(__name__)
    logger.info(
        "Starting candle ingestion job",
        extra={
        "service": "syncer-service",
        "event": "syncer.job_started",
        "status": "started",
        "operation": "candle_ingestion",
        "cycle_id": cycle_id,
    },
    )

    # -------------------------
    # preflight
    # -------------------------
    preflight_validation()

    # -------------------------
    # load ingestion units
    # -------------------------
    with get_session() as session:
        units = load_ingestion_units(session)

    if not units:
        logger.warning(
            "No ingestion units found. Exiting.",
            extra={
            "service": "syncer-service",
            "event": "syncer.job_completed",
            "status": "no_units",
            "operation": "candle_ingestion",
            "unit_count": 0,
            "cycle_id": cycle_id,
            },
        )
        return

    logger.info(
        "Ingestion units loaded",
        extra = {
            "service": "syncer-service",
            "event": "syncer.units_loaded",
            "status": "success",
            "operation": "load_ingestion_units",
            "unit_count": len(units),
            "cycle_id": cycle_id,
            }
        )

    # -------------------------
    # run ingestion per unit
    # -------------------------
    success = 0
    failed = 0

    for unit in units:
        try:
            ingest_unit(unit=unit, cycle_id= cycle_id)
            success += 1
        except Exception as exc:
            failed += 1
            logger.exception(
                "Ingestion failed",
                extra={
                    "service": "syncer-service",
                    "event": "syncer.unit_failed",
                    "status": "error",
                    "operation": "fetch_candles",
                    "exchange": unit.exchange_name,
                    "market_type": unit.market_type,
                    "symbol": unit.canonical_symbol,
                    "interval": unit.interval,
                    "error_message": str(exc),
                    "cycle_id": cycle_id,
                },
            )

    # -------------------------
    # job summary
    # -------------------------
    logger.info(
        "Candle ingestion job completed",
        extra={
            "service": "syncer-service",
            "event": "syncer.job_completed",
            "status": "success" if failed == 0 else "partial_success",
            "operation": "candle_ingestion",
            "success_count": success,
            "failed_count": failed,
            "cycle_id": cycle_id,
        },
    )


if __name__ == "__main__":
    import uuid
    from core.observability.logging_config import configure_logging

    configure_logging()
    main(cycle_id=str(uuid.uuid4()))