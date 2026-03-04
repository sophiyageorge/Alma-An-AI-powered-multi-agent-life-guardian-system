from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, TIMESTAMP, func
from app.database import Base   

class DoctorAppointment(Base):  
    __tablename__ = "doctor_appointments"
    appointment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    member_id = Column(Integer, ForeignKey("family_members.member_id"), nullable=True)
    doctor_name = Column(String(100), nullable=False)
    specialization = Column(String(100))
    appointment_date = Column(DateTime, nullable=False)
    location = Column(String(255))
    telemedicine = Column(Boolean, default=False)
    reminder_sent = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

