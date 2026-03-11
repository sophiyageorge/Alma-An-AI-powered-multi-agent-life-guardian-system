"""
Exercise Agent: LLM-based recommendations for health metrics.
"""

import json
import re
from app.llm.llm_client import llm
from app.agents.exercise.prompt import build_exercise_prompt
from app.crud.exercise import save_exercise_entry
from app.database import get_db
from app.core.logging_config import setup_logger
from app.core.exceptions import ExerciseAgentError

logger = setup_logger(__name__)


def recommend_exercise(user_id: int, metrics: dict) -> dict:
    """
    Main Exercise Agent function.

    Generate structured exercise recommendations via LLM and store in DB.

    Args:
        user_id (int): ID of the user
        metrics (dict): Health metrics including heart_rate, spo2, bp, steps, workout duration

    Returns:
        dict: Exercise recommendation dict, ready for orchestrator state or API response
    """

    try:
        logger.info(f"Starting exercise recommendation for user_id={user_id}")
        logger.info(f"Received health metrics: {metrics}")

        db = next(get_db())

        # 1️⃣ Build prompt
        logger.info("Building exercise prompt for LLM")
        prompt = build_exercise_prompt(metrics)

        # 2️⃣ Call LLM
        logger.info("Invoking LLM for exercise recommendation")
        llm_response = llm.invoke(prompt)
        logger.debug(f"Raw LLM response: {llm_response}")

        # 3️⃣ Parse LLM response
        try:
            # Remove markdown ```json wrapper
            cleaned = re.sub(r"```json|```", "", llm_response).strip()
            recommendation = json.loads(cleaned)

            # Ensure required fields exist
            recommendation.setdefault("intensity", "moderate")
            recommendation.setdefault("plan", [])
            recommendation.setdefault("warnings", [])
            recommendation.setdefault("recovery_advice", "")

            logger.info("LLM response successfully parsed as JSON")

        except Exception as e:
            logger.warning(f"LLM response parsing failed: {e}")

            # Fallback recommendation
            recommendation = {
                "intensity": "moderate",
                "plan": [],
                "warnings": [],
                "recovery_advice": str(llm_response)
            }

        logger.debug(f"Parsed recommendation: {recommendation}")

        # 4️⃣ Save to DB
        logger.info(f"Saving exercise recommendation to database for user_id={user_id}")
        entry = save_exercise_entry(
            db=db,
            user_id=user_id,
            metrics=metrics,
            llm_response=llm_response,
            recommendation=recommendation
        )
        logger.info(f"Exercise entry saved successfully with id={entry.id}")

        # 5️⃣ Return structured dict for orchestrator/API
        result = {
            "id": entry.id,
            "user_id": entry.user_id,
            "heart_rate": entry.heart_rate,
            "spo2": entry.spo2,
            "bp_systolic": entry.bp_systolic,
            "bp_diastolic": entry.bp_diastolic,
            "steps": entry.steps,
            "workout_duration_minutes": entry.workout_duration_minutes,
            "llm_response": entry.llm_response,
            "intensity": recommendation.get("intensity"),
            "plan": recommendation.get("plan", []),
            "warnings": recommendation.get("warnings", []),
            "recovery_advice": recommendation.get("recovery_advice"),
            "date_created": entry.date_created
        }

        return result

    except Exception as e:
        logger.exception(f"Error occurred in exercise recommendation agent for user_id={user_id}")
        raise ExerciseAgentError(str(e)) from e
# """
# Exercise Agent: LLM-based recommendations for health metrics.
# """

# import json
# import re
# from app.llm.llm_client import llm
# from app.agents.exercise.prompt import build_exercise_prompt
# from app.crud.exercise import save_exercise_entry
# from app.database import get_db
# from app.core.logging_config import setup_logger
# from app.core.exceptions import ExerciseAgentError

# logger = setup_logger(__name__)


# def recommend_exercise(user_id: int, metrics: dict) -> dict:
#     """
#     Main Exercise Agent function.

#     Generate structured exercise recommendations via LLM and store in DB.

#     Args:
#         user_id (int): ID of the user
#         metrics (dict): Health metrics including heart_rate, spo2, bp, steps, workout duration

#     Returns:
#         dict: Structured exercise recommendation
#     """

#     try:
#         logger.info(f"Starting exercise recommendation for user_id={user_id}")
#         logger.info(f"Received health metrics: {metrics}")

#         db = next(get_db())

#         # 1️⃣ Build prompt
#         logger.info("Building exercise prompt for LLM")
#         # prompt = build_exercise_prompt(metrics)

        
#         logger.info("Building exercise prompt for LLM")
#         prompt = build_exercise_prompt(metrics)

#         logger.info("Invoking LLM for exercise recommendation")
#         llm_response = llm.invoke(prompt)

#         logger.debug(f"Raw LLM response: {llm_response}")

#         try:
#             # Remove markdown ```json ``` wrapper
#             cleaned = re.sub(r"```json|```", "", llm_response).strip()

#             recommendation = json.loads(cleaned)

#             logger.info("LLM response successfully parsed as JSON")

#         except Exception as e:

#             logger.warning("LLM response parsing failed")

#             recommendation = {
#                 "intensity": "moderate",
#                 "plan": [],
#                 "warnings": [],
#                 "recovery_advice": str(llm_response)
#             }

#         logger.debug(f"Parsed recommendation: {recommendation}")


#         logger.info("Saving exercise recommendation to database")

#         entry = save_exercise_entry(
#             db,
#             user_id,
#             metrics,
#             llm_response,
#             recommendation
#         )

#         logger.info(f"Exercise entry saved successfully with id={entry.id}")

#         return entry

#     except Exception as e:
#         logger.exception("Error occurred in exercise recommendation agent")
#         raise ExerciseAgentError(str(e)) from e
