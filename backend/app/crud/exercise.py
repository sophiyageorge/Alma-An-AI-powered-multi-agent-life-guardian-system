from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.exercise import ExerciseRecommendation
import json
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


# --------------------------
# Exercise DB Operations
# --------------------------

def save_exercise_entry(
    db: Session,
    user_id: int,
    llm_response: str,
    recommendation: dict,
    health_metric_id: int | None = None
) -> ExerciseRecommendation:
    """
    Save a new ExerciseRecommendation for a user.
    Associates with a health_metric record if provided; otherwise health_metric_id is None.

    Args:
        db (Session): SQLAlchemy DB session
        user_id (int): User ID
        llm_response (str): Raw LLM-generated recommendation text
        recommendation (dict): Structured recommendation (intensity, plan, warnings, recovery_advice)
        health_metric_id (int | None): Optional foreign key to health metric snapshot

    Returns:
        ExerciseRecommendation: The newly created DB entry
    """
    try:
        entry = ExerciseRecommendation(
            user_id=user_id,
            health_metric_id=health_metric_id,  # can be None
            llm_response=llm_response,
            intensity=recommendation.get("intensity"),
            plan=json.dumps(recommendation.get("plan", [])),
            warnings=json.dumps(recommendation.get("warnings", [])),
            recovery_advice=recommendation.get("recovery_advice"),
            created_at=datetime.utcnow()
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)

        logger.info(
            f"Exercise entry saved | user_id={user_id} | "
            f"health_metric_id={health_metric_id} | "
            f"intensity={entry.intensity}"
        )
        return entry

    except Exception as e:
        db.rollback()
        logger.exception(f"Failed to save exercise entry | user_id={user_id}")
        raise e


def get_today_exercise_entry(db: Session, user_id: int) -> ExerciseRecommendation | None:
    """
    Fetch today's ExerciseRecommendation for a user. Returns existing entry if found,
    otherwise returns None (so agent can generate a new recommendation).

    Args:
        db (Session): SQLAlchemy DB session
        user_id (int): User ID

    Returns:
        ExerciseRecommendation | None: Today's entry if exists
    """
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    try:
        existing_entry = db.query(ExerciseRecommendation).filter(
            ExerciseRecommendation.user_id == user_id,
            ExerciseRecommendation.created_at >= today_start,
            ExerciseRecommendation.created_at < today_end
        ).first()

        if existing_entry:
            logger.info(f"Found existing exercise entry for today | user_id={user_id} | entry_id={existing_entry.id}")
        else:
            logger.info(f"No exercise entry found for today | user_id={user_id}")

        return existing_entry

    except Exception as e:
        logger.exception(f"Failed to fetch today's exercise entry | user_id={user_id}")
        raise e