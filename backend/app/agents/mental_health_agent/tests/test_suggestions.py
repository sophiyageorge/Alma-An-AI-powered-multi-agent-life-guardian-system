"""
test_suggestions.py
Unit tests for suggestions engine.
"""

from app.agents.mental_health_agent.suggestions import suggest_activity


def test_negative_suggestion():
    suggestion = suggest_activity("negative")
    assert "activity" in suggestion
    assert "reading" in suggestion


def test_unknown_emotion():
    suggestion = suggest_activity("unknown")
    assert suggestion == {}