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
from app.crud import weekly_meal_plan as meal_crud
from app.agents.nutrition.nutrition_plan import generate_nutrition_plan
from app.orchestrator.store import orchestrator_store

logger = setup_logger(__name__)


def nutrition_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Generate or fetch the weekly nutrition plan for the user.

    Steps:
    1. Check if a plan exists for the current week in the DB.
    2. If exists, load it into the state and orchestrator_store.
    3. If not, generate a new plan using the LLM, save via CRUD,
       and update the state and orchestrator_store.

    Args:
        state (OrchestratorState): Orchestrator state with 'user_profile' and 'db'.

    Returns:
        OrchestratorState: Updated state with 'nutrition_plan' key.
    """

    try:
        # -------------------------------
        # Validate input state
        # -------------------------------
        user_profile = state.get("user_profile", {})
        user_id = user_profile.get("user_id")
        db: Session = state.get("db")

        if not user_id or not db:
            raise NutritionAgentError("Missing user_id or database session in state")

        logger.info("Nutrition Agent started for user_id=%s", user_id)

        # -------------------------------
        # Fetch current week's plan
        # -------------------------------
        existing_plan = meal_crud.get_current_week_meal_plan(db, user_id)

        if existing_plan:
            logger.info("Existing nutrition plan found for current week | plan_id=%s", existing_plan.id)
            plan = existing_plan

        else:
            # -------------------------------
            # Generate new weekly plan using LLM
            # -------------------------------
            logger.info("No plan found for current week, generating new plan for user_id=%s", user_id)
            new_plan_text = generate_nutrition_plan(user_profile)

            # Save new plan via CRUD
            plan = meal_crud.create_weekly_meal_plan(
                db=db,
                user_id=user_id,
                calories=user_profile.get("calories"),
                diet=user_profile.get("diet"),
                region=user_profile.get("region"),
                goal=user_profile.get("goal"),
                restrictions=user_profile.get("restrictions"),
                meal_plan_text=new_plan_text
            )

            logger.info("New nutrition plan saved to database | plan_id=%s", plan.id)

        # -------------------------------
        # Update orchestrator state
        # -------------------------------
        state["nutrition_plan"] = {
            "id": plan.id,
            "created_date": plan.created_at,
            "calories_per_day": plan.calories,
            "diet": plan.diet,
            "region": plan.region,
            "restrictions": plan.restrictions,
            "goal": plan.goal,
            "meal_plan_text": plan.meal_plan_text,
            "is_approved": plan.is_approved,
        }

        # Save in global orchestrator_store for quick access
        if user_id not in orchestrator_store:
            orchestrator_store[user_id] = {}

        orchestrator_store[user_id]["nutrition_plan"] = state["nutrition_plan"]

        logger.info("Nutrition plan updated in orchestrator store for user_id=%s", user_id)

        return state

    except Exception as e:
        logger.exception("Nutrition Agent failed for user_id=%s", user_profile.get("user_id"))
        raise NutritionAgentError(str(e)) from e
