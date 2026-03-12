"""
User Profile Model
------------------

Stores user dietary preferences and nutrition settings used
by the Nutrition Agent to generate personalized meal plans.

This table contains:
• User nutrition preferences
• Dietary restrictions
• Calorie goals
• Regional food preferences
"""

from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func

from app.database import Base
from app.core.logging_config import setup_logger


# Initialize logger
logger = setup_logger(__name__)


class UserProfile(Base):
    """
    SQLAlchemy model representing a user's nutrition profile.
    """

    __tablename__ = "user_profiles"

    # ---------------------------------------------------------
    # Primary Identifier
    # ---------------------------------------------------------

    id = Column(Integer, primary_key=True, autoincrement=True)

    # ---------------------------------------------------------
    # User Reference
    # ---------------------------------------------------------

    user_id = Column(Integer, unique=True, index=True, nullable=False)
    """
    Unique identifier for the user.
    One profile per user.
    """

    # ---------------------------------------------------------
    # Nutrition Preferences
    # ---------------------------------------------------------

    calories = Column(Integer, default=1800)
    """
    Target daily calorie intake used for meal planning.
    """

    diet = Column(String(50), default="vegetarian")
    """
    Preferred diet type.

    Examples:
    - vegetarian
    - vegan
    - keto
    - balanced
    """

    goal = Column(String(50), default="weight loss")
    """
    Health goal for nutrition planning.

    Examples:
    - weight loss
    - muscle gain
    - maintenance
    """

    region = Column(String(50), default="Kerala")
    """
    Regional cuisine preference used by the Nutrition Agent.
    """

    meal_type = Column(String(50), default="home food")
    """
    Type of meal preference.

    Examples:
    - home food
    - restaurant style
    - quick meals
    """

    restrictions = Column(JSON, default=list)
    """
    Dietary restrictions stored as JSON list.

    Example:
    ["gluten free", "no dairy"]
    """

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )
    """
    Timestamp when the profile was created.
    """

    # ---------------------------------------------------------
    # Debug Representation
    # ---------------------------------------------------------

    def __repr__(self):
        """
        Developer-friendly representation for debugging.
        """
        return (
            f"<UserProfile("
            f"user_id={self.user_id}, "
            f"diet={self.diet}, "
            f"goal={self.goal}, "
            f"region={self.region})>"
        )

    # ---------------------------------------------------------
    # Logging Helpers
    # ---------------------------------------------------------

    def log_creation(self):
        """
        Log creation of a new user profile.
        """
        logger.info(
            f"User profile created | "
            f"user_id={self.user_id} | "
            f"diet={self.diet} | "
            f"goal={self.goal}"
        )

    def log_update(self):
        """
        Log profile updates.
        """
        logger.info(
            f"User profile updated | "
            f"user_id={self.user_id}"
        )
# # app/models/user_profile.py
# from sqlalchemy import Column, Integer, String, JSON, DateTime
# from sqlalchemy.sql import func
# from app.database import Base


# class UserProfile(Base):
#     __tablename__ = "user_profiles"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, unique=True, index=True, nullable=False)
#     calories = Column(Integer, default=1800)
#     diet = Column(String(50), default="vegetarian")
#     goal = Column(String(50), default="weight loss")
#     region = Column(String(50), default="Kerala")
#     restrictions = Column(JSON, default=[])  # list of strings
#     meal_type = Column(String(50), default="home food")
#     created_at = Column(DateTime(timezone=True), server_default=func.now())