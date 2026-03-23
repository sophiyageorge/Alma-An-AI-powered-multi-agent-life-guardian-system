import pytest
from app.agents.health.rules import detect_anomaly  # adjust import


def test_normal_values():
    data = {
        "heart_rate": 72,
        "spo2": 98,
        "bp_systolic": 120,
        "bp_diastolic": 80
    }

    result = detect_anomaly(data)

    assert result["alert_level"] == "normal"
    assert result["anomalies"] == []


def test_heart_rate_warning():
    data = {
        "heart_rate": 105,
        "spo2": 98,
        "bp_systolic": 120,
        "bp_diastolic": 80
    }

    result = detect_anomaly(data)

    assert result["alert_level"] == "warning"
    assert "heart_rate" in result["anomalies"]


def test_heart_rate_critical():
    data = {
        "heart_rate": 130,
        "spo2": 98,
        "bp_systolic": 120,
        "bp_diastolic": 80
    }

    result = detect_anomaly(data)

    assert result["alert_level"] == "critical"
    assert "heart_rate" in result["anomalies"]


def test_spo2_critical():
    data = {
        "heart_rate": 80,
        "spo2": 85,
        "bp_systolic": 120,
        "bp_diastolic": 80
    }

    result = detect_anomaly(data)

    assert result["alert_level"] == "critical"
    assert "spo2" in result["anomalies"]


def test_blood_pressure_warning():
    data = {
        "heart_rate": 80,
        "spo2": 98,
        "bp_systolic": 145,
        "bp_diastolic": 95
    }

    result = detect_anomaly(data)

    assert result["alert_level"] == "warning"
    assert "blood_pressure" in result["anomalies"]


def test_blood_pressure_critical():
    data = {
        "heart_rate": 80,
        "spo2": 98,
        "bp_systolic": 170,
        "bp_diastolic": 110
    }

    result = detect_anomaly(data)

    assert result["alert_level"] == "critical"
    assert "blood_pressure" in result["anomalies"]


def test_multiple_anomalies():
    data = {
        "heart_rate": 130,
        "spo2": 85,
        "bp_systolic": 170,
        "bp_diastolic": 110
    }

    result = detect_anomaly(data)

    assert result["alert_level"] == "critical"
    assert "heart_rate" in result["anomalies"]
    assert "spo2" in result["anomalies"]
    assert "blood_pressure" in result["anomalies"]


def test_missing_values():
    data = {
        "heart_rate": None,
        "spo2": None,
        "bp_systolic": None,
        "bp_diastolic": None
    }

    result = detect_anomaly(data)

    assert result["alert_level"] == "normal"
    assert result["anomalies"] == []