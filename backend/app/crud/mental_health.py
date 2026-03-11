# --------------------------
# Journal DB operations
# --------------------------

# def save_journal_entry(db: Session, user_id: int, journal_text: str, llm_response: str, language: str = "en", duration: float = None) -> JournalEntry:
#     entry = JournalEntry(
#         user_id=user_id,
#         journal_text=journal_text,
#         language=language,
#         duration=duration,
#         llm_response=llm_response,
#         date_created=datetime.utcnow()
#     )
#     db.add(entry)
#     db.commit()
#     db.refresh(entry)
#     return entry


# def get_today_journal(db: Session, user_id: int):
#     from datetime import timedelta
#     today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
#     today_end = today_start + timedelta(days=1)
#     return db.query(JournalEntry).filter(
#         JournalEntry.user_id == user_id,
#         JournalEntry.date_created >= today_start,
#         JournalEntry.date_created < today_end
#     ).first()


from app.models.mental_health import JournalEntry
from datetime import datetime, timedelta

def get_today_journal(db, user_id):
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    return db.query(JournalEntry).filter(
        JournalEntry.user_id==user_id,
        JournalEntry.date_created >= today_start,
        JournalEntry.date_created < today_end
    ).first()

def save_journal(db, user_id, journal_text, llm_response):
    new_entry = JournalEntry(
        user_id=user_id,
        journal_text=journal_text,
        language="en",
        llm_response=llm_response
    )
    db.add(new_entry)
    db.commit()
    # db.refresh(new_entry)
    return new_entry