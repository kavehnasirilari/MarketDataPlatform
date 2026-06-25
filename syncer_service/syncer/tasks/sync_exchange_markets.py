# syncer_service/syncer/tasks/sync_exchange_markets.py

import logging

from core.mapping.symbol_mapping import SYMBOL_MAPPING
from core.mapping.market_mapping import EXCHANGE_MARKET_MAPPING
from core.models.enums import Exchange as ExchangeEnum
from database.models import Exchange, CanonicalSymbol, ExchangeMarket

logger = logging.getLogger(__name__)


def _build_core_exchange_markets():
    """
    Build canonical ExchangeMarket definitions from Core mappings.

    Returns a set of tuples:
    (exchange_name, canonical_symbol, exchange_symbol, market_type)
    """
    core_set = set()

    for exchange_enum, symbol_map in SYMBOL_MAPPING.items():
        exchange_name = exchange_enum.value
        market_types = EXCHANGE_MARKET_MAPPING.get(exchange_enum, [])

        for canonical_symbol, exchange_symbol in symbol_map.items():
            for market_type in market_types:
                core_set.add(
                    (
                        exchange_name,
                        canonical_symbol,
                        exchange_symbol,
                        market_type.value,
                    )
                )

    return core_set


def sync_exchange_markets(session, cycle_id: str | None = None):
    core_markets = _build_core_exchange_markets()

    # Load DB state
    exchanges = {
        e.name: e for e in session.query(Exchange).all()
    }

    symbols = {
        s.symbol: s for s in session.query(CanonicalSymbol).all()
    }

    db_rows = session.query(ExchangeMarket).all()

    db_set = {
        (
            row.exchange.name,
            row.canonical_symbol.symbol,
            row.exchange_symbol,
            row.market_type,
        )
        for row in db_rows
    }

    added = 0
    deleted = 0

    logger.info(
        "Exchange market synchronization started",
        extra={
            "service": "syncer-service",
            "event": "syncer.base_sync.exchange_markets_started",
            "status": "started",
            "operation": "sync_exchange_markets",
            "cycle_id": cycle_id,
            "core_count": len(core_markets),
            "db_count": len(db_rows),
        },
    )

    # INSERT: Core -> DB
    for exchange_name, symbol, exchange_symbol, market_type in core_markets:
        key = (exchange_name, symbol, exchange_symbol, market_type)

        if key not in db_set:
            exchange = exchanges.get(exchange_name)
            canonical_symbol = symbols.get(symbol)

            if exchange is None:
                raise RuntimeError(f"Exchange not found in DB: {exchange_name}")

            if canonical_symbol is None:
                raise RuntimeError(f"CanonicalSymbol not found in DB: {symbol}")

            session.add(
                ExchangeMarket(
                    exchange_id=exchange.id,
                    canonical_symbol_id=canonical_symbol.id,
                    exchange_symbol=exchange_symbol,
                    market_type=market_type,
                )
            )
            added += 1
            logger.info(
                "Exchange market added",
                extra={
                    "service": "syncer-service",
                    "event": "syncer.base_sync.exchange_market_added",
                    "status": "success",
                    "operation": "sync_exchange_markets",
                    "cycle_id": cycle_id,
                    "exchange": exchange_name,
                    "symbol": symbol,
                    "exchange_symbol": exchange_symbol,
                    "market_type": market_type,
                },
            )

    # DELETE: DB -> Core
    for row in db_rows:
        key = (
            row.exchange.name,
            row.canonical_symbol.symbol,
            row.exchange_symbol,
            row.market_type,
        )

        if key not in core_markets:
            session.delete(row)
            deleted += 1
            logger.info(
                "Exchange market deleted",
                extra={
                    "service": "syncer-service",
                    "event": "syncer.base_sync.exchange_market_deleted",
                    "status": "success",
                    "operation": "sync_exchange_markets",
                    "cycle_id": cycle_id,
                    "exchange": row.exchange.name,
                    "symbol": row.canonical_symbol.symbol,
                    "exchange_symbol": row.exchange_symbol,
                    "market_type": row.market_type,
                },
            )

    logger.info(
        "Exchange market synchronization completed",
        extra={
            "service": "syncer-service",
            "event": "syncer.base_sync.exchange_markets_completed",
            "status": "success",
            "operation": "sync_exchange_markets",
            "cycle_id": cycle_id,
            "added_count": added,
            "deleted_count": deleted,
            "total_count": len(core_markets),
        },
    )

    return {
        "added": added,
        "deleted": deleted,
        "total": len(core_markets),
    }

if __name__ == "__main__":
    from syncer_service.syncer.bootstrap import preflight_validation
    from database.session import get_session
    from core.observability.logging_config import configure_logging

    configure_logging()
    

    with get_session() as session:
        logger.info("Starting Syncer Phase 4A")

        preflight_validation(session)
        result = sync_exchange_markets(session)
        
        logger.info("Sync result: %s", result)
        
        logger.info("Syncer Phase 4A finished")

