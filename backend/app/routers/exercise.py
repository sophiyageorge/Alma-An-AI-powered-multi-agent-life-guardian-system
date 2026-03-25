from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import json
from typing import Optional, Dict, Any

from app.database import get_db
from app.schemas.exercise import ExerciseEntryResponse
from app.orchestrator.store import orchestrator_store
from app.core.logging_config import setup_logger
from app.dependencies import get_current_user
from app.models.health import HealthMetrics
from app.crud.exercise import get_today_exercise_entry

router = APIRouter()
logger = setup_logger(__name__)


def safe_json_load(data: Optional[str]) -> list:
    """
    Safely parse JSON string into Python list.

    Args:
        data (Optional[str]): JSON string.

    Returns:
        list: Parsed list or empty list if invalid.
    """
    if not data:
        return []
    try:
        parsed = json.loads(data)

        # ✅ Ensure list of strings
        if isinstance(parsed, list):
            return [str(item) for item in parsed]

        return []
    except json.JSONDecodeError:
        logger.warning("Invalid JSON format encountered.")
        return []


@router.get("/recommendation", response_model=ExerciseEntryResponse)
def get_exercise_recommendation(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Get today's exercise recommendation for the authenticated user.

    Workflow:
    - Validate user session via orchestrator state
    - Fetch latest health metrics
    - Retrieve today's exercise entry (if exists)
    - Build and return structured response

    Args:
        current_user: Authenticated user dependency
        db (Session): Database session

    Returns:
        Dict[str, Any]: Exercise recommendation response

    Raises:
        HTTPException: If user state or health data is missing
    """
    user_id = current_user.user_id
    logger.info("Exercise recommendation request received", extra={"user_id": user_id})

    try:
        
        
        # Fetch latest health metrics
        latest_health = (
            db.query(HealthMetrics)
            .filter(HealthMetrics.user_id == user_id)  # ✅ FIXED
            .order_by(HealthMetrics.timestamp.desc())
            .first()
        )
        
        
        if not latest_health:
            logger.warning("No health metrics found", extra={"user_id": user_id})


        # Fetch today's exercise entry
        today_entry = get_today_exercise_entry(db, user_id)
 
        if today_entry:
            logger.info("Existing exercise entry found", extra={"user_id": user_id})

            recommendation = {
                "intensity": today_entry.intensity,
                "plan": safe_json_load(today_entry.plan),
                "warnings": safe_json_load(today_entry.warnings),
                "recovery_advice": today_entry.recovery_advice,
            }

            entry_data = {
                "id": today_entry.id,
                "user_id": today_entry.user_id,
                "health_metric_id":today_entry.id,
                "llm_response": today_entry.llm_response,
                "date_created": today_entry.created_at,
            }

        else:
            logger.warning("No exercise entry found for today", extra={"user_id": user_id})

            recommendation = {
                "intensity": None,
                "plan": [],
                "warnings": [],
                "recovery_advice": None,
            }

            entry_data = {
                "id": 0,
                "user_id": user_id,
                "llm_response": "",
                "date_created": datetime.utcnow(),
            }

        # Final response
        response = {
            **entry_data,
            **recommendation,
        }

        logger.info("Exercise recommendation returned successfully", extra={"user_id": user_id})

        return response

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception(
            "Unexpected error in exercise recommendation",
            extra={"user_id": user_id},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )