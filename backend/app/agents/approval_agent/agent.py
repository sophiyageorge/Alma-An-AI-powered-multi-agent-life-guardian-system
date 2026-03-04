from app.orchestrator.state import OrchestratorState

def meal_plan_approval_check(state: OrchestratorState) -> OrchestratorState:
    # If meal plan exists and is approved, mark 'is_approved'
    meal_plan = state.get("nutrition_plan", {})
    approved = meal_plan.get("is_approved", False)
    state["nutrition_plan"]["is_approved"] = approved
    return state


# 2️⃣ Condition function (returns key for add_conditional_edges)
def approval_condition(state: OrchestratorState) -> str:
    if state.get("nutrition_plan", {}).get("is_approved", False):
        return "approved"
    return "pending"
