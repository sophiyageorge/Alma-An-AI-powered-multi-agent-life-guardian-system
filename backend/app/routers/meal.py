from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.schemas.meal import MealPlanResponse
from app.crud.weekly_meal_plan import get_current_week_meal_plan
from app.orchestrator.store import orchestrator_store
from app.core.logging_config import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.get("/meals", response_model=MealPlanResponse)
def get_my_meals(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Fetch the weekly nutrition plan for the logged-in user.

    Steps:
    1️⃣ Try to get the plan from orchestrator state (LangGraph).
    2️⃣ If missing, fetch the current week's meal plan from the database via CRUD.
    3️⃣ Return a MealPlanResponse always, even if no plan exists.

    Returns:
        MealPlanResponse: Weekly meal plan information for the user.
    """
    user_id = current_user.user_id
    logger.info("Fetching weekly nutrition plan | user_id=%s", user_id)

    # 1️⃣ Attempt to fetch from orchestrator state first
    state = orchestrator_store.get(user_id, {})
    nutrition_plan = state.get("nutrition_plan")

    if nutrition_plan:
        logger.info("Found nutrition plan in orchestrator state | user_id=%s", user_id)
    else:
        logger.warning("Nutrition plan not found in orchestrator state | user_id=%s, fetching from DB", user_id)

        # 2️⃣ Fallback to DB using CRUD function
        try:
            existing_plan = get_current_week_meal_plan(db, user_id)
        except Exception as e:
            logger.exception("Error fetching current week meal plan from DB | user_id=%s", user_id)
            existing_plan = None

        if existing_plan:
            logger.info(
                "Found current week meal plan in DB | user_id=%s | plan_id=%s",
                user_id,
                existing_plan.id,
            )
            nutrition_plan = {
                "id": existing_plan.id,
                "created_date": existing_plan.created_at,
                "meal_plan_text": existing_plan.meal_plan_text,
                "is_approved": existing_plan.is_approved,
            }

            # Update orchestrator state for faster future access
            if user_id not in orchestrator_store:
                orchestrator_store[user_id] = {}
            orchestrator_store[user_id]["nutrition_plan"] = nutrition_plan
        else:
            logger.warning("No nutrition plan found in DB for user_id=%s", user_id)
            # Return default placeholder to satisfy response model
            return MealPlanResponse(
                meal_plan_id=0,
                user_id=user_id,
                week=datetime.utcnow().strftime("%Y-W%W"),
                meal_plan="Not available",
                approved=False,
            )

    # 3️⃣ Build response from available plan
    response = MealPlanResponse(
        meal_plan_id=nutrition_plan.get("id", 0),
        user_id=user_id,
        week=nutrition_plan.get("created_date", datetime.utcnow()).strftime("%Y-W%W"),
        meal_plan=nutrition_plan.get("meal_plan_text", "Not available"),
        approved=nutrition_plan.get("is_approved", False),
    )

    logger.info(
        "Returning nutrition plan | user_id=%s | plan_id=%s",
        user_id,
        response.meal_plan_id,
    )

    return response
