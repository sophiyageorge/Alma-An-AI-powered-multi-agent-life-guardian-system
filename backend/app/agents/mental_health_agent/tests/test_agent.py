"""
test_agent.py
Unit tests for MentalHealthAgent.
"""

from app.agents.mental_health_agent.agent import MentalHealthAgent


def test_checkin():
    agent = MentalHealthAgent()
    response = agent.checkin("user1", "I feel happy today.")

    assert response["user_id"] == "user1"
    assert "mood_score" in response
    assert "emotion" in response
    assert "suggestion" in response


def test_trend():
    agent = MentalHealthAgent()
    agent.checkin("user1", "I feel good.")
    agent.checkin("user1", "I feel great.")

    trend = agent.get_trend("user1")

    assert trend["entries"] == 2
    assert isinstance(trend["average_mood"], float)