from typing import Optional
from sqlalchemy.orm import Session
from app.orchestrator.state import OrchestratorState
from app.llm.llm_client import llm
from app.core.logging_config import setup_logger
from app.services.send_whatsapp_message import send_whatsapp_message
from app.core.exceptions import GroceryAgentError, NutritionAgentError
from app.crud.weekly_meal_plan import update_grocery_list, WeeklyMealPlan
from sqlalchemy.exc import SQLAlchemyError

logger = setup_logger(__name__)

def grocery_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Generate a weekly grocery list from the given nutrition plan, save it to the DB,
    and optionally send via WhatsApp if shop_number is available.

    Args:
        state (OrchestratorState): Current orchestrator state containing 'nutrition_plan'.
        db (Session): SQLAlchemy session for DB operations.

    Returns:
        OrchestratorState: Updated state with 'grocery_list'.
    """
    logger.info("Starting grocery agent...")

    nutrition_plan = state.get("nutrition_plan")
    if not nutrition_plan:
        logger.warning("No nutrition plan found in state. Returning empty grocery list.")
        state["grocery_list"] = []
        return state

    meal_plan_text = nutrition_plan.get("meal_plan_text", "")
    meal_plan_id = nutrition_plan.get("id")  # Needed to update DB
    db = state.get("db")
    if not meal_plan_text or not meal_plan_id or not db:
        logger.warning("db Session,meal plan text or ID is missing. Returning empty grocery list.")
        state["grocery_list"] = []
        return state

    # -----------------------------
    # Build LLM prompt
    # -----------------------------
    prompt = f"""
You are a grocery planning assistant.

From the following 7-day meal plan, generate a WEEKLY grocery list.

Rules:

- Combine quantities for the whole week
- Use simple household quantities (kg, g, pieces)
- One grocery item per line
- No explanations, only the list

Meal Plan:
{meal_plan_text}
"""
    logger.info("Calling LLM to generate grocery list...")
    try:
        response = llm.invoke(prompt)
    except Exception as e:
        logger.exception("LLM invocation failed in grocery agent")
        state["grocery_list"] = []
        return state

    # -----------------------------
    # Parse LLM output into list
    # -----------------------------
    grocery_items = [
        line.strip("-• ").strip()
        for line in response.split("\n")
        if line.strip()
    ]
    state["grocery_list"] = grocery_items

    # -----------------------------
    # Update DB with grocery list
    # -----------------------------
    try:
        meal_plan: Optional[WeeklyMealPlan] = update_grocery_list(
            db=db,
            meal_plan_id=meal_plan_id,
            grocery_list=grocery_items,
            shop_number=nutrition_plan.get("shop_number")
        )
        if not meal_plan:
            logger.warning(f"Failed to update grocery list in DB for plan_id={meal_plan_id}")
        else:
            logger.info(f"Grocery list saved to DB for plan_id={meal_plan_id}")

            # -----------------------------
            # Send WhatsApp message if shop_number exists
            # -----------------------------
            shop_number = meal_plan.shop_number
            if shop_number and grocery_items:
                logger.info(f"Sending grocery list via WhatsApp to {shop_number}")
                try:
                    send_whatsapp_message(shop_number, "Grocery list:\n" + "\n".join(grocery_items))
                    logger.info(f"Grocery list WhatsApp sent successfully to {shop_number}")
                except Exception as e:
                    logger.exception(f"Failed to send grocery list WhatsApp to {shop_number}")

    except NutritionAgentError as e:
        logger.error(f"Failed to update grocery list in DB: {str(e)}")

    logger.info("Grocery agent completed successfully | items=%d", len(grocery_items))
    return state