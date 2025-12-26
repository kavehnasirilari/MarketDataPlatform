import logging

from core.mapping.supported_market_mapping import SUPPORTED_MARKET_MAPPING
from database.models import ExchangeMarket, Interval, SupportedMarket

logger = logging.getLogger(__name__)


def sync_supported_markets(session):
    # Load DB state
    exchange_markets = session.query(ExchangeMarket).all()
    intervals = session.query(Interval).all()
    db_rows = session.query(SupportedMarket).all()

    # Build lookups
    exchange_market_lookup = {
        (
            em.exchange.name,
            em.canonical_symbol.symbol,
            em.market_type,  # stored as string
        ): em
        for em in exchange_markets
    }

    interval_lookup = {
        interval.interval: interval
        for interval in intervals
    }

    # Build core allow-list (ids)
    core_set = set()

    for exchange_enum, symbol, interval_enum, market_type in SUPPORTED_MARKET_MAPPING:
        key = (exchange_enum.value, symbol, market_type.value)

        em = exchange_market_lookup.get(key)
        if em is None:
            raise RuntimeError(f"ExchangeMarket not found for {key}")

        interval = interval_lookup.get(interval_enum.value)
        if interval is None:
            raise RuntimeError(f"Interval not found: {interval_enum.value}")

        core_set.add((em.id, interval.id))

    # DB active set
    db_active_set = {
        (row.exchange_market_id, row.interval_id)
        for row in db_rows
        if row.status == "active"
    }

    added = 0
    activated = 0
    deactivated = 0

    logger.info(
        "Start supported market synchronization (core=%s, db=%s)",
        len(core_set),
        len(db_rows),
    )

    # INSERT or ACTIVATE
    for exchange_market_id, interval_id in core_set:
        row = next(
            (
                r for r in db_rows
                if r.exchange_market_id == exchange_market_id
                and r.interval_id == interval_id
            ),
            None,
        )

        if row is None:
            session.add(
                SupportedMarket(
                    exchange_market_id=exchange_market_id,
                    interval_id=interval_id,
                    status="active",
                )
            )
            added += 1

        elif row.status != "active":
            row.status = "active"
            activated += 1

    # DEACTIVATE (anything not in allow-list)
    for row in db_rows:
        key = (row.exchange_market_id, row.interval_id)
        if key not in core_set and row.status == "active":
            row.status = "inactive"
            deactivated += 1

    logger.info(
        "SupportedMarket sync completed: added=%s, activated=%s, deactivated=%s, total=%s",
        added,
        activated,
        deactivated,
        len(core_set),
    )

    return {
        "added": added,
        "activated": activated,
        "deactivated": deactivated,
        "total": len(core_set),
    }

if __name__ == "__main__":
    from syncer_service.syncer.bootstrap import init_logging, preflight_validation
    from database.session import get_session

    init_logging()
    

    with get_session() as session:
        logger.info("Starting Syncer Phase 4A")

        preflight_validation(session)
        result = sync_supported_markets(session)
        
        logger.info("Sync result: %s", result)
        
        logger.info("Syncer Phase 4A finished")


