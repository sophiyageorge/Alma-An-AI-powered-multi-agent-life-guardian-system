"""
Wellness AI Orchestrator Graph
==============================

This module defines the LangGraph-based orchestrator responsible for
coordinating multiple wellness agents in a structured workflow.

The orchestrator executes a series of AI agents that analyze user
health data, generate personalized recommendations, and validate
outputs before delivering the final wellness plan.

Workflow Overview
-----------------

The system follows a structured pipeline:

    Health Agent
          ↓
    Emergency Alert Agent
          ↓
    Nutrition Agent
          ↓
    Exercise Agent
          ↓
    Mental Health Agent
          ↓
    Meal Plan Approval Check
          ↓
    Grocery Agent (only if meal plan approved)
          ↓
    Compliance Agent
          ↓
         END

Agent Responsibilities
----------------------

Health Agent
    Collects and analyzes user health metrics such as heart rate,
    blood pressure, SpO2, steps, and workout duration.

Emergency Alert Agent
    Detects dangerous health conditions (e.g., abnormal heart rate,
    critical blood pressure) and raises alerts if needed.

Nutrition Agent
    Generates a personalized weekly meal plan based on user profile
    including calorie target, dietary preference, region, and
    restrictions.

Exercise Agent
    Creates a workout recommendation aligned with the user's
    health metrics and fitness goals.

Mental Health Agent
    Generates mental wellness insights based on user journal entries
    and emotional indicators.

Meal Plan Approval Check
    Verifies whether the user approved the generated meal plan
    before grocery recommendations are created.

Grocery Agent
    Extracts grocery items from the approved meal plan and prepares
    a shopping list.

Compliance Agent
    Performs a final verification step ensuring that all generated
    outputs are consistent, safe, and aligned with the user's
    health profile and goals.

State Management
----------------

The orchestrator operates on a shared state object (`OrchestratorState`)
which contains:

    - user_profile
    - health_data
    - nutrition_plan
    - exercise_plan
    - mental_health_output
    - meal_plan_approved
    - compliance_passed
    - anomaly_detected

Each agent reads from and writes to this shared state.

Logging
-------

The module uses the centralized logging system defined in
`app.core.logging_config` to track agent execution and workflow steps.

Usage
-----

The `build_orchestrator()` function compiles and returns a LangGraph
workflow which can be invoked using:

    graph.invoke(initial_state)

This orchestrator is typically triggered after user login to generate
a full wellness recommendation pipeline.

Author
------

Wellness AI Platform
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
from app.agents.compliance.agent import compliance_agent

# Logging
from app.core.logging_config import setup_logger

logger = setup_logger(__name__)
from langgraph.graph import StateGraph, END
from app.orchestrator.state import OrchestratorState


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
def build_orchestrator():
    """
    Build and compile the LangGraph workflow with conditional emergency handling.
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
    # graph.add_node("compliance", compliance_agent)

    # ----------------------------
    # Entry Point
    # ----------------------------
    graph.set_entry_point("health")
    logger.info("Entry point set to 'health' agent")

    # ----------------------------
    # Health → Emergency
    # ----------------------------
    graph.add_edge("health", "emergency")

    # ----------------------------
    # Conditional routing based on emergency
    # ----------------------------
    graph.add_conditional_edges(
        "emergency",
        emergency_router,
        {
            "emergency": END,       # Stop workflow if emergency
            "normal_flow": "nutrition"  # Continue if no emergency
        }
    )
    logger.info("Emergency routing configured")

    # ----------------------------
    # Series Execution: nutrition → exercise → mental
    # ----------------------------
    graph.add_edge("nutrition", "exercise")
    graph.add_edge("exercise", "mental")

    # ----------------------------
    # Mental → Compliance
    # ----------------------------
    graph.add_edge("mental", END)

    # ----------------------------
    # Compliance → END
    # ----------------------------
    # graph.add_edge("compliance", END)
    
    logger.info("Workflow end nodes configured")

    # ----------------------------
    # Compile Graph
    # ----------------------------
    compiled_graph = graph.compile()
    logger.info("LangGraph orchestrator compiled successfully")

    return compiled_graph

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
    # graph.add_node("compliance", compliance_agent)

    logger.info("Agent nodes registered")

    # ----------------------------
    # Entry Point
    # ----------------------------
    graph.set_entry_point("health")

    # ----------------------------
    # Health → Emergency
    # ----------------------------
    graph.add_edge("health", "emergency")

    # ----------------------------
    # Emergency → Nutrition
    # ----------------------------
    graph.add_edge("emergency", "nutrition")

    # ----------------------------
    # Series Flow
    # ----------------------------
    graph.add_edge("nutrition", "exercise")
    graph.add_edge("exercise", "mental")
    graph.add_edge("mental", "grocery")

   

    # ----------------------------
    # Grocery → Compliance
    # ----------------------------
    graph.add_edge("grocery", END)

    # ----------------------------
    # Mental → Compliance
    # ----------------------------
    # graph.add_edge("mental", END)

    # ----------------------------
    # Compliance → END
    # ----------------------------
    # graph.add_edge("compliance", END)

    logger.info("Compliance verification step added")

    compiled_graph = graph.compile()

    logger.info("Orchestrator graph compiled successfully")

    return compiled_graph