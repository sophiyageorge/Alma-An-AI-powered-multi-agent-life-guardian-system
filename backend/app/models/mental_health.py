"""
SQLAlchemy model for Journal Entries (Mental Health Agent).
"""

from sqlalchemy import Column, BigInteger, Text, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class JournalEntry(Base):
    """
    SQLAlchemy model for a user's journal entry and LLM response.
    """

    __tablename__ = "journal_entries"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)  # Can be linked to Users table
    journal_text = Column(Text, nullable=False)
    language = Column(String(10), default="en")
    duration = Column(Float, nullable=True)  # Duration of audio in seconds
    date_created = Column(DateTime, default=datetime.utcnow)
    llm_response = Column(Text, nullable=True)

    # Optional: if you have a Users table
    # user = relationship("User", back_populates="journal_entries")

    def __repr__(self):
        return (
            f"<JournalEntry(id={self.id}, user_id={self.user_id}, "
            f"language={self.language}, date_created={self.date_created})>"
        )

