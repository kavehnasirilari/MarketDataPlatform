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


def sync_intervals(session, cycle_id: str | None = None):
    """
    Synchronize canonical intervals from Core into the database.
    """

    core_intervals = _extract_core_intervals()

    db_rows = session.query(Interval).all()
    db_intervals = {EnumInterval(s.interval) for s in db_rows}


    added = 0
    deleted = 0

    logger.info(
        "Interval synchronization started",
        extra={
            "service": "syncer-service",
            "event": "syncer.base_sync.intervals_started",
            "status": "started",
            "operation": "sync_intervals",
            "cycle_id": cycle_id,
            "core_count": len(core_intervals),
            "db_count": len(db_rows),
        },
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
                "Interval added",
                extra={
                    "service": "syncer-service",
                    "event": "syncer.base_sync.interval_added",
                    "status": "success",
                    "operation": "sync_intervals",
                    "cycle_id": cycle_id,
                    "interval": core_interval.value,
                    "ms": ms,
                },
            )


    # DELETE: DB -> Core
    for db_row in db_rows:
        if EnumInterval(db_row.interval) not in core_intervals:
            session.delete(db_row)

            deleted += 1
            logger.info(
                "Interval deleted",
                extra={
                    "service": "syncer-service",
                    "event": "syncer.base_sync.interval_deleted",
                    "status": "success",
                    "operation": "sync_intervals",
                    "cycle_id": cycle_id,
                    "interval": db_row.interval,
                },
            )


    logger.info(
        "Interval synchronization completed",
        extra={
            "service": "syncer-service",
            "event": "syncer.base_sync.intervals_completed",
            "status": "success",
            "operation": "sync_intervals",
            "cycle_id": cycle_id,
            "added_count": added,
            "deleted_count": deleted,
            "total_count": len(core_intervals),
        },
    )


    return {
        "added": added,
        "deleted": deleted,
        "total": len(core_intervals),
    }

if __name__ == "__main__":
    from syncer_service.syncer.bootstrap import preflight_validation
    from database.session import get_session
    from core.observability.logging_config import configure_logging

    configure_logging()
    

    with get_session() as session:
        logger.info("Starting Syncer Phase 4A")

        preflight_validation(session)
        result = sync_intervals(session)
        
        logger.info("Sync result: %s", result)
        
        logger.info("Syncer Phase 4A finished")


