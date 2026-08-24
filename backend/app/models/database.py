"""SQLAlchemy database models"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.database.connection import Base
import enum


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    external_user_id = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    game_rounds = relationship("GameRound", back_populates="user")


class Game(Base):
    """Game model"""
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    game_name = Column(String(255), index=True)
    provider = Column(String(255))
    game_type = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    game_rounds = relationship("GameRound", back_populates="game")


class ResultEnum(str, enum.Enum):
    """Result type enum"""
    WIN = "WIN"
    LOSE = "LOSE"
    DRAW = "DRAW"
    UNKNOWN = "UNKNOWN"


class GameRound(Base):
    """Game round/history model"""
    __tablename__ = "game_rounds"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    game_id = Column(Integer, ForeignKey("games.id"), index=True)
    external_round_id = Column(String(255), unique=True, index=True)
    timestamp = Column(DateTime, index=True)
    bet_amount = Column(Float)
    win_amount = Column(Float)
    multiplier = Column(Float, nullable=True)
    currency = Column(String(10))
    result = Column(Enum(ResultEnum), default=ResultEnum.UNKNOWN)
    raw_data_hash = Column(String(64), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    user = relationship("User", back_populates="game_rounds")
    game = relationship("Game", back_populates="game_rounds")


class CollectionRun(Base):
    """Collection run tracking"""
    __tablename__ = "collection_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    status = Column(String(50))  # PENDING, RUNNING, COMPLETED, FAILED
    records_found = Column(Integer, default=0)
    records_saved = Column(Integer, default=0)
    records_skipped = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
