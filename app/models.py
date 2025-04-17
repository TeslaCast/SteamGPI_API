from sqlalchemy import Column, Integer, String, JSON, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base
from datetime import datetime

class Game(Base):
    __tablename__ = "games"

    appid = Column(Integer, primary_key=True, index=True)  # Use appid as the primary key
    data = Column(JSONB)
    updated_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("appid", name="uix_appid"),
    )