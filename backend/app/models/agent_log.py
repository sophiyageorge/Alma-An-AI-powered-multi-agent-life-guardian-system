
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, TIMESTAMP, func
from app.database import Base

class AgentLog(Base):
    __tablename__ = "agent_logs"
    log_id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(50))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    member_id = Column(Integer, ForeignKey("family_members.member_id"), nullable=True)
    action = Column(String(255))
    timestamp = Column(TIMESTAMP, server_default=func.current_timestamp())
    status = Column(Enum('Success','Failed'))