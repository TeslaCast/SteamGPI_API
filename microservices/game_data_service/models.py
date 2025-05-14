from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Game(Base):
    __tablename__ = "games"

    appid = Column(Integer, primary_key=True, index=True)
    data = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow)

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
