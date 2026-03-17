from unittest.mock import MagicMock
from app.orchestrator.graph import build_graph


def test_agents_workflow():

    graph = build_graph()

    state = {
        "user_profile": {
            "user_id": 1,
            "calories": 1800,
            "diet": "veg",
            "goal": "maintain",
            "region": "test",
            "restrictions": [],
            "meal_type": "home"
        },
        "db": MagicMock(),   # ✅ IMPORTANT
        "health_data": None,
        "journal_text": None,
        "meal_plan_approved": False,
        "exercise_plan_approved": False,
        "anomaly_detected": False,
        "compliance_passed": True
    }

    result = graph.invoke(state)

    assert result is not None