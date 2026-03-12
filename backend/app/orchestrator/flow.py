"""
Orchestrator Graph (Series Flow)
--------------------------------
Workflow connecting wellness agents in series:

health_agent
      ↓
emergency_router
      ↓
nutrition_agent → exercise_agent → mental_health_agent
      ↓
approval_check → grocery_agent (if approved)
"""

from langgraph.graph import StateGraph, END
from .state import OrchestratorState

# Agents
from app.agents.health.agent import health_agent
from app.agents.nutrition.agent import nutrition_agent
from app.agents.approval_agent.agent import meal_plan_approval_check, approval_condition
from app.agents.grocery.agent import grocery_agent
from app.agents.exercise.agent import exercise_agent
from app.agents.mental_health_agent.agent import mental_health_agent
from app.agents.emergency.agent import emergency_alert_agent

# Logging
from app.core.logging_config import setup_logger

logger = setup_logger(__name__)


# ---------------------------------------------------------
# Emergency Router
# ---------------------------------------------------------
def emergency_router(state: OrchestratorState) -> str:
    """
    Decide whether the workflow should stop due to an emergency.

    Returns:
        "emergency" → stop graph execution
        "normal_flow" → continue workflow
    """
    logger.info("Checking emergency condition in orchestrator")

    if state.get("emergency_detected"):
        logger.warning("Emergency detected. Routing to emergency handler")
        return "emergency"

    logger.info("No emergency detected. Continuing normal workflow")
    return "normal_flow"


# ---------------------------------------------------------
# Build Orchestrator Graph
# ---------------------------------------------------------
def build_orchestrator():
    """
    Builds and compiles the LangGraph orchestrator
    with series execution: nutrition → exercise → mental health.
    """

    logger.info("Building orchestrator graph (series flow)")

    graph = StateGraph(OrchestratorState)

    # ----------------------------
    # Register Agent Nodes
    # ----------------------------
    graph.add_node("health", health_agent)
    graph.add_node("emergency", emergency_alert_agent)
    graph.add_node("nutrition", nutrition_agent)
    graph.add_node("exercise", exercise_agent)
    graph.add_node("mental", mental_health_agent)
    graph.add_node("approval_check", meal_plan_approval_check)
    graph.add_node("grocery", grocery_agent)

    logger.info("Agent nodes registered")

    # ----------------------------
    # Entry Point
    # ----------------------------
    graph.set_entry_point("health")
    logger.info("Entry point set to health agent")

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
    logger.info("Series agent execution configured")

    # ----------------------------
    # Nutrition → Approval Check → Grocery
    # ----------------------------
    graph.add_edge("nutrition", "approval_check")
    graph.add_conditional_edges(
        "approval_check",
        approval_condition,  # returns "approved" or "pending"
        {
            "approved": "grocery",
            "pending": END
        }
    )
    graph.add_edge("grocery", END)
    graph.add_edge("mental", END)
    logger.info("Meal approval workflow configured")

    # ----------------------------
    # Compile Graph
    # ----------------------------
    compiled_graph = graph.compile()
    logger.info("Orchestrator graph compiled successfully")

    return compiled_graph
# """
# Orchestrator Graph
# ------------------
# Defines the workflow connecting all wellness agents using LangGraph.

# Flow Overview
# -------------
# health_agent
#       ↓
# emergency_router
#       ↓
#  ┌───────────────┐
#  │ Normal Flow   │
#  └───────────────┘
#       ↓
#   Parallel Execution
#   ├─ nutrition_agent → approval_check → grocery_agent
#   ├─ exercise_agent
#   └─ mental_health_agent
# """

# from langgraph.graph import StateGraph, END

# from .state import OrchestratorState

# # Agents
# from app.agents.health.agent import health_agent
# from app.agents.nutrition.agent import nutrition_agent
# from app.agents.approval_agent.agent import meal_plan_approval_check, approval_condition
# from app.agents.grocery.agent import grocery_agent
# from app.agents.exercise.agent import exercise_agent
# from app.agents.mental_health_agent.agent import mental_health_agent
# from app.agents.emergency.agent import emergency_alert_agent

# # Logging
# from app.core.logging_config import setup_logger

# logger = setup_logger(__name__)


# # ---------------------------------------------------------
# # Emergency Router
# # ---------------------------------------------------------

# def emergency_router(state: OrchestratorState) -> str:
#     """
#     Decide whether the workflow should stop due to an emergency.

#     Returns:
#         "emergency" → stop graph execution
#         "normal_flow" → continue workflow
#     """

#     logger.info("Checking emergency condition in orchestrator")

#     if state.get("emergency_detected"):
#         logger.warning("Emergency detected. Routing to emergency handler")
#         return "emergency"

#     logger.info("No emergency detected. Continuing normal workflow")

#     return "normal_flow"


# # ---------------------------------------------------------
# # Build Orchestrator Graph
# # ---------------------------------------------------------

# def build_orchestrator():
#     """
#     Builds and compiles the LangGraph orchestrator.

#     Agents Included:
#     - Health Agent
#     - Emergency Agent
#     - Nutrition Agent
#     - Meal Approval Agent
#     - Grocery Agent
#     - Exercise Agent
#     - Mental Health Agent
#     """

#     logger.info("Building orchestrator graph")

#     graph = StateGraph(OrchestratorState)

#     # ---------------------------------------------------------
#     # Register Agent Nodes
#     # ---------------------------------------------------------

#     graph.add_node("health", health_agent)
#     graph.add_node("emergency", emergency_alert_agent)
#     graph.add_node("nutrition", nutrition_agent)
#     graph.add_node("approval_check", meal_plan_approval_check)
#     graph.add_node("grocery", grocery_agent)
#     graph.add_node("exercise", exercise_agent)
#     graph.add_node("mental", mental_health_agent)

#     # Dummy node used to split execution into parallel branches
#     graph.add_node("parallel_start", lambda state: {})

#     logger.info("Agent nodes registered")

#     # ---------------------------------------------------------
#     # Entry Point
#     # ---------------------------------------------------------

#     graph.set_entry_point("health")

#     logger.info("Entry point set to health agent")

#     # ---------------------------------------------------------
#     # Health → Emergency Check
#     # ---------------------------------------------------------

#     graph.add_edge("health", "emergency")

#     graph.add_conditional_edges(
#         "emergency",
#         emergency_router,
#         {
#             "emergency": END,
#             "normal_flow": "parallel_start"
#         }
#     )

#     logger.info("Emergency routing configured")

#     # ---------------------------------------------------------
#     # Parallel Agent Execution
#     # ---------------------------------------------------------

#     graph.add_edge("parallel_start", "nutrition")
#     graph.add_edge("parallel_start", "exercise")
#     graph.add_edge("parallel_start", "mental")

#     logger.info("Parallel agent execution configured")

#     # ---------------------------------------------------------
#     # Nutrition → Approval Check
#     # ---------------------------------------------------------

#     graph.add_edge("nutrition", "approval_check")

#     graph.add_conditional_edges(
#         "approval_check",
#         approval_condition,
#         {
#             "approved": "grocery",
#             "pending": END
#         }
#     )

#     logger.info("Meal approval workflow configured")

#     # ---------------------------------------------------------
#     # Final Endpoints
#     # ---------------------------------------------------------

#     graph.add_edge("grocery", END)
#     graph.add_edge("exercise", END)
#     graph.add_edge("mental", END)

#     logger.info("Workflow end points configured")

#     # ---------------------------------------------------------
#     # Compile Graph
#     # ---------------------------------------------------------

#     compiled_graph = graph.compile()

#     logger.info("Orchestrator graph compiled successfully")

#     return compiled_graph
# # from langgraph.graph import StateGraph,END
# # from .state import OrchestratorState
# # from app.agents.health.agent import health_agent
# # from app.agents.nutrition.agent import nutrition_agent
# # from app.agents.approval_agent.agent import meal_plan_approval_check, approval_condition
# # from app.agents.grocery.agent import grocery_agent
# # from app.agents.exercise.agent import exercise_agent
# # from app.agents.mental_health_agent.agent import mental_health_agent
# # from app.agents.emergency.agent import emergency_alert_agent


# # # def is_emergency(state: OrchestratorState) -> str:
# # #     return "emergency" if state.get("anomaly_detected") else "continue"


# # def build_orchestrator():
    

# #     graph = StateGraph(OrchestratorState)

# #     # Nodes
# #     graph.add_node("health", health_agent)
# #     graph.add_node("emergency", emergency_alert_agent)
# #     graph.add_node("nutrition", nutrition_agent)
# #     graph.add_node("approval_check", meal_plan_approval_check)
# #     graph.add_node("grocery", grocery_agent)
# #     graph.add_node("exercise", exercise_agent)
# #     graph.add_node("mental", mental_health_agent)

# #     # Entry point
# #     graph.set_entry_point("health")

# #     # Flow
# #     graph.add_edge("health", "emergency")
# #     graph.add_conditional_edges(
# #         "emergency",
# #         emergency_router,
# #         {
# #             "emergency": END,
# #             "normal_flow": "parallel_start"
# #         }
# #     )
# #     # Dummy node to branch parallel
# #     graph.add_node("parallel_start", lambda state: {})

# #     # Parallel edges
# #     graph.add_edge("parallel_start", "nutrition")
# #     graph.add_edge("parallel_start", "exercise")
# #     graph.add_edge("parallel_start", "mental")

# #     graph.add_edge("nutrition", "approval_check")
    
# #     # Conditional path based on approval
# #     graph.add_conditional_edges(
# #         "approval_check",
# #         approval_condition,  # returns "approved" or "pending"
# #         {
# #             "approved": "grocery",  # approved → grocery agent
# #             "pending": END           # not approved → stop execution
# #         }
# #     )

# #     # End of flow
# #     graph.add_edge("grocery", END)
# #     graph.add_edge("mental", END)
# #     graph.add_edge("exercise", END)


# #     return graph.compile()


# # def emergency_router(state: OrchestratorState) -> str:
# #     """
# #     Decides whether to stop graph or continue workflow.
# #     """

# #     if state.get("emergency_detected"):
# #         return "emergency"

# #     return "normal_flow"
