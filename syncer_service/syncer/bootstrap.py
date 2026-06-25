# syncer_service/syncer/bootstrap.py
from database.models import Exchange

def preflight_validation(session):

    count = session.query(Exchange).count()

    if count == 0:
        raise RuntimeError("No exchanges found in database")