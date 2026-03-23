from typing import Optional, List
from sqlalchemy.orm import Session
from app.llm.llm_client import llm
from app.core.logging_config import setup_logger
from app.services.send_whatsapp_message import send_whatsapp_message
from app.crud.weekly_meal_plan import update_grocery_list, get_meal_plan_by_id, WeeklyMealPlan

logger = setup_logger(__name__)

def grocery_agent(
    db: Session,
    meal_plan_id: int,
    shop_number: Optional[str] = None,
    meal_plan_text: Optional[str] = None,
    current_grocery_list: Optional[List[str]] = None,
    approved: bool = False
) -> List[str]:
    """
    Generate a weekly grocery list if the meal plan is approved and grocery list is empty.
    Updates DB and optionally sends WhatsApp message.

    Args:
        db (Session): SQLAlchemy session.
        meal_plan_id (int): ID of the meal plan to process.
        shop_number (Optional[str]): Optional WhatsApp number to send the list.
        meal_plan_text (Optional[str]): Meal plan text for LLM generation.
        current_grocery_list (Optional[List[str]]): Existing grocery list.
        approved (bool): Whether the meal plan is approved.

    Returns:
        List[str]: Generated grocery list (empty if not generated).
    """
    logger.info("Starting grocery agent for plan_id=%s", meal_plan_id)

    # If not approved or grocery list exists, skip generation
    if not approved:
        logger.info("Meal plan not approved. Skipping grocery generation.")
        return current_grocery_list or []

    if current_grocery_list:
        logger.info("Grocery list already exists. Skipping generation.")
        return current_grocery_list

    if not meal_plan_text:
        # Fetch meal plan text from DB
        meal_plan: Optional[WeeklyMealPlan] = get_meal_plan_by_id(db, meal_plan_id)
        if not meal_plan:
            logger.warning("Meal plan not found in DB for plan_id=%s", meal_plan_id)
            return []
        meal_plan_text = meal_plan.meal_plan_text
        shop_number = shop_number or meal_plan.shop_number

    # Build LLM prompt
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

    # Generate grocery list
    try:
        response = llm.invoke(prompt)
        grocery_items = [line.strip("-• ").strip() for line in response.split("\n") if line.strip()]
    except Exception:
        logger.exception("LLM invocation failed")
        return []

    # Update DB
    try:
        update_grocery_list(
            db=db,
            meal_plan_id=meal_plan_id,
            grocery_list=grocery_items,
            shop_number=shop_number,
            mark_approved=True,
        )
        logger.info("Grocery list saved to DB for plan_id=%s", meal_plan_id)
    except Exception:
        logger.exception("Failed to update grocery list in DB for plan_id=%s", meal_plan_id)

    # Send WhatsApp if number exists
    if shop_number and grocery_items:
        try:
            send_whatsapp_message(shop_number, "Grocery list:\n" + "\n".join(grocery_items))
            logger.info("Grocery list sent via WhatsApp to %s", shop_number)
        except Exception:
            logger.exception("Failed to send WhatsApp to %s", shop_number)

    return grocery_items