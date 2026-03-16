"""
Mental Health Agent Implementation
----------------------------------
Processes user's daily journal entry. If no entry exists for today, 
generates a default entry, invokes LLM for advisor response, and 
updates the orchestrator state.
"""

from datetime import datetime
from app.orchestrator.state import OrchestratorState
from app.llm.llm_client import llm
from app.agents.mental_health_agent.prompt import build_mental_health_prompt
from app.core.logging_config import setup_logger
from app.core.exceptions import MentalHealthAgentError
from app.crud.mental_health import get_today_journal, save_journal

logger = setup_logger(__name__)


def mental_health_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Processes the user's daily journal entry.

    Steps:
    1. Fetch today's journal entry from the DB.
    2. If exists, do nothing (or optionally return it in state).
    3. If not, generate a default entry and get LLM response.
    4. Save new journal entry to DB via CRUD.
    5. Update orchestrator state with today's journal.

    Args:
        state (OrchestratorState): Current orchestrator state containing 'user_profile' and 'db'.

    Returns:
        OrchestratorState: Updated state with today's journal.
    """

    try:
        user_profile = state.get("user_profile", {})
        user_id = user_profile.get("user_id")
        db = state.get("db")

        if not user_id or not db:
            raise MentalHealthAgentError("Missing user_id or database session in state")

        logger.info("Mental Health Agent started for user_id=%s", user_id)

        # -------------------------------
        # Fetch today's journal entry
        # -------------------------------
        journal = get_today_journal(db, user_id)

        if journal:
            logger.info("Journal entry already exists for today | journal_id=%s", journal.id)
            # Optionally, include in state for downstream agents
            state["daily_journal"] = {
                "journal_id": journal.id,
                "journal_text": journal.journal_text,
                "llm_response": journal.llm_response
            }
            return state

        # -------------------------------
        # No journal entry found, create default
        # -------------------------------
        logger.info("No journal entry for today, generating default entry")
        journal_text = "I am starting my day."
        prompt = build_mental_health_prompt(journal_text)

        # Invoke LLM for advisor response
        llm_response = llm.invoke(prompt)
        logger.debug("LLM response generated for user_id=%s", user_id)

        # -------------------------------
        # Save journal entry via CRUD
        # -------------------------------
        journal = save_journal(db, user_id, journal_text, llm_response)

        if not journal:
            logger.error("Failed to save journal entry for user_id=%s", user_id)
            raise MentalHealthAgentError("Failed to save journal entry to DB")

        logger.info("Journal entry saved successfully | journal_id=%s", journal.id)

        # -------------------------------
        # Update orchestrator state
        # -------------------------------
        state["daily_journal"] = {
            "journal_id": journal.id,
            "journal_text": journal.journal_text,
            "llm_response": journal.llm_response
        }

        return state

    except Exception as e:
        logger.exception("Mental Health Agent failed for user_id=%s", user_profile.get("user_id"))
        raise MentalHealthAgentError(str(e)) from e
