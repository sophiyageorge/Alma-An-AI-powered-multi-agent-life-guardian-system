"""
Grocery Service Layer
---------------------
Handles:
- Grocery list generation using LLM
- DB operations for grocery list
- WhatsApp notifications
"""

from typing import Optional, List
from sqlalchemy.orm import Session

from app.llm.llm_client import llm
from app.core.logging_config import setup_logger
from app.services.send_whatsapp_message import send_whatsapp_message
from app.crud.weekly_meal_plan import (
    update_grocery_list,
    get_meal_plan_by_id,
    WeeklyMealPlan,
)

logger = setup_logger(__name__)


# ---------------------------------------------------------
# LLM GENERATION
# ---------------------------------------------------------
def generate_grocery_list_from_llm(meal_plan_text: str) -> List[str]:
    """
    Generate grocery list using LLM from meal plan text.
    """
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

    try:
        response = llm.invoke(prompt)

        grocery_items = [
            line.strip("-• ").strip()
            for line in response.split("\n")
            if line.strip()
        ]

        return grocery_items

    except Exception:
        logger.exception("LLM invocation failed")
        return []


# ---------------------------------------------------------
# DB OPERATIONS
# ---------------------------------------------------------
def fetch_meal_plan(
    db: Session, meal_plan_id: int
) -> Optional[WeeklyMealPlan]:
    """
    Fetch meal plan from DB.
    """
    try:
        return get_meal_plan_by_id(db, meal_plan_id)
    except Exception:
        logger.exception("Error fetching meal plan from DB")
        return None


def save_grocery_list(
    db: Session,
    meal_plan_id: int,
    grocery_list: List[str],
    shop_number: Optional[str],
) -> bool:
    """
    Save grocery list into DB.
    """
    try:
        update_grocery_list(
            db=db,
            meal_plan_id=meal_plan_id,
            grocery_list=grocery_list,
            shop_number=shop_number,
           
        )
        logger.info("Grocery list saved for plan_id=%s", meal_plan_id)
        return True

    except Exception:
        logger.exception(
            "Failed to update grocery list in DB for plan_id=%s",
            meal_plan_id,
        )
        return False


# ---------------------------------------------------------
# NOTIFICATION
# ---------------------------------------------------------
def send_grocery_whatsapp(
    shop_number: str, grocery_items: List[str]
) -> bool:
    """
    Send grocery list via WhatsApp.
    """
    try:
        message = "Grocery list:\n" + "\n".join(grocery_items)
        send_whatsapp_message(shop_number, message)

        logger.info("WhatsApp sent to %s", shop_number)
        return True

    except Exception:
        logger.exception("Failed to send WhatsApp to %s", shop_number)
        return False


# ---------------------------------------------------------
# MAIN SERVICE FUNCTION (ORCHESTRATOR LOGIC)
# ---------------------------------------------------------
def process_grocery_generation(
    db: Session,
    meal_plan_id: int,
    shop_number: Optional[str] = None,
    meal_plan_text: Optional[str] = None,
    current_grocery_list: Optional[List[str]] = None,
    approved: bool = False,
) -> List[str]:
    """
    Main service to handle grocery list generation workflow.
    """

    logger.info("Processing grocery generation for plan_id=%s", meal_plan_id)

    # ----------------------------
    # VALIDATION
    # ----------------------------
    if not approved:
        logger.info("Meal plan not approved. Skipping.")
        return current_grocery_list or []

    if current_grocery_list:
        logger.info("Grocery list already exists. Skipping.")
        return current_grocery_list

    # ----------------------------
    # FETCH MEAL PLAN IF NEEDED
    # ----------------------------
    if not meal_plan_text:
        meal_plan = fetch_meal_plan(db, meal_plan_id)

        if not meal_plan:
            logger.warning("Meal plan not found for plan_id=%s", meal_plan_id)
            return []

        meal_plan_text = meal_plan.meal_plan_text
        shop_number = shop_number or meal_plan.shop_number

    # ----------------------------
    # GENERATE GROCERY LIST
    # ----------------------------
    grocery_items = generate_grocery_list_from_llm(meal_plan_text)

    if not grocery_items:
        logger.warning("Empty grocery list generated")
        return []

    # ----------------------------
    # SAVE TO DB
    # ----------------------------
    save_grocery_list(
        db=db,
        meal_plan_id=meal_plan_id,
        grocery_list=grocery_items,
        shop_number=shop_number,
    )

    # ----------------------------
    # SEND WHATSAPP
    # ----------------------------
    if shop_number:
        send_grocery_whatsapp(shop_number, grocery_items)

    return grocery_items