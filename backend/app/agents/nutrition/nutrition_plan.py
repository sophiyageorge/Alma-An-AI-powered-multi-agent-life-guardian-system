import logging
from app.agents.nutrition.prompt import build_nutrition_prompt
from app.llm.llm_client import llm

logger = logging.getLogger(__name__)

def generate_nutrition_plan(user_profile):

    logger.info("Building nutrition prompt")
    prompt = build_nutrition_prompt(user_profile)

    logger.info("Invoking LLM for nutrition plan")
    response = llm.invoke(prompt)

    return response