"""
Exercise Agent

Generates personalized exercise recommendations based on
health data already available in the orchestrator state.

Workflow
--------
1. Read health data from orchestrator state
2. Stop execution if emergency detected
3. Check if today's exercise plan exists in DB
4. If exists → return stored plan
5. If not → generate recommendation via LLM
6. If health data missing → generate safe plan with disclaimer
7. Update orchestrator state
"""

from datetime import datetime

from app.orchestrator.state import OrchestratorState
from app.agents.exercise.recommendation import recommend_exercise
from app.crud.exercise import get_today_exercise_entry

from app.core.logging_config import setup_logger
from app.core.exceptions import ExerciseAgentError


logger = setup_logger(__name__)


def exercise_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Exercise recommendation agent.

    Args:
        state (OrchestratorState): Shared orchestrator state

    Returns:
        OrchestratorState: Updated state containing exercise plan
    """

    try:
        logger.info("Exercise Agent started")

        db = state.get("db")
        user_profile = state.get("user_profile", {})
        user_id = user_profile.get("user_id")

        if not db or not user_id:
            raise ValueError("Missing db session or user_id")

        # ------------------------------------------------
        # 1️⃣ Stop if emergency detected
        # ------------------------------------------------

        if state.get("emergency_triggered"):
            logger.warning("Emergency detected. Skipping exercise generation.")
            return state

        # ------------------------------------------------
        # 2️⃣ Get health data from orchestrator state
        # ------------------------------------------------

        health_metrics = state.get("health_data")

        if not health_metrics:
            logger.warning("Health data missing. Generating safe recommendation.")

        # ------------------------------------------------
        # 3️⃣ Check if today's exercise plan exists
        # ------------------------------------------------

        today_entry = get_today_exercise_entry(db, user_id)

        if today_entry:

            logger.info("Using existing exercise recommendation")

            exercise_plan = {
                "id": today_entry.id,
                "user_id": today_entry.user_id,
                "intensity": today_entry.intensity,
                "plan": today_entry.plan or [],
                "warnings": today_entry.warnings or [],
                "recovery_advice": today_entry.recovery_advice,
                "llm_response": today_entry.llm_response,
                "date_created": today_entry.created_at,
            }

        else:

            logger.info("Generating new exercise recommendation")

            llm_result = recommend_exercise(
                user_id=user_id,
                metrics=health_metrics ,
                db=db
            )

            exercise_plan = {
                "id": None,
                "user_id": user_id,
                "intensity": llm_result.get("intensity"),
                "plan": llm_result.get("plan", []),
                "warnings": llm_result.get("warnings", []),
                "recovery_advice": llm_result.get("recovery_advice"),
                "llm_response": llm_result.get("llm_response"),
                "date_created": datetime.utcnow(),
            }

            # Optional disclaimer if health data missing
            if not health_metrics:
                exercise_plan["warnings"].append(
                    "Health metrics unavailable. Recommendation is generic and should be followed cautiously."
                )

        # ------------------------------------------------
        # 4️⃣ Update orchestrator state
        # ------------------------------------------------

        state["exercise_plan"] = exercise_plan

        logger.info(f"Exercise Agent completed for user_id={user_id}")

        return state

    except Exception as e:

        logger.exception(
            f"Exercise Agent failed for user_id={state.get('user_profile', {}).get('user_id')}"
        )

        raise ExerciseAgentError(str(e)) from e