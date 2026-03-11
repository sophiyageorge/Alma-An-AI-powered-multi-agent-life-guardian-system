"""
Nutrition Agent Implementation.
"""

from datetime import datetime
from sqlalchemy import extract
from app.orchestrator.state import OrchestratorState
from app.llm.llm_client import llm
# from app.agents.nutrition.prompt import build_nutrition_prompt
from app.agents.nutrition.utils import validate_user_profile
from app.core.logging_config import setup_logger
from app.core.exceptions import NutritionAgentError
from app.models.meal import WeeklyMealPlan
from app.database import get_db
from app.orchestrator.store import orchestrator_store
from app.agents.nutrition.nutrition_plan import generate_nutrition_plan


logger = setup_logger(__name__)


def nutrition_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Generates a 7-day nutrition plan using LLM
    or fetches existing weekly plan from database.
    """

    try:
        user_profile = state.get("user_profile", {})

        logger.info("Starting Nutrition Agent")

        today = datetime.utcnow().date()
        current_week = today.isocalendar()[1]
        current_year = today.year

        logger.info("Checking if meal plan exists for current week")

        db = next(get_db())

        existing_plan = db.query(WeeklyMealPlan).filter(
            WeeklyMealPlan.user_id == user_profile.get("user_id"),
            extract("week", WeeklyMealPlan.created_at) == current_week,
            extract("year", WeeklyMealPlan.created_at) == current_year
        ).order_by(WeeklyMealPlan.created_at.desc()).first()

        # ✅ If meal plan already exists
        if existing_plan:
            logger.info("Existing meal plan found for current week")

            state["nutrition_plan"] = {
                "created_date": existing_plan.created_at,
                "calories_per_day": existing_plan.calories,
                "diet": existing_plan.diet,
                "region": existing_plan.region,
                "restrictions": existing_plan.restrictions,
                "goal": existing_plan.goal,
                "meal_plan_text": existing_plan.meal_plan_text,
                "id": existing_plan.id,
                "is_approved": existing_plan.is_approved
            }

            return {"nutrition_plan": state["nutrition_plan"]}

        # ❌ If no plan exists generate new one
        logger.info("Building nutrition prompt")

        response = generate_nutrition_plan(user_profile)
        
        logger.info("Saving new meal plan to database")

        new_plan = WeeklyMealPlan(
            user_id=user_profile.get("user_id"),
            created_at=today,
            calories=user_profile.get("calories"),
            diet=user_profile.get("diet"),
            region=user_profile.get("region"),
            restrictions=user_profile.get("restrictions"),
            goal=user_profile.get("goal"),
            meal_plan_text=response
        )

        

        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)

        
        state["nutrition_plan"] = {
            "created_date": new_plan.created_at,
            "calories_per_day": new_plan.calories,
            "diet": new_plan.diet,
            "region": new_plan.region,
            "restrictions": new_plan.restrictions,
            "goal": new_plan.goal,
            "meal_plan_text": new_plan.meal_plan_text,
            "id": new_plan.id,
            "is_approved": new_plan.is_approved
        }
        
        # 2️⃣ Save updated state in memory
        # orchestrator_store[user_profile.get("user_id")] = state
        user_id = user_profile.get("user_id")

        # Initialize user dict if it doesn't exist
        if user_id not in orchestrator_store:
            orchestrator_store[user_id] = {}

        # Now safe to write
        # orchestrator_store[user_id]["nutrition_plan"] = state["nutrition_plan"]
        orchestrator_store[user_profile.get("user_id")]["nutrition_plan"] = state["nutrition_plan"]



        return {"nutrition_plan": state["nutrition_plan"]} # Return only the nutrition plan part of the state

    except Exception as e:
        logger.exception("Error occurred in Nutrition Agent")

        raise NutritionAgentError(str(e)) from e
 