"""
Health Metrics Model
--------------------

Stores health data collected from wearable devices, APIs,
or manual user input. These metrics are used by the Health
Agent and other AI agents to generate wellness insights
and recommendations.

Example Metrics:
- Heart rate
- SpO2 (blood oxygen)
- Blood pressure
- Steps
- Workout duration
"""

from sqlalchemy import Column, Integer, Float, DateTime , ForeignKey
from datetime import datetime


from app.database import Base
from app.core.logging_config import setup_logger

# Initialize logger
logger = setup_logger(__name__)


class HealthMetrics(Base):
    """
    SQLAlchemy model representing user health metrics.

    Each row represents a health snapshot that can be used
    by AI agents to generate recommendations or detect anomalies.
    """

    __tablename__ = "health_metrics"

    # ---------------------------------------------------------
    # Primary Key
    # ---------------------------------------------------------

    id = Column(Integer, primary_key=True, autoincrement=True)

    # ---------------------------------------------------------
    # User Reference
    # ---------------------------------------------------------

    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)

    """
    ID of the user who generated this health data.
    Indexed for faster querying of user history.
    """

    # ---------------------------------------------------------
    # Health Metrics
    # ---------------------------------------------------------

    heart_rate = Column(Integer, nullable=True)
    """Heart rate in beats per minute (BPM)"""

    spo2 = Column(Integer, nullable=True)
    """Blood oxygen saturation percentage"""

    bp_systolic = Column(Integer, nullable=True)
    """Systolic blood pressure"""

    bp_diastolic = Column(Integer, nullable=True)
    """Diastolic blood pressure"""

 

    # ---------------------------------------------------------
    # Timestamp
    # ---------------------------------------------------------

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    """
    Timestamp when the health data was recorded.
    Indexed for efficient time-series queries.
    """

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self):
        """
        Developer-friendly representation used for debugging.
        """
        return (
            f"<HealthMetrics("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"heart_rate={self.heart_rate}, "
            f"spo2={self.spo2}, "
            f"timestamp={self.timestamp})>"
        )

    # ---------------------------------------------------------
    # Logging Helper
    # ---------------------------------------------------------

    def log_creation(self):
        """
        Log creation of a new health metric entry.
        Useful for monitoring incoming health data streams.
        """
        logger.info(
            f"HealthMetrics entry created | user_id={self.user_id} | "
            f"heart_rate={self.heart_rate} | spo2={self.spo2}"
        )
