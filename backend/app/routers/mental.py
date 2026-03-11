"""
STT FastAPI Router 
Accepts audio from frontend, transcribes it, calls LLM,
updates journal in DB and LangGraph state.
"""

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from loguru import logger

from app.agents.mental_health_agent.journal import process_audio_journal
from app.orchestrator.state import OrchestratorState

router = APIRouter(prefix="/stt", tags=["Speech-to-Text"])

# Shared orchestrator state
state = OrchestratorState()


@router.post("/transcribe")
async def transcribe_and_process_audio(file: UploadFile = File(...), user_id: int = 1):
    """
    Accepts an audio file from frontend, transcribes it, calls LLM for advice,
    updates DB, and LangGraph state.
    """
    try:
        audio_bytes = await file.read()

        # Call journal service to process audio
        updated_state = process_audio_journal(
            audio_bytes=audio_bytes,
            user_id=user_id,
            state=state
        )

        journal_data = updated_state.get("daily_journal", {})

        return JSONResponse(content={
            "journal_text": journal_data.get("journal_text", ""),
            "llm_response": journal_data.get("llm_response", ""),
            "journal_id": journal_data.get("journal_id", None),
            "duration": journal_data.get("duration", None)
        })

    except Exception as exc:
        logger.exception("Error processing audio journal")
        return JSONResponse(status_code=500, content={"error": str(exc)})