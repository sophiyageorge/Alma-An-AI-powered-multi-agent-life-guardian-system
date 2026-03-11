"""
Exercise Agent Implementation with DB check.
"""

from datetime import datetime
from app.orchestrator.state import OrchestratorState
from app.agents.exercise.recommendation import recommend_exercise
from app.crud.exercise import get_today_exercise_entry
from app.database import get_db
from app.core.logging_config import setup_logger
from app.core.exceptions import ExerciseAgentError
from app.models.health import HealthMetrics
import threading
# from app.orchestrator.store import orchestrator_store

logger = setup_logger(__name__)
lock = threading.Lock()


def exercise_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Generates exercise recommendation based on daily health metrics.
    Checks DB first for today's entry; if none, generates a new one via LLM.

    Args:
        state (OrchestratorState): Current orchestrator state.

    Returns:
        OrchestratorState: Updated state with exercise recommendation.
    """
    try:
        user_profile = state.get("user_profile", {})
        user_id = user_profile.get("user_id")
        if not user_id:
            raise ValueError("Missing user_id in user_profile")

        db = next(get_db())

        # -----------------------------
        # 1️⃣ Get latest health metrics from DB
        # -----------------------------
        latest_health = (
            db.query(HealthMetrics)
            .filter(HealthMetrics.user_id == 1)
            .order_by(HealthMetrics.timestamp.desc())
            .first()
        )

        if not latest_health:
            logger.warning(f"No health metrics found in DB for user_id={user_id}")
            return state  # Cannot generate recommendation

        health_metrics = {
            "heart_rate": latest_health.heart_rate,
            "spo2": latest_health.spo2,
            "bp_systolic": latest_health.bp_systolic,
            "bp_diastolic": latest_health.bp_diastolic,
            "steps": latest_health.steps,
            "workout_duration_minutes": latest_health.workout_duration_minutes,
        }

        logger.info(f"Latest health metrics: {health_metrics}")

        # -----------------------------
        # 2️⃣ Check for today's exercise entry
        # -----------------------------
        today_entry = get_today_exercise_entry(db, user_id, metrics=health_metrics)

        if today_entry:
            logger.info(f"Found existing exercise entry for user_id={user_id} today")
            # Use DB entry as response
            entry_for_response = today_entry
            recommendation = {
                "intensity": today_entry.intensity,
                "plan": today_entry.plan or [],
                "warnings": today_entry.warnings or [],
                "recovery_advice": today_entry.recovery_advice,
            }
            llm_response = today_entry.llm_response

        else:
            # -----------------------------
            # 3️⃣ Generate new recommendation via LLM
            # -----------------------------
            logger.info(f"No entry for today, generating new recommendation for user_id={user_id}")
            entry_for_response = recommend_exercise(user_id=user_id, metrics=health_metrics)
            recommendation = {
                "intensity": entry_for_response.get("intensity"),
                "plan": entry_for_response.get("plan", []),
                "warnings": entry_for_response.get("warnings", []),
                "recovery_advice": entry_for_response.get("recovery_advice"),
            }
            llm_response = entry_for_response.get("llm_response", "")

        # -----------------------------
        # 4️⃣ Update orchestrator state
        # -----------------------------
        state["exercise_plan"] = {
            "heart_rate": health_metrics.get("heart_rate", 0),
            "steps": health_metrics.get("steps"),
            "intensity": recommendation.get("intensity"),
            "plan": recommendation.get("plan", []),
            "warnings": recommendation.get("warnings", []),
            "recovery_advice": recommendation.get("recovery_advice"),
        }

        # -----------------------------
        # 5️⃣ Prepare API response
        # -----------------------------
        response = {
            "id": getattr(entry_for_response, "id", 0),
            "user_id": getattr(entry_for_response, "user_id", user_id),
            "heart_rate": getattr(entry_for_response, "heart_rate", health_metrics.get("heart_rate")),
            "spo2": getattr(entry_for_response, "spo2", health_metrics.get("spo2")),
            "bp_systolic": getattr(entry_for_response, "bp_systolic", health_metrics.get("bp_systolic")),
            "bp_diastolic": getattr(entry_for_response, "bp_diastolic", health_metrics.get("bp_diastolic")),
            "steps": getattr(entry_for_response, "steps", health_metrics.get("steps")),
            "workout_duration_minutes": getattr(entry_for_response, "workout_duration_minutes", health_metrics.get("workout_duration_minutes")),
            "llm_response": llm_response,
            "intensity": recommendation.get("intensity"),
            "plan": recommendation.get("plan", []),
            "warnings": recommendation.get("warnings", []),
            "recovery_advice": recommendation.get("recovery_advice"),
            "date_created": getattr(entry_for_response, "date_created", datetime.utcnow()),
        }

        # Store response in orchestrator state
        state["exercise_plan"] = response

        logger.info("Exercise Agent completed successfully")
        logger.info(f"Exercise recommendation response: {state["exercise_plan"]}")
       

        
        # try:
        #     # with lock:
        #     # state = orchestrator_store.get(user_id, {})
        #         state["exercise_response"] = response
        #         # orchestrator_store[user_id] = state

        #         # if user_id not in orchestrator_store:
        #         #         orchestrator_store[user_id] = {}


        #         # orchestrator_store[user_profile.get("user_id")]["exercise_response"] = state["exercise_response"]



        #         logger.info(f"Updated exercise_response for user_id {user_id}: {response}")

        # except Exception as e:
        #     logger.info("Exercise Agent fai")
            # logger.error(f"Error updating orchestrator_store for user_id {user_id}: {e}", exc_info=True)

        return state

    except Exception as e:
        logger.exception("Error occurred in Exercise Agent")
        raise ExerciseAgentError(str(e)) from e
