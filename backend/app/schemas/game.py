"""Game schema"""
from datetime import datetime
from pydantic import BaseModel


class GameCreateSchema(BaseModel):
    """Game creation schema"""
    game_name: str
    provider: str | None = None
    game_type: str | None = None


class GameSchema(BaseModel):
    """Game schema"""
    id: int
    game_name: str
    provider: str | None = None
    game_type: str | None = None
    created_at: datetime
    
    class Config:
        from_attributes = True
