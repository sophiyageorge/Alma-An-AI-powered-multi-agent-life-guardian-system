import sys
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.orchestrator.state import OrchestratorState
from app.agents.nutrition.agent import nutrition_agent

def test_nutrition_agent_run():
    state: OrchestratorState = {
        "user_id": "user_123",
        "user_profile": {
            "calories": 1800,
            "diet": "vegetarian",
            "goal": "weight loss",
            "region": "Indian",
            "restrictions": "no dairy",
            "meal_type": "home cooked",
            "week": 1
        },
        "health_data": None,
        "journal_text": None,
        "nutrition_plan": None,
        "exercise_plan": None,
        "grocery_list": None,
        "mental_insights": None,
        "meal_plan_approved": False,
        "anomaly_detected": False,
        "emergency_level": None,
        "compliance_passed": True,
        "response": None
    }

    # Run the agent
    updated_state = nutrition_agent(state)

    # Assertions (basic example)
    assert "nutrition_plan" in updated_state
    assert updated_state["nutrition_plan"]["meal_plan_text"] is not None

    # Optional: print meal plan (pytest will show with -s)
    print("\n===== 7-Day Meal Plan =====\n")
    print(updated_state["nutrition_plan"]["meal_plan_text"])
