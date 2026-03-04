"""
Pydantic schemas for Exercise Agent.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ExerciseEntryCreate(BaseModel):
    """
    Schema for creating a new exercise entry from frontend.
    """
    user_id: int = Field(..., description="ID of the user")
    heart_rate: Optional[int] = Field(None, description="Heart rate in bpm")
    spo2: Optional[int] = Field(None, description="Oxygen saturation %")
    bp_systolic: Optional[int] = Field(None, description="Systolic blood pressure")
    bp_diastolic: Optional[int] = Field(None, description="Diastolic blood pressure")
    steps: Optional[int] = Field(None, description="Step count today")
    workout_duration_minutes: Optional[float] = Field(None, description="Workout duration in minutes")


class ExerciseEntryResponse(BaseModel):
    """
    Schema for returning exercise entry including LLM recommendations.
    """
    id: int
    user_id: int
    heart_rate: Optional[int]
    spo2: Optional[int]
    bp_systolic: Optional[int]
    bp_diastolic: Optional[int]
    steps: Optional[int]
    workout_duration_minutes: Optional[float]
    llm_response: Optional[str]
    intensity: Optional[str]
    plan: Optional[List[str]] = Field(default_factory=list)
    warnings: Optional[List[str]] = Field(default_factory=list)
    recovery_advice: Optional[str]
    date_created: datetime

    class Config:
        orm_mode = True