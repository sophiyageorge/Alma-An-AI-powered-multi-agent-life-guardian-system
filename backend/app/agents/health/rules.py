def detect_anomaly(health_point: dict) -> dict:
    alert_level = "normal"
    anomalies = []

    bp_sys = health_point.get("bp_systolic")
    bp_dia = health_point.get("bp_diastolic")
    hr = health_point.get("heart_rate")
    spo2 = health_point.get("spo2")



    # Convert to numbers safely
    bp_sys = int(bp_sys) if bp_sys is not None else None
    bp_dia = int(bp_dia) if bp_dia is not None else None
    hr = int(hr) if hr is not None else None
    spo2 = int(spo2) if spo2 is not None else None

    # Heart Rate
    if hr is not None:
        if hr < 60 or hr > 120:
            alert_level = "critical"
            anomalies.append("heart_rate")
        elif hr > 100 and alert_level != "critical":
            alert_level = "warning"
            anomalies.append("heart_rate")

    # SpO2
    if spo2 is not None:
        if spo2 < 90:
            alert_level = "critical"
            anomalies.append("spo2")
        elif spo2 < 95 and alert_level != "critical":
            alert_level = "warning"
            anomalies.append("spo2")

    # Blood Pressure
    if bp_sys is not None and bp_dia is not None:
        if bp_sys > 160 or bp_dia > 100:
            alert_level = "critical"
            anomalies.append("blood_pressure")
        elif (bp_sys > 140 or bp_dia > 90) and alert_level != "critical":
            alert_level = "warning"
            anomalies.append("blood_pressure")

    health_point["alert_level"] = alert_level
    health_point["anomalies"] = anomalies

    return health_point