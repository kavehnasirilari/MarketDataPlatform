# syncer_service/syncer/bootstrap.py

import logging
from database.models import Exchange

def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

def preflight_validation(session):

    # session.execute("select 1")

    count = session.query(Exchange).count()

    if count == 0:
        raise RuntimeError("No exchanges found in database")