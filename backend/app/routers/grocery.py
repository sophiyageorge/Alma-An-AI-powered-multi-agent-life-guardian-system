# app/routers/grocery.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.models.meal import WeeklyMealPlan
from app.orchestrator.flow import grocery_agent
from app.orchestrator.state import OrchestratorState

router = APIRouter()


@router.post("/meal-plan/{meal_plan_id}/grocery")
def generate_grocery_list(
    meal_plan_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate weekly grocery list from approved meal plan.
    """
    entry = db.query(WeeklyMealPlan).filter(
        WeeklyMealPlan.id == meal_plan_id,
        WeeklyMealPlan.user_id == current_user.user_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    if not entry.is_approved:
        raise HTTPException(status_code=400, detail="Meal plan not approved yet")

    # Build LangGraph state
    state: OrchestratorState = {
        "nutrition_plan": {
            "meal_plan_text": entry.meal_plan_text
        }
    }

# commented for testing
    # # Run grocery agent
    # state = grocery_agent(state)

    # # Save grocery list in DB
    # entry.grocery_list = state["grocery_list"]
    # db.commit()
    # db.refresh(entry)

    return {
        "meal_plan_id": entry.id,
        "grocery_list": entry.grocery_list
    }
