
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
#     try:
#         user_profile = state.get("user_profile", {})
#         user_id = user_profile.get("user_id")

#         if not user_id:
#             raise MentalHealthAgentError("user_id is missing in user_profile")

#         logger.info(f"Processing daily journal for user_id={user_id}")

#         # db = next(get_db())
#         db_gen = get_db()
#         db = next(db_gen)

#         today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
#         today_end = today_start + timedelta(days=1)

#         existing_entry = (
#             db.query(JournalEntry)
#             .filter(
#                 JournalEntry.user_id == user_id,
#                 JournalEntry.date_created >= today_start,
#                 JournalEntry.date_created < today_end,
#             )
#             .first()
#         )

#         # If journal already exists
#         if existing_entry:
#             logger.info(f"Journal entry for today already exists for user_id={user_id}")

#             state["daily_journal"] = {
#                 "journal_id": existing_entry.id,
#                 "journal_text": existing_entry.journal_text,
#                 "llm_response": existing_entry.llm_response
#             }

#             return state

#         # Default journal
#         journal_text = "I am starting my day."

#         logger.info("Building LLM prompt for mental health advisor")
#         prompt = build_mental_health_prompt(journal_text)

#         logger.info("Invoking LLM for mental health advice")
#         llm_response = llm.invoke(prompt)

#         # Save to DB
#         try:
#             new_entry = JournalEntry(
#                 user_id=user_id,
#                 journal_text=journal_text,
#                 language="en",
#                 duration=None,
#                 llm_response=llm_response
#             )

#             db.add(new_entry)
#             db.commit()
#             db.refresh(new_entry)

#             entry_id = new_entry.id
#             journal_text_value = new_entry.journal_text
#             llm_response_value = new_entry.llm_response

#             logger.info(f"Journal entry saved for user_id={user_id} with id={entry_id}")

#         except Exception as db_exc:
#             logger.exception("Failed to save journal entry to DB")
#             db.rollback()

#             entry_id = None
#             journal_text_value = journal_text
#             llm_response_value = llm_response

#         finally:
#             db_gen.close()

#         # Update state
#         state["daily_journal"] = {
#             "journal_id": entry_id,
#             "journal_text": journal_text_value,
#             "llm_response": llm_response_value
#         }

#         # Update orchestrator store
#         # orchestrator_store.setdefault(user_id, {})["daily_journal"] = state["daily_journal"]

#         return state

#     except Exception as e:
#         logger.exception("Error occurred in Mental Health Agent")
#         raise MentalHealthAgentError(str(e)) from e


# # def mental_health_agent(state: OrchestratorState) -> OrchestratorState:
# #     """
# #     Processes user's daily journal entry.
# #     If there is no entry for today, generates a default entry,
# #     invokes LLM to get advisor response, and updates state.

# #     Args:
# #         state (OrchestratorState): Current orchestrator state.

# #     Returns:
# #         OrchestratorState: Updated state with today's journal and LLM response.
# #     """
# #     try:
# #         user_profile = state.get("user_profile", {})
# #         user_id = user_profile.get("user_id")

# #         if not user_id:
# #             raise MentalHealthAgentError("user_id is missing in user_profile")

# #         logger.info(f"Processing daily journal for user_id={user_id}")

# #         # Database session
# #         db = next(get_db())
 
# #         today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
# #         today_end = today_start + timedelta(days=1)

# #         # Check if there is already a journal for today
# #         existing_entry = (
# #             db.query(JournalEntry)
# #             .filter(
# #                 JournalEntry.user_id == user_id,
# #                 JournalEntry.date_created >= today_start,
# #                 JournalEntry.date_created < today_end,
# #             )
# #             .first()
# #         )

# #         if existing_entry:
# #             logger.info(f"Journal entry for today already exists for user_id={user_id}")
# #             state["daily_journal"] = {
# #                 "journal_id": existing_entry.id,
# #                 "journal_text": existing_entry.journal_text,
# #                 "llm_response": existing_entry.llm_response
# #             }
# #             return state

# #         # No entry for today, create default journal
# #         journal_text = "I am starting my day."

# #         logger.info("Building LLM prompt for mental health advisor")
# #         prompt = build_mental_health_prompt(journal_text)

# #         logger.info("Invoking LLM for mental health advice")
# #         llm_response = llm.invoke(prompt)
# #         try:

# #         # Save journal + LLM response to DB
# #                 new_entry = JournalEntry(
# #                     user_id=user_id,
# #                     journal_text=journal_text,
# #                     language="en",
# #                     duration=None,
# #                     llm_response=llm_response
# #                 )
# #                 db.add(new_entry)
# #                 db.commit()
# #                 db.refresh(new_entry)
# #                 logger.info(f"Journal entry saved for user_id={user_id} with id={new_entry.id}")

# #                 entry_id = new_entry.id
# #                 journal_text = new_entry.journal_text
# #                 llm_response_value = new_entry.llm_response

# #         except Exception as db_exc:
# #             logger.info("Failed to save journal entry to DB")
# #             entry_id = None
# #             journal_text_value = journal_text
# #             llm_response_value = llm_response
        
# #         finally:
# #             db.close()

        

# #         # Update orchestrator state
# #         state["daily_journal"] = {
# #             "journal_id": entry_id,
# #             "journal_text": journal_text,
# #             "llm_response": llm_response_value
# #         }

# #         if user_id not in orchestrator_store:
# #             orchestrator_store[user_id] = {}

# #         orchestrator_store[user_id]["daily_journal"] = {
# #             "journal_id": entry_id,
# #             "journal_text": journal_text,
# #             "llm_response": llm_response_value
# #         }

# #         return state

# #     except Exception as e:
# #         print("Original error:", e)
# #         logger.exception("Error occurred in Mental Health Agent")
# #         raise MentalHealthAgentError(str(e)) from e
# def mental_health_agent(state: OrchestratorState) -> OrchestratorState:
    user_id = state["user_id"]
    db = state["db"]

    journal = get_today_journal(db,user_id)
    if journal:
        state["daily_journal"] = {
            "journal_id": journal.id,
            "journal_text": journal.journal_text,
            "llm_response": journal.llm_response
        }
        return state

    # Generate default journal
    journal_text = "I am starting my day."
    prompt = build_mental_health_prompt(journal_text)
    llm_response = llm.invoke(prompt)

    journal = save_journal(db, user_id, journal_text, llm_response)
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