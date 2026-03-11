from sqlalchemy.orm import Session
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate
from app.agents.nutrition.nutrition_plan import generate_nutrition_plan


def create_profile(db: Session, profile: UserProfileCreate):
    new_profile = UserProfile(**profile.model_dump())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


def get_profile(db: Session, user_id: int):
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()


def update_profile(db: Session, user_id: int, profile: UserProfileUpdate):
    db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    if not db_profile:
        return None

    update_data = profile.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_profile, key, value)

    db.commit()
    db.refresh(db_profile)

    


    return db_profile


def delete_profile(db: Session, user_id: int):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    if not profile:
        return None

    db.delete(profile)
    db.commit()

    return profile