"""
test_exercise_service.py
Unit tests for recommend_exercise service
"""

import pytest
from unittest.mock import MagicMock, patch

from app.agents.exercise.service import recommend_exercise
from app.core.exceptions import ExerciseAgentError


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_metrics():
    return {
        "id": 10,
        "heart_rate": 75,
        "bp_systolic": 120,
        "bp_diastolic": 80,
        "spo2": 98,
        "steps": 5000
    }


# ---------------------------------------------------------
# ✅ 1. Test NEW entry (save)
# ---------------------------------------------------------
@patch("app.agents.exercise.service.save_exercise_entry")
@patch("app.agents.exercise.service.get_today_exercise_entry")
@patch("app.agents.exercise.service.llm")
@patch("app.agents.exercise.service.build_exercise_prompt")
def test_recommend_exercise_new_entry(
    mock_prompt, mock_llm, mock_get_today, mock_save, mock_db, mock_metrics
):
    """Test creating a new exercise recommendation"""

    mock_prompt.return_value = "PROMPT"

    mock_llm.invoke.return_value = """
    {
        "intensity": "medium",
        "plan": ["Walk 20 mins"],
        "warnings": ["None"],
        "recovery_advice": "Drink water"
    }
    """

    mock_get_today.return_value = None

    mock_entry = MagicMock()
    mock_entry.id = 1
    mock_entry.created_at = "2026-01-01"
    mock_save.return_value = mock_entry

    result = recommend_exercise(user_id=1, metrics=mock_metrics, db=mock_db)

    assert result["id"] == 1
    assert result["intensity"] == "medium"
    assert result["plan"] == ["Walk 20 mins"]
    mock_save.assert_called_once()
    mock_get_today.assert_called_once()


# ---------------------------------------------------------
# ✅ 2. Test UPDATE existing entry
# ---------------------------------------------------------
@patch("app.agents.exercise.service.update_exercise_entry")
@patch("app.agents.exercise.service.get_today_exercise_entry")
@patch("app.agents.exercise.service.llm")
@patch("app.agents.exercise.service.build_exercise_prompt")
def test_recommend_exercise_update_entry(
    mock_prompt, mock_llm, mock_get_today, mock_update, mock_db, mock_metrics
):
    """Test updating existing recommendation"""

    mock_prompt.return_value = "PROMPT"

    mock_llm.invoke.return_value = """
    {
        "intensity": "high",
        "plan": ["Run 30 mins"],
        "warnings": ["High HR"],
        "recovery_advice": "Rest well"
    }
    """

    existing_entry = MagicMock()
    existing_entry.id = 2
    mock_get_today.return_value = existing_entry

    updated_entry = MagicMock()
    updated_entry.id = 2
    updated_entry.created_at = "2026-01-01"
    mock_update.return_value = updated_entry

    result = recommend_exercise(user_id=1, metrics=mock_metrics, db=mock_db)

    assert result["id"] == 2
    assert result["intensity"] == "high"
    mock_update.assert_called_once()
    mock_get_today.assert_called_once()


# ---------------------------------------------------------
# ✅ 3. Test fallback when LLM returns invalid JSON
# ---------------------------------------------------------
@patch("app.agents.exercise.service.save_exercise_entry")
@patch("app.agents.exercise.service.get_today_exercise_entry")
@patch("app.agents.exercise.service.llm")
@patch("app.agents.exercise.service.build_exercise_prompt")
def test_recommend_exercise_fallback(
    mock_prompt, mock_llm, mock_get_today, mock_save, mock_db, mock_metrics
):
    """Test fallback plan when LLM response is invalid"""

    mock_prompt.return_value = "PROMPT"

    # Invalid JSON
    mock_llm.invoke.return_value = "INVALID RESPONSE"

    mock_get_today.return_value = None

    mock_entry = MagicMock()
    mock_entry.id = 3
    mock_entry.created_at = "2026-01-01"
    mock_save.return_value = mock_entry

    result = recommend_exercise(user_id=1, metrics=mock_metrics, db=mock_db)

    assert result["intensity"] == "low"   # fallback default
    assert "plan" in result
    assert "warnings" in result


# ---------------------------------------------------------
# ✅ 4. Test exception handling
# ---------------------------------------------------------
@patch("app.agents.exercise.service.build_exercise_prompt")
def test_recommend_exercise_exception(mock_prompt, mock_db):
    """Test exception handling"""

    mock_prompt.side_effect = Exception("Prompt failed")

    with pytest.raises(ExerciseAgentError):
        recommend_exercise(user_id=1, metrics=None, db=mock_db)