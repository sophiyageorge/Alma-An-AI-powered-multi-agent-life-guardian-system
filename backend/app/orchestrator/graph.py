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
"""

from langgraph.graph import StateGraph, END
from app.orchestrator.state import OrchestratorState

# Agents
from app.agents.health.agent import health_agent
from app.agents.emergency.agent import emergency_alert_agent
from app.agents.nutrition.agent import nutrition_agent
from app.agents.exercise.agent import exercise_agent
from app.agents.mental_health_agent.agent import mental_health_agent
from app.agents.grocery.agent import grocery_agent
from app.agents.approval_agent.agent import meal_plan_approval_check, approval_condition

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

    if state.get("emergency_detected"):
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
    graph.add_node("approval_check", meal_plan_approval_check)
    graph.add_node("grocery", grocery_agent)

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

    # ----------------------------
    # Endpoints
    # ----------------------------
    graph.add_edge("grocery", END)
    graph.add_edge("mental", END)
    logger.info("Workflow end nodes configured")

    # ----------------------------
    # Compile Graph
    # ----------------------------
    compiled_graph = graph.compile()
    logger.info("LangGraph orchestrator compiled successfully")

    return compiled_graph
# """
# LangGraph Orchestrator
# ----------------------

# This module defines the workflow for the Wellness Guidance System
# using LangGraph.

# Workflow Overview
# -----------------

# Health Agent
#       ↓
# Emergency Check
#       ↓
#  ┌────────────────────────────┐
#  │ If Emergency → STOP        │
#  │ If Normal → Continue Flow  │
#  └────────────────────────────┘
#       ↓
# Parallel Execution
#    ├── Nutrition Agent → Approval Check → Grocery Agent
#    ├── Exercise Agent
#    └── Mental Health Agent
# """

# from langgraph.graph import StateGraph, END

# # Orchestrator State
# from app.orchestrator.state import OrchestratorState

# # Agents
# from app.agents.health.agent import health_agent
# from app.agents.emergency.agent import emergency_alert_agent
# from app.agents.nutrition.agent import nutrition_agent
# from app.agents.exercise.agent import exercise_agent
# from app.agents.mental_health_agent.agent import mental_health_agent
# from app.agents.grocery.agent import grocery_agent
# from app.agents.approval_agent.agent import meal_plan_approval_check, approval_condition

# # Logging
# from app.core.logging_config import setup_logger

# logger = setup_logger(__name__)


# # ---------------------------------------------------------
# # Emergency Router
# # ---------------------------------------------------------

# def emergency_router(state: OrchestratorState) -> str:
#     """
#     Decide whether the workflow should stop due to emergency.

#     Returns
#     -------
#     "emergency"
#         If emergency is detected → terminate graph.

#     "normal_flow"
#         Continue workflow.
#     """

#     logger.info("Checking emergency condition")

#     if state.get("emergency_detected"):
#         logger.warning("Emergency detected. Stopping workflow.")
#         return "emergency"

#     logger.info("No emergency detected. Continuing workflow.")

#     return "normal_flow"


# # ---------------------------------------------------------
# # Build Orchestrator Graph
# # ---------------------------------------------------------

# def build_graph():
#     """
#     Build and compile the LangGraph workflow.

#     Returns
#     -------
#     Compiled LangGraph workflow.
#     """

#     logger.info("Initializing LangGraph orchestrator")

#     graph = StateGraph(OrchestratorState)

#     # ---------------------------------------------------------
#     # Register Agent Nodes
#     # ---------------------------------------------------------

#     logger.info("Registering agent nodes")

#     graph.add_node("health", health_agent)
#     graph.add_node("emergency", emergency_alert_agent)
#     graph.add_node("nutrition", nutrition_agent)
#     graph.add_node("approval_check", meal_plan_approval_check)
#     graph.add_node("grocery", grocery_agent)
#     graph.add_node("exercise", exercise_agent)
#     graph.add_node("mental", mental_health_agent)

#     # Dummy node used to start parallel execution
#     graph.add_node("parallel_start", lambda state: {})

#     # ---------------------------------------------------------
#     # Entry Point
#     # ---------------------------------------------------------

#     graph.set_entry_point("health")
#     logger.info("Entry point set to 'health' agent")

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

#     logger.info("Parallel execution paths configured")

#     # ---------------------------------------------------------
#     # Nutrition → Meal Plan Approval
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
#     # Final End Points
#     # ---------------------------------------------------------

#     graph.add_edge("grocery", END)
#     graph.add_edge("mental", END)
#     graph.add_edge("exercise", END)

#     logger.info("Workflow end nodes configured")

#     # ---------------------------------------------------------
#     # Compile Graph
#     # ---------------------------------------------------------

#     compiled_graph = graph.compile()

#     logger.info("LangGraph orchestrator compiled successfully")

#     return compiled_graph
# # from langgraph.graph import StateGraph, END
# # from app.orchestrator.state import OrchestratorState
# # from app.agents.health.agent import health_agent
# # from app.agents.emergency.agent import emergency_alert_agent
# # from app.agents.nutrition.agent import nutrition_agent
# # from app.agents.exercise.agent import exercise_agent
# # from app.agents.mental_health_agent.agent import mental_health_agent
# # from app.agents.grocery.agent import grocery_agent
# # from app.agents.approval_agent.agent import meal_plan_approval_check, approval_condition


# # # from app.agents.mental_agent import mental_agent
# # # from app.agents.compliance_agent import compliance_agent


# # def build_graph():
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
# #     graph.add_conditional_edges(
# #         "approval_check",
# #         approval_condition,   # ⬅️ returns "approved" or "pending"
# #         {
# #             "approved": "grocery",
# #             "pending": END
# #         }
# #     )

# #      # End points
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