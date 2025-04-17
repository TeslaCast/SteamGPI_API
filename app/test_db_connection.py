from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create the engine for connecting to the database
engine = create_engine(settings.DATABASE_URL_psycopg)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_connection():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")  # Simple query to test the connection
        print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
