""" 
Health Metrics Schemas
----------------------

Pydantic schemas used for validation and serialization
of HealthMetrics data in FastAPI endpoints.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ---------------------------------------------------------
# Base Schema
# ---------------------------------------------------------

class HealthMetricsBase(BaseModel):
    """
    Base schema containing all health metric fields.
    Used for sharing common attributes across schemas.
    """

    heart_rate: Optional[int] = None
    spo2: Optional[int] = None
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None
    timestamp: Optional[datetime] = None


# ---------------------------------------------------------
# Create Schema (Insert)
# ---------------------------------------------------------

class HealthMetricsCreate(HealthMetricsBase):
    """
    Schema used when creating a new health metric entry.
    """
    pass

    # user_id: int


# ---------------------------------------------------------
# Update Schema
# ---------------------------------------------------------

class HealthMetricsUpdate(BaseModel):
    """
    Schema used for updating existing health metrics.
    All fields are optional to allow partial updates.
    """

    heart_rate: Optional[int] = None
    spo2: Optional[int] = None
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None
    steps: Optional[int] = None
    workout_duration_minutes: Optional[float] = None


# ---------------------------------------------------------
# Response Schema (Get)
# ---------------------------------------------------------

class HealthMetricsResponse(HealthMetricsBase):
    """
    Schema returned to clients when retrieving health metrics.
    """

    id: int
    # user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True


# ---------------------------------------------------------
# Delete Schema (Optional)
# ---------------------------------------------------------

class HealthMetricsDelete(BaseModel):
    """
    Schema used when deleting a health metric entry.
    """

    id: int