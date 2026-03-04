import random
from datetime import datetime, timedelta
from typing import List, Dict


def generate_normal_health_data(minutes: int = 5, interval_sec: int = 30) -> List[Dict]:
    return _generate_generic_data(
        minutes, interval_sec,
        context="rest",
        hr_range=(70, 90),
        spo2_range=(95, 99),
        bp_sys=(110, 130),
        bp_dia=(70, 85),
        steps_range=(0, 20),
        workout_duration_range=(0, 0)
    )


def generate_slight_variation_health_data(minutes: int = 5, interval_sec: int = 30) -> List[Dict]:
    return _generate_generic_data(
        minutes, interval_sec,
        context="warning",
        hr_range=(90, 110),
        spo2_range=(92, 95),
        bp_sys=(130, 145),
        bp_dia=(85, 95),
        steps_range=(0, 25),
        workout_duration_range=(0, 10)
    )


def generate_critical_health_data(minutes: int = 5, interval_sec: int = 30) -> List[Dict]:
    return _generate_generic_data(
        minutes, interval_sec,
        context="critical",
        hr_range=(120, 180),
        spo2_range=(85, 90),
        bp_sys=(150, 200),
        bp_dia=(95, 130),
        steps_range=(0, 5),
        workout_duration_range=(0, 0)
    )


def generate_exercise_health_data(minutes: int = 5, interval_sec: int = 30) -> List[Dict]:
    return _generate_generic_data(
        minutes, interval_sec,
        context="exercise",
        hr_range=(110, 150),
        spo2_range=(93, 97),
        bp_sys=(120, 150),
        bp_dia=(80, 100),
        steps_range=(10, 60),
        workout_duration_range=(10, 60)
    )


# 🔹 Generic generator
def _generate_generic_data(
    minutes: int,
    interval_sec: int,
    context: str,
    hr_range,
    spo2_range,
    bp_sys,
    bp_dia,
    steps_range,
    workout_duration_range
) -> List[Dict]:

    data = []
    now = datetime.now()
    total_points = int((minutes * 60) / interval_sec)

    prev_hr = random.randint(*hr_range)
    prev_spo2 = random.randint(*spo2_range)
    workout_minutes = 0

    for i in range(total_points):
        timestamp = (now - timedelta(seconds=(total_points - i) * interval_sec)).strftime("%H:%M:%S")

        # Heart rate continuity
        heart_rate = max(hr_range[0], min(hr_range[1], prev_hr + random.randint(-3, 5)))
        prev_hr = heart_rate

        # SpO2 continuity
        spo2 = max(spo2_range[0], min(spo2_range[1], prev_spo2 + random.choice([-1, 0, 1])))
        prev_spo2 = spo2

        steps = random.randint(*steps_range)
        calories_burned = round(steps * 0.04, 2)  # estimated

        if context == "exercise":
            workout_minutes += interval_sec / 60

        point = {
            "time": timestamp,
            "context": context,
            "heart_rate": heart_rate,
            "spo2": spo2,
            "bp_systolic": random.randint(*bp_sys),
            "bp_diastolic": random.randint(*bp_dia),
            "steps": steps,
            "calories_burned": calories_burned,
            "workout_duration_minutes": round(workout_minutes, 2)
        }

        data.append(point)

    return data
