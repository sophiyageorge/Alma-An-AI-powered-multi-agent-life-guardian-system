from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json

from app.database import get_db
from app.schemas.exercise import ExerciseEntryResponse
from app.orchestrator.store import orchestrator_store
from app.core.logging_config import setup_logger
from app.dependencies import get_current_user
from app.models.health import HealthMetrics
from app.crud.exercise import get_today_exercise_entry

router = APIRouter()
logger = setup_logger(__name__)


@router.get("/recommendation", response_model=ExerciseEntryResponse)
def get_exercise_recommendation(current_user=Depends(get_current_user),
                                db: Session = Depends(get_db)):
    try:
        logger.info("Received exercise recommendation request")
        user_id = current_user.user_id
        logger.info(f"Authenticated user_id: {user_id}")

        # Fetch orchestrator state
        orchestrator_state = orchestrator_store.get(user_id)
        if not orchestrator_state:
            logger.error(f"No orchestrator state found for user_id {user_id}")
            raise HTTPException(status_code=404, detail="User state not found. Please login first.")

        # Fetch latest health metrics for the authenticated user
        latest_health = (
            db.query(HealthMetrics)
            .filter(HealthMetrics.user_id == 1)  # fixed
            .order_by(HealthMetrics.timestamp.desc())
            .first()
        )

        if not latest_health:
            logger.warning(f"No health metrics found in DB for user_id={user_id}")
            raise HTTPException(status_code=404, detail="No health metrics found for user today")

        health_metrics = {
            "heart_rate": latest_health.heart_rate,
            "spo2": latest_health.spo2,
            "bp_systolic": latest_health.bp_systolic,
            "bp_diastolic": latest_health.bp_diastolic,
            "steps": latest_health.steps,
            "workout_duration_minutes": latest_health.workout_duration_minutes,
        }
        logger.info(f"Latest health metrics: {health_metrics}")

        # Check for today's exercise entry
        today_entry = get_today_exercise_entry(db, user_id)

        if today_entry:
            logger.info(f"Found existing exercise entry for user_id={user_id} today")
            entry_for_response = today_entry
            recommendation = {
                "intensity": today_entry.intensity,
                "plan": json.loads(today_entry.plan) if today_entry.plan else [],
                "warnings": json.loads(today_entry.warnings) if today_entry.warnings else [],
                "recovery_advice": today_entry.recovery_advice,
            }
            llm_response = today_entry.llm_response
        else:
            # No entry exists → return a default response or handle generation via LLM
            logger.warning(f"No exercise entry found for today | user_id={user_id}")
            # Provide empty/default response to avoid UnboundLocalError
            entry_for_response = None
            recommendation = {
                "intensity": None,
                "plan": [],
                "warnings": [],
                "recovery_advice": None
            }
            llm_response = ""

        # Build the response safely
        exercise_plan = {
            "id": getattr(entry_for_response, "id", 0) if entry_for_response else 0,
            "user_id": getattr(entry_for_response, "user_id", user_id) if entry_for_response else user_id,
            "heart_rate": getattr(entry_for_response, "heart_rate", health_metrics.get("heart_rate")) if entry_for_response else health_metrics.get("heart_rate"),
            "spo2": getattr(entry_for_response, "spo2", health_metrics.get("spo2")) if entry_for_response else health_metrics.get("spo2"),
            "bp_systolic": getattr(entry_for_response, "bp_systolic", health_metrics.get("bp_systolic")) if entry_for_response else health_metrics.get("bp_systolic"),
            "bp_diastolic": getattr(entry_for_response, "bp_diastolic", health_metrics.get("bp_diastolic")) if entry_for_response else health_metrics.get("bp_diastolic"),
            "steps": getattr(entry_for_response, "steps", health_metrics.get("steps")) if entry_for_response else health_metrics.get("steps"),
            "workout_duration_minutes": getattr(entry_for_response, "workout_duration_minutes", health_metrics.get("workout_duration_minutes")) if entry_for_response else health_metrics.get("workout_duration_minutes"),
            "llm_response": llm_response,
            "intensity": recommendation.get("intensity"),
            "plan": recommendation.get("plan", []),
            "warnings": recommendation.get("warnings", []),
            "recovery_advice": recommendation.get("recovery_advice"),
            "date_created": getattr(entry_for_response, "date_created", datetime.utcnow()) if entry_for_response else datetime.utcnow(),
        }

        logger.info("Returning exercise recommendation successfully")
        return exercise_plan

    except HTTPException as http_error:
        logger.error(f"HTTP error occurred: {http_error.detail}")
        raise http_error
    except Exception as e:
        logger.exception("Unexpected error in exercise recommendation endpoint")
        raise HTTPException(status_code=500, detail="Internal server error")
# # # from fastapi import APIRouter, Depends, HTTPException
# # # from sqlalchemy.orm import Session

# # # from app.database import get_db
# # # from app.orchestrator.state import OrchestratorState
# # # from app.orchestrator.graph import build_graph
# # # from app.schemas.exercise import ExerciseEntryResponse
# # # from app.schemas.exercise import ExerciseEntryCreate
# # # from app.core.logger import setup_logger
# # # from app.core.exceptions import ExerciseAgentError

# # # router = APIRouter()
# # # logger = setup_logger(__name__)

# # # orchestrator_state = OrchestratorState()

# # # @router.post("/recommendation", response_model=ExerciseEntryResponse)
# # # def get_exercise_recommendation(
# # #     metrics: ExerciseEntryCreate,
# # #     db: Session = Depends(get_db)
# # # ):
# # #     try:

# # #         # 1️⃣ Build orchestrator state
# # #        # assuming state is stored globally or in memory
        



# # #         exercise_plan = orchestrator_state.get("exercise_plan")

# # #         if not exercise_plan:
# # #             raise HTTPException(
# # #                 status_code=404,
# # #                 detail="Exercise recommendation not available yet"
# # #             )

# # #         return exercise_plan

# # #     except Exception as e:
# # #         raise HTTPException(status_code=500, detail=str(e))

# # from fastapi import APIRouter, Depends, HTTPException
# # from sqlalchemy.orm import Session

# # from app.database import get_db
# # from app.orchestrator.state import OrchestratorState
# # from app.orchestrator.graph import build_graph
# # from app.schemas.exercise import ExerciseEntryResponse, ExerciseEntryCreate
# # from app.orchestrator.store import orchestrator_store
# # from app.core.logging_config import setup_logger

# # router = APIRouter()
# # logger = setup_logger(__name__)

# # # graph = build_graph()


# # @router.post("/recommendation", response_model=ExerciseEntryResponse)
# # def get_exercise_recommendation(
# #     metrics: ExerciseEntryCreate,
# #     db: Session = Depends(get_db)
# # ):
# #     try:
# #         logger.info("Received exercise recommendation request")

# #         # 1️⃣ Log incoming metrics
# #         logger.info(f"Incoming metrics: {metrics}")

# #         user_id = metrics.user_id
# #         logger.info(f"Fetching orchestrator state for user_id: {user_id}")

# #         # 2️⃣ Fetch orchestrator state
# #         orchestrator_state = orchestrator_store.get(user_id)

# #         if not orchestrator_state:
# #             logger.error(f"No orchestrator state found for user_id {user_id}")
# #             raise HTTPException(
# #                 status_code=404,
# #                 detail="User state not found. Please login first."
# #             )

# #         logger.info("Orchestrator state fetched successfully")

# #         # 3️⃣ Extract exercise plan
# #         exercise_plan = orchestrator_state.get("exercise_plan")

# #         logger.info(f"Exercise plan fetched: {exercise_plan}")

# #         if not exercise_plan:
# #             logger.warning("Exercise recommendation not available yet")

# #             raise HTTPException(
# #                 status_code=404,
# #                 detail="Exercise recommendation not available yet"
# #             )

# #         logger.info("Returning exercise recommendation successfully")

# #         return exercise_plan

# #     except HTTPException as http_error:
# #         logger.error(f"HTTP error occurred: {http_error.detail}")
# #         raise http_error

# #     except Exception as e:
# #         logger.exception("Unexpected error in exercise recommendation endpoint")
# #         raise HTTPException(status_code=500, detail="Internal server error")

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.database import get_db
# from app.schemas.exercise import ExerciseEntryResponse
# from app.orchestrator.store import orchestrator_store
# from app.core.logging_config import setup_logger
# from app.dependencies import get_current_user
# from app.models.health import HealthMetrics
# from datetime import datetime
# from app.crud.exercise import get_today_exercise_entry


# router = APIRouter()
# logger = setup_logger(__name__)


# @router.get("/recommendation", response_model=ExerciseEntryResponse)
# def get_exercise_recommendation(current_user=Depends(get_current_user),
#     db: Session = Depends(get_db)
#     # current_user=Depends(get_current_user)
# ):
#     try:
#         logger.info("Received exercise recommendation request")

#         # 1️⃣ Get user_id from authenticated user
#         user_id = current_user.user_id
#         logger.info(f"Authenticated user_id: {user_id}")

#         # 2️⃣ Fetch orchestrator state
#         orchestrator_state = orchestrator_store.get(user_id)

#         if not orchestrator_state:
#             logger.error(f"No orchestrator state found for user_id {user_id}")
#             raise HTTPException(
#                 status_code=404,
#                 detail="User state not found. Please login first."

#             )

#         # db = next(get_db())

#         # -----------------------------
#         # 1️⃣ Get latest health metrics from DB
#         # -----------------------------
#         latest_health = (
#             db.query(HealthMetrics)
#             .filter(HealthMetrics.user_id == 1)
#             .order_by(HealthMetrics.timestamp.desc())
#             .first()
#         )

#         if not latest_health:
#             logger.warning(f"No health metrics found in DB for user_id={user_id}")
#             return state  # Cannot generate recommendation

#         health_metrics = {
#             "heart_rate": latest_health.heart_rate,
#             "spo2": latest_health.spo2,
#             "bp_systolic": latest_health.bp_systolic,
#             "bp_diastolic": latest_health.bp_diastolic,
#             "steps": latest_health.steps,
#             "workout_duration_minutes": latest_health.workout_duration_minutes,
#         }

#         logger.info(f"Latest health metrics: {health_metrics}")

#         # -----------------------------
#         # 2️⃣ Check for today's exercise entry
#         # -----------------------------
#         today_entry = get_today_exercise_entry(db, user_id)

#         if today_entry:
#             logger.info(f"Found existing exercise entry for user_id={user_id} today")
#             # Use DB entry as response
#             entry_for_response = today_entry
#             import json

#             recommendation = {
#                 "intensity": today_entry.intensity,
#                 "plan": json.loads(today_entry.plan) if today_entry.plan else [],
#                 "warnings": json.loads(today_entry.warnings) if today_entry.warnings else [],
#                 "recovery_advice": today_entry.recovery_advice,
#             }
#             llm_response = today_entry.llm_response

      

       

#         # -----------------------------
#         # 5️⃣ Prepare API response
#         # -----------------------------
#         exercise_plan = {
#             "id": getattr(entry_for_response, "id", 0),
#             "user_id": getattr(entry_for_response, "user_id", user_id),
#             "heart_rate": getattr(entry_for_response, "heart_rate", health_metrics.get("heart_rate")),
#             "spo2": getattr(entry_for_response, "spo2", health_metrics.get("spo2")),
#             "bp_systolic": getattr(entry_for_response, "bp_systolic", health_metrics.get("bp_systolic")),
#             "bp_diastolic": getattr(entry_for_response, "bp_diastolic", health_metrics.get("bp_diastolic")),
#             "steps": getattr(entry_for_response, "steps", health_metrics.get("steps")),
#             "workout_duration_minutes": getattr(entry_for_response, "workout_duration_minutes", health_metrics.get("workout_duration_minutes")),
#             "llm_response": llm_response,
#             "intensity": recommendation.get("intensity"),
#             "plan": recommendation.get("plan", []),
#             "warnings": recommendation.get("warnings", []),
#             "recovery_advice": recommendation.get("recovery_advice"),
#             "date_created": getattr(entry_for_response, "date_created", datetime.utcnow()),
#         }


#         logger.info("Exercise plan fetched successfully")

#         # 3️⃣ Extract exercise plan
#         # exercise_plan = orchestrator_state.get("exercise_response")

#         logger.info(f"Exercise plan fetched: {exercise_plan}")

#         if not exercise_plan:
#             logger.warning("Exercise recommendation not available yet")
#             raise HTTPException(
#                 status_code=404,
#                 detail="Exercise recommendation not available yet"
#             )

#         logger.info("Returning exercise recommendation successfully")

       

#         return exercise_plan

#     except HTTPException as http_error:
#         logger.error(f"HTTP error occurred: {http_error.detail}")
#         raise http_error

#     except Exception as e:
#         logger.exception("Unexpected error in exercise recommendation endpoint")
#         raise HTTPException(status_code=500, detail="Internal server error")