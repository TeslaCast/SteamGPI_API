from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
 
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/SteamGPI_API")

# Create the engine for connecting to the database without check_same_thread
engine = create_engine(DATABASE_URL)

# Create the database using SQLAlchemy
Base = declarative_base()

# Session for communicating with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()