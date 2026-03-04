"""
Pydantic schemas for Journal Entries (Mental Health Agent).
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class JournalEntryCreate(BaseModel):
    """
    Schema for creating a new journal entry from frontend.
    """
    user_id: int = Field(..., description="ID of the user")
    journal_text: str = Field(..., description="User's journal entry text")
    language: Optional[str] = Field("en", description="Language code of the journal text")
    duration: Optional[float] = Field(None, description="Duration of audio recording in seconds")


class JournalEntryResponse(BaseModel):
    """
    Schema for returning journal entry data including LLM response.
    """
    id: int
    user_id: int
    journal_text: str
    language: str
    duration: Optional[float]
    date_created: datetime
    llm_response: Optional[str]

    class Config:
        orm_mode = True  # Allows SQLAlchemy models to be returned directly