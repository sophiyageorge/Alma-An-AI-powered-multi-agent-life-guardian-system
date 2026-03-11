from app.orchestrator.state import OrchestratorState

def meal_plan_approval_check(state: OrchestratorState):
    return {}

# 2️⃣ Condition function (returns key for add_conditional_edges)


def approval_condition(state: OrchestratorState):
    if state.get("nutrition_plan", {}).get("is_approved", False):
        return "approved"
    return "pending"
