"""
LangGraph Orchestrator (Series Flow)
------------------------------------
Workflow for Wellness Guidance System:

health_agent
      ↓
emergency_check
      ↓
nutrition_agent
      ↓
exercise_agent
      ↓
mental_health_agent
      ↓
approval_check → grocery_agent (if approved)
      ↓
compliance agent
"""

from langgraph.graph import StateGraph, END
from app.orchestrator.state import OrchestratorState

# Agents
from app.agents.health.agent import health_agent
from app.agents.emergency.agent import emergency_alert_agent
from app.agents.nutrition.agent import nutrition_agent
from app.agents.exercise.agent import exercise_agent
from app.agents.mental_health_agent.agent import mental_health_agent
from app.agents.approval_agent.agent import meal_plan_approval_check, approval_condition
from app.agents.compliance.agent import compliance_agent

# Logging
from app.core.logging_config import setup_logger
logger = setup_logger(__name__)


# ---------------------------------------------------------
# Emergency Router
# ---------------------------------------------------------
def emergency_router(state: OrchestratorState) -> str:
    """
    Decide whether the workflow should stop due to emergency.

    Returns:
        "emergency" → terminate workflow
        "normal_flow" → continue workflow
    """
    logger.info("Checking emergency condition")

    if state.get("emergency_triggered"):
        logger.warning("Emergency detected. Stopping workflow.")
        return "emergency"

    logger.info("No emergency detected. Continuing workflow.")
    return "normal_flow"


# ---------------------------------------------------------
# Build Series Workflow
# ---------------------------------------------------------
def build_graph():
    """
    Build and compile the LangGraph workflow in series.
    """
    logger.info("Initializing LangGraph orchestrator (series flow)")

    graph = StateGraph(OrchestratorState)

    # ----------------------------
    # Register Nodes
    # ----------------------------
    graph.add_node("health", health_agent)
    graph.add_node("emergency", emergency_alert_agent)
    graph.add_node("nutrition", nutrition_agent)
    graph.add_node("exercise", exercise_agent)
    graph.add_node("mental", mental_health_agent)
    graph.add_node("compliance", compliance_agent)

    # ----------------------------
    # Entry Point
    # ----------------------------
    graph.set_entry_point("health")
    logger.info("Entry point set to 'health' agent")

    # ----------------------------
    # Health → Emergency Check
    # ----------------------------
    graph.add_edge("health", "emergency")
    graph.add_conditional_edges(
        "emergency",
        emergency_router,
        {
            "emergency": END,
            "normal_flow": "nutrition"
        }
    )
    logger.info("Emergency routing configured")

    # ----------------------------
    # Series Execution: nutrition → exercise → mental
    # ----------------------------
    graph.add_edge("nutrition", "exercise")
    graph.add_edge("exercise", "mental")
   

    # ----------------------------
    # Nutrition → Approval Check → Grocery
    # ----------------------------
    graph.add_edge("mental", END)
   
   

    # ----------------------------
    # Endpoints
    # ----------------------------
#     graph.add_edge("compliance", END)
    
    logger.info("Workflow end nodes configured")

    # ----------------------------
    # Compile Graph
    # ----------------------------
    compiled_graph = graph.compile()
    logger.info("LangGraph orchestrator compiled successfully")

    return compiled_graph
