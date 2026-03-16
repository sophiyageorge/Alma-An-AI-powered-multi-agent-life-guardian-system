"""
Journal Service: Handles audio -> STT -> LLM -> DB -> state updates
"""

from io import BytesIO
from datetime import datetime, timedelta
import os

from loguru import logger
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.mental_health import JournalEntry
from app.crud.mental_health import get_today_journal, save_journal, update_journal
from app.agents.mental_health_agent.prompt import build_mental_health_prompt
from app.llm.llm_client import llm
from app.orchestrator.state import OrchestratorState
from app.core.exceptions import MentalHealthAgentError
from app.agents.mental_health_agent.stt.speech_to_text import SpeechToTextEngine
from app.agents.mental_health_agent.stt.config import STTConfig


def process_audio_journal(
    audio_bytes: bytes,
    user_id: int,
    stt_model_size: str = "base",
    db: Session = None
) -> JournalEntry:
    """
    Process a recorded audio journal for a user.

    Steps:
    1. Convert audio bytes to text using STT engine
    2. Generate LLM response for mental health advice
    3. Save or update today's journal entry using CRUD
    4. (Optional) Update orchestrator state
    5. Return the DB journal entry

    Args:
        audio_bytes (bytes): Audio file content
        user_id (int): User identifier
        stt_model_size (str, optional): STT model size. Defaults to "base".
        db (Session, optional): SQLAlchemy DB session. If None, a new session is created.

    Returns:
        JournalEntry: DB object for today's journal entry
    """

    try:
        # -------------------------------
        # Initialize DB session
        # -------------------------------
        if db is None:
            db = next(get_db())

        logger.info("Processing audio journal for user_id=%s", user_id)

        # -------------------------------
        # Initialize STT engine
        # -------------------------------
        stt_config = STTConfig(model_size=stt_model_size, device="cpu")
        stt_engine = SpeechToTextEngine(config=stt_config)

        # Convert audio bytes into a temporary file-like object
        temp_file = f"temp_audio_{user_id}.mp4"
        with open(temp_file, "wb") as f:
            f.write(audio_bytes)

        logger.info("Running STT on audio file for user_id=%s", user_id)
        stt_result = stt_engine.transcribe(temp_file)
        journal_text = stt_result.get("text", "")
        duration = stt_result.get("duration", None)
        language = stt_result.get("language", "en")

        logger.debug("STT result for user_id=%s: %s", user_id, journal_text[:50])

        # -------------------------------
        # Generate LLM response
        # -------------------------------
        prompt = build_mental_health_prompt(journal_text)
        logger.info("Invoking LLM for mental health advice for user_id=%s", user_id)
        llm_response = llm.invoke(prompt)

        # -------------------------------
        # Check if today's journal already exists
        # -------------------------------
        today_entry = get_today_journal(db, user_id)

        if today_entry:
            # Update existing entry using CRUD
            logger.info("Updating existing journal entry | journal_id=%s", today_entry.id)
            updated_entry = update_journal(
                db=db,
                journal_id=today_entry.id,
                journal_text=journal_text,
                llm_response=llm_response,
                language=language,
                duration=duration
            )
            journal_entry = updated_entry
        else:
            # Create a new journal entry via CRUD
            logger.info("Creating new journal entry for user_id=%s", user_id)
            journal_entry = save_journal(
                db=db,
                user_id=user_id,
                journal_text=journal_text,
                llm_response=llm_response,
                language=language,
                duration=duration
            )

        # -------------------------------
        # Cleanup temporary file
        # -------------------------------
        if os.path.exists(temp_file):
            os.remove(temp_file)
            logger.debug("Temporary audio file removed: %s", temp_file)

        logger.info(
            "Audio journal processed successfully | journal_id=%s | user_id=%s",
            journal_entry.id, user_id
        )

        return journal_entry

    except Exception as exc:
        logger.exception("Error processing audio journal for user_id=%s", user_id)
        raise MentalHealthAgentError(str(exc)) from exc
