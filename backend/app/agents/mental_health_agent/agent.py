"""
Mental Health Agent Implementation.
"""

from datetime import datetime, timedelta
from app.orchestrator.state import OrchestratorState
from app.llm.llm_client import llm
from app.agents.mental_health_agent.prompt import build_mental_health_prompt
from app.core.logging_config import setup_logger
from app.core.exceptions import MentalHealthAgentError
from app.database import get_db
from app.models.mental_health import JournalEntry

logger = setup_logger(__name__)


def mental_health_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Processes user's daily journal entry.
    If there is no entry for today, generates a default entry,
    invokes LLM to get advisor response, and updates state.

    Args:
        state (OrchestratorState): Current orchestrator state.

    Returns:
        OrchestratorState: Updated state with today's journal and LLM response.
    """
    try:
        user_profile = state.get("user_profile", {})
        user_id = user_profile.get("user_id")

        if not user_id:
            raise MentalHealthAgentError("user_id is missing in user_profile")

        logger.info(f"Processing daily journal for user_id={user_id}")

        # Database session
        db = next(get_db())

        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        # Check if there is already a journal for today
        existing_entry = (
            db.query(JournalEntry)
            .filter(
                JournalEntry.user_id == user_id,
                JournalEntry.date_created >= today_start,
                JournalEntry.date_created < today_end,
            )
            .first()
        )

        if existing_entry:
            logger.info(f"Journal entry for today already exists for user_id={user_id}")
            state["daily_journal"] = {
                "journal_id": existing_entry.id,
                "journal_text": existing_entry.journal_text,
                "llm_response": existing_entry.llm_response
            }
            return state

        # No entry for today, create default journal
        journal_text = "I am starting my day."

        logger.info("Building LLM prompt for mental health advisor")
        prompt = build_mental_health_prompt(journal_text)

        logger.info("Invoking LLM for mental health advice")
        llm_response = llm.invoke(prompt)

        # Save journal + LLM response to DB
        new_entry = JournalEntry(
            user_id=user_id,
            journal_text=journal_text,
            language="en",
            duration=None,
            llm_response=llm_response
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        logger.info(f"Journal entry saved for user_id={user_id} with id={new_entry.id}")

        # Update orchestrator state
        state["daily_journal"] = {
            "journal_id": new_entry.id,
            "journal_text": new_entry.journal_text,
            "llm_response": new_entry.llm_response
        }

        return state

    except Exception as e:
        print("Original error:", e)
        logger.exception("Error occurred in Mental Health Agent")
        raise MentalHealthAgentError(str(e)) from e