"""
Health Agent
------------

Fetches today's health metrics from the database and runs
rule-based anomaly detection using the rules engine.

Responsibilities
----------------
1. Fetch today's health metrics
2. Run anomaly detection for each record
3. Detect emergency situations
4. Update orchestrator state
"""

import logging

from app.orchestrator.state import OrchestratorState
from app.crud.health import get_today_health_metrics
from app.agents.health.rules import detect_anomaly

logger = logging.getLogger("HealthAgent")
logger.setLevel(logging.INFO)


def health_agent(state: OrchestratorState) -> OrchestratorState:
    """
    LangGraph node for health analysis.
    """

    try:

        db = state.get("db")
        user_profile = state.get("user_profile", {})
        user_id = user_profile.get("user_id")

        if not db or not user_id:
            logger.warning("HealthAgent missing db or user_id")
            # state["health_data"] = None
            # state["emergency_detected"] = False
            return state

        # ---------------------------------------------------------
        # Fetch today's health metrics
        # ---------------------------------------------------------

        metrics = get_today_health_metrics(db, user_id)

        if not metrics:
            logger.info(f"No health metrics found for user {user_id}")
            # state["health_data"] = None
            # state["emergency_detected"] = False
            return state

        logger.info(f"Fetched  health records")

   

        # ---------------------------------------------------------
        # Run anomaly detection
        # ---------------------------------------------------------

        health_point = {
            "id": metrics.id,
            "heart_rate": metrics.heart_rate,
            "spo2": metrics.spo2,
            "bp_systolic": metrics.bp_systolic,
            "bp_diastolic": metrics.bp_diastolic,
            "timestamp": metrics.timestamp
        }

        result = detect_anomaly(health_point)

        emergency_detected = result["alert_level"] == "critical"
        logger.info(f"DEBUG: anomaly detection result: {result["alert_level"] == "critical"}")

        # ---------------------------------------------------------
        # Update orchestrator state
        # ---------------------------------------------------------

        state["health_data"] = result   # ✅ dict (NOT list)

        state["emergency_triggered"] = emergency_detected

        logger.info(
            f"HealthAgent completed | emergency_detected={emergency_detected}"
        )

        logger.info(
            f"HealthAgent completed | emergency_detected={emergency_detected}"
        )

        return state

    except Exception as e:

        logger.exception("HealthAgent failed")

        state["health_data"] = None
        state["emergency_detected"] = False

        return state