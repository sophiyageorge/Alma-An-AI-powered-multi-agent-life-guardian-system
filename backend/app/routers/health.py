"""
Health Metrics API Routes
-------------------------

Provides endpoints for managing user health metrics.
These endpoints are used by wearable integrations,
manual user input, and AI health agents.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.schemas.health import (
    HealthMetricsCreate,
    HealthMetricsUpdate,
    HealthMetricsResponse
)

from app.crud.health import (
    create_health_metric,
    get_health_metric_by_id,
    get_today_health_metrics,
    get_user_health_history,
    update_health_metric,
    delete_health_metric
)

from app.models.health import HealthMetrics

from app.core.logging_config import setup_logger

logger = setup_logger(__name__)

router = APIRouter(
    prefix="/health-metrics",
    tags=["Health Metrics"]
)


# ---------------------------------------------------------
# Create Health Metric
# ---------------------------------------------------------

@router.post(
    "/",
    response_model=HealthMetricsResponse,
    summary="Create health metrics entry"
)
def create_metric(
    data: HealthMetricsCreate,
    db: Session = Depends(get_db)
):
    """
    Insert a new health metrics entry.
    """

    metric = create_health_metric(db, data)

    return metric


# ---------------------------------------------------------
# Get Health Metric By ID
# ---------------------------------------------------------

@router.get(
    "/{metric_id}",
    response_model=HealthMetricsResponse,
    summary="Get health metric by ID"
)
def get_metric(
    metric_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a single health metric entry.
    """

    metric = get_health_metric_by_id(db, metric_id)

    if not metric:
        raise HTTPException(
            status_code=404,
            detail="Health metric not found"
        )

    return metric


# ---------------------------------------------------------
# Get Today's Health Metrics
# ---------------------------------------------------------

@router.get(
    "/user/{user_id}/today",
    response_model=HealthMetricsResponse,
    summary="Get today's health metrics"
)
def get_today_metrics(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve today's health metrics for a user.
    Used by the Health Agent.
    """

    metrics = get_today_health_metrics(db, user_id)

    return metrics


# ---------------------------------------------------------
# Get User Health History
# ---------------------------------------------------------

@router.get(
    "/user/{user_id}/history",
    response_model=List[HealthMetricsResponse],
    summary="Get health history"
)
def get_health_history(
    user_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Retrieve historical health metrics for a user.
    """

    history = get_user_health_history(db, user_id, limit)

    return history


# ---------------------------------------------------------
# Update Health Metric
# ---------------------------------------------------------

@router.put(
    "/{metric_id}",
    response_model=HealthMetricsResponse,
    summary="Update health metric"
)
def update_metric(
    metric_id: int,
    data: HealthMetricsUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing health metric entry.
    """

    metric = update_health_metric(db, metric_id, data)

    if not metric:
        raise HTTPException(
            status_code=404,
            detail="Health metric not found"
        )

    return metric


# ---------------------------------------------------------
# Delete Health Metric
# ---------------------------------------------------------

@router.delete(
    "/{metric_id}",
    summary="Delete health metric"
)
def delete_metric(
    metric_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a health metric entry.
    """

    success = delete_health_metric(db, metric_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Health metric not found"
        )

    return {"message": "Health metric deleted successfully"}


#     from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.database import get_db

# from sqlalchemy import func

# router = APIRouter()

@router.get("/health/last-week")
def get_last_week_health(user_id: int, db: Session = Depends(get_db)):
    """
    Returns health metrics for the last 7 days.
    """
    start_date = datetime.utcnow() - timedelta(days=7)

    rows = db.query(HealthMetrics).filter(
        HealthMetrics.user_id == user_id,
        HealthMetrics.timestamp >= start_date
    ).order_by(HealthMetrics.timestamp).all()

    result = [
        {
            "timestamp": row.timestamp,
            "heart_rate": row.heart_rate,
            "spo2": row.spo2,
            "bp_systolic": row.bp_systolic,
            "bp_diastolic": row.bp_diastolic
        }
        for row in rows
    ]

    return result

@router.get("/health/last-month")
def get_last_month_health(user_id: int, db: Session = Depends(get_db)):
    """
    Returns health metrics for the last 30 days.
    """
    start_date = datetime.utcnow() - timedelta(days=30)

    rows = db.query(HealthMetrics).filter(
        HealthMetrics.user_id == user_id,
        HealthMetrics.timestamp >= start_date
    ).order_by(HealthMetrics.timestamp).all()

    result = [
        {
            "timestamp": row.timestamp,
            "heart_rate": row.heart_rate,
            "spo2": row.spo2,
            "bp_systolic": row.bp_systolic,
            "bp_diastolic": row.bp_diastolic
        }
        for row in rows
    ]

    return result