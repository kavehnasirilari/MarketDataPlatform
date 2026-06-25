
import logging

from core.mapping.symbol_mapping import SYMBOL_MAPPING
from database.models import CanonicalSymbol
from database.session import get_session

logger = logging.getLogger(__name__)

def _extract_core_symbols() -> set[str]:
    """
    extract unique canonical symbol from Core symbol_mapping
    """

    symbols: set[str] = set()

    for exchange_map in SYMBOL_MAPPING.values():
        symbols.update(exchange_map.keys())

    return symbols


def _parse_symbol(symbol: str) -> tuple[str, str]:

    try:
        base, quote = symbol.split("/")
    except ValueError:
        raise ValueError(f"invalid canonical symbol format: {symbol}")
    
    return base, quote

def sync_symbols(session, cycle_id: str | None = None):
    """
    Synchronize canonical symbols from Core into database.
    """

    core_symbols = _extract_core_symbols()

    db_symbols = session.query(CanonicalSymbol).all()
    db_symbol_names = {s.symbol for s in db_symbols}

    added = 0
    deleted = 0

    logger.info(
        "Symbol synchronization started",
        extra={
            "service": "syncer-service",
            "event": "syncer.base_sync.symbols_started",
            "status": "started",
            "operation": "sync_symbols",
            "cycle_id": cycle_id,
            "core_count": len(core_symbols),
            "db_count": len(db_symbols),
        },
    )

    # INSERT: Core -> DB
    for symbol in core_symbols:
        if symbol not in db_symbol_names:

            base, quote = _parse_symbol(symbol)

            session.add(CanonicalSymbol(
                symbol = symbol,
                base_asset = base,
                quote_asset = quote
            ))
            added += 1 
            
            logger.info(
                "Canonical symbol added",
                extra={
                    "service": "syncer-service",
                    "event": "syncer.base_sync.symbol_added",
                    "status": "success",
                    "operation": "sync_symbols",
                    "cycle_id": cycle_id,
                    "symbol": symbol,
                    "base_asset": base,
                    "quote_asset": quote,
                },
            )


    # DELETE: DB -> Core
    for db_symbol in db_symbols:
        if db_symbol.symbol not in core_symbols:
            
            session.delete(db_symbol)
            deleted += 1

            logger.info(
                "Canonical symbol deleted",
                extra={
                    "service": "syncer-service",
                    "event": "syncer.base_sync.symbol_deleted",
                    "status": "success",
                    "operation": "sync_symbols",
                    "cycle_id": cycle_id,
                    "symbol": db_symbol.symbol,
                },
            )            

    logger.info(
        "Symbol synchronization completed",
        extra={
            "service": "syncer-service",
            "event": "syncer.base_sync.symbols_completed",
            "status": "success",
            "operation": "sync_symbols",
            "cycle_id": cycle_id,
            "added_count": added,
            "deleted_count": deleted,
            "total_count": len(core_symbols),
        },
    )

    return {
        "added": added,
        "deleted": deleted,
        "total": len(core_symbols)
    }


if __name__ == "__main__":
    from syncer_service.syncer.bootstrap import preflight_validation
    from core.observability.logging_config import configure_logging

    configure_logging()
    

    with get_session() as session:
        logger.info("Starting Syncer Phase 4A")

        preflight_validation(session)
        result = sync_symbols(session)
        
        logger.info("Sync result: %s", result)
        
        logger.info("Syncer Phase 4A finished")
