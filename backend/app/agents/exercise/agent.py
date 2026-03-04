# """
# Exercise Agent Implementation.
# """

# from app.orchestrator.state import OrchestratorState
# from app.agents.exercise.recommendation import recommend_exercise
# from app.core.logging_config import setup_logger
# from app.core.exceptions import ExerciseAgentError

# logger = setup_logger(__name__)


# def exercise_agent(state: OrchestratorState) -> OrchestratorState:
#     """
#     Generates exercise recommendation based on daily health metrics.

#     Args:
#         state (OrchestratorState): Current orchestrator state.

#     Returns:
#         OrchestratorState: Updated state with exercise recommendation.
#     """

#     try:
#         health_metrics = state.get("health_metrics", {})

#         logger.info("Validating health metrics input")

#         required_fields = [
#             "heart_rate",
#             "spo2",
#             "bp_systolic",
#             "bp_diastolic",
#             "steps",
#             "workout_duration_minutes"
#         ]

#         for field in required_fields:
#             if field not in health_metrics:
#                 raise ValueError(f"Missing required field: {field}")

#         logger.info("Generating exercise recommendation")

#         recommendation = recommend_exercise(**health_metrics)

#         logger.info("Updating orchestrator state with exercise plan")

#         state["exercise_plan"] = {
#             "heart_rate": health_metrics["heart_rate"],
#             "steps": health_metrics["steps"],
#             "intensity": recommendation["intensity"],
#             "plan": recommendation["plan"],
#             "warnings": recommendation["warnings"],
#             "recovery_advice": recommendation["recovery_advice"]
#         }

#         logger.info("Exercise Agent completed successfully")

#         return state

#     except Exception as e:
#         logger.exception("Error occurred in Exercise Agent")
#         raise ExerciseAgentError(str(e)) from e

"""
Exercise Agent Implementation with DB check.
"""

from datetime import datetime, timedelta
from app.orchestrator.state import OrchestratorState
from app.agents.exercise.recommendation import recommend_exercise
from app.crud.exercise import get_today_exercise_entry, save_exercise_entry
from app.database import get_db
from app.core.logging_config import setup_logger
from app.core.exceptions import ExerciseAgentError

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
        health_metrics = state.get("health_data", {})
        user_profile = state.get("user_profile", {})
        user_id = user_profile.get("user_id")
        logger.info("Validating health metrics input")
        # required_fields = [
        #     "heart_rate",
        #     "spo2",
        #     "bp_systolic",
        #     "bp_diastolic",
        #     "steps",
        #     "workout_duration_minutes"
        # ]

        # for field in required_fields:
        #     if field not in health_metrics:
        #         raise ValueError(f"Missing required field: {field}")

        # user_id = health_metrics.get("user_id")
        # if user_id is None:
        #     raise ValueError("Missing required field: user_id")
        print("user id in exercise agent", user_id)
        db = next(get_db())

        # -----------------------------
        # 1️⃣ Check for today's entry
        # -----------------------------
        today_entry = get_today_exercise_entry(db,user_id,metrics=health_metrics)
        if today_entry:
            logger.info(f"Found existing exercise entry for user_id={user_id} today")
            recommendation = {

                "recovery_advice": today_entry.recovery_advice
            }
        else:
            # -----------------------------
            # 2️⃣ Generate new recommendation
            # -----------------------------
            logger.info("No entry for today, generating new recommendation via LLM")
            recommendation = recommend_exercise(user_id=user_id,metrics=health_metrics)

           

        # -----------------------------
        # 4️⃣ Update orchestrator state
        # -----------------------------
        state["exercise_plan"] = {
            "heart_rate": health_metrics["heart_rate"],
            "steps": health_metrics["steps"],
            "intensity": recommendation["intensity"],
            "plan": recommendation["plan"],
            "warnings": recommendation["warnings"],
            "recovery_advice": recommendation["recovery_advice"]
        }

        logger.info("Exercise Agent completed successfully")
        return state

    except Exception as e:
        logger.exception("Error occurred in Exercise Agent")
        raise ExerciseAgentError(str(e)) from e