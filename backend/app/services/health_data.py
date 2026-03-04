import random
from datetime import datetime


def generate_health_datapoint(context: str = "normal") -> dict:
    """
    Generate a single health datapoint based on context.
    Designed for real-time streaming.
    """

    if context == "normal":
        heart_rate = random.randint(70, 90)
        spo2 = random.randint(95, 99)
        systolic = random.randint(110, 125)
        diastolic = random.randint(70, 85)

    elif context == "slight_variation":
        heart_rate = random.randint(60, 105)
        spo2 = random.randint(93, 98)
        systolic = random.randint(105, 140)
        diastolic = random.randint(65, 95)

    elif context == "critical":
        heart_rate = random.randint(40, 160)
        spo2 = random.randint(80, 92)
        systolic = random.randint(80, 180)
        diastolic = random.randint(50, 110)

    elif context == "exercise":
        heart_rate = random.randint(110, 150)
        spo2 = random.randint(94, 99)
        systolic = random.randint(120, 160)
        diastolic = random.randint(75, 95)

    else:
        raise ValueError(f"Invalid context: {context}")

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "context": context,
        "heart_rate": heart_rate,
        "spo2": spo2,
        "blood_pressure": f"{systolic}/{diastolic}"
    }
