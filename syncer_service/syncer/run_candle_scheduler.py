import time
import logging

from syncer_service.syncer.run_candle_ingestion import main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INTERVAL_SECONDS = 300  # 5 minutes


def run_forever():
    logger.info("Candle scheduler started")

    while True:
        try:
            logger.info("Starting candle ingestion cycle")
            main()
            logger.info("Candle ingestion cycle completed")
        except Exception:
            logger.exception("Candle ingestion cycle failed")

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    run_forever()