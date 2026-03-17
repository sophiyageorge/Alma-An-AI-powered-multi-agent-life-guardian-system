# app/services/orchestrator_service.py
from app.orchestrator.state import OrchestratorState
from app.orchestrator.graph import build_graph  # your LangGraph graph
from app.core.logging_config import setup_logger
from fastapi import HTTPException

logger = setup_logger(__name__)

# In-memory store for user states (can be replaced with Redis/db if needed)
orchestrator_store: dict[int, OrchestratorState] = {}


def invoke_orchestrator(state: OrchestratorState, user_id: int) -> OrchestratorState:
    """
    Invokes LangGraph orchestrator and stores the final state in memory.

    Args:
        state (OrchestratorState): Initial orchestrator state
        user_id (int): User ID for storing state

    Returns:
        OrchestratorState: Final orchestrator state
    """
    try:
        logger.info(f"Invoking orchestrator graph for user_id={user_id}")

        final_state = graph.invoke(state)

        logger.info(f"Orchestrator completed successfully for user_id={user_id}")

        # Save state in memory
        orchestrator_store[user_id] = final_state

        logger.info(f"Final orchestrator state stored for user_id={user_id}")

        return final_state

    except Exception as e:
        logger.exception(f"Orchestrator execution failed for user_id={user_id}")
        raise HTTPException(
            status_code=500,
            detail="Failed to initialize wellness workflow"
        )