# syncer_service/syncer/tasks/sync_exchanges.py
import logging

from database.models import Exchange
from syncer_service.syncer.adapters.registry import ADAPTER_REGISTRY
from syncer_service.syncer.bootstrap import preflight_validation
from database.session import get_session
from core.models.enums import ExchangeStatus

logger = logging.getLogger(__name__)

def sync_exchanges(session, cycle_id: str | None = None):
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

    logger.info(
        "Exchange synchronization started",
        extra={
            "service": "syncer-service",
            "event": "syncer.base_sync.exchanges_started",
            "status": "started",
            "operation": "sync_exchanges",
            "cycle_id": cycle_id,
            "total_count": total,
            "db_count": len(exchanges),
        },
    )

    for exchange_name, _ in ADAPTER_REGISTRY.items():
        
        if exchange_name not in exchange_names_in_db:            
            new_exchange = Exchange(name= exchange_name, status = ExchangeStatus.ACTIVE.value)
            session.add(new_exchange)
            added += 1
            active += 1
            
            logger.info(
                "Exchange added",
                extra={
                    "service": "syncer-service",
                    "event": "syncer.base_sync.exchange_added",
                    "status": "success",
                    "operation": "sync_exchanges",
                    "cycle_id": cycle_id,
                    "exchange": exchange_name,
                },
            )

    for exchange in exchanges:        

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
                "Exchange status changed",
                extra={
                    "service": "syncer-service",
                    "event": "syncer.base_sync.exchange_status_changed",
                    "status": "success",
                    "operation": "sync_exchanges",
                    "cycle_id": cycle_id,
                    "exchange": exchange.name,
                    "old_status": exchange.status,
                    "new_status": new_status.value,
                },
            )


            exchange.status = new_status.value
            changed += 1

    logger.info(
        "Exchange synchronization completed",
        extra={
            "service": "syncer-service",
            "event": "syncer.base_sync.exchanges_completed",
            "status": "success",
            "operation": "sync_exchanges",
            "cycle_id": cycle_id,
            "total_count": total,
            "added_count": added,
            "active_count": active,
            "unsupported_count": unsupported,
            "changed_count": changed,
        },
    )

    return {
        "total": total,
        "added": added,
        "active": active,
        "unsupported": unsupported,
        "changed": changed,
    }

if __name__ == "__main__":
    from core.observability.logging_config import configure_logging

    configure_logging()
    

    with get_session() as session:
        logger.info("Starting Syncer Phase 4A")

        preflight_validation(session)
        result = sync_exchanges(session)
        
        logger.info("Sync result: %s", result)
        
        logger.info("Syncer Phase 4A finished")

