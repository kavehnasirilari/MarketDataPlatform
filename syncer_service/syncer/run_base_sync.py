# syncer_service/syncer/run_base_syncer.py
import logging

from syncer_service.syncer.tasks.sync_exchanges import sync_exchanges
from syncer_service.syncer.tasks.sync_symbols import sync_symbols
from syncer_service.syncer.tasks.sync_intervals import sync_intervals
from syncer_service.syncer.tasks.sync_exchange_markets import sync_exchange_markets
from syncer_service.syncer.tasks.sync_supported_markets import sync_supported_markets
from database.session import get_session

logger = logging.getLogger(__name__)


def run_base_sync(session):
    logger.info("starting base sync")
    sync_exchanges(session)
    session.commit()
    sync_symbols(session)
    session.commit()
    sync_intervals(session)
    session.commit()
    sync_exchange_markets(session)
    session.commit()
    sync_supported_markets(session)
    session.commit()
    logger.info("base sync completed")


if __name__ == "__main__":
    from syncer_service.syncer.bootstrap import init_logging

    init_logging()

    with get_session() as session:
        run_base_sync(session)
    


