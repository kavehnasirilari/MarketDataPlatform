from __future__ import annotations

import logging

from database.session import get_session
from database.models import Exchange

from syncer_service.syncer.bootstrap import init_logging
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


def main() -> None:
    # -------------------------
    # bootstrap
    # -------------------------
    init_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting candle ingestion job")

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
        logger.warning("No ingestion units found. Exiting.")
        return

    logger.info("Loaded %d ingestion units", len(units))

    # -------------------------
    # run ingestion per unit
    # -------------------------
    success = 0
    failed = 0

    for unit in units:
        try:
            ingest_unit(unit=unit)
            success += 1
        except Exception as e:
            failed += 1
            logger.exception(
                "Ingestion failed for unit %s:%s:%s:%s",
                unit.exchange_name,
                unit.market_type,
                unit.canonical_symbol,
                unit.interval,
            )

    # -------------------------
    # job summary
    # -------------------------
    logger.info(
        "Candle ingestion job finished. success=%d failed=%d",
        success,
        failed,
    )


if __name__ == "__main__":
    main()
