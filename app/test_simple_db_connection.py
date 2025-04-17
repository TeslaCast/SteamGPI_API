import psycopg
from app.config import settings

def test_simple_connection():
    try:
        conn = psycopg.connect(
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            host=settings.DB_HOST,
            port=settings.DB_PORT
        )
        print("Database connection successful.")
        conn.close()
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_simple_connection()
