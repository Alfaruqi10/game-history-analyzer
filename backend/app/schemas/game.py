"""Game schemas"""
from pydantic import BaseModel
from datetime import datetime


class GameCreateSchema(BaseModel):
    """Game creation schema"""
    game_name: str
    provider: str = None
    game_type: str = None


class GameSchema(GameCreateSchema):
    """Game response schema"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
