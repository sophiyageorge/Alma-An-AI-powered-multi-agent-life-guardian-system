from langgraph.graph import StateGraph, END
from app.orchestrator.state import OrchestratorState
from app.agents.health.agent import health_agent
from app.agents.emergency.agent import emergency_alert_agent
from app.agents.nutrition.agent import nutrition_agent
from app.agents.exercise.agent import exercise_agent
from app.agents.mental_health_agent.agent import mental_health_agent
from app.agents.grocery.agent import grocery_agent
from app.agents.approval_agent.agent import meal_plan_approval_check, approval_condition


# from app.agents.mental_agent import mental_agent
# from app.agents.compliance_agent import compliance_agent


def build_graph():
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
    graph.add_node("parallel_start", lambda state: state)

    # Parallel edges
    graph.add_edge("parallel_start", "nutrition")
    # graph.add_edge("parallel_start", "exercise")
    # graph.add_edge("parallel_start", "mental")
    
    graph.add_edge("nutrition", "approval_check")
    graph.add_conditional_edges(
        "approval_check",
        approval_condition,   # ⬅️ returns "approved" or "pending"
        {
            "approved": "grocery",
            "pending": END
        }
    )

     # End points
    graph.add_edge("grocery", END)
    # graph.add_edge("mental", END)
    # graph.add_edge("exercise", END)


    return graph.compile()

    


   

def emergency_router(state: OrchestratorState) -> str:
    """
    Decides whether to stop graph or continue workflow.
    """

    if state.get("emergency_detected"):
        return "emergency"

    return "normal_flow"