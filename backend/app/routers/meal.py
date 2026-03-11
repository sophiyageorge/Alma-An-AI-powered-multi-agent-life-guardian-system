# app/routers/nutrition.py
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.schemas.meal import MealPlanResponse
from app.orchestrator.store import orchestrator_store

router = APIRouter()

@router.get("/meals", response_model=MealPlanResponse)
def get_my_meals(current_user=Depends(get_current_user)):

    """
    Return the weekly meal plan stored in the orchestrator state.
    """

    # 1️⃣ Fetch the orchestrator state for the user
    state = orchestrator_store.get(current_user.user_id)
    if not state:
        return {"message": "Orchestrator state not initialized"}

    nutrition_plan = state.get("nutrition_plan")
    if not nutrition_plan:
        return {"message": "Nutrition plan not available in state"}

    # 2️⃣ Build the response from state
    return MealPlanResponse(
        meal_plan_id=nutrition_plan.get("id"),  
        user_id=current_user.user_id,
        week=nutrition_plan.get("created_date").strftime("%Y-W%W"),
        meal_plan=nutrition_plan.get("meal_plan_text"),
        approved=nutrition_plan.get("is_approved", False)
    )