from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.crud import user_profile as crud
from app.models.weekly_meal_plan import WeeklyMealPlan
from app.agents.nutrition.nutrition_plan import generate_nutrition_plan
from app.orchestrator.store import orchestrator_store
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate, UserProfileResponse
from app.core.logging_config import setup_logger
from app.core.exceptions import NutritionAgentError

logger = setup_logger(__name__)

router = APIRouter(prefix="/profile", tags=["User Profile"])


@router.post("/", response_model=UserProfileResponse)
def create_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    """
    Create a new user profile.
    """
    logger.info("Creating new user profile for email=%s", profile.email)
    created_profile = crud.create_profile(db, profile)
    logger.info("Profile created | user_id=%s", created_profile.user_id)
    return created_profile


@router.get("/{user_id}", response_model=UserProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user profile by ID.
    """
    logger.info("Fetching profile for user_id=%s", user_id)
    profile = crud.get_profile(db, user_id)
    if not profile:
        logger.warning("Profile not found | user_id=%s", user_id)
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/{user_id}", response_model=UserProfileResponse)
def update_profile(user_id: int, profile: UserProfileUpdate, db: Session = Depends(get_db)):
    """
    Update a user profile and regenerate nutrition plan if profile data changed.

    Steps:
    1. Update profile via CRUD.
    2. Generate new nutrition plan using updated profile.
    3. Update existing weekly meal plan for current week.
    4. Update orchestrator state (LangGraph).
    """
    logger.info("Updating profile for user_id=%s", user_id)

    # 1️⃣ Update profile in DB
    updated_profile = crud.update_profile(db, user_id, profile)
    if not updated_profile:
        logger.warning("Profile not found for update | user_id=%s", user_id)
        raise HTTPException(status_code=404, detail="Profile not found")

    user_profile_dict = updated_profile.__dict__

    # 2️⃣ Generate updated nutrition plan
    try:
        logger.info("Generating new nutrition plan for user_id=%s", user_id)
        nutrition_plan_text = generate_nutrition_plan(user_profile_dict)
    except Exception as e:
        logger.exception("Failed to generate nutrition plan | user_id=%s", user_id)
        raise NutritionAgentError(f"Failed to generate nutrition plan: {str(e)}") from e

    # 3️⃣ Update current week's meal plan
    today = datetime.utcnow()
    week_plan = (
        db.query(WeeklyMealPlan)
        .filter(WeeklyMealPlan.user_id == user_id)
        .order_by(WeeklyMealPlan.created_at.desc())
        .first()
    )

    if not week_plan:
        logger.warning("No existing weekly meal plan found | user_id=%s", user_id)
        raise HTTPException(status_code=404, detail="Meal plan not found for this week")

    week_plan.calories = user_profile_dict.get("calories")
    week_plan.diet = user_profile_dict.get("diet")
    week_plan.region = user_profile_dict.get("region")
    week_plan.restrictions = user_profile_dict.get("restrictions")
    week_plan.goal = user_profile_dict.get("goal")
    week_plan.meal_plan_text = nutrition_plan_text
    week_plan.created_at = today

    db.commit()
    db.refresh(week_plan)
    logger.info("Weekly meal plan updated | plan_id=%s | user_id=%s", week_plan.id, user_id)

    # 4️⃣ Update orchestrator store for LangGraph
    state = orchestrator_store.get(user_id, {})
    state["nutrition_plan"] = {
        "id": week_plan.id,
        "created_date": week_plan.created_at,
        "calories_per_day": week_plan.calories,
        "diet": week_plan.diet,
        "region": week_plan.region,
        "restrictions": week_plan.restrictions,
        "goal": week_plan.goal,
        "meal_plan_text": week_plan.meal_plan_text,
        "is_approved": week_plan.is_approved
    }
    orchestrator_store[user_id] = state
    logger.info("Orchestrator state updated for user_id=%s", user_id)

    return updated_profile


@router.delete("/{user_id}")
def delete_profile(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user profile.
    """
    logger.info("Deleting profile for user_id=%s", user_id)
    deleted = crud.delete_profile(db, user_id)
    if not deleted:
        logger.warning("Profile not found for deletion | user_id=%s", user_id)
        raise HTTPException(status_code=404, detail="Profile not found")
    logger.info("Profile deleted successfully | user_id=%s", user_id)
    return {"message": "Profile deleted successfully"}
