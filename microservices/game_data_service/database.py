from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.config import settings

print(settings.DATABASE_URL_psycopg)
engine = create_engine(
    settings.DATABASE_URL_psycopg,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from sqlalchemy.exc import OperationalError
import logging

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    except OperationalError as e:
        logging.error(f"Database connection error: {e}")
        raise
    finally:
        if db:
            db.close()