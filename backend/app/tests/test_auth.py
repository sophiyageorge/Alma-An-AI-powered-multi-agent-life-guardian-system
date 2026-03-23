import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


def test_register_user():
    payload = {
        "name": "Test User",
        "email": f"test_{uuid.uuid4()}@example.com",
        "date_of_birth": "2000-01-01",
        "gender": "Male",
        "password": "test123",
        "phone": "1234567890"
    }

    response = client.post("/users/register", json=payload)
    print(response.status_code)
    print(response.json()) 

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert "user_id" in data


def test_register_existing_user():
    payload = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "test123",
        "date_of_birth": "2000-01-01",
        "gender": "Male",
        "phone": "1234567890"
    }

    # First registration
    client.post("/users/register", json=payload)

    # Second registration should fail
    response = client.post("/users/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success():
    payload = {
        "name": "Test User",
        "email": f"test_{uuid.uuid4()}@example.com",
        "date_of_birth": "2000-01-01",
        "gender": "Male",
        "password": "test123",
        "phone": "1234567890"
    }

    # Register first
    client.post("/users/register", json=payload)

    # Login
    login_payload = {
        "email": payload["email"],
        "password": payload["password"]
    }
    response = client.post("/users/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    payload = {
        "email": "wrong@example.com",
        "password": "wrongpass"
    }

    response = client.post("/users/login", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"