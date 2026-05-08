# database/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

class Base(DeclarativeBase):
    pass


def build_database_url():
    return (
        f"postgresql+psycopg2://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
        f"{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )



DATABASE_URL = build_database_url()

#engin
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"
engin= create_engine(DATABASE_URL, echo=SQL_ECHO)

#Session Facotry
SessionLocal = sessionmaker(bind=engin, autoflush=False, autocommit=False)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
