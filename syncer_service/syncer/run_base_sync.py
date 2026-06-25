# syncer_service/syncer/run_base_syncer.py
import logging
import time
import uuid

from syncer_service.syncer.tasks.sync_exchanges import sync_exchanges
from syncer_service.syncer.tasks.sync_symbols import sync_symbols
from syncer_service.syncer.tasks.sync_intervals import sync_intervals
from syncer_service.syncer.tasks.sync_exchange_markets import sync_exchange_markets
from syncer_service.syncer.tasks.sync_supported_markets import sync_supported_markets
from database.session import get_session

logger = logging.getLogger(__name__)


def run_base_sync(session):
    cycle_id = str(uuid.uuid4())
    start = time.perf_counter()

    logger.info(
        "starting base sync",
        extra={
        "service": "syncer-service",
        "event": "syncer.base_sync.started",
        "status": "started",
        "operation": "base_sync",
        "cycle_id": cycle_id,
        },
    )
    
    try:

        results = {}

        results["exchanges"] = sync_exchanges(session, cycle_id=cycle_id)
        session.commit()

        results["symbols"] = sync_symbols(session, cycle_id=cycle_id)
        session.commit()

        results["intervals"] = sync_intervals(session, cycle_id=cycle_id)
        session.commit()

        results["exchange_markets"] = sync_exchange_markets(session, cycle_id=cycle_id)
        session.commit()

        results["supported_markets"] = sync_supported_markets(session, cycle_id=cycle_id)
        session.commit()

        latency_ms = round((time.perf_counter() - start) * 1000, 2)

        logger.info(
            "Base sync completed",
            extra={
                "service": "syncer-service",
                "event": "syncer.base_sync.completed",
                "status": "success",
                "operation": "base_sync",
                "cycle_id": cycle_id,
                "latency_ms": latency_ms,
                "results": results,
            },
        )

        return results


    except Exception:
        session.rollback()
        latency_ms = round((time.perf_counter() - start) * 1000, 2)

        logger.exception(
            "Base sync failed",
            extra={
                "service": "syncer-service",
                "event": "syncer.base_sync.failed",
                "status": "error",
                "operation": "base_sync",
                "cycle_id": cycle_id,
                "latency_ms": latency_ms,
            },
        )
        raise   

if __name__ == "__main__":
    from core.observability.logging_config import configure_logging

    configure_logging()

    with get_session() as session:
        run_base_sync(session)
    


