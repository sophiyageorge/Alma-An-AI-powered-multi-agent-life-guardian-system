from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime



class MealPlanResponse(BaseModel):
    meal_plan_id: int
    user_id: int
    week: str
    meal_plan: str
    approved: bool

    class Config:
        from_attributes = True


class WeeklyMealPlanCreate(BaseModel):
    user_id: int
    calories: int
    diet: str
    region: str
    restrictions: Optional[List[str]] = None
    goal: str
    meal_plan_text: str

class WeeklyMealPlanUpdate(BaseModel):
    calories: Optional[int] = None
    diet: Optional[str] = None
    region: Optional[str] = None
    restrictions: Optional[List[str]] = None
    goal: Optional[str] = None
    meal_plan_text: Optional[str] = None

class WeeklyMealPlanResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    calories: int
    diet: str
    region: str
    restrictions: Optional[List[str]]
    goal: str
    meal_plan_text: str
    is_approved: bool

    class Config:
        orm_mode = True