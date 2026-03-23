from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Dict

from app.database import get_db
from app.crud import user_profile as crud
from app.models.weekly_meal_plan import WeeklyMealPlan
from app.agents.nutrition.nutrition_plan import generate_nutrition_plan
from app.orchestrator.store import orchestrator_store
from app.schemas.user_profile import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
)
from app.core.logging_config import setup_logger
from app.core.exceptions import NutritionAgentError

logger = setup_logger(__name__)

router = APIRouter(prefix="/profile", tags=["User Profile"])


@router.post("/", response_model=UserProfileResponse)
def create_profile(profile: UserProfileCreate, db: Session = Depends(get_db)) -> UserProfileResponse:
    """
    Create a new user profile.

    Args:
        profile (UserProfileCreate): User profile data.
        db (Session, optional): SQLAlchemy DB session. Defaults to Depends(get_db).

    Returns:
        UserProfileResponse: Created user profile.
    """
    try:
        logger.info("Creating new user profile | email=%s", profile.email)
        created_profile = crud.create_profile(db, profile)
        logger.info("Profile created successfully | user_id=%s", created_profile.user_id)
        return created_profile
    except Exception as e:
        logger.exception("Error creating profile | email=%s", profile.email)
        raise HTTPException(status_code=500, detail="Failed to create user profile") from e


@router.get("/{user_id}", response_model=UserProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)) -> UserProfileResponse:
    """
    Retrieve a user profile by ID.

    Args:
        user_id (int): ID of the user.
        db (Session, optional): SQLAlchemy DB session. Defaults to Depends(get_db).

    Returns:
        UserProfileResponse: User profile data.
    """
    logger.info("Fetching profile | user_id=%s", user_id)
    profile = crud.get_profile(db, user_id)
    if not profile:
        logger.warning("Profile not found | user_id=%s", user_id)
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/{user_id}", response_model=UserProfileResponse)
def update_profile(
    user_id: int, profile: UserProfileUpdate, db: Session = Depends(get_db)
) -> UserProfileResponse:
    """
    Update a user profile and regenerate weekly nutrition plan.

    Steps:
    1. Update user profile in the database.
    2. Generate updated nutrition plan using NutritionAgent.
    3. Update the current week's weekly meal plan.
    4. Update orchestrator state for LangGraph.

    Args:
        user_id (int): ID of the user.
        profile (UserProfileUpdate): Profile data to update.
        db (Session, optional): SQLAlchemy DB session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If user profile or weekly meal plan not found.
        NutritionAgentError: If nutrition plan generation fails.

    Returns:
        UserProfileResponse: Updated user profile.
    """
    logger.info("Updating profile | user_id=%s", user_id)

    # Update profile in DB
    updated_profile = crud.update_profile(db, user_id, profile)
    if not updated_profile:
        logger.warning("Profile not found for update | user_id=%s", user_id)
        raise HTTPException(status_code=404, detail="Profile not found")

    user_profile_dict = updated_profile.__dict__

    # Generate nutrition plan
    try:
        logger.info("Generating nutrition plan | user_id=%s", user_id)
        nutrition_plan_text = generate_nutrition_plan(user_profile_dict)
    except Exception as e:
        logger.exception("Failed to generate nutrition plan | user_id=%s", user_id)
        raise NutritionAgentError(f"Failed to generate nutrition plan: {str(e)}") from e

    # Update current week's meal plan
    week_plan = (
        db.query(WeeklyMealPlan)
        .filter(WeeklyMealPlan.user_id == user_id)
        .order_by(WeeklyMealPlan.created_at.desc())
        .first()
    )

    if not week_plan:
        logger.warning("Weekly meal plan not found | user_id=%s", user_id)
        raise HTTPException(status_code=404, detail="Meal plan not found for this week")

    today = datetime.now(timezone.utc)
    week_plan.calories = user_profile_dict.get("calories")
    week_plan.diet = user_profile_dict.get("diet")
    week_plan.region = user_profile_dict.get("region")
    week_plan.restrictions = user_profile_dict.get("restrictions")
    week_plan.goal = user_profile_dict.get("goal")
    week_plan.meal_plan_text = nutrition_plan_text
    week_plan.grocery_list=None
    week_plan.shop_number=None
    week_plan.is_approved=False
    week_plan.created_at = today

    try:
        db.commit()
        db.refresh(week_plan)
        logger.info("Weekly meal plan updated | plan_id=%s | user_id=%s", week_plan.id, user_id)
    except Exception as e:
        logger.exception("Failed to update weekly meal plan | user_id=%s", user_id)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update weekly meal plan") from e

    # Update orchestrator state
    state: Dict = orchestrator_store.get(user_id, {})
    state["nutrition_plan"] = {
        "id": week_plan.id,
        "created_date": week_plan.created_at,
        "calories_per_day": week_plan.calories,
        "diet": week_plan.diet,
        "region": week_plan.region,
        "restrictions": week_plan.restrictions,
        "goal": week_plan.goal,
        "meal_plan_text": week_plan.meal_plan_text,
        "is_approved": week_plan.is_approved,
    }
    orchestrator_store[user_id] = state
    logger.info("Orchestrator state updated | user_id=%s", user_id)

    return updated_profile


@router.delete("/{user_id}")
def delete_profile(user_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Delete a user profile by ID.

    Args:
        user_id (int): ID of the user.
        db (Session, optional): SQLAlchemy DB session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If profile not found.

    Returns:
        dict: Success message.
    """
    logger.info("Deleting profile | user_id=%s", user_id)
    try:
        deleted = crud.delete_profile(db, user_id)
        if not deleted:
            logger.warning("Profile not found for deletion | user_id=%s", user_id)
            raise HTTPException(status_code=404, detail="Profile not found")
        logger.info("Profile deleted successfully | user_id=%s", user_id)
        return {"message": "Profile deleted successfully"}
    except Exception as e:
        logger.exception("Failed to delete profile | user_id=%s", user_id)
        raise HTTPException(status_code=500, detail="Failed to delete profile") from e