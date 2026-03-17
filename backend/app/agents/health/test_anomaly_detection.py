# """
# test_anomaly_detection.py

# Unit tests for detect_anomaly function.
# """

# import pytest
# from app.agents.health.rules     import detect_anomaly


# def test_normal_health_data():
#     """
#     Test that normal health values return 'normal' alert level.
#     """
#     sample = {
#         "heart_rate": 80,
#         "spo2": 97,
#         "blood_pressure": "120/80"
#     }

#     result = detect_anomaly(sample)

#     assert result["alert_level"] == "normal"
#     assert result["anomalies"] == []


# def test_warning_health_data():
#     """
#     Test warning level detection.
#     """
#     sample = {
#         "heart_rate": 105,
#         "spo2": 94,
#         # "blood_pressure": "145/92"
#         "bp_systolic": 145,
#         "bp_diastolic": 92
#     }

#     result = detect_anomaly(sample)

#     assert result["alert_level"] == "warning"
#     assert "heart_rate" in result["anomalies"]
#     assert "spo2" in result["anomalies"]
#     assert "bp_systolic" in result["anomalies"]
#     assert "bp_diastolic" in result["anomalies"]

# def test_critical_health_data():
#     """
#     Test critical level detection.
#     """
#     sample = {
#         "heart_rate": 130,
#         "spo2": 85,
#         # "blood_pressure": "170/110",
#         "bp_systolic": 170,
#         "bp_diastolic": 110 
    
#     }

#     result = detect_anomaly(sample)

#     assert result["alert_level"] == "critical"
#     assert "heart_rate" in result["anomalies"]
#     assert "spo2" in result["anomalies"]
#     assert "blood_pressure" in result["anomalies"]


# def test_edge_case_threshold_values():
#     """
#     Test exact boundary values.
#     """
#     sample = {
#         "heart_rate": 100,
#         "spo2": 95,
#         "bp_systolic": 140,
#         "bp_diastolic": 90
#     }

#     result = detect_anomaly(sample)

#     # These are boundary values, should be normal
#     assert result["alert_level"] == "normal"
#     assert result["anomalies"] == []


# def test_invalid_blood_pressure_format():
#     """
#     Test invalid blood pressure format handling.
#     """
#     sample = {
#         "heart_rate": 80,
#         "spo2": 98,
#         "blood_pressure": "invalid_format"
#     }

#     with pytest.raises(ValueError):
#         detect_anomaly(sample)