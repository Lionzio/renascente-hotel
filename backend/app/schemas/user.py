# backend/app/schemas/user.py
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from app.models.user import UserRole


class UserBase(BaseModel):
    name: str
    role: UserRole = UserRole.EMPLOYEE


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: UUID

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
