# app/agents/compliance_agent/agent.py
from app.orchestrator.state import OrchestratorState

def compliance_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Checks if user has followed nutrition + exercise plans.
    Sets compliance_passed flag.
    """
    nutrition_done = state.get("meal_plan_approved", False)
    exercise_done = state.get("exercise_plan_approved", False)

    state["compliance_passed"] = nutrition_done and exercise_done
    return state