import logging
from app.orchestrator.state import OrchestratorState

logger = logging.getLogger("HealthAgent")
logger.setLevel(logging.INFO)


def health_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Health Agent (Graph Node)

    - Reads latest health_data from state
    - Checks alert_level
    - Sets emergency_detected flag
    """

    health_data = state.get("health_data", {})

    if not health_data:
        logger.info("No health data found.")
        state["emergency_detected"] = False
        return state

    alert_level = health_data.get("alert_level")

    if alert_level == "critical":
        logger.warning("Critical alert detected.")
        state["emergency_detected"] = True
    else:
        state["emergency_detected"] = False

    return state