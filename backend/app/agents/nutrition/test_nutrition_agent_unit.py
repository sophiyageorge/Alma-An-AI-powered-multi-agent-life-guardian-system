import sys
from pathlib import Path
import pytest
from unittest.mock import patch

# Add backend folder to Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.agents.nutrition.agent import nutrition_agent
from app.agents.nutrition.utils import validate_user_profile
from app.core.exceptions import NutritionAgentError

# -------------------------------
# Utility Tests
# -------------------------------

def test_validate_user_profile_success():
    profile = {
        "calories": 1500,
        "diet": "vegetarian",
        "goal": "weight loss"
    }
    validate_user_profile(profile)


def test_validate_user_profile_missing_field():
    profile = {"diet": "vegetarian"}
    with pytest.raises(ValueError):
        validate_user_profile(profile)


# -------------------------------
# Agent Tests
# -------------------------------

def test_nutrition_agent_success():
    mock_state = {
        "user_profile": {
            "calories": 1500,
            "diet": "vegetarian",
            "goal": "weight loss",
            "region": "Indian",
            "restrictions": "no dairy",
            "meal_type": "home cooked",
            "week": 1
        }
    }

    # Mock LLM
    with patch("app.agents.nutrition.agent.llm.invoke") as mock_llm:
        mock_llm.return_value = "Mocked 7-day meal plan paragraph"
        updated_state = nutrition_agent(mock_state)

        # Assertions
        assert "nutrition_plan" in updated_state
        assert updated_state["nutrition_plan"]["calories_per_day"] == 1500
        assert updated_state["nutrition_plan"]["meal_plan_text"] == "Mocked 7-day meal plan paragraph"


def test_nutrition_agent_missing_required_fields():
    mock_state = {"user_profile": {"diet": "vegetarian"}}
    with patch("app.agents.nutrition.agent.llm.invoke"):
        with pytest.raises(NutritionAgentError):
            nutrition_agent(mock_state)
