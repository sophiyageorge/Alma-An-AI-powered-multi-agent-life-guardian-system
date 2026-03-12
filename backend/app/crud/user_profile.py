"""
CRUD operations for UserProfile.
--------------------------------

Provides helper functions to create, read, update, and delete
user profiles. Includes logging and error handling for robust
operation in agents like Nutrition or Exercise.
"""

from sqlalchemy.orm import Session
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


# --------------------------
# Create Profile
# --------------------------
def create_profile(db: Session, profile: UserProfileCreate) -> UserProfile:
    """
    Create a new user profile.

    Args:
        db (Session): SQLAlchemy DB session
        profile (UserProfileCreate): Pydantic profile object

    Returns:
        UserProfile: Newly created profile
    """
    try:
        new_profile = UserProfile(**profile.model_dump())
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        logger.info(f"Created user profile | user_id={new_profile.user_id}")
        return new_profile

    except Exception as e:
        db.rollback()
        logger.exception(f"Failed to create profile | user_id={profile.user_id}")
        raise e


# --------------------------
# Get Profile
# --------------------------
def get_profile(db: Session, user_id: int) -> UserProfile | None:
    """
    Retrieve a user profile by user_id.

    Args:
        db (Session): SQLAlchemy DB session
        user_id (int): User ID

    Returns:
        UserProfile | None: UserProfile object if found, else None
    """
    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if profile:
            logger.info(f"Fetched profile | user_id={user_id}")
        else:
            logger.warning(f"No profile found | user_id={user_id}")
        return profile

    except Exception as e:
        logger.exception(f"Failed to fetch profile | user_id={user_id}")
        raise e


# --------------------------
# Update Profile
# --------------------------
def update_profile(db: Session, user_id: int, profile: UserProfileUpdate) -> UserProfile | None:
    """
    Update an existing user profile.

    Args:
        db (Session): SQLAlchemy DB session
        user_id (int): User ID
        profile (UserProfileUpdate): Fields to update (partial update allowed)

    Returns:
        UserProfile | None: Updated profile or None if not found
    """
    try:
        db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not db_profile:
            logger.warning(f"Profile not found for update | user_id={user_id}")
            return None

        update_data = profile.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_profile, key, value)

        db.commit()
        db.refresh(db_profile)

        logger.info(f"Updated profile | user_id={user_id}")
        return db_profile

    except Exception as e:
        db.rollback()
        logger.exception(f"Failed to update profile | user_id={user_id}")
        raise e


# --------------------------
# Delete Profile
# --------------------------
def delete_profile(db: Session, user_id: int) -> UserProfile | None:
    """
    Delete a user profile.

    Args:
        db (Session): SQLAlchemy DB session
        user_id (int): User ID

    Returns:
        UserProfile | None: Deleted profile object or None if not found
    """
    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            logger.warning(f"Profile not found for deletion | user_id={user_id}")
            return None

        db.delete(profile)
        db.commit()
        logger.info(f"Deleted profile | user_id={user_id}")
        return profile

    except Exception as e:
        db.rollback()
        logger.exception(f"Failed to delete profile | user_id={user_id}")
        raise e
# from sqlalchemy.orm import Session
# from app.models.user_profile import UserProfile
# from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate
# from app.agents.nutrition.nutrition_plan import generate_nutrition_plan


# def create_profile(db: Session, profile: UserProfileCreate):
#     new_profile = UserProfile(**profile.model_dump())
#     db.add(new_profile)
#     db.commit()
#     db.refresh(new_profile)

#     return new_profile


# def get_profile(db: Session, user_id: int):
#     return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()


# def update_profile(db: Session, user_id: int, profile: UserProfileUpdate):
#     db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

#     if not db_profile:
#         return None

#     update_data = profile.model_dump(exclude_unset=True)

#     for key, value in update_data.items():
#         setattr(db_profile, key, value)

#     db.commit()
#     db.refresh(db_profile)

    


#     return db_profile


# def delete_profile(db: Session, user_id: int):
#     profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

#     if not profile:
#         return None

#     db.delete(profile)
#     db.commit()

#     return profile