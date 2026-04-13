import json
import re
from app.llm.llm_client import llm
from app.agents.exercise.prompt import build_exercise_prompt
from app.crud.exercise import save_exercise_entry, update_exercise_entry, get_today_exercise_entry
from app.core.logging_config import setup_logger
from app.core.exceptions import ExerciseAgentError

logger = setup_logger(__name__)

def _parse_llm_json(response: str) -> dict:
    """
    Extract JSON safely from LLM output.
    """
    try:
        # 1. Clean markdown if present
        cleaned = re.sub(r"```json|```", "", response).strip()

        # 2. Parse the string into a dict
        data = json.loads(cleaned)
        return data

    except Exception as e:
        logger.warning(f"Failed to parse LLM JSON: {e}")
        # If parsing fails, we return the fallback
        return _fallback_plan()

def _fallback_plan() -> dict:
    return {
        "safety_assessment": "System fallback due to technical error.",
        "intensity": "low",
        "plan": [{"activity": "Light stretching", "duration": "10 mins", "notes": "Safe movement"}],
        "warnings": ["Technical error occurred. Consult a doctor before proceeding."],
        "recovery_advice": "Stay hydrated and rest.",
        "medical_disclaimer": "I am an AI assistant and not a medical professional."
    }

def recommend_exercise(user_id: int, metrics: dict | None, db) -> dict:
    try:
        logger.info(f"Starting exercise recommendation for user {user_id}")

        # 1. Build prompt
        prompt = build_exercise_prompt(metrics)

        # 2. Call LLM
        response = llm.invoke(prompt)

        # 3. Ensure response is a string (llm.invoke returns raw content)
        llm_text = response if isinstance(response, str) else str(response)

        # 4. Parse the response for logic, but keep the raw text for DB
        recommendation = _parse_llm_json(llm_text)

        # 5. Check if today's entry exists
        today_entry = get_today_exercise_entry(db, user_id)
        
        # 6. Prepare data for DB (Ensure raw response is a clean string)
        clean_llm_string = llm_text.strip()

        if today_entry:
            logger.info(f"Updating existing exercise entry | id={today_entry.id}")
            entry = update_exercise_entry(
                db=db,
                entry_id=today_entry.id,
                llm_response=clean_llm_string, # Save as string
                recommendation=recommendation,  # CRUD handles dict->JSON if configured
                health_metric_id=metrics.get("id") if metrics else None
            )
        else:
            logger.info(f"Saving new exercise entry for user {user_id}")
            entry = save_exercise_entry(
                db=db,
                user_id=user_id,
                llm_response=clean_llm_string, # Save as string
                recommendation=recommendation,
                health_metric_id=metrics.get("id") if metrics else None
            )

        # 7. Return structured dictionary
        return {
            "id": entry.id,
            "intensity": recommendation.get("intensity", "low"),
            "plan": recommendation.get("plan", []),
            "warnings": recommendation.get("warnings", []),
            "recovery_advice": recommendation.get("recovery_advice", ""),
            "llm_response": clean_llm_string,
            "date_created": entry.created_at,
        }

    except Exception as e:
        logger.exception(f"Exercise recommendation failed for user_id={user_id}")
        raise ExerciseAgentError(str(e)) from e

# """
# Exercise Recommendation Service

# Uses LLM to generate safe exercise plans based on health metrics.
# Stores recommendations in database via CRUD layer.
# """

# import json
# import re

# from app.llm.llm_client import llm
# from app.agents.exercise.prompt import build_exercise_prompt
# from app.crud.exercise import save_exercise_entry,update_exercise_entry,get_today_exercise_entry
# from app.core.logging_config import setup_logger
# from app.core.exceptions import ExerciseAgentError


# logger = setup_logger(__name__)


# def _parse_llm_json(response: str) -> dict:
#     """
#     Extract JSON safely from LLM output.
#     """

#     try:
#         cleaned = re.sub(r"```json|```", "", response).strip()

#         # Extract JSON block
#         json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)

#         if not json_match:
#             raise ValueError("No JSON found in LLM response")

#         data = json.loads(json_match.group())

#         return data

#     except Exception:
#         logger.warning("Failed to parse LLM JSON response")
#         raise


# def _fallback_plan() -> dict:
#     """
#     Safe fallback exercise plan.
#     """
 
#     return {
#         "intensity": "low",
#         "plan": [
#             "5-10 minutes light stretching",
#             "10 minutes slow walking",
#             "Breathing exercises"
#         ],
#         "warnings": [
#             "Health metrics unavailable or LLM response invalid",
#             "Consult a healthcare professional before intense exercise"
#         ],
#         "recovery_advice": "Stay hydrated and rest if discomfort occurs"
#     }


# def recommend_exercise(user_id: int, metrics: dict | None, db) -> dict:
#     """
#     Generate exercise recommendation using LLM.

#     Args:
#         user_id: user id
#         metrics: health metrics dictionary
#         db: database session

#     Returns:
#         dict: structured exercise recommendation
#     """

#     try:

#         logger.info(f"Starting exercise recommendation for user {user_id}")

#         # ------------------------------------------------
#         # 1️⃣ Build prompt
#         # ------------------------------------------------

#         prompt = build_exercise_prompt(metrics)

#         # ------------------------------------------------
#         # 2️⃣ Call LLM
#         # ------------------------------------------------

#         response = llm.invoke(prompt)

#         if isinstance(response, str):
#             llm_text = response
#         else:
#             llm_text = getattr(response, "content", str(response))

#         logger.debug(f"Raw LLM response: {llm_text}")

#         # ------------------------------------------------
#         # 3️⃣ Parse response
#         # ------------------------------------------------

#         try:

#             recommendation = _parse_llm_json(llm_text)

#             recommendation.setdefault("intensity", "moderate")
#             recommendation.setdefault("plan", [])
#             recommendation.setdefault("warnings", [])
#             recommendation.setdefault("recovery_advice", "")

#         except Exception:

#             recommendation = _fallback_plan()


#         today_entry = get_today_exercise_entry(db, user_id)
#         clean_llm = re.sub(r"```json|```", "", llm_text).strip()
#         if today_entry:
#              # ------------------------------------------------
#         # 4️⃣  Update database
#         # ------------------------------------------------

#             entry = update_exercise_entry(
#                 db=db,
#                 entry_id=today_entry.id,
#                 llm_response=clean_llm,
#                 recommendation=recommendation,
#                 health_metric_id=metrics["id"] if metrics else None
#             )
#             logger.info(f"Exercise recommendation updated id={entry.id}") 
#         else:
#              # ------------------------------------------------
#         # 4️⃣ Save to database
#         # ------------------------------------------------

#             entry = save_exercise_entry(
#                 db=db,
#                 user_id=user_id,
#                 llm_response=clean_llm,
#                 recommendation=recommendation,
#                 health_metric_id=metrics.id if metrics else None
#             )

    

#             logger.info(f"Exercise recommendation saved id={entry.id}")

#         # ------------------------------------------------
#         # 5️⃣ Return  exercise plan
#         # ------------------------------------------------

#         return {
#             "id": entry.id,
#             "intensity": recommendation["intensity"],
#             "plan": recommendation["plan"],
#             "warnings": recommendation["warnings"],
#             "recovery_advice": recommendation["recovery_advice"],
#             "llm_response": clean_llm,
#             "date_created": entry.created_at,
#         }

#     except Exception as e:

#         logger.exception(
#             f"Exercise recommendation failed for user_id={user_id}"
#         )

#         raise ExerciseAgentError(str(e)) from e