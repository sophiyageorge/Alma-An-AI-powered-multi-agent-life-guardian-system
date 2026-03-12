
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
from app.crud.mental_health import get_today_journal, save_journal
# from app.orchestrator.store import orchestrator_store

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


    user_profile = state.get("user_profile", {})
    db = state["db"]

    journal = get_today_journal(db,user_profile.get("user_id"))
    if journal:
        # state["daily_journal"] = {
        #     "journal_id": journal.id,
        #     "journal_text": journal.journal_text,
        #     "llm_response": journal.llm_response
        # }
        return state
    else:

        # Generate default journal
        journal_text = "I am starting my day."
        prompt = build_mental_health_prompt(journal_text)
        llm_response = llm.invoke(prompt)

        journal = save_journal(db, user_profile.get("user_id"), journal_text, llm_response)
    # if not journal:
    #     logger.error("Failed to save journal entry to DB")
    #     raise MentalHealthAgentError("Failed to save journal entry to DB")
    # else:
    #     logger.info(f"Journal entry saved for user_id={user_id} with id={journal}")
    #     state["daily_journal"] = {
    #         "journal_id": journal.id,
    #         "journal_text": journal.journal_text,
    #         "llm_response": journal.llm_response
        # }
    return state