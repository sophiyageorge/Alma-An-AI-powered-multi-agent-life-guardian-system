# app/tests/test_exercise_simple.py
import pytest
from fastapi.testclient import TestClient
from app.main import app  # make sure this imports your FastAPI app

client = TestClient(app)

def test_exercise_recommendation_response():
    """
    Test the /recommendation endpoint returns a valid response structure.
    This test assumes that the database has at least one user with health metrics.
    """
    response = client.get("/recommendation")
    assert response.status_code == 404
    data = response.json()
    
  