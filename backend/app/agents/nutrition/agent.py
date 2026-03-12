"""
Nutrition Agent Implementation
------------------------------
Responsible for generating or fetching a 7-day nutrition plan
for a user. Uses LLM to generate new plans if one does not exist
for the current week.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.orchestrator.state import OrchestratorState
from app.core.logging_config import setup_logger
from app.core.exceptions import NutritionAgentError
from app.models.meal import WeeklyMealPlan
from app.agents.nutrition.nutrition_plan import generate_nutrition_plan
from app.orchestrator.store import orchestrator_store

logger = setup_logger(__name__)


def nutrition_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Generate or fetch the weekly nutrition plan for the user.

    Steps:
    1. Check if a plan exists for the current week in the DB.
    2. If exists, load it into the state and orchestrator_store.
    3. If not, generate a new plan using the LLM, save to DB,
       and update the state and orchestrator_store.

    Returns
    -------
    Updated OrchestratorState with 'nutrition_plan' key.
    """

    try:
        user_profile = state.get("user_profile", {})
        user_id = user_profile.get("user_id")
        db: Session = state.get("db")

        if not user_id or not db:
            raise NutritionAgentError("Missing user_id or database session in state")

        logger.info("Nutrition Agent started for user_id=%s", user_id)

        # Calculate current week's start (Monday) and end (next Monday)
        today = datetime.utcnow().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=7)

        # -------------------------------
        # Check for existing weekly plan
        # -------------------------------
        existing_plan = (
            db.query(WeeklyMealPlan)
            .filter(
                WeeklyMealPlan.user_id == user_id,
                WeeklyMealPlan.created_at >= week_start,
                WeeklyMealPlan.created_at < week_end,
            )
            .order_by(WeeklyMealPlan.created_at.desc())
            .first()
        )

        if existing_plan:
            logger.info("Existing nutrition plan found for current week")

            # Update state with existing plan
            state["nutrition_plan"] = {
                "id": existing_plan.id,
                "created_date": existing_plan.created_at,
                "calories_per_day": existing_plan.calories,
                "diet": existing_plan.diet,
                "region": existing_plan.region,
                "restrictions": existing_plan.restrictions,
                "goal": existing_plan.goal,
                "meal_plan_text": existing_plan.meal_plan_text,
                "is_approved": existing_plan.is_approved,
            }

        else:
            # -------------------------------
            # Generate new weekly plan
            # -------------------------------
            logger.info("No plan found for this week, generating new plan")

            new_plan_text = generate_nutrition_plan(user_profile)

            new_plan = WeeklyMealPlan(
                user_id=user_id,
                created_at=today,
                calories=user_profile.get("calories"),
                diet=user_profile.get("diet"),
                region=user_profile.get("region"),
                restrictions=user_profile.get("restrictions"),
                goal=user_profile.get("goal"),
                meal_plan_text=new_plan_text,
            )

            db.add(new_plan)
            db.commit()
            db.refresh(new_plan)

            logger.info("New nutrition plan saved to database (id=%s)", new_plan.id)

            # Update state with new plan
            state["nutrition_plan"] = {
                "id": new_plan.id,
                "created_date": new_plan.created_at,
                "calories_per_day": new_plan.calories,
                "diet": new_plan.diet,
                "region": new_plan.region,
                "restrictions": new_plan.restrictions,
                "goal": new_plan.goal,
                "meal_plan_text": new_plan.meal_plan_text,
                "is_approved": new_plan.is_approved,
            }

        # -------------------------------
        # Save plan in orchestrator_store
        # -------------------------------
        if user_id not in orchestrator_store:
            orchestrator_store[user_id] = {}

        orchestrator_store[user_id]["nutrition_plan"] = state["nutrition_plan"]

        logger.info("Nutrition plan updated in orchestrator state for user_id=%s", user_id)

        return state

    except Exception as e:
        logger.exception("Nutrition Agent failed for user_id=%s", user_profile.get("user_id"))
        raise NutritionAgentError(str(e)) from e
