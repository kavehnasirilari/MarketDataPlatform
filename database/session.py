# database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

#-------------------------------------------------------------
# NOTE for reviewers / futur maintainers:
# in phase 2 we hardcode DATABASE_URL only for local development
# and ambelic migration initialization.

# TODO (phase 5-6)
#   -move DATABASE_URL to environment variables (.env)
#   -configure docker-compose to inject env values
#   -replace this hardcode string with `os.getenv("DATABASE_URL")`
#   -insure engin works in both local & docker environments
#-----------------------------------------------------------------


class Base(DeclarativeBase):
    pass

#engin
DATABASE_URL = "postgresql+psycopg2://mdp_user:StrongPassword123!@localhost:5432/market_data"

engin= create_engine(DATABASE_URL, echo=True)

#Session Facotry
SessionLocal = sessionmaker(bind=engin, autoflush=False, autocommit=False)


