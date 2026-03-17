"""
Journal DB Operations
---------------------

Helper functions for managing user journal entries for the
Mental Health Agent.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.mental_health import JournalEntry
import logging
from app.core.exceptions import MentalHealthAgentError

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


# --------------------------
# Get Today's Journal Entry
# --------------------------
def get_today_journal(db: Session, user_id: int) -> JournalEntry | None:
    """
    Fetch today's journal entry for a given user.

    Args:
        db (Session): SQLAlchemy database session
        user_id (int): User ID

    Returns:
        JournalEntry | None: Today's journal entry if exists, else None
    """
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    try:
        entry = db.query(JournalEntry).filter(
            JournalEntry.user_id == user_id,
            JournalEntry.date_created >= today_start,
            JournalEntry.date_created < today_end
        ).first()

        if entry:
            logger.info(f"Found existing journal entry | user_id={user_id} | entry_id={entry.id}")
        else:
            logger.info(f"No journal entry found for today | user_id={user_id}")

        return entry

    except Exception as e:
        logger.exception(f"Failed to fetch today's journal entry | user_id={user_id}")
        raise e


# --------------------------
# Save Journal Entry
# --------------------------
def save_journal(db: Session, user_id: int, journal_text: str, llm_response: str, language: str = "en") -> JournalEntry:
    """
    Save a new journal entry for the user.

    Args:
        db (Session): SQLAlchemy database session
        user_id (int): User ID
        journal_text (str): Raw journal text from user
        llm_response (str): LLM-generated insights/response
        language (str): Language code (default: 'en')

    Returns:
        JournalEntry: Newly created journal entry
    """
    try:
        new_entry = JournalEntry(
            user_id=user_id,
            journal_text=journal_text,
            llm_response=llm_response,
            language=language,
            date_created=datetime.utcnow()
        )

        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        logger.info(f"Journal entry saved | user_id={user_id} | entry_id={new_entry.id}")
        return new_entry

    except Exception as e:
        db.rollback()
        logger.exception(f"Failed to save journal entry | user_id={user_id}")
        raise e


def update_journal(
    db: Session,
    journal_id: int,
    journal_text: str,
    llm_response: str,
    language: str = "en"
) -> JournalEntry:
    """
    Update an existing journal entry by ID.

    Args:
        db: SQLAlchemy Session
        journal_id: ID of the journal entry to update
        journal_text: updated journal text
        llm_response: updated LLM response
        language: language of the journal (default "en")

    Returns:
        Updated JournalEntry object

    Raises:
        MentalHealthAgentError: if journal entry not found
    """

    # 1️⃣ Fetch existing journal entry
    entry = db.query(JournalEntry).filter(JournalEntry.id == journal_id).first()
    
    if not entry:
        raise MentalHealthAgentError(f"Journal entry with id={journal_id} not found")

    # 2️⃣ Update fields
    entry.journal_text = journal_text
    entry.llm_response = llm_response
    entry.language = language
    entry.updated_at = datetime.utcnow()  # assuming your model has updated_at

    # 3️⃣ Commit changes
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry
