from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies import get_current_user, get_db
from app.crud.weekly_meal_plan import approve_meal_plan as crud_approve_meal_plan
from app.crud.weekly_meal_plan import update_grocery_list
from app.models.weekly_meal_plan import WeeklyMealPlan
from app.orchestrator.flow import grocery_agent
from app.orchestrator.state import OrchestratorState
from app.core.logging_config import setup_logger
from app.core.exceptions import NutritionAgentError

logger = setup_logger(__name__)
router = APIRouter()
 

@router.post("/meal-plan/{meal_plan_id}/approve")
def approve_meal_plan_endpoint(
    meal_plan_id: int,
    shop_number: Optional[str] = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Approve a weekly meal plan for the current user and automatically generate grocery list.

    Args:
        meal_plan_id (int): ID of the meal plan to approve.
        shop_number (str, optional): Grocery store number.
        current_user: Current authenticated user.
        db (Session): SQLAlchemy DB session.

    Returns:
        dict: Meal plan approval status and generated grocery list.
    """
    try:
        logger.info(
            "Approving meal plan | plan_id=%s | user_id=%s | shop_number=%s",
            meal_plan_id,
            current_user.user_id,
            shop_number
        )

        # ✅ Approve meal plan via CRUD
        meal_plan: WeeklyMealPlan = crud_approve_meal_plan(db, meal_plan_id, shop_number)
        if not meal_plan:
            logger.warning(
                "Meal plan not found for approval | plan_id=%s | user_id=%s",
                meal_plan_id,
                current_user.user_id
            )
            raise HTTPException(status_code=404, detail="Meal plan not found")

        # ✅ If grocery list already exists, skip generation
        if meal_plan.grocery_list:
            logger.info(
                "Grocery list already exists | meal_plan_id=%s | user_id=%s",
                meal_plan.id,
                current_user.user_id
            )
        else:
            # 1️⃣ Build minimal orchestrator state for grocery agent
            state: OrchestratorState = {
                "nutrition_plan": {
                    "id": meal_plan.id,
                    "meal_plan_text": meal_plan.meal_plan_text,
                    "calories": meal_plan.calories,
                    "diet": meal_plan.diet,
                    "region": meal_plan.region,
                    "goal": meal_plan.goal,
                    "restrictions": meal_plan.restrictions
                }
            }

            # 2️⃣ Invoke grocery agent
            logger.info("Invoking grocery agent | meal_plan_id=%s | user_id=%s", meal_plan.id, current_user.user_id)
            state = grocery_agent(state)

            # 3️⃣ Save grocery list to DB
            update_meal_plan_grocery_list(db, meal_plan.id, state.get("grocery_list", []))
            logger.info("Grocery list saved | meal_plan_id=%s | user_id=%s", meal_plan.id, current_user.user_id)

        return {
            "meal_plan_id": meal_plan.id,
            "approved": meal_plan.is_approved,
            "shop_number": meal_plan.shop_number,
            "grocery_list": meal_plan.grocery_list,
            "message": "Meal plan approved and grocery list generated."
        }

    except NutritionAgentError as e:
        logger.exception("Failed to approve meal plan | plan_id=%s | user_id=%s", meal_plan_id, current_user.user_id)
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error during meal plan approval | plan_id=%s | user_id=%s", meal_plan_id, current_user.user_id)
        raise HTTPException(status_code=500, detail="Internal server error")
