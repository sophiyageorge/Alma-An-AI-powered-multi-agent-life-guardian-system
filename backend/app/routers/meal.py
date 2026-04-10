"""
Retrieve the current week's meal plan for the authenticated user.

This endpoint follows a fallback strategy:
1. Attempts to retrieve the nutrition plan from the in-memory orchestrator state.
2. If not found, queries the database for the current week's meal plan.
3. Returns a default response if no plan exists.

Args:
    current_user (User): Authenticated user object.
    db (Session): Database session dependency.

Returns:
    MealPlanResponse: Structured response containing meal plan details.

Raises:
    HTTPException: If database retrieval fails.
"""
"""
Meal Plan Router
----------------
Handles retrieval of the current week's meal plan for authenticated users.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Dependencies
from app.dependencies import get_current_user, get_db

# Schemas
from app.schemas.meal import MealPlanResponse

# CRUD
from app.crud.weekly_meal_plan import get_current_week_meal_plan

# Orchestrator
from app.orchestrator.store import orchestrator_store

# Logging
from app.core.logging_config import setup_logger

# Models (adjust import if needed)
from app.models.user import User

logger = setup_logger(__name__)
router = APIRouter()


def get_current_week() -> str:
    """
    Generate current ISO week string.

    Returns:
        str: Current week in format YYYY-WWW (ISO standard)
    """
    now = datetime.utcnow()
    iso_week = now.isocalendar().week
    return f"{now.year}-W{iso_week}"

import json

def parse_meal_plan_text(meal_plan_text: str) -> Dict[str, Any]:
    try:
        if not meal_plan_text:
            return {}

        cleaned = meal_plan_text.strip()

        # ✅ Extract JSON if LLM added extra text
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start != -1 and end != -1:
            cleaned = cleaned[start:end + 1]

        return json.loads(cleaned)

    except Exception as e:
        logger.error("Failed to parse meal plan JSON", extra={"error": str(e)})
        return {}

def build_meal_response(user_id: int, plan: Optional[Dict[str, Any]]) -> MealPlanResponse:
    """
    Build standardized MealPlanResponse from plan dictionary.

    Args:
        user_id (int): User ID
        plan (dict | None): Nutrition plan data

    Returns:
        MealPlanResponse: Structured response
    """
    if not plan:
        return MealPlanResponse(
            meal_plan_id=0,
            user_id=user_id,
            week=get_current_week(),
            meal_plan={},
            approved=False,
        )

    created_date = plan.get("created_date", datetime.utcnow())
  
    return MealPlanResponse(
        meal_plan_id=plan.get("id", 0),
        user_id=user_id,
        week=created_date.strftime("%Y-W%W"),
        meal_plan=parse_meal_plan_text(plan.get("meal_plan_text")),
        approved=plan.get("is_approved", False),
    )


@router.get("/meals", response_model=MealPlanResponse)
def get_my_meals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db), 
) -> MealPlanResponse:
    """
    Retrieve the current week's meal plan for the authenticated user.

    Workflow:
    1. Attempt to retrieve meal plan from in-memory orchestrator state.
    2. If not found, fetch from database via CRUD layer.
    3. Cache DB result in orchestrator for future requests.
    4. Return standardized response.

    Args:
        current_user (User): Authenticated user object
        db (Session): Database session

    Returns:
        MealPlanResponse: Meal plan details

    Raises:
        HTTPException: If database access fails
    """

    user_id = current_user.user_id

    logger.info(
        "Fetching weekly nutrition plan",
        extra={"user_id": user_id}
    )

    # Step 1: Check orchestrator state
    state: Dict[str, Any] = orchestrator_store.get(user_id, {})
    nutrition_plan: Optional[Dict[str, Any]] = state.get("nutrition_plan")

    if nutrition_plan:
        logger.info(
            "Nutrition plan found in orchestrator",
            extra={"user_id": user_id}
        )
    else:
        logger.warning(
            "Nutrition plan not in orchestrator, fetching from DB",
            extra={"user_id": user_id}
        )

        # Step 2: Fetch from DB
        try:
            existing_plan = get_current_week_meal_plan(db, user_id)
        except Exception:
            logger.exception(
                "Database error while fetching meal plan",
                extra={"user_id": user_id}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch meal plan"
            )

        # Step 3: Process DB result
        if existing_plan:
            logger.info(
                "Meal plan found in database",
                extra={"user_id": user_id, "plan_id": existing_plan.is_approved}
            )

            nutrition_plan = {
                "id": existing_plan.id,
                "created_date": existing_plan.created_at,
                "meal_plan_text": existing_plan.meal_plan_text,
                "is_approved": existing_plan.is_approved,
            }

            # Cache in orchestrator (thread-safe pattern)
            orchestrator_store.setdefault(user_id, {})
            orchestrator_store[user_id]["nutrition_plan"] = nutrition_plan

        else:
            logger.warning(
                "No meal plan found in database",
                extra={"user_id": user_id}
            )
            return build_meal_response(user_id, None)

    # Step 4: Return response
    response = build_meal_response(user_id, nutrition_plan)

    logger.info(
        "Returning nutrition plan ",
        extra={"user_id": user_id, "plan_id": response.meal_plan_id}
    )
   

    return response
