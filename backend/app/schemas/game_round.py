"""Game round schemas"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class GameRoundImportSchema(BaseModel):
    """Schema for importing game rounds"""
    user_id: Optional[str] = Field(None, description="ID Pengguna")
    game: str = Field(..., description="Nama permainan")
    provider: Optional[str] = Field(None, description="Penyedia permainan")
    round_id: str = Field(..., description="ID putaran")
    timestamp: datetime = Field(..., description="Waktu putaran")
    bet_amount: float = Field(..., description="Jumlah taruhan")
    win_amount: float = Field(..., description="Jumlah kemenangan")
    multiplier: Optional[float] = Field(None, description="Multiplier")
    currency: str = Field(..., description="Mata uang")
    result: Optional[str] = Field(None, description="Hasil (WIN/LOSE/DRAW)")


class GameRoundSchema(BaseModel):
    """Game round response schema"""
    id: int
    user_id: Optional[int] = None
    game_id: Optional[int] = None
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
