from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_NAME: str = "SteamGPI_API"

    @property
    def DATABASE_URL_psycopg(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"  # Работает только локально, не в Docker

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
