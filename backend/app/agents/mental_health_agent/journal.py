        
# """
# Journal Service: handles audio -> STT -> LLM -> DB -> state updates.
# """

from io import BytesIO
from datetime import datetime, timedelta
from loguru import logger

from sqlalchemy.orm import Session
from app.database import get_db
from app.models.mental_health import JournalEntry
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
    Process a recorded audio journal:
    1. Convert audio to text (STT)
    2. Call LLM for friendly advice
    3. Save or update today's journal entry in DB
    4. Update LangGraph state

    Returns:
        JournalEntry: The DB entry for today's journal
    """
    try:
        if db is None:
            db = next(get_db())

        # 1️⃣ Initialize STT engine
        stt_config = STTConfig(model_size=stt_model_size, device="cpu")
        stt_engine = SpeechToTextEngine(config=stt_config)

        # 2️⃣ Convert audio bytes to text
        temp_file = f"temp_audio_{user_id}.mp4"
        with open(temp_file, "wb") as f:
            f.write(audio_bytes)

        logger.info("Running STT on uploaded audio...")
        stt_result = stt_engine.transcribe(temp_file)
        journal_text = stt_result.get("text", "")
        duration = stt_result.get("duration", None)
        language = stt_result.get("language", "en")

        logger.info(f"STT completed: {journal_text[:50]}...")

        # 3️⃣ Build LLM prompt and get response
        prompt = build_mental_health_prompt(journal_text)
        logger.info("Calling LLM for mental health advice...")
        llm_response = llm.invoke(prompt)

        # 4️⃣ Check if a journal entry exists for this user today
        today = datetime.utcnow().date()
        existing_entry = (
            db.query(JournalEntry)
            .filter(
                JournalEntry.user_id == user_id,
                JournalEntry.date_created >= datetime(today.year, today.month, today.day),
                JournalEntry.date_created < datetime(today.year, today.month, today.day) + timedelta(days=1)
            )
            .first()
        )

        if existing_entry:
            # Update the existing entry
            logger.info(f"Updating existing journal entry ID {existing_entry.id} for today")
            existing_entry.journal_text = journal_text
            existing_entry.llm_response = llm_response
            existing_entry.language = language
            existing_entry.duration = duration
            existing_entry.date_created = datetime.utcnow()
            db.commit()
            db.refresh(existing_entry)
            journal_entry = existing_entry
        else:
            # Create a new entry
            logger.info("Creating new journal entry for today")
            new_entry = JournalEntry(
                user_id=user_id,
                journal_text=journal_text,
                language=language,
                duration=duration,
                llm_response=llm_response,
                date_created=datetime.utcnow()
            )
            db.add(new_entry)
            db.commit()
            db.refresh(new_entry)
            journal_entry = new_entry

        # 5️⃣ Update orchestrator state
        # state["daily_journal"] = {
        #     "journal_id": journal_entry.id,
        #     "journal_text": journal_text,
        #     "llm_response": llm_response,
        #     "duration": duration
        # }

        # Cleanup temp file
        import os
        os.remove(temp_file)

        return journal_entry

    except Exception as exc:
        logger.exception("Error processing audio journal")
        raise MentalHealthAgentError(str(exc)) from exc


# """
# Journal Service: handles audio -> STT -> LLM -> DB -> state updates.
# """

# from io import BytesIO
# from datetime import datetime
# from loguru import logger

# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models.mental_health import JournalEntry
# from app.agents.mental_health_agent.prompt import build_mental_health_prompt
# from app.llm.llm_client import llm
# from app.orchestrator.state import OrchestratorState
# from app.core.exceptions import MentalHealthAgentError
# from app.agents.mental_health_agent.stt.speech_to_text import SpeechToTextEngine
# from app.agents.mental_health_agent.stt.config import STTConfig


# def process_audio_journal(
#     audio_bytes: bytes,
#     user_id: int,
#     state: OrchestratorState,
#     stt_model_size: str = "base",
#     db: Session = None
# ) -> OrchestratorState:
#     """
#     Process a recorded audio journal:
#     1. Convert audio to text (STT)
#     2. Call LLM for friendly advice
#     3. Save journal + LLM response to DB
#     4. Update LangGraph state

#     Args:
#         audio_bytes (bytes): Raw audio bytes from frontend
#         user_id (int): User ID
#         state (OrchestratorState): Current orchestrator state
#         stt_model_size (str): Whisper model size
#         db (Session): Optional SQLAlchemy session

#     Returns:
#         OrchestratorState: Updated state
#     """
#     try:
#         if db is None:
#             db = next(get_db())

#         # 1️⃣ Initialize STT engine
#         stt_config = STTConfig(model_size=stt_model_size, device="cpu")
#         stt_engine = SpeechToTextEngine(config=stt_config)

#         # 2️⃣ Convert audio bytes to text
#         temp_file = f"temp_audio_{user_id}.mp4"
#         with open(temp_file, "wb") as f:
#             f.write(audio_bytes)

#         logger.info("Running STT on uploaded audio...")
#         stt_result = stt_engine.transcribe(temp_file)
#         journal_text = stt_result.get("text", "")
#         duration = stt_result.get("duration", None)

#         logger.info(f"STT completed: {journal_text[:50]}...")

#         # 3️⃣ Build LLM prompt
#         prompt = build_mental_health_prompt(journal_text)
#         logger.info("Calling LLM for mental health advice...")
#         llm_response = llm.invoke(prompt)

#         # 4️⃣ Save to DB
#         new_entry = JournalEntry(
#             user_id=user_id,
#             journal_text=journal_text,
#             language=stt_result.get("language", "en"),
#             duration=duration,
#             llm_response=llm_response,
#             date_created=datetime.utcnow()
#         )
#         db.add(new_entry)
#         db.commit()
#         db.refresh(new_entry)
#         logger.info(f"Journal saved with ID {new_entry.id}")

#         # 5️⃣ Update LangGraph orchestrator state
#         state["daily_journal"] = {
#             "journal_id": new_entry.id,
#             "journal_text": journal_text,
#             "llm_response": llm_response,
#             "duration": duration
#         }

#         # Cleanup temp file
#         import os
#         os.remove(temp_file)

#         return new_entry

#     except Exception as exc:
#         logger.exception("Error processing audio journal")
#         raise MentalHealthAgentError(str(exc)) from exc