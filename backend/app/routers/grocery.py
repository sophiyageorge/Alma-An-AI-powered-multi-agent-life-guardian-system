from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.crud.weekly_meal_plan import get_current_week_meal_plan
from app.models.weekly_meal_plan import WeeklyMealPlan
from app.core.logging_config import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/meal-plan/{meal_plan_id}/grocery")
def generate_grocery_list(
    meal_plan_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate weekly grocery list from an approved meal plan.

    Steps:
    1. Fetch the current week's meal plan by ID and user via CRUD.
    2. Ensure the plan exists and is approved.
    3. Return the grocery list.

    Raises:
        HTTPException: If the meal plan is not found or not approved.

    Returns:
        dict: Contains 'meal_plan_id' and 'grocery_list'.
    """
    user_id = current_user.user_id
    logger.info("Starting grocery list generation | meal_plan_id=%s | user_id=%s", meal_plan_id, user_id)

    try:
        # 1️⃣ Fetch meal plan using CRUD
        meal_plan: WeeklyMealPlan = get_current_week_meal_plan(db, meal_plan_id, user_id)

        # 2️⃣ Validate meal plan
        if not meal_plan:
            logger.warning("Meal plan not found | meal_plan_id=%s | user_id=%s", meal_plan_id, user_id)
            raise HTTPException(status_code=404, detail="Meal plan not found")

        if not meal_plan.is_approved:
            logger.warning("Meal plan not approved | meal_plan_id=%s | user_id=%s", meal_plan_id, user_id)
            raise HTTPException(status_code=400, detail="Meal plan is not approved yet")

        logger.info("Grocery list fetched successfully | meal_plan_id=%s | user_id=%s", meal_plan.id, user_id)

        # 3️⃣ Return grocery list
        return {
            "meal_plan_id": meal_plan.id,
            "grocery_list": meal_plan.grocery_list or []
        }

    except HTTPException:
        # Reraise HTTP errors as-is
        raise
    except Exception as e:
        # Log unexpected errors and return 500
        logger.exception("Failed to generate grocery list | meal_plan_id=%s | user_id=%s", meal_plan_id, user_id)
        raise HTTPException(status_code=500, detail="Internal server error") from e
