import uuid
from unittest.mock import patch
import pytest
from app.main import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_login_success_with_orchestrator():
    payload = {
        "name": "Test User",
        "email": f"test_{uuid.uuid4()}@example.com",
        "date_of_birth": "2000-01-01",
        "gender": "Male",
        "password": "test123",
        "phone": "1234567890"
    }

    client.post("/users/register", json=payload)

    with patch("app.routers.user.run_orchestrator") as mock_orch:
        login_payload = {
            "email": payload["email"],
            "password": payload["password"]
        }
        response = client.post("/users/login", json=login_payload)

        assert response.status_code == 200
        mock_orch.assert_called_once()  # verify orchestrator was scheduled