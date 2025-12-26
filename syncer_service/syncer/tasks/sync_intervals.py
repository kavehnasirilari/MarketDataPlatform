import logging

from core.mapping.interval_mapping import INTERVAL_MAPPING
from database.models import Interval
from core.models.enums import Interval as EnumInterval
from core.mapping.interval_ms_mapping import INTERVAL_MS_MAPPING

logger = logging.getLogger(__name__)

def _extract_core_intervals() -> set[EnumInterval]:

    intervals: set[EnumInterval] = set()

    for exchange_map in INTERVAL_MAPPING.values():
        intervals.update(exchange_map.keys())

    return intervals


def sync_intervals(session):
    """
    Synchronize canonical intervals from Core into the database.
    """

    core_intervals = _extract_core_intervals()

    db_rows = session.query(Interval).all()
    db_intervals = {EnumInterval(s.interval) for s in db_rows}


    added = 0
    deleted = 0

    logger.info(
        "Start interval synchronization (core=%s, db=%s)",
        len(core_intervals),
        len(db_rows),
    )

    # INSERT: Core -> DB
    for core_interval in core_intervals:
        if core_interval not in db_intervals:

            ms = INTERVAL_MS_MAPPING.get(core_interval)

            if ms is None:
                raise ValueError(
                    f"Interval not supported in INTERVAL_MS_MAPPING: {core_interval.value}"
                )

            session.add(Interval(
                interval = core_interval.value,
                ms = ms
            ))
            added += 1
            logger.info(
                "Added interval: %s", core_interval.value
            )


    # DELETE: DB -> Core
    for db_row in db_rows:
        if EnumInterval(db_row.interval) not in core_intervals:
            session.delete(db_row)

            deleted += 1
            logger.info("Deleted interval: %s", db_row.interval)


    logger.info(
        "Interval sync completed: added= %s, deleted=%s, total=%s",
        added,
        deleted,
        len(core_intervals),
    )


    return {
        "added": added,
        "deleted": deleted,
        "total": len(core_intervals),
    }

if __name__ == "__main__":
    from syncer_service.syncer.bootstrap import init_logging, preflight_validation
    from database.session import get_session

    init_logging()
    

    with get_session() as session:
        logger.info("Starting Syncer Phase 4A")

        preflight_validation(session)
        result = sync_intervals(session)
        
        logger.info("Sync result: %s", result)
        
        logger.info("Syncer Phase 4A finished")


