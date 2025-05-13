from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.config import settings

# Create the engine for connecting to the database
print(settings.DATABASE_URL_psycopg)
engine = create_engine(
    settings.DATABASE_URL_psycopg,
)

# Session for communicating with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

from sqlalchemy.exc import OperationalError
import logging

# Function to get a session with error handling
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    except OperationalError as e:
        logging.error(f"Database connection error: {e}")
        # Можно здесь добавить логику повторных попыток или возврата ошибки
        raise
    finally:
        if db:
            db.close()
