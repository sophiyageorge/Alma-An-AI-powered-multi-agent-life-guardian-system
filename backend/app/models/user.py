from sqlalchemy import Column, Integer, String, Enum, Date
from app.database import Base
from app.schemas.enums import ModeEnum, GenderEnum

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    date_of_birth = Column(Date)
    gender = Column(Enum(GenderEnum))
