from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_current_user
from app.models.user import User

def override_get_current_user():
    return User(user_id=1, name="Test User", email="test@example.com")

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_get_today_journal_not_found():
    response = client.get("/stt/journal/today")
    assert response.status_code == 404