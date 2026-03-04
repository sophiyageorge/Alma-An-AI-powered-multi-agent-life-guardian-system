"""
test_journal.py
Unit tests for JournalManager.
"""

from app.agents.mental_health_agent.journal import JournalManager


def test_add_entry():
    manager = JournalManager()
    entry = manager.add_entry("user1", "I feel good today.")

    assert entry.user_id == "user1"
    assert isinstance(entry.mood_score, float)
    assert entry.emotion in ["positive", "neutral", "negative"]


def test_mood_trend():
    manager = JournalManager()
    manager.add_entry("user1", "I am happy.")
    manager.add_entry("user1", "Feeling great!")

    trend = manager.get_mood_trend("user1")

    assert trend["entries"] == 2
    assert isinstance(trend["average_mood"], float)


def test_empty_trend():
    manager = JournalManager()
    trend = manager.get_mood_trend("unknown_user")

    assert trend["entries"] == 0
    assert trend["average_mood"] == 0