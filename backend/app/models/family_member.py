from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class FamilyMember(Base):
    __tablename__ = "family_members"
    member_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String, nullable=False)
    relation = Column(String)
