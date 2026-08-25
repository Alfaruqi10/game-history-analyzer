"""User schema"""
from datetime import datetime
from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    """User creation schema"""
    external_user_id: str
    username: str


class UserSchema(BaseModel):
    """User schema"""
    id: int
    external_user_id: str
    username: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
