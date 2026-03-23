from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import json


class ExerciseEntryCreate(BaseModel):
    """
    Schema for creating a new exercise entry from frontend.
    """
    user_id: Optional[int] = None
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
    # heart_rate: Optional[int]
    # spo2: Optional[int]
    # bp_systolic: Optional[int]
    # bp_diastolic: Optional[int]
    

    llm_response: Optional[str]
    intensity: Optional[str]

    plan: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    recovery_advice: Optional[str]

    date_created: datetime

    model_config = {"from_attributes": True}

    # @classmethod
    # def from_orm_with_json(cls, entry):
    #     """
    #     Convert SQLAlchemy ExerciseEntry to Pydantic schema,
    #     deserializing JSON string fields (plan, warnings) into lists.
    #     """
    #     plan = []
    #     warnings = []
    #     if entry.plan:
    #         try:
    #             plan = json.loads(entry.plan)
    #         except Exception:
    #             plan = []

    #     if entry.warnings:
    #         try:
    #             warnings = json.loads(entry.warnings)
    #         except Exception:
    #             warnings = []

    #     return cls(
    #         id=entry.id,
    #         user_id=entry.user_id,
    #         heart_rate=entry.heart_rate,
    #         spo2=entry.spo2,
    #         bp_systolic=entry.bp_systolic,
    #         bp_diastolic=entry.bp_diastolic,
    #         steps=entry.steps,
    #         workout_duration_minutes=entry.workout_duration_minutes,
    #         llm_response=entry.llm_response,
    #         intensity=entry.intensity,
    #         plan=plan,
    #         warnings=warnings,
    #         recovery_advice=entry.recovery_advice,
    #         date_created=entry.date_created
    #     )