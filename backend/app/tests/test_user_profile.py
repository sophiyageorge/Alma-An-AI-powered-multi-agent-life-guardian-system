import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime

from app.main import app
from app.schemas.user_profile import UserProfileResponse
from app.models.weekly_meal_plan import WeeklyMealPlan

client = TestClient(app, raise_server_exceptions=False)

# =========================
# MOCK RESPONSE DATA (IMPORTANT)
# =========================
mock_profile = {
    "id": 1,
    "user_id": 1,
    "calories": 1800,
    "diet": "vegetarian",
    "goal": "weight loss",
    "region": "Kerala",
    "restrictions": [],
    "meal_type": "home food",
    "created_at": "2026-03-19T00:00:00Z"  # MUST be string
}

mock_week_plan = WeeklyMealPlan(
    id=1,
    user_id=1,
    calories=2000,
    diet="vegetarian",
    region="US",
    restrictions=[],
    goal="weight_loss",
    meal_plan_text="Sample Meal Plan",
    created_at=datetime.utcnow(),
    is_approved=False,
)


# =========================
# GET PROFILE
# =========================
@patch("app.routers.user_profile.crud.get_profile")
def test_get_profile(mock_get):
    mock_get.return_value = mock_profile

    response = client.get("/profile/1")

    assert response.status_code == 200
    assert response.json()["user_id"] == 1


# =========================
# UPDATE PROFILE
# =========================
@patch("app.routers.user_profile.crud.update_profile")
@patch("app.routers.user_profile.generate_nutrition_plan")
def test_update_profile(mock_nutrition, mock_update):
    from app.routers.user_profile import orchestrator_store

    orchestrator_store.clear()

    updated_data = {
        "id": 1,
        "user_id": 1,
        "calories": 2200,
        "diet": "vegan",
        "goal": "muscle_gain",
        "region": "US",
        "restrictions": [],
        "meal_type": "standard",
        "created_at": "2026-03-19T00:00:00Z"
    }

    mock_update.return_value = UserProfileResponse(**updated_data)
    mock_nutrition.return_value = "Updated Meal Plan"

    response = client.put("/profile/1", json={
        "calories": 2200,
        "diet": "vegan",
        "goal": "muscle_gain",
        "region": "US",
        "restrictions": []
    })

    assert response.status_code == 200
    assert response.json()["goal"] == "muscle_gain"


