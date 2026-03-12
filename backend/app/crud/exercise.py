"""
Database helper functions for agents
------------------------------------

Provides CRUD operations for Exercise and Mental Health agents.
Includes logging, error handling, and structured comments.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.exercise import ExerciseEntry
from app.models.mental_health import JournalEntry
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
    metrics: dict,
    llm_response: str,
    recommendation: dict
) -> ExerciseEntry:
    """
    Save a new ExerciseEntry for a user with health metrics and LLM-generated recommendations.

    Args:
        db (Session): SQLAlchemy DB session
        user_id (int): User ID
        metrics (dict): Health metrics (heart_rate, spo2, bp, steps, etc.)
        llm_response (str): Raw LLM-generated recommendation text
        recommendation (dict): Structured recommendation (intensity, plan, warnings, recovery_advice)

    Returns:
        ExerciseEntry: The newly created DB entry
    """
    try:
        entry = ExerciseEntry(
            user_id=user_id,
            heart_rate=metrics.get("heart_rate"),
            spo2=metrics.get("spo2"),
            bp_systolic=metrics.get("bp_systolic"),
            bp_diastolic=metrics.get("bp_diastolic"),
            steps=metrics.get("steps"),
            workout_duration_minutes=metrics.get("workout_duration_minutes"),
            llm_response=llm_response,
            intensity=recommendation.get("intensity"),
            plan=json.dumps(recommendation.get("plan", [])),
            warnings=json.dumps(recommendation.get("warnings", [])),
            recovery_advice=recommendation.get("recovery_advice"),
            date_created=datetime.utcnow()
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)

        logger.info(f"Exercise entry saved | user_id={user_id} | intensity={entry.intensity} | steps={entry.steps}")
        return entry

    except Exception as e:
        db.rollback()
        logger.exception(f"Failed to save exercise entry | user_id={user_id}")
        raise e


def get_today_exercise_entry(
    db: Session,
    user_id: int
) -> ExerciseEntry:
    """
    Fetch today's ExerciseEntry for a user. Returns existing entry if found,
    otherwise returns None (so agent can generate a new recommendation).

    Args:
        db (Session): SQLAlchemy DB session
        user_id (int): User ID

    Returns:
        ExerciseEntry | None: Today's entry if exists
    """
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    try:
        existing_entry = db.query(ExerciseEntry).filter(
            ExerciseEntry.user_id == user_id,
            ExerciseEntry.date_created >= today_start,
            ExerciseEntry.date_created < today_end
        ).first()

        if existing_entry:
            logger.info(f"Found existing exercise entry for today | user_id={user_id} | entry_id={existing_entry.id}")
        else:
            logger.info(f"No exercise entry found for today | user_id={user_id}")

        return existing_entry

    except Exception as e:
        logger.exception(f"Failed to fetch today's exercise entry | user_id={user_id}")
        raise e
# """
# Database helper functions for agents.
# """

# from datetime import datetime,timedelta
# from sqlalchemy.orm import Session
# from app.models.exercise import ExerciseEntry
# from app.models.mental_health import  JournalEntry
# import json


# # --------------------------
# # Exercise DB operations
# # --------------------------

# def save_exercise_entry(db: Session, user_id: int, metrics: dict, llm_response: str, recommendation: dict) -> ExerciseEntry:
#     entry = ExerciseEntry(
#         user_id=user_id,
#         heart_rate=metrics.get("heart_rate"),
#         spo2=metrics.get("spo2"),
#         bp_systolic=metrics.get("bp_systolic"),
#         bp_diastolic=metrics.get("bp_diastolic"),
#         steps=metrics.get("steps"),
#         workout_duration_minutes=metrics.get("workout_duration_minutes"),
#         llm_response=llm_response,
#         intensity=recommendation.get("intensity"),
#         plan=json.dumps(recommendation.get("plan", [])),
#         warnings=json.dumps(recommendation.get("warnings", [])),
#         recovery_advice=recommendation.get("recovery_advice"),
#         date_created=datetime.utcnow()
#     )
#     db.add(entry)
#     db.commit()
#     db.refresh(entry)
#     return entry

# def get_today_exercise_entry(db: Session, user_id: int, metrics: dict) -> ExerciseEntry:
#     """
#     Check if an ExerciseEntry exists for today for the user.
#     If yes, return the existing entry.
#     If no, generate a new recommendation via LLM and save it.

#     Args:
#         db (Session): SQLAlchemy DB session
#         user_id (int): User ID
#         metrics (dict): Health metrics dictionary

#     Returns:
#         ExerciseEntry: Existing or newly created entry
#     """
#     # ---------------------------
#     # 1️⃣ Check for today’s entry
#     # ---------------------------
#     today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
#     today_end = today_start + timedelta(days=1)

#     existing_entry = db.query(ExerciseEntry).filter(
#         ExerciseEntry.user_id == user_id,
#         ExerciseEntry.date_created >= today_start,
#         ExerciseEntry.date_created < today_end
#     ).first()

#     if existing_entry:
#         return existing_entry

    