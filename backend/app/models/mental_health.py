"""
Journal Entry Model
-------------------

Stores journal entries submitted by users and the
AI-generated mental health insights produced by the
Mental Health Agent.

Each entry may come from:
• Text input
• Speech-to-text transcription

The model stores:
- User journal content
- Language of the entry
- Optional audio duration
- AI response
- Timestamp
"""

from sqlalchemy import Column,Integer, Text, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base
from app.core.logging_config import setup_logger


# Initialize logger
logger = setup_logger(__name__)


class JournalEntry(Base):
    """
    SQLAlchemy model representing a user's mental health journal entry.
    """

    __tablename__ = "journal_entries"

    # ---------------------------------------------------------
    # Primary Identifier
    # ---------------------------------------------------------

    id = Column(Integer, primary_key=True, autoincrement=True)

    # ---------------------------------------------------------
    # User Reference
    # ---------------------------------------------------------

    user_id =  Column(Integer, index=True, nullable=False)
    """
    ID of the user who created the journal entry.
    Indexed for fast retrieval of user journals.
    """

    # ---------------------------------------------------------
    # Journal Content
    # ---------------------------------------------------------

    journal_text = Column(Text, nullable=False)
    """
    Raw journal text written or transcribed from audio.
    """

    language = Column(String(10), default="en")
    """
    Language code of the journal entry (ISO code).
    Example:
    - en → English
    - es → Spanish
    - fr → French
    """

    duration = Column(Float, nullable=True)
    """
    Duration of audio journal in seconds (if speech input).
    Null if journal is typed text.
    """

    # ---------------------------------------------------------
    # AI Generated Output
    # ---------------------------------------------------------

    llm_response = Column(Text, nullable=True)
    """
    AI-generated response from the Mental Health Agent.
    Example:
    - Emotional insights
    - Reflection prompts
    - Coping strategies
    """

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    date_created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )
    """
    Timestamp when the journal entry was created.
    """

    # ---------------------------------------------------------
    # Optional Relationship Example
    # ---------------------------------------------------------
    # If you have a Users table:
    #
    # user = relationship("User", back_populates="journal_entries")
    #

    # ---------------------------------------------------------
    # Debug Representation
    # ---------------------------------------------------------

    def __repr__(self):
        """
        Developer-friendly representation for debugging.
        """
        return (
            f"<JournalEntry("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"language={self.language}, "
            f"created_at={self.date_created})>"
        )

    # ---------------------------------------------------------
    # Logging Helpers
    # ---------------------------------------------------------

    def log_creation(self):
        """
        Log journal entry creation.
        """
        logger.info(
            f"Journal entry created | user_id={self.user_id} | "
            f"language={self.language}"
        )

    def log_llm_response(self):
        """
        Log when LLM response is stored.
        """
        logger.info(
            f"LLM response stored for journal | "
            f"user_id={self.user_id} | entry_id={self.id}"
        )
