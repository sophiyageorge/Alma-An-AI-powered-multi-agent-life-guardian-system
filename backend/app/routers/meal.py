
# app/routers/meal.py
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.schemas.meal import MealPlanResponse
from app.models.meal import WeeklyMealPlan
from app.orchestrator.store import orchestrator_store
from app.core.logging_config import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.get("/meals", response_model=MealPlanResponse)
def get_my_meals(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Fetch the weekly nutrition plan for the logged-in user.

    1️⃣ Try to get the plan from orchestrator state.
    2️⃣ If missing, fetch the latest plan from the database.
    3️⃣ Return a MealPlanResponse always (schema-safe).
    """

    user_id = current_user.user_id
    logger.info("Fetching nutrition plan for user_id=%s", user_id)

    # 1️⃣ Attempt to get from orchestrator state
    state = orchestrator_store.get(user_id, {})
    nutrition_plan = state.get("nutrition_plan")

    # 2️⃣ If missing, fallback to DB
    if not nutrition_plan:
        logger.warning("Nutrition plan not found in orchestrator state for user_id=%s, fetching from DB", user_id)

        today = datetime.utcnow().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=7)

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
            logger.info("Found nutrition plan in DB for user_id=%s, id=%s", user_id, existing_plan.id)
            nutrition_plan = {
                "id": existing_plan.id,
                "created_date": existing_plan.created_at,
                "meal_plan_text": existing_plan.meal_plan_text,
                "is_approved": existing_plan.is_approved,
            }
            # Optionally update orchestrator state
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
        "Returning nutrition plan id=%s for user_id=%s",
        response.meal_plan_id,
        user_id,
    )

    return response
# from fastapi import APIRouter, Depends
# from datetime import datetime
# from app.dependencies import get_current_user
# from app.schemas.meal import MealPlanResponse
# from app.orchestrator.store import orchestrator_store
# from app.core.logging_config import setup_logger

# logger = setup_logger(__name__)

# router = APIRouter()


# @router.get("/meals", response_model=MealPlanResponse)
# def get_my_meals(current_user=Depends(get_current_user)):
#     """
#     Fetch the current weekly nutrition plan for the logged-in user
#     from the orchestrator state.

#     Steps:
#     1. Retrieve the user's orchestrator state from memory.
#     2. Check if a nutrition plan exists for the current week.
#     3. Return the nutrition plan if available, otherwise return
#        default placeholders to satisfy the response schema.
#     """

#     user_id = current_user.user_id
#     logger.info("Fetching nutrition plan for user_id=%s", user_id)

#     # Fetch orchestrator state for this user
#     state = orchestrator_store.get(user_id, {})
    

#     if not state:
#         logger.warning("Orchestrator state not initialized for user_id=%s", user_id)
#         # Return a default response to satisfy Pydantic schema
#         return MealPlanResponse(
#             meal_plan_id=0,
#             user_id=user_id,
#             week=datetime.utcnow().strftime("%Y-W%W"),
#             meal_plan="Not available",
#             approved=False,
#         )

#     # Fetch nutrition plan from state
#     nutrition_plan = state.get("nutrition_plan")
#     if not nutrition_plan:
#         logger.warning("Nutrition plan not available in state for user_id=%s", user_id)
#         # Return a default response to satisfy Pydantic schema
#         return MealPlanResponse(
#             meal_plan_id=0,
#             user_id=user_id,
#             week=datetime.utcnow().strftime("%Y-W%W"),
#             meal_plan="Not available",
#             approved=False,
#         )
#     else:
#         # Calculate current week's start (Monday) and end (next Monday)
#         today = datetime.utcnow().date()
#         week_start = today - timedelta(days=today.weekday())
#         week_end = week_start + timedelta(days=7)

#         # -------------------------------
#         # Check for existing weekly plan
#         # -------------------------------
#         existing_plan = (
#             db.query(WeeklyMealPlan)
#             .filter(
#                 WeeklyMealPlan.user_id == user_id,
#                 WeeklyMealPlan.created_at >= week_start,
#                 WeeklyMealPlan.created_at < week_end,
#             )
#             .order_by(WeeklyMealPlan.created_at.desc())
#             .first()
#         )

#     # Build and return the response from the existing nutrition plan
#     response = MealPlanResponse(
#         meal_plan_id=nutrition_plan.get("id", 0),
#         user_id=user_id,
#         week=nutrition_plan.get("created_date", datetime.utcnow()).strftime("%Y-W%W"),
#         meal_plan=nutrition_plan.get("meal_plan_text", "Not available"),
#         approved=nutrition_plan.get("is_approved", False),
#     )

#     logger.info(
#         "Returning nutrition plan id=%s for user_id=%s", 
#         response.meal_plan_id, 
#         user_id
#     )

#     return response
# # # app/routers/nutrition.py
# # from fastapi import APIRouter, Depends 
# # from app.dependencies import get_current_user
# # from app.schemas.meal import MealPlanResponse
# # from app.orchestrator.store import orchestrator_store

# # router = APIRouter()

# # @router.get("/meals", response_model=MealPlanResponse)
# # def get_my_meals(current_user=Depends(get_current_user)):

# #     """
# #     Return the weekly meal plan stored in the orchestrator state.
# #     """

# #     # 1️⃣ Fetch the orchestrator state for the user
# #     state = orchestrator_store.get(current_user.user_id)
# #     if not state:
# #         return {"message": "Orchestrator state not initialized"}

# #     nutrition_plan = state.get("nutrition_plan")

# #     if not nutrition_plan:
# #         return MealPlanResponse(
# #             meal_plan_id=0,
# #             user_id=current_user.user_id,
# #             week=datetime.utcnow().strftime("%Y-W%W"),
# #             meal_plan="Not available",
# #             approved=False
# #         )
# #         # return {"message": "Nutrition plan not available in state"}

# #     # 2️⃣ Build the response from state
# #     return MealPlanResponse(
# #         meal_plan_id=nutrition_plan.get("id"),  
# #         user_id=current_user.user_id,
# #         week=f"{nutrition_plan.get("created_date").strftime("%Y-W%W")}",
# #         meal_plan=f"{nutrition_plan.get("meal_plan_text")}",
# #         approved=nutrition_plan.get("is_approved", False)
# #     )
  