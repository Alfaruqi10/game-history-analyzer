"""Game round schema"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class GameRoundImportSchema(BaseModel):
    """Game round import schema"""
    user_id: Optional[str] = None
    game: str
    provider: Optional[str] = None
    round_id: str
    timestamp: datetime
    bet_amount: float
    win_amount: float
    multiplier: Optional[float] = None
    currency: str = "IDR"
    result: Optional[str] = "UNKNOWN"


class GameRoundSchema(BaseModel):
    """Game round schema"""
    id: int
    external_round_id: str
    timestamp: datetime
    bet_amount: float
    win_amount: float
    multiplier: Optional[float] = None
    currency: str
    result: str
    created_at: datetime
    
    class Config:
        from_attributes = True
