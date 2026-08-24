"""User schemas"""
from pydantic import BaseModel
from datetime import datetime


class UserCreateSchema(BaseModel):
    """User creation schema"""
    external_user_id: str
    username: str


class UserSchema(UserCreateSchema):
    """User response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
