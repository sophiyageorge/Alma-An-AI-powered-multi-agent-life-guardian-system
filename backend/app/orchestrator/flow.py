from langgraph.graph import StateGraph,END
from .state import OrchestratorState
from app.agents.health.agent import health_agent
from app.agents.nutrition.agent import nutrition_agent
from app.agents.approval_agent.agent import meal_plan_approval_check, approval_condition
from app.agents.grocery.agent import grocery_agent
from app.agents.exercise.agent import exercise_agent
from app.agents.mental_health_agent.agent import mental_health_agent
from app.agents.emergency.agent import emergency_alert_agent


# def is_emergency(state: OrchestratorState) -> str:
#     return "emergency" if state.get("anomaly_detected") else "continue"


def build_orchestrator():
    

    graph = StateGraph(OrchestratorState)

    # Nodes
    graph.add_node("health", health_agent)
    graph.add_node("emergency", emergency_alert_agent)
    graph.add_node("nutrition", nutrition_agent)
    graph.add_node("approval_check", meal_plan_approval_check)
    graph.add_node("grocery", grocery_agent)
    graph.add_node("exercise", exercise_agent)
    graph.add_node("mental", mental_health_agent)

    # Entry point
    graph.set_entry_point("health")

    # Flow
    graph.add_edge("health", "emergency")
    graph.add_conditional_edges(
        "emergency",
        emergency_router,
        {
            "emergency": END,
            "normal_flow": "parallel_start"
        }
    )
    # Dummy node to branch parallel
    graph.add_node("parallel_start", lambda state: {})

    # Parallel edges
    graph.add_edge("parallel_start", "nutrition")
    graph.add_edge("parallel_start", "exercise")
    graph.add_edge("parallel_start", "mental")

    graph.add_edge("nutrition", "approval_check")
    
    # Conditional path based on approval
    graph.add_conditional_edges(
        "approval_check",
        approval_condition,  # returns "approved" or "pending"
        {
            "approved": "grocery",  # approved → grocery agent
            "pending": END           # not approved → stop execution
        }
    )

    # End of flow
    graph.add_edge("grocery", END)
    graph.add_edge("mental", END)
    graph.add_edge("exercise", END)


    return graph.compile()


def emergency_router(state: OrchestratorState) -> str:
    """
    Decides whether to stop graph or continue workflow.
    """

    if state.get("emergency_detected"):
        return "emergency"

    return "normal_flow"
