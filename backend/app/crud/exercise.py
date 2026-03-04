"""
Database helper functions for agents.
"""

from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from app.models.exercise import ExerciseEntry
from app.models.mental_health import  JournalEntry
import json


# --------------------------
# Exercise DB operations
# --------------------------

def save_exercise_entry(db: Session, user_id: int, metrics: dict, llm_response: str, recommendation: dict) -> ExerciseEntry:
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
    return entry

def get_today_exercise_entry(db: Session, user_id: int, metrics: dict) -> ExerciseEntry:
    """
    Check if an ExerciseEntry exists for today for the user.
    If yes, return the existing entry.
    If no, generate a new recommendation via LLM and save it.

    Args:
        db (Session): SQLAlchemy DB session
        user_id (int): User ID
        metrics (dict): Health metrics dictionary

    Returns:
        ExerciseEntry: Existing or newly created entry
    """
    # ---------------------------
    # 1️⃣ Check for today’s entry
    # ---------------------------
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    existing_entry = db.query(ExerciseEntry).filter(
        ExerciseEntry.user_id == user_id,
        ExerciseEntry.date_created >= today_start,
        ExerciseEntry.date_created < today_end
    ).first()

    if existing_entry:
        return existing_entry

    