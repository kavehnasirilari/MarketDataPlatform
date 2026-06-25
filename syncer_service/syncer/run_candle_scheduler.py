import time
import logging
import uuid

from syncer_service.syncer.run_candle_ingestion import main
from core.observability.logging_config import configure_logging

logger = logging.getLogger(__name__)

INTERVAL_SECONDS = 300  # 5 minutes


def run_forever():
    logger.info(
        "Candle scheduler started",
        extra={
            "service": "syncer-service",
            "event": "syncer.scheduler_started",
            "status": "started",
            "operation": "candle_scheduler",
            "interval_seconds": INTERVAL_SECONDS,
        },
    )

    while True:
        cycle_id = str(uuid.uuid4())
        start = time.perf_counter()
        try:
            logger.info(
                "Starting candle ingestion cycle",
                extra={
                    "service": "syncer-service",
                    "event": "syncer.cycle_started",
                    "status": "started",
                    "operation": "candle_ingestion_cycle",
                    "cycle_id": cycle_id,
                },
            )

            main(cycle_id)

            latency_ms = round((time.perf_counter() - start) * 1000, 2)

            logger.info(
                "Candle ingestion cycle completed",
                extra={
                    "service": "syncer-service",
                    "event": "syncer.cycle_completed",
                    "status": "success",
                    "operation": "candle_ingestion_cycle",
                    "cycle_id": cycle_id,
                    "latency_ms": latency_ms,
                    "next_run_in_seconds": INTERVAL_SECONDS,
                },
            )

        except Exception:
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.exception(
                "Candle ingestion cycle failed",
                extra={
                    "service": "syncer-service",
                    "event": "syncer.cycle_failed",
                    "status": "error",
                    "operation": "candle_ingestion_cycle",
                    "cycle_id": cycle_id,
                    "latency_ms": latency_ms,
                    "next_run_in_seconds": INTERVAL_SECONDS,
                },
            )

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    configure_logging()
    run_forever()