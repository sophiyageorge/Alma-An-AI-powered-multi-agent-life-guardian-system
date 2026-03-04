def detect_anomaly(health_point: dict) -> dict:
    """
    Detect anomalies based on predefined thresholds.

    Args:
        health_point (dict): Single health data point

    Returns:
        dict: health_point with anomaly and alert_level added
    """
    alert_level = "normal"
    anomalies = []

    bp_sys, bp_dia = health_point["bp_systolic"], health_point["bp_diastolic"]
    # map(int, health_point["blood_pressure"].split("/"))
    hr = health_point["heart_rate"]
    spo2 = health_point["spo2"]
    # bp_sys = health_point["bp_systolic"]
    # bp_dia = health_point["bp_diastolic"]

    # Heart Rate
    if hr < 60 or hr > 120:
        alert_level = "critical"
        anomalies.append("heart_rate")
    elif hr > 100:
        alert_level = "warning"
        anomalies.append("heart_rate")

    # SpO2
    if spo2 < 90:
        alert_level = "critical"
        anomalies.append("spo2")
    elif spo2 < 95:
        alert_level = "warning"
        anomalies.append("spo2")

    # Blood Pressure
    if bp_sys > 160 or bp_dia > 100:
        alert_level = "critical"
        anomalies.append("blood_pressure")
    elif bp_sys > 140 or bp_dia > 90:
        alert_level = "warning"
        anomalies.append("blood_pressure")

    health_point["alert_level"] = alert_level
    health_point["anomalies"] = anomalies
    return health_point
