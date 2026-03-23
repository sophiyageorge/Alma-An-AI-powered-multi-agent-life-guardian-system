"""
User Model
----------

Stores core user account information for authentication
and demographic details. Used across the Wellness Guidance
System for agent orchestration and personalized recommendations.
"""

from sqlalchemy import Column, Integer, String, Enum, Date
from app.database import Base
from app.schemas.enums import GenderEnum, ModeEnum
from app.core.logging_config import setup_logger

# Initialize logger
logger = setup_logger(__name__)


class User(Base):
    """
    SQLAlchemy model representing a system user.
    """

    __tablename__ = "users"

    # ---------------------------------------------------------
    # Primary Identifier
    # ---------------------------------------------------------
    user_id = Column(Integer, primary_key=True, index=True)
    """
    Unique user identifier.
    """

    # ---------------------------------------------------------
    # Personal Information
    # ---------------------------------------------------------
    name = Column(String, nullable=False)
    """
    Full name of the user.
    """

    email = Column(String, unique=True, nullable=False, index=True)
    """
    User's email used for authentication.
    Indexed for fast lookup during login.
    """
    # ---------------------------------------------------------
    # Contact Information
    # ---------------------------------------------------------
    phone = Column(String, unique=True, nullable=True, index=True)
    """
    Optional phone number for the user.
    Can be used for OTP, contact, or personalized notifications.
    """

    password_hash = Column(String, nullable=False)
    """
    Hashed password for secure authentication.
    Never store plain text passwords.
    """

    date_of_birth = Column(Date, nullable=True)
    """
    Date of birth of the user (optional).
    """

    gender = Column(Enum(GenderEnum), nullable=True)
    """
    User gender for demographic analytics or personalization.
    """

  

    # ---------------------------------------------------------
    # Debug Representation
    # ---------------------------------------------------------
    def __repr__(self):
        return (
            f"<User("
            f"user_id={self.user_id}, "
            f"name={self.name}, "
            f"email={self.email}, "
            f"gender={self.gender})>"
        )

    # ---------------------------------------------------------
    # Logging Helpers
    # ---------------------------------------------------------
    def log_creation(self):
        """
        Log user creation event.
        """
        logger.info(f"New user created | user_id={self.user_id} | email={self.email}")

    def log_update(self):
        """
        Log when user profile is updated.
        """
        logger.info(f"User profile updated | user_id={self.user_id}")

