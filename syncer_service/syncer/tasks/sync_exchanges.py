# syncer_service/syncer/tasks/sync_exchanges.py
import logging

from database.models import Exchange
from syncer_service.syncer.adapters.registry import ADAPTER_REGISTRY
from syncer_service.syncer.bootstrap import preflight_validation, init_logging
from database.session import get_session
from core.models.enums import ExchangeStatus

logger = logging.getLogger(__name__)

def sync_exchanges(session):
    """
    Sync exchanges from external sources.
    """
    exchanges = session.query(Exchange).all()
    exchange_names_in_db = {exchange.name for exchange in exchanges}


    total = len(ADAPTER_REGISTRY)
    added = 0
    changed = 0
    active = 0
    unsupported = 0

    logger.info("Starting exchange synchronization (total=%s)", total)

    for exchange_name, adapter in ADAPTER_REGISTRY.items():
        
        if exchange_name not in exchange_names_in_db:
            
            logger.info("Adding new exchange to the database: %s", exchange_name)
            new_exchange = Exchange(name= exchange_name, status = ExchangeStatus.ACTIVE)
            session.add(new_exchange)
            added += 1
            

    for exchange in exchanges:
        print(f"Syncing exchange: {exchange.name}")
        

        new_status = (
            ExchangeStatus.ACTIVE
            if exchange.name in ADAPTER_REGISTRY
            else ExchangeStatus.UNSUPPORTED
        )

        if new_status == ExchangeStatus.ACTIVE:
            active += 1
        else:
            unsupported += 1


        if exchange.status != new_status.value:
            logger.info(
                "exchange status Changed: %s (%s -> %s)",
                exchange.name,
                exchange.status,
                new_status
            )


            exchange.status = new_status.value
            changed += 1

    logger.info(
        "Exchange sync completed: total=%s, added=%s, active%s, unsupported=%s, changed=%s",
        total,
        added,
        active,
        unsupported,
        changed,
    )

    return {
        "total": total,
        "added": added,
        "active": active,
        "unsupported": unsupported,
        "changed": changed,
    }

if __name__ == "__main__":
    init_logging()
    

    with get_session() as session:
        logger.info("Starting Syncer Phase 4A")

        preflight_validation(session)
        result = sync_exchanges(session)
        
        logger.info("Sync result: %s", result)
        
        logger.info("Syncer Phase 4A finished")

