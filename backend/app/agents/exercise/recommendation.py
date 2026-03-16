"""
Exercise Recommendation Service

Uses LLM to generate safe exercise plans based on health metrics.
Stores recommendations in database via CRUD layer.
"""

import json
import re

from app.llm.llm_client import llm
from app.agents.exercise.prompt import build_exercise_prompt
from app.crud.exercise import save_exercise_entry
from app.core.logging_config import setup_logger
from app.core.exceptions import ExerciseAgentError


logger = setup_logger(__name__)


def _parse_llm_json(response: str) -> dict:
    """
    Extract JSON safely from LLM output.
    """

    try:
        cleaned = re.sub(r"```json|```", "", response).strip()

        # Extract JSON block
        json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found in LLM response")

        data = json.loads(json_match.group())

        return data

    except Exception:
        logger.warning("Failed to parse LLM JSON response")
        raise


def _fallback_plan() -> dict:
    """
    Safe fallback exercise plan.
    """
 
    return {
        "intensity": "low",
        "plan": [
            "5-10 minutes light stretching",
            "10 minutes slow walking",
            "Breathing exercises"
        ],
        "warnings": [
            "Health metrics unavailable or LLM response invalid",
            "Consult a healthcare professional before intense exercise"
        ],
        "recovery_advice": "Stay hydrated and rest if discomfort occurs"
    }


def recommend_exercise(user_id: int, metrics: dict | None, db) -> dict:
    """
    Generate exercise recommendation using LLM.

    Args:
        user_id: user id
        metrics: health metrics dictionary
        db: database session

    Returns:
        dict: structured exercise recommendation
    """

    try:

        logger.info(f"Starting exercise recommendation for user {user_id}")

        # ------------------------------------------------
        # 1️⃣ Build prompt
        # ------------------------------------------------

        prompt = build_exercise_prompt(metrics)

        # ------------------------------------------------
        # 2️⃣ Call LLM
        # ------------------------------------------------

        response = llm.invoke(prompt)

        if isinstance(response, str):
            llm_text = response
        else:
            llm_text = getattr(response, "content", str(response))

        logger.debug(f"Raw LLM response: {llm_text}")

        # ------------------------------------------------
        # 3️⃣ Parse response
        # ------------------------------------------------

        try:

            recommendation = _parse_llm_json(llm_text)

            recommendation.setdefault("intensity", "moderate")
            recommendation.setdefault("plan", [])
            recommendation.setdefault("warnings", [])
            recommendation.setdefault("recovery_advice", "")

        except Exception:

            recommendation = _fallback_plan()

        # ------------------------------------------------
        # 4️⃣ Save to database
        # ------------------------------------------------

        entry = save_exercise_entry(
            db=db,
            user_id=user_id,
            llm_response=llm_text,
            recommendation=recommendation,
            health_metric_id=metrics.id if metrics else None
        )

        logger.info(f"Exercise recommendation saved id={entry.id}")

        # ------------------------------------------------
        # 5️⃣ Return  exercise plan
        # ------------------------------------------------

        return {
            "id": entry.id,
            "intensity": recommendation["intensity"],
            "plan": recommendation["plan"],
            "warnings": recommendation["warnings"],
            "recovery_advice": recommendation["recovery_advice"],
            "llm_response": llm_text,
            "date_created": entry.created_at,
        }

    except Exception as e:

        logger.exception(
            f"Exercise recommendation failed for user_id={user_id}"
        )

        raise ExerciseAgentError(str(e)) from e