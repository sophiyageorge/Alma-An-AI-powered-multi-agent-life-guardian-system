"""
STT FastAPI Router 
Accepts audio from frontend, transcribes it, calls LLM,
updates journal in DB and LangGraph state.
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from loguru import logger

from app.agents.mental_health_agent.journal import process_audio_journal
from app.orchestrator.state import OrchestratorState

from app.schemas.mental_health import JournalEntryResponse
from app.dependencies import get_current_user, get_db
from datetime import datetime, timedelta
from app.models.mental_health import JournalEntry


router = APIRouter(prefix="/stt", tags=["Speech-to-Text"])

# Shared orchestrator state
state = OrchestratorState()


@router.post("/transcribe")
async def transcribe_and_process_audio(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    """
    Accepts an audio file from frontend, transcribes it, calls LLM for advice,
    updates DB, and LangGraph state.
    """
    try:
        audio_bytes = await file.read()

        user_id = current_user.user_id
        logger.info(f"Received audio journal from user_id={user_id}, filename={file.filename}")
        # Call journal service to process audio
        updated_data = process_audio_journal(
            audio_bytes=audio_bytes,
            user_id=user_id,
           
        )

        # journal_data = updated_state.get("daily_journal", {})

        return  {
    "journal_id": updated_data.id,
    "journal_text": updated_data.journal_text,
    "llm_response": updated_data.llm_response,
    "duration": updated_data.duration
}

    except Exception as exc:
        logger.exception("Error processing audio journal")
        return JSONResponse(status_code=500, content={"error": str(exc)})



@router.get("/journal/today", response_model=JournalEntryResponse)
def get_today_journal(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetch today's journal entry for the logged-in user.
    If no entry exists for today, returns 404.
    """

    user_id = current_user.user_id
    today = datetime.utcnow().date()
    logger.info(f"Fetching today's journal for user_id={user_id}")

    journal_entry = (
        db.query(JournalEntry)
        .filter(
            JournalEntry.user_id == user_id,
            JournalEntry.date_created >= datetime(today.year, today.month, today.day),
            JournalEntry.date_created < datetime(today.year, today.month, today.day) + timedelta(days=1)
        )
        .order_by(JournalEntry.date_created.desc())
        .first()
    )

    if not journal_entry:
        logger.warning(f"No journal entry found for today for user_id={user_id}")
        raise HTTPException(status_code=404, detail="No journal entry for today")

    logger.info(f"Returning journal entry id={journal_entry.id} for user_id={user_id}")
    return JournalEntryResponse.from_orm(journal_entry)