# app/schemas/user.py
from .enums import ModeEnum, GenderEnum   # <- correct!
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: Optional[date]
    gender: Optional[GenderEnum]

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    user_id: int

    class Config:
        from_attributes = True   # Pydantic v2

class Token(BaseModel):
    access_token: str
    token_type: str
