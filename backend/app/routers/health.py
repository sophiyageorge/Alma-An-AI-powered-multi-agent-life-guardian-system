"""
Health Metrics API Routes
-------------------------

Provides endpoints for managing user health metrics.
These endpoints are used by wearable integrations,
manual user input, and AI health agents.
"""

from fastapi import APIRouter, Depends, HTTPException,BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from datetime import datetime, timedelta
from app.agents.exercise.agent import exercise_agent
from app.orchestrator.state import OrchestratorState
from app.crud.user_profile import get_profile

from app.database import get_db
from app.database import SessionLocal
from app.dependencies import get_current_user
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
from app.models.user import User
from app.models.health import HealthMetrics

from app.orchestrator.graph import build_graph

from app.core.logging_config import setup_logger

logger = setup_logger(__name__)

router = APIRouter(
    prefix="/health-metrics",
    tags=["Health Metrics"]
)



def run_orchestrator(user_id: int):
    """
    Run the orchestrator workflow for a given user.

    Args:
        user_id (int): ID of the authenticated user.
        db (Session): Database session.

    Raises:
        HTTPException: If orchestrator execution fails.
    """

    db = SessionLocal()   # ✅ create new DB session

    # ---------------------------------------------------------
    # Fetch User Profile
    # ---------------------------------------------------------

    profile = get_profile(db,user_id)

    logger.info(f"Profile fetched for user_id={user_id}")

    # ---------------------------------------------------------
    # Build User Profile State
    # ---------------------------------------------------------

    if profile:
        user_profile = {
                "user_id": user_id,
                "calories": profile.calories,
                "diet": profile.diet,
                "goal": profile.goal,
                "region": profile.region,
                "restrictions": profile.restrictions or [],
                "meal_type": profile.meal_type
            }

        logger.info(
                f"Using stored profile for user_id={user_id}"
            )

            # ---------------------------------------------------------
            # Initialize Orchestrator State
            # ---------------------------------------------------------

        state: OrchestratorState = {
                # "user_id": db_user.user_id,
                "user_profile": user_profile,
                "db": db,
                "health_data": None,
                "journal_text": None,
                "meal_plan_approved": False,
                "exercise_plan_approved": False,
                "anomaly_detected": False,
                "compliance_passed": True
            }

        logger.info(
                f"Orchestrator state initialized for user_id={user_id}"
            )

        logger.info(f"Initial orchestrator state for user_id={user_id}: {state}")

        # ---------------------------------------------------------
        # Invoke LangGraph Orchestrator
        # ---------------------------------------------------------

        try:

            logger.info(
                    f"Invoking orchestrator graph for user_id={user_id}"
                )
            
            # Build LangGraph orchestrator
            graph = build_graph()

            final_state = graph.invoke(state)

            logger.info(
                    f"Orchestrator completed successfully for user_id={user_id}"
                )

                
        
        except Exception as e:

            logger.exception("Orchestrator failed", extra={"user_id": user_id})

            raise HTTPException(
                    status_code=500,
                    detail="Failed to initialize wellness workflow"
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
    background_tasks: BackgroundTasks,
    data: HealthMetricsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Insert a new health metrics entry.
    """
    user_id = current_user.user_id
    print("inside health post",user_id)
    metric = create_health_metric(db, data,user_id)

    # Convert SQLAlchemy model to dict
    metrics_dict = {
        "id":metric.id,
        "heart_rate": metric.heart_rate,
        "bp_systolic": metric.bp_systolic,
        "bp_diastolic": metric.bp_diastolic,
        "sp02": metric.spo2,
       
        # add any other fields your prompt expects
    }

    # Build minimal state just for exercise agent
    profile = get_profile(db, user_id)
    state: OrchestratorState = {
        "user_profile": {
            "user_id": user_id,
            "calories": profile.calories,
            "diet": profile.diet,
            "goal": profile.goal,
            "region": profile.region,
            "restrictions": profile.restrictions or [],
            "meal_type": profile.meal_type
        },
        "db": db,
        "health_data": metrics_dict,
    }

    try:
        # Invoke only the exercise agent
        updated_state = exercise_agent(state)

        # Save updated state in memory or orchestrator store if you have one
        orchestrator_store[user_id] = updated_state

    except Exception as e:
        print("Exercise Agent failed:", e)
        # Decide whether to fail request or ignore
        # pass

   
        # ---------------------------------------------------------
    # Add orchestrator workflow as background task
    # ---------------------------------------------------------

    background_tasks.add_task(run_orchestrator,user_id)
   
    # -----------------------------
    # 4️⃣ Return saved metric
    # -----------------------------
    if not metric:
        raise HTTPException(
            status_code=404,
            detail="No health metrics found for today"
        )
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

    if metrics is None:
        raise HTTPException(
            status_code=404,
            detail="No health metrics found for today"
        )

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

    # Current date
    today = datetime.utcnow()

    # Find start of current week (Monday)
    start_of_current_week = today - timedelta(days=today.weekday())

    # Start of previous week (7 days before start of current week)
    start_of_prev_week = start_of_current_week - timedelta(days=7)

    # End of previous week (1 day before start of current week)
    end_of_prev_week = start_of_current_week - timedelta(seconds=1)

    rows = db.query(HealthMetrics).filter(
    HealthMetrics.user_id == user_id,
    HealthMetrics.timestamp >= start_of_prev_week,
    HealthMetrics.timestamp <= end_of_prev_week
).order_by(HealthMetrics.timestamp.asc()).all()
    result = [
        {
            "timestamp": row.timestamp.isoformat(),
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
    ).order_by(HealthMetrics.timestamp.asc()).all()

    result = [
        {
            "timestamp": row.timestamp.isoformat(),
            "heart_rate": row.heart_rate,
            "spo2": row.spo2,
            "bp_systolic": row.bp_systolic,
            "bp_diastolic": row.bp_diastolic
        }
        for row in rows
    ]

    return result