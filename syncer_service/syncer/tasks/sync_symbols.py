
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

def sync_symbols(session):
    """
    Synchronize canonical symbols from Core into database.
    """

    core_symbols = _extract_core_symbols()

    db_symbols = session.query(CanonicalSymbol).all()
    db_symbol_names = {s.symbol for s in db_symbols}

    added = 0
    deleted = 0

    logger.info(
        "starting symbol synchronization (core=%s, db= %s)",
        len(core_symbols),
        len(db_symbol_names),
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
            logger.info("Added canonical symbol: %s", symbol)

    # DELETE: DB -> Core
    for db_symbol in db_symbols:
        if db_symbol.symbol not in core_symbols:
            
            session.delete(db_symbol)
            deleted += 1
            logger.info("Deleted canonical symbol: %s", db_symbol.symbol)

    logger.info(
        "Symbol sync completed: added=%s, deleted=%s, total=%s",
        added,
        deleted,
        len(core_symbols),
    )

    return {
        "added": added,
        "deleted": deleted,
        "total": len(core_symbols)
    }


if __name__ == "__main__":
    from syncer_service.syncer.bootstrap import init_logging, preflight_validation

    init_logging()
    

    with get_session() as session:
        logger.info("Starting Syncer Phase 4A")

        preflight_validation(session)
        result = sync_symbols(session)
        
        logger.info("Sync result: %s", result)
        
        logger.info("Syncer Phase 4A finished")
