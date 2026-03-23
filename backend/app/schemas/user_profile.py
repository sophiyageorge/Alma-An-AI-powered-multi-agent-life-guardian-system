from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class UserProfileCreate(BaseModel):
    user_id: int
    calories: int = 1800
    diet: str = "vegetarian"
    goal: str = "weight loss"
    region: str = "Kerala"
    restrictions: List[str] = Field(default_factory=list)
    meal_type: str = "home food"


class UserProfileUpdate(BaseModel):
    calories: int | None = None
    diet: str | None = None
    goal: str | None = None
    region: str | None = None
    restrictions: List[str] | None = None
    meal_type: str | None = None
    


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    calories: int
    diet: str
    goal: str
    region: str
    restrictions: List[str]
    meal_type: str
    created_at: datetime

    class Config:
        from_attributes = True