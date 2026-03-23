import pytest
from app.agents.health.rules import detect_anomaly  # Adjust import path if needed

def test_normal_values():
    health_point = {
        "bp_systolic": 120,
        "bp_diastolic": 80,
        "heart_rate": 75,
        "spo2": 98
    }

    result = detect_anomaly(health_point)
    assert result["alert_level"] == "normal"
    assert result["anomalies"] == []


def test_heart_rate_warning():
    health_point = {"heart_rate": 105}
    result = detect_anomaly(health_point)
    assert result["alert_level"] == "warning"
    assert "heart_rate" in result["anomalies"]


def test_heart_rate_critical():
    health_point = {"heart_rate": 130}
    result = detect_anomaly(health_point)
    assert result["alert_level"] == "critical"
    assert "heart_rate" in result["anomalies"]


def test_spo2_warning():
    health_point = {"spo2": 93}
    result = detect_anomaly(health_point)
    assert result["alert_level"] == "warning"
    assert "spo2" in result["anomalies"]


def test_spo2_critical():
    health_point = {"spo2": 85}
    result = detect_anomaly(health_point)
    assert result["alert_level"] == "critical"
    assert "spo2" in result["anomalies"]


def test_bp_warning():
    health_point = {"bp_systolic": 145, "bp_diastolic": 95}
    result = detect_anomaly(health_point)
    assert result["alert_level"] == "warning"
    assert "blood_pressure" in result["anomalies"]


def test_bp_critical():
    health_point = {"bp_systolic": 165, "bp_diastolic": 105}
    result = detect_anomaly(health_point)
    assert result["alert_level"] == "critical"
    assert "blood_pressure" in result["anomalies"]


def test_multiple_anomalies():
    health_point = {
        "bp_systolic": 170,
        "bp_diastolic": 110,
        "heart_rate": 125,
        "spo2": 88
    }
    result = detect_anomaly(health_point)
    # Critical should override warning
    assert result["alert_level"] == "critical"
    assert set(result["anomalies"]) == {"blood_pressure", "heart_rate", "spo2"}


def test_missing_values():
    health_point = {}
    result = detect_anomaly(health_point)
    assert result["alert_level"] == "normal"
    assert result["anomalies"] == []