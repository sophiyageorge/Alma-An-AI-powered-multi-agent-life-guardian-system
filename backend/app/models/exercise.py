"""
SQLAlchemy model for Exercise Agent entries.
"""

from sqlalchemy import Column, BigInteger, Integer, Float, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class ExerciseEntry(Base):
    """
    Stores user health metrics and LLM-based exercise recommendations.
    """

    __tablename__ = "exercise_entries"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    heart_rate = Column(Integer, nullable=True)
    spo2 = Column(Integer, nullable=True)
    bp_systolic = Column(Integer, nullable=True)
    bp_diastolic = Column(Integer, nullable=True)
    steps = Column(Integer, nullable=True)
    workout_duration_minutes = Column(Float, nullable=True)
    llm_response = Column(Text, nullable=True)
    intensity = Column(String(50), nullable=True)
    plan = Column(Text, nullable=True)  # JSON stringified list
    warnings = Column(Text, nullable=True)  # JSON stringified list
    recovery_advice = Column(Text, nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"<ExerciseEntry(id={self.id}, user_id={self.user_id}, "
            f"intensity={self.intensity}, date_created={self.date_created})>"
        )