from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, TIMESTAMP, func
from app.database import Base

class EmergencyEvent(Base):
    __tablename__ = "emergency_events"
    event_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    member_id = Column(Integer, ForeignKey("family_members.member_id"), nullable=True)
    event_type = Column(Enum('BP Anomaly','Heart Rate Anomaly','Accident','Other'))
    event_time = Column(TIMESTAMP, server_default=func.current_timestamp())
    action_taken = Column(String(255))
    status = Column(Enum('Pending','Resolved'))

