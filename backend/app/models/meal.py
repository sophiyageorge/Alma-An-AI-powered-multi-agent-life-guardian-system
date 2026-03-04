from sqlalchemy import Column, Integer, String, Text, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base

class WeeklyMealPlan(Base):
    __tablename__ = "weekly_meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)

    meal_plan_text = Column(Text, nullable=False)   # LONG text ✔
    grocery_list = Column(JSON, nullable=True)      # list[str]

    is_approved = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
