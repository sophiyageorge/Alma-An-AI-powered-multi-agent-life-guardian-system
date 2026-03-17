"""
test_mental_health_agent.py
Unit tests for mental_health_agent function.
"""

import pytest
from unittest.mock import MagicMock, patch

from app.agents.mental_health_agent.agent import mental_health_agent
from app.core.exceptions import MentalHealthAgentError


@pytest.fixture
def mock_state():
    """Returns a minimal valid orchestrator state."""
    return {
        "user_profile": {"user_id": "user1"},
        "db": MagicMock()
    }


@patch("app.agents.mental_health_agent.agent_impl.get_today_journal")
@patch("app.agents.mental_health_agent.agent_impl.save_journal")
@patch("app.agents.mental_health_agent.agent_impl.llm")
@patch("app.agents.mental_health_agent.agent_impl.build_mental_health_prompt")
def test_mental_health_agent_creates_entry(mock_build_prompt, mock_llm, mock_save, mock_get_journal, mock_state):
    """
    Test that a journal entry is created if none exists for today,
    LLM is invoked, and state is updated.
    """
    mock_get_journal.return_value = None  # No journal exists
    mock_build_prompt.return_value = "PROMPT"
    mock_llm.invoke.return_value = "LLM ADVICE"
    
    # Mock saved journal object
    mock_journal = MagicMock()
    mock_journal.id = 123
    mock_journal.journal_text = "I am starting my day."
    mock_journal.llm_response = "LLM ADVICE"
    mock_save.return_value = mock_journal

    updated_state = mental_health_agent(mock_state)

    # Assertions
    assert "daily_journal" in updated_state
    dj = updated_state["daily_journal"]
    assert dj["journal_id"] == 123
    assert dj["journal_text"] == "I am starting my day."
    assert dj["llm_response"] == "LLM ADVICE"
    mock_llm.invoke.assert_called_once_with("PROMPT")
    mock_save.assert_called_once_with(mock_state["db"], "user1", "I am starting my day.", "LLM ADVICE")


@patch("app.agents.mental_health_agent.agent_impl.get_today_journal")
def test_mental_health_agent_existing_entry(mock_get_journal, mock_state):
    """
    Test that if today's journal exists, state is updated without calling LLM or save.
    """
    mock_journal = MagicMock()
    mock_journal.id = 321
    mock_journal.journal_text = "Existing journal"
    mock_journal.llm_response = "Existing advice"
    mock_get_journal.return_value = mock_journal

    updated_state = mental_health_agent(mock_state)

    dj = updated_state["daily_journal"]
    assert dj["journal_id"] == 321
    assert dj["journal_text"] == "Existing journal"
    assert dj["llm_response"] == "Existing advice"


def test_mental_health_agent_missing_user_or_db():
    """Test that missing user_id or db raises MentalHealthAgentError."""
    from app.agents.mental_health_agent.agent_impl import mental_health_agent

    # Missing user_id
    state1 = {"user_profile": {}, "db": MagicMock()}
    with pytest.raises(MentalHealthAgentError):
        mental_health_agent(state1)

    # Missing db
    state2 = {"user_profile": {"user_id": "user1"}}
    with pytest.raises(MentalHealthAgentError):
        mental_health_agent(state2)