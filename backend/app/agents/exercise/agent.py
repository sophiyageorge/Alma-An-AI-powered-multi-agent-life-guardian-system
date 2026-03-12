"""
Exercise Agent Implementation with DB check.
Generates personalized exercise recommendations based on daily health metrics.
"""

from datetime import datetime
from app.orchestrator.state import OrchestratorState
from app.agents.exercise.recommendation import recommend_exercise
from app.crud.exercise import get_today_exercise_entry
from app.database import get_db
from app.core.logging_config import setup_logger
from app.core.exceptions import ExerciseAgentError
from app.models.health import HealthMetrics

logger = setup_logger(__name__)


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
        logger.info("Exercise Agent started")
        user_profile = state.get("user_profile", {})
        user_id = user_profile.get("user_id")
        if not user_id:
            raise ValueError("Missing user_id in user_profile")

        db = next(get_db())

        # -----------------------------
        # 1️⃣ Fetch latest health metrics
        # -----------------------------
        latest_health: HealthMetrics = (
            db.query(HealthMetrics)
            .filter(HealthMetrics.user_id == 1)
            .order_by(HealthMetrics.timestamp.desc())
            .first()
        )

        if not latest_health:
            logger.warning(f"No health metrics found for user_id={user_id}")
            return state  # Cannot generate recommendation

        health_metrics = {
            "heart_rate": latest_health.heart_rate,
            "spo2": latest_health.spo2,
            "bp_systolic": latest_health.bp_systolic,
            "bp_diastolic": latest_health.bp_diastolic,
            "steps": latest_health.steps,
            "workout_duration_minutes": latest_health.workout_duration_minutes,
        }
        logger.info(f"Latest health metrics fetched: {health_metrics}")

        # -----------------------------
        # 2️⃣ Check if today's exercise entry exists
        # -----------------------------
        today_entry = get_today_exercise_entry(db, user_id)

        if today_entry:
            logger.info(f"Using existing exercise entry for user_id={user_id}")
            entry_for_response = today_entry
            recommendation = {
                "intensity": today_entry.intensity,
                "plan": today_entry.plan or [],
                "warnings": today_entry.warnings or [],
                "recovery_advice": today_entry.recovery_advice,
            }
            llm_response = today_entry.llm_response
            entry_id = getattr(today_entry, "id", 0)
            date_created = getattr(today_entry, "date_created", datetime.utcnow())
        else:
            logger.info(f"No entry for today. Generating new recommendation for user_id={user_id}")
            llm_result = recommend_exercise(user_id=user_id, metrics=health_metrics)

            # Create a consistent dict for orchestrator state
            entry_for_response = {
                "id": 0,  # not saved in DB yet
                "user_id": user_id,
                "intensity": llm_result.get("intensity"),
                "plan": llm_result.get("plan", []),
                "warnings": llm_result.get("warnings", []),
                "recovery_advice": llm_result.get("recovery_advice"),
                "llm_response": llm_result.get("llm_response", ""),
                "date_created": datetime.utcnow(),
            }

            recommendation = {
                "intensity": entry_for_response["intensity"],
                "plan": entry_for_response["plan"],
                "warnings": entry_for_response["warnings"],
                "recovery_advice": entry_for_response["recovery_advice"],
            }
            llm_response = entry_for_response["llm_response"]
            entry_id = entry_for_response["id"]
            date_created = entry_for_response["date_created"]

        # -----------------------------
        # 3️⃣ Update orchestrator state
        # -----------------------------
        # state["exercise_plan"] = {
        #     "id": entry_id,
        #     "user_id": user_id,
        #     "heart_rate": health_metrics.get("heart_rate"),
        #     "spo2": health_metrics.get("spo2"),
        #     "bp_systolic": health_metrics.get("bp_systolic"),
        #     "bp_diastolic": health_metrics.get("bp_diastolic"),
        #     "steps": health_metrics.get("steps"),
        #     "workout_duration_minutes": health_metrics.get("workout_duration_minutes"),
        #     "llm_response": llm_response,
        #     "intensity": recommendation.get("intensity"),
        #     "plan": recommendation.get("plan", []),
        #     "warnings": recommendation.get("warnings", []),
        #     "recovery_advice": recommendation.get("recovery_advice"),
        #     "date_created": date_created,
        # }

        logger.info(f"Exercise Agent completed for user_id={user_id}")
        return state

    except Exception as e:
        logger.exception(
            f"Exercise Agent failed for user_id={state.get('user_profile', {}).get('user_id')}"
        )
        raise ExerciseAgentError(str(e)) from e
# """
# Exercise Agent Implementation with DB check.
# Generates personalized exercise recommendations based on daily health metrics.
# """

# from datetime import datetime
# from app.orchestrator.state import OrchestratorState
# from app.agents.exercise.recommendation import recommend_exercise
# from app.crud.exercise import get_today_exercise_entry
# from app.database import get_db
# from app.core.logging_config import setup_logger
# from app.core.exceptions import ExerciseAgentError
# from app.models.health import HealthMetrics

# logger = setup_logger(__name__)


# def exercise_agent(state: OrchestratorState) -> OrchestratorState:
#     """
#     Generates exercise recommendation based on daily health metrics.
#     Checks DB first for today's entry; if none, generates a new one via LLM.

#     Args:
#         state (OrchestratorState): Current orchestrator state.

#     Returns:
#         OrchestratorState: Updated state with exercise recommendation.
#     """
#     try:
#         user_profile = state.get("user_profile", {})
#         user_id = user_profile.get("user_id")
#         if not user_id:
#             raise ValueError("Missing user_id in user_profile")

#         db = next(get_db())

#         # -----------------------------
#         # 1️⃣ Fetch latest health metrics
#         # -----------------------------
#         latest_health: HealthMetrics = (
#             db.query(HealthMetrics)
#             .filter(HealthMetrics.user_id == user_id)
#             .order_by(HealthMetrics.timestamp.desc())
#             .first()
#         )

#         if not latest_health:
#             logger.warning(f"No health metrics found for user_id={user_id}")
#             return state  # Cannot generate recommendation

#         health_metrics = {
#             "heart_rate": latest_health.heart_rate,
#             "spo2": latest_health.spo2,
#             "bp_systolic": latest_health.bp_systolic,
#             "bp_diastolic": latest_health.bp_diastolic,
#             "steps": latest_health.steps,
#             "workout_duration_minutes": latest_health.workout_duration_minutes,
#         }
#         logger.info(f"Latest health metrics fetched")

#         # -----------------------------
#         # 2️⃣ Check if today's exercise entry exists
#         # -----------------------------
#         today_entry = get_today_exercise_entry(db, user_id) 

#         if today_entry:
#             logger.info(f"Using existing exercise entry for user_id={user_id}")
#             entry_for_response = today_entry
#             recommendation = {
#                 "intensity": today_entry.intensity,
#                 "plan": today_entry.plan or [],
#                 "warnings": today_entry.warnings or [],
#                 "recovery_advice": today_entry.recovery_advice,
#             }
#             llm_response = today_entry.llm_response
#         else:
#             # -----------------------------
#             # 3️⃣ Generate new recommendation via LLM
#             # -----------------------------
#             logger.info(f"No entry for today. Generating new recommendation for user_id={user_id}")
#             entry_for_response = recommend_exercise(user_id=user_id, metrics=health_metrics)
#             recommendation = {
#                 "intensity": entry_for_response.get("intensity"),
#                 "plan": entry_for_response.get("plan", []),
#                 "warnings": entry_for_response.get("warnings", []),
#                 "recovery_advice": entry_for_response.get("recovery_advice"),
#             }
#             llm_response = entry_for_response.get("llm_response", "")

#         # -----------------------------
#         # 4️⃣ Update orchestrator state
#         # -----------------------------
#         # state["exercise_plan"] = {
#         #     "id": getattr(entry_for_response, "id", 0),
#         #     "user_id": getattr(entry_for_response, "user_id", user_id),
#         #     "heart_rate": health_metrics.get("heart_rate"),
#         #     "spo2": health_metrics.get("spo2"),
#         #     "bp_systolic": health_metrics.get("bp_systolic"),
#         #     "bp_diastolic": health_metrics.get("bp_diastolic"),
#         #     "steps": health_metrics.get("steps"),
#         #     "workout_duration_minutes": health_metrics.get("workout_duration_minutes"),
#         #     "llm_response": llm_response,
#         #     "intensity": recommendation.get("intensity"),
#         #     "plan": recommendation.get("plan", []),
#         #     "warnings": recommendation.get("warnings", []),
#         #     "recovery_advice": recommendation.get("recovery_advice"),
#         #     "date_created": getattr(entry_for_response, "date_created", datetime.utcnow()),
#         # }

#         logger.info(f"Exercise Agent completed for user_id={user_id}")
#         return state

#     except Exception as e:
#         logger.exception(f"Exercise Agent failed for user_id={state.get('user_profile', {}).get('user_id')}")
#         raise ExerciseAgentError(str(e)) from e
