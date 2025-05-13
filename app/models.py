from sqlalchemy import Column, Integer, String, JSON, DateTime, UniqueConstraint, ForeignKey, Numeric
from app.database import Base
from datetime import datetime

class Game(Base):
    __tablename__ = "games"

    appid = Column(Integer, primary_key=True, index=True)  # Use appid as the primary key
    data = Column(JSON)  # Changed from JSONB to JSON
    updated_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("appid", name="appid"),
    )

class User(Base):
    __tablename__ = "users"

    userid = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Alert(Base):
    __tablename__ = "alerts"

    alertid = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey("users.userid"), nullable=False)
    appid = Column(Integer, ForeignKey("games.appid"), nullable=False)
    price = Column(Numeric, nullable=False)
