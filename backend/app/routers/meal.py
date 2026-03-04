# app/routers/nutrition.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_current_user,get_db
from app.schemas.meal import MealPlanResponse
from app.models.meal import WeeklyMealPlan
from app.orchestrator.state import OrchestratorState
from app.orchestrator.graph import build_graph 

router = APIRouter()
graph = build_graph()

@router.get("/meals", response_model=MealPlanResponse)
def get_my_meals(current_user = Depends(get_current_user),db : Session = Depends(get_db)):
    

    """
    Generate weekly meal plan via LangGraph, store in DB, and return meal plan.
    """
    # 1️⃣ Build initial state
    state: OrchestratorState = {
        "user_id": current_user.user_id,

        # Inputs
        "user_profile": {
            "user_id" : current_user.user_id,
            "calories": 1800,
            "diet": "vegetarian",
            "goal": "weight loss",
            "region": "Kerala",
            "restrictions": "no dairy",
            "meal_type": "home food",
            "week": "2026-W05"
        },
        # "health_data": None,
        # "journal_text": None,
        # "user_request": "Generate weekly meal plan",

        # # Agent outputs
        # "nutrition_plan": None,
        # "exercise_plan": None,
        # "grocery_list": None,
        # "mental_insights": None,

        # # System flags
        # "anomaly_detected": False,
        # "emergency_level": None,
        # "compliance_passed": False,

        # Final output
        "response": None
    }
# commented for testing
    # 2️⃣ Execute LangGraph
    print("user id",current_user.user_id)
    final_state = graph.invoke(state)

    # Store meal plan in DB
    meal_plan_text = final_state["nutrition_plan"]["meal_plan_text"]
    week = final_state["nutrition_plan"]["week"]

    db_entry = WeeklyMealPlan(
        user_id=current_user.user_id,
        meal_plan_text=meal_plan_text,
        is_approved=False  # user must approve before grocery
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)


    # 3️⃣ Return agent response
    return {
        "meal_plan_id": db_entry.id,
        "user_id": current_user.user_id,
        "week": week,
        "meal_plan": meal_plan_text,
        "approved": db_entry.is_approved
    }

    
