# app/models/user_profile.py
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)
    calories = Column(Integer, default=1800)
    diet = Column(String(50), default="vegetarian")
    goal = Column(String(50), default="weight loss")
    region = Column(String(50), default="Kerala")
    restrictions = Column(JSON, default=[])  # list of strings
    meal_type = Column(String(50), default="home food")
    created_at = Column(DateTime(timezone=True), server_default=func.now())