"""
test_journal.py
Unit tests for process_audio_journal function.
"""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.mental_health_agent.journal import process_audio_journal
from app.core.exceptions import MentalHealthAgentError


@pytest.fixture
def mock_audio_bytes():
    return b"dummy audio content"


@pytest.fixture
def mock_db():
    return MagicMock()


@patch("app.agents.mental_health_agent.journal_service.SpeechToTextEngine")
@patch("app.agents.mental_health_agent.journal_service.llm")
@patch("app.agents.mental_health_agent.journal_service.build_mental_health_prompt")
@patch("app.agents.mental_health_agent.journal_service.get_today_journal")
@patch("app.agents.mental_health_agent.journal_service.save_journal")
@patch("app.agents.mental_health_agent.journal_service.update_journal")
def test_process_audio_journal_new_entry(
    mock_update, mock_save, mock_get_journal, mock_build_prompt, mock_llm, mock_stt, 
    mock_audio_bytes, mock_db
):
    """Test creating a new journal entry when none exists for today."""
    # No existing journal
    mock_get_journal.return_value = None
    
    # Mock STT
    stt_instance = mock_stt.return_value
    stt_instance.transcribe.return_value = {"text": "I am happy", "duration": 10, "language": "en"}

    # Mock LLM
    mock_build_prompt.return_value = "PROMPT"
    mock_llm.invoke.return_value = "LLM advice"

    # Mock saved journal
    mock_journal = MagicMock()
    mock_journal.id = 1
    mock_journal.journal_text = "I am happy"
    mock_journal.llm_response = "LLM advice"
    mock_save.return_value = mock_journal

    result = process_audio_journal(mock_audio_bytes, user_id=123, db=mock_db)

    # Assertions
    assert result.id == 1
    assert result.journal_text == "I am happy"
    assert result.llm_response == "LLM advice"
    mock_save.assert_called_once()
    mock_update.assert_not_called()


@patch("app.agents.mental_health_agent.journal_service.SpeechToTextEngine")
@patch("app.agents.mental_health_agent.journal_service.llm")
@patch("app.agents.mental_health_agent.journal_service.build_mental_health_prompt")
@patch("app.agents.mental_health_agent.journal_service.get_today_journal")
@patch("app.agents.mental_health_agent.journal_service.save_journal")
@patch("app.agents.mental_health_agent.journal_service.update_journal")
def test_process_audio_journal_update_entry(
    mock_update, mock_save, mock_get_journal, mock_build_prompt, mock_llm, mock_stt, 
    mock_audio_bytes, mock_db
):
    """Test updating today's existing journal entry."""
    # Existing journal
    existing_journal = MagicMock()
    existing_journal.id = 2
    mock_get_journal.return_value = existing_journal

    # Mock STT
    stt_instance = mock_stt.return_value
    stt_instance.transcribe.return_value = {"text": "Feeling good", "duration": 5, "language": "en"}

    # Mock LLM
    mock_build_prompt.return_value = "PROMPT"
    mock_llm.invoke.return_value = "LLM advice updated"

    # Mock updated journal
    updated_journal = MagicMock()
    updated_journal.id = 2
    updated_journal.journal_text = "Feeling good"
    updated_journal.llm_response = "LLM advice updated"
    mock_update.return_value = updated_journal

    result = process_audio_journal(mock_audio_bytes, user_id=123, db=mock_db)

    # Assertions
    assert result.id == 2
    assert result.journal_text == "Feeling good"
    assert result.llm_response == "LLM advice updated"
    mock_update.assert_called_once()
    mock_save.assert_not_called()


def test_process_audio_journal_missing_user(monkeypatch, mock_audio_bytes):
    """Test that exceptions are properly raised if something fails."""
    from app.agents.mental_health_agent.journal_service import process_audio_journal, MentalHealthAgentError

    # Force transcribe to raise error
    class FailingSTT:
        def transcribe(self, _):
            raise Exception("STT failed")

    monkeypatch.setattr("app.agents.mental_health_agent.journal_service.SpeechToTextEngine", lambda **kwargs: FailingSTT())

    with pytest.raises(MentalHealthAgentError):
        process_audio_journal(mock_audio_bytes, user_id=None, db=MagicMock())