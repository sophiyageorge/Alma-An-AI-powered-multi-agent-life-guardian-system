from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.agents.nutrition.nutrition_plan import generate_nutrition_plan
from app.core.logging_config import setup_logger
from app.core.exceptions import NutritionAgentError
from datetime import datetime
from app.models.meal import WeeklyMealPlan
from app.orchestrator.store import orchestrator_store

from app.database import get_db
from app.schemas.user_profile import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
)
from app.crud import user_profile as crud

logger = setup_logger(__name__)

router = APIRouter(prefix="/profile", tags=["User Profile"])


@router.post("/", response_model=UserProfileResponse)
def create_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db, profile)


@router.get("/{user_id}", response_model=UserProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = crud.get_profile(db, user_id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

        


    return profile


@router.put("/{user_id}", response_model=UserProfileResponse)
def update_profile(user_id: int, profile: UserProfileUpdate, db: Session = Depends(get_db)):
    updated = crud.update_profile(db, user_id, profile)

    if not updated:
        raise HTTPException(status_code=404, detail="Profile not found")

    updated = crud.update_profile(db, user_id, profile)

    if not updated:
        raise HTTPException(status_code=404, detail="Profile not found")

    user_profile = updated.__dict__

    logger.info("Generating new nutrition plan")

    # Generate plan
    response = generate_nutrition_plan(user_profile)

    today = datetime.utcnow()

    # 1️⃣ Find current week meal plan
    nutrition_plan = (
        db.query(WeeklyMealPlan)
        .filter(WeeklyMealPlan.user_id == user_id)
        .order_by(WeeklyMealPlan.created_at.desc())
        .first()
    )

    if not nutrition_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found for this week")

    # 2️⃣ Update existing meal plan
    nutrition_plan.calories = user_profile.get("calories")
    nutrition_plan.diet = user_profile.get("diet")
    nutrition_plan.region = user_profile.get("region")
    nutrition_plan.restrictions = user_profile.get("restrictions")
    nutrition_plan.goal = user_profile.get("goal")
    nutrition_plan.meal_plan_text = response
    nutrition_plan.created_at = today

    db.commit()
    db.refresh(nutrition_plan)

    # 3️⃣ Update LangGraph state
    state = orchestrator_store.get(user_id, {})

    state["nutrition_plan"] = {
        "created_date": nutrition_plan.created_at,
        "calories_per_day": nutrition_plan.calories,
        "diet": nutrition_plan.diet,
        "region": nutrition_plan.region,
        "restrictions": nutrition_plan.restrictions,
        "goal": nutrition_plan.goal,
        "meal_plan_text": nutrition_plan.meal_plan_text,
        "id": nutrition_plan.id,
        "is_approved": nutrition_plan.is_approved
    }

    orchestrator_store[user_id] = state

    return updated


        


    # return updated


@router.delete("/{user_id}")
def delete_profile(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_profile(db, user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {"message": "Profile deleted"}