"""
Speech-to-Text (STT) Router
---------------------------
Handles:
- Audio upload from frontend
- Speech-to-text transcription
- LLM processing for journaling insights
- Database updates
- Fetching today's journal entry
"""

from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from loguru import logger

# Internal imports
from app.agents.mental_health_agent.journal import process_audio_journal
from app.orchestrator.state import OrchestratorState
from app.schemas.mental_health import JournalEntryResponse
from app.dependencies import get_current_user, get_db
from app.models.mental_health import JournalEntry


router = APIRouter(prefix="/stt", tags=["Speech-to-Text"])

# Shared orchestrator state (consider dependency injection if scaling)
state = OrchestratorState()


@router.post("/transcribe", status_code=status.HTTP_200_OK)
async def transcribe_and_process_audio(
    file: UploadFile = File(...),
    current_user: Any = Depends(get_current_user)
) -> dict:
    """
    Transcribe and process an uploaded audio journal.

    Steps:
    1. Read audio file from request
    2. Convert speech to text
    3. Send text to LLM for analysis
    4. Store results in database
    5. Return structured response

    Args:
        file (UploadFile): Audio file uploaded by the user
        current_user (Any): Authenticated user object

    Returns:
        dict: Processed journal data including:
            - journal_id
            - journal_text
            - llm_response
            - duration

    Raises:
        HTTPException: If processing fails
    """
    try:
        # Validate file
        if not file.filename:
            logger.warning("Empty filename received")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file"
            )

        audio_bytes = await file.read()
        user_id = current_user.user_id

        logger.bind(user_id=user_id).info(
            "Received audio journal",
            filename=file.filename,
            size=len(audio_bytes)
        )

        # Process audio journal
        updated_data = process_audio_journal(
            audio_bytes=audio_bytes,
            user_id=user_id,
        )

        logger.bind(user_id=user_id, journal_id=updated_data.id).info(
            "Journal processed successfully"
        )

        return {
            "journal_id": updated_data.id,
            "journal_text": updated_data.journal_text,
            "llm_response": updated_data.llm_response,
            "duration": updated_data.duration,
        }

    except HTTPException:
        raise  # Re-raise known exceptions

    except ValueError as exc:
        logger.error(f"Validation error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    except Exception as exc:
        logger.exception("Unexpected error during audio processing")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get(
    "/journal/today",
    response_model=JournalEntryResponse,
    status_code=status.HTTP_200_OK
)
def get_today_journal(
    current_user: Any = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> JournalEntryResponse:
    """
    Retrieve today's journal entry for the authenticated user.

    Logic:
    - Filters journal entries for current UTC day
    - Returns latest entry if multiple exist

    Args:
        current_user (Any): Authenticated user object
        db (Session): Database session

    Returns:
        JournalEntryResponse: Journal entry for today

    Raises:
        HTTPException:
            - 404 if no journal entry exists
            - 500 for unexpected errors
    """
    try:
        user_id = current_user.user_id
        today = datetime.utcnow().date()

        start_of_day = datetime(today.year, today.month, today.day)
        end_of_day = start_of_day + timedelta(days=1)

        logger.bind(user_id=user_id).info("Fetching today's journal")

        journal_entry = (
            db.query(JournalEntry)
            .filter(
                JournalEntry.user_id == user_id,
                JournalEntry.date_created >= start_of_day,
                JournalEntry.date_created < end_of_day,
            )
            .order_by(JournalEntry.date_created.desc())
            .first()
        )

        if not journal_entry:
            logger.bind(user_id=user_id).warning("No journal entry found for today")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No journal entry for today"
            )

        logger.bind(user_id=user_id, journal_id=journal_entry.id).info(
            "Journal entry retrieved successfully"
        )

        return JournalEntryResponse.from_orm(journal_entry)

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception("Error fetching today's journal")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch journal"
        )