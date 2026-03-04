import logging
from app.orchestrator.state import OrchestratorState
from app.services.send_sms import send_emergency_sms


# Configure logger
logger = logging.getLogger("EmergencyAgent")
logger.setLevel(logging.INFO)


def emergency_alert_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Emergency Alert Agent

    Checks if the latest health data contains a critical alert.
    If critical, triggers SMS notification.

    Args:
        state (OrchestratorState): Shared system state

    Returns:
        OrchestratorState: Updated state
    """

    try:
        health_data = state.get("health_data", {})

        if not health_data:
            logger.info("No health data available in state.")
            return state

        alert_level = health_data.get("alert_level")

        if alert_level == "critical":
            logger.warning("Critical alert detected. Triggering emergency SMS.")

            phone_number = state.get("emergency_contact")

            if not phone_number:
                logger.error("No emergency contact found in state.")
                return state

            # Call SMS service
            send_emergency_sms(
                to_phone=phone_number,
                message=(
                    "🚨 CRITICAL HEALTH ALERT!\n"
                    f"Heart Rate: {health_data.get('heart_rate')}\n"
                    f"SpO2: {health_data.get('spo2')}\n"
                    f"BP: {health_data.get('blood_pressure')}\n"
                    "Immediate attention required."
                )
            )

            state["emergency_triggered"] = True
            logger.info("Emergency SMS successfully triggered.")

        else:
            logger.info("Health status normal or warning. No emergency action.")
            state["emergency_triggered"] = False

    except Exception as e:
        logger.error(
            f"Error in emergency_alert_agent: {e}",
            exc_info=True
        )
        state["emergency_triggered"] = False

    return state