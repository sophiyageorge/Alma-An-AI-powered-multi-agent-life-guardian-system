"""
Health Metrics CRUD Operations
------------------------------

Handles database operations for the HealthMetrics model.
Used by the Health Agent and API routes.
"""

from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta

from app.models.health import HealthMetrics
from app.schemas.health import (
    HealthMetricsCreate,
    HealthMetricsUpdate
)

from app.core.logging_config import setup_logger

logger = setup_logger(__name__)


# ---------------------------------------------------------
# Create Health Metric
# ---------------------------------------------------------

def create_health_metric(db: Session, data: HealthMetricsCreate,user_id:int):
    """
    Insert a new health metrics entry.
    """

    metric = HealthMetrics(

        user_id=user_id,
        heart_rate=data.heart_rate,
        spo2=data.spo2,
        bp_systolic=data.bp_systolic,
        bp_diastolic=data.bp_diastolic,
        timestamp=datetime.utcnow()
        
       
    )

    db.add(metric)
    db.commit()
    db.refresh(metric)

    logger.info(
        f"Health metric created | user_id={metric.user_id} | "
        f"heart_rate={metric.heart_rate}"
    )
 
    return metric


# ---------------------------------------------------------
# Get Health Metric By ID
# ---------------------------------------------------------

def get_health_metric_by_id(db: Session, metric_id: int):
    """
    Retrieve a single health metric entry by ID.
    """

    return db.query(HealthMetrics).filter(
        HealthMetrics.id == metric_id
    ).first()


# ---------------------------------------------------------
# Get Today's Health Metrics
# ---------------------------------------------------------




def get_today_health_metrics(db: Session, user_id: int):
    """
    Retrieve the latest health metric for today for a user.
    Returns a single record even if multiple entries exist.
    """

    logger.info("Fetching today's health metrics", extra={"user_id": user_id})

    try:
        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = start_of_day + timedelta(days=1)

        logger.debug(
            "Calculated date range for today's metrics",
            extra={
                "user_id": user_id,
                "start_of_day": start_of_day.isoformat(),
                "end_of_day": end_of_day.isoformat()
            }
        )

        metric = (
            db.query(HealthMetrics)
            .filter(
                HealthMetrics.user_id == user_id,
                HealthMetrics.timestamp >= start_of_day,
                HealthMetrics.timestamp < end_of_day
            )
            .order_by(HealthMetrics.timestamp.desc())
            .first()
        )

        if metric:
            logger.info(
                "Health metric found for today",
                extra={
                    "user_id": user_id,
                    "metric_id": metric.id,
                    "timestamp": metric.timestamp.isoformat()
                }
            )
        else:
            logger.warning(
                "No health metrics found for today",
                extra={"user_id": user_id}
            )

        return metric

    except Exception as e:
        logger.exception(
            "Error retrieving today's health metrics",
            extra={"user_id": user_id}
        )
        raise

# ---------------------------------------------------------
# Get User Health History
# ---------------------------------------------------------

def get_user_health_history(db: Session, user_id: int, limit: int = 50):
    """
    Retrieve historical health metrics for a user.
    Useful for trend analysis by AI agents.
    """

    return (
        db.query(HealthMetrics)
        .filter(HealthMetrics.user_id == user_id)
        .order_by(HealthMetrics.timestamp.desc())
        .limit(limit)
        .all()
    )


# ---------------------------------------------------------
# Update Health Metric
# ---------------------------------------------------------

def update_health_metric(
    db: Session,
    metric_id: int,
    data: HealthMetricsUpdate
):
    """
    Update an existing health metric entry.
    """

    metric = db.query(HealthMetrics).filter(
        HealthMetrics.id == metric_id
    ).first()

    if not metric:
        return None

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(metric, key, value)

    db.commit()
    db.refresh(metric)

    logger.info(
        f"Health metric updated | id={metric.id} | user_id={metric.user_id}"
    )

    return metric


# ---------------------------------------------------------
# Delete Health Metric
# ---------------------------------------------------------

def delete_health_metric(db: Session, metric_id: int):
    """
    Delete a health metric entry.
    """

    metric = db.query(HealthMetrics).filter(
        HealthMetrics.id == metric_id
    ).first()

    if not metric:
        return False

    db.delete(metric)
    db.commit()

    logger.info(f"Health metric deleted | id={metric_id}")

    return True