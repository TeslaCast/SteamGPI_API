from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from config import settings

# Create the engine for connecting to the database
print(settings.DATABASE_URL_psycopg)
engine = create_engine(
    settings.DATABASE_URL_psycopg,
)

# Session for communicating with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Function to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
