from sqlalchemy import Column, Integer, Float, Date, ForeignKey, TIMESTAMP, func, String, DateTime
from datetime import datetime
from app.database import Base   

# class HealthData(Base):
#     __tablename__ = "health_data"
#     health_id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.user_id"))
#     member_id = Column(Integer, ForeignKey("family_members.member_id"), nullable=True)
#     date = Column(Date, nullable=False)
#     bp_systolic = Column(Integer)
#     bp_diastolic = Column(Integer)
#     weight = Column(Float)
#     steps = Column(Integer)
#     sleep_hours = Column(Float)
#     activity_type = Column(String(100))
#     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

class HealthMetrics(Base):
    __tablename__ = "health_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    heart_rate = Column(Integer)
    spo2 = Column(Integer)
    bp_systolic = Column(Integer)
    bp_diastolic = Column(Integer)
    steps = Column(Integer)
    workout_duration_minutes = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)