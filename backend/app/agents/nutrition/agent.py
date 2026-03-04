"""
Nutrition Agent Implementation.
"""

from app.orchestrator.state import OrchestratorState
from app.llm.llm_client import llm
from app.agents.nutrition.prompt import build_nutrition_prompt
from app.agents.nutrition.utils import validate_user_profile
from app.core.logging_config import setup_logger
from app.core.exceptions import NutritionAgentError

logger = setup_logger(__name__)


def nutrition_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Generates a 7-day nutrition plan using LLM.

    Args:
        state (OrchestratorState): Current orchestrator state.

    Returns:
        OrchestratorState: Updated state with nutrition plan.
    """

    try:
        user_profile = state.get("user_profile", {})

        logger.info("Validating user profile")
        validate_user_profile(user_profile)

        logger.info("Building nutrition prompt")
        prompt = build_nutrition_prompt(user_profile)

        logger.info("Invoking LLM for nutrition plan")
        response = llm.invoke(prompt)

        logger.info("Updating orchestrator state with nutrition plan")

        state["nutrition_plan"] = {
            "week": user_profile.get("week"),
            "calories_per_day": user_profile.get("calories"),
            "diet": user_profile.get("diet"),
            "region": user_profile.get("region"),
            "restrictions": user_profile.get("restrictions"),
            "goal": user_profile.get("goal"),
            "meal_plan_text": response
        }

        return state

    except Exception as e:
        logger.exception("Error occurred in Nutrition Agent")
        raise NutritionAgentError(str(e)) from e

