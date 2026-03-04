from pydantic import BaseModel

class MealPlanResponse(BaseModel):
    meal_plan_id:int
    user_id: int
    week: str
    meal_plan: str
    approved: bool
