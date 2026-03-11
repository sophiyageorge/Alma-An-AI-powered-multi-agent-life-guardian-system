from sqlalchemy import Column, Integer, String, Text, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base


class WeeklyMealPlan(Base):
    __tablename__ = "weekly_meal_plans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, index=True)

    # user preferences used to generate meal plan
    calories = Column(Integer, nullable=True)
    diet = Column(String(50), nullable=True)
    region = Column(String(50), nullable=True)
    goal = Column(String(50), nullable=True)
    restrictions = Column(JSON, nullable=True)

    # generated outputs
    meal_plan_text = Column(Text, nullable=False)
    grocery_list = Column(JSON, nullable=True)

    is_approved = Column(Boolean, default=False)

    # timestamp when plan is generated
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)