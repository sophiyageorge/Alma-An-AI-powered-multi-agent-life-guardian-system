"""
Meal Plan Approval Agent
------------------------

Provides a placeholder agent for processing meal plan approval
and a condition function to route workflow in the orchestrator graph.
"""

from app.orchestrator.state import OrchestratorState
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


# --------------------------
# Meal Plan Approval Check
# --------------------------
def meal_plan_approval_check(state: OrchestratorState) -> dict:
    """
    Placeholder agent function for meal plan approval processing.

    Currently, it returns an empty dict but can be extended
    to perform additional checks or update state with approval info.

    Args:
        state (OrchestratorState): Current orchestrator state

    Returns:
        dict: Updated state or approval info
    """
    logger.info(f"Executing meal_plan_approval_check | user_id={state.get('user_id')}")
   
    return {}


# --------------------------
# Approval Condition Function
# --------------------------
def approval_condition(state: OrchestratorState) -> str:
    """
    Determines the conditional path in the orchestrator
    based on meal plan approval.

    Args:
        state (OrchestratorState): Current orchestrator state

    Returns:
        str: "approved" if meal plan approved, else "pending"
    """
    nutrition_plan = state.get("nutrition_plan", {})
    is_approved = nutrition_plan.get("is_approved", False)

    if is_approved:
        logger.info(f"Meal plan approved | user_id={state.get('user_id')}")
        return "approved"
    else:
        logger.warning(f"Meal plan pending approval | user_id={state.get('user_id')}")
        return "pending"
# from app.orchestrator.state import OrchestratorState

# def meal_plan_approval_check(state: OrchestratorState):
#     return {}

# # 2️⃣ Condition function (returns key for add_conditional_edges)


# def approval_condition(state: OrchestratorState):
#     if state.get("nutrition_plan", {}).get("is_approved", False):
#         return "approved"
#     return "pending"
