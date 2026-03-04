"""
Unit tests for Exercise recommendation logic.
"""


from pathlib import Path
import pytest




from app.agents.exercise.recommendation import recommend_exercise


# -------------------------
# 🚨 SAFETY TEST CASES
# -------------------------

def test_low_spo2_triggers_breathing_exercises():
    result = recommend_exercise(
        heart_rate=80,
        spo2=92,
        bp_systolic=120,
        bp_diastolic=80,
        steps=7000,
        workout_duration_minutes=30
    )

    assert result["intensity"] == "very_low"
    assert "Low oxygen level detected" in result["warnings"]
    assert "Breathing exercises" in result["plan"]


def test_high_bp_triggers_low_intensity():
    result = recommend_exercise(
        heart_rate=85,
        spo2=98,
        bp_systolic=150,
        bp_diastolic=95,
        steps=7000,
        workout_duration_minutes=30
    )

    assert result["intensity"] == "low"
    assert "High blood pressure detected" in result["warnings"]
    assert "Yoga" in result["plan"]


def test_high_heart_rate_triggers_rest():
    result = recommend_exercise(
        heart_rate=120,
        spo2=98,
        bp_systolic=120,
        bp_diastolic=80,
        steps=7000,
        workout_duration_minutes=30
    )

    assert result["intensity"] == "rest"
    assert "Elevated heart rate" in result["warnings"]
    assert "Rest" in result["plan"]


# -------------------------
# 🏃 FITNESS LEVEL TESTS
# -------------------------

def test_sedentary_user_gets_moderate_plan():
    result = recommend_exercise(
        heart_rate=80,
        spo2=98,
        bp_systolic=120,
        bp_diastolic=80,
        steps=3000,
        workout_duration_minutes=30
    )

    assert result["intensity"] == "moderate"
    assert "30-minute brisk walk" in result["plan"]


def test_moderate_user_gets_strength_plan():
    result = recommend_exercise(
        heart_rate=80,
        spo2=98,
        bp_systolic=120,
        bp_diastolic=80,
        steps=8000,
        workout_duration_minutes=30
    )

    assert result["intensity"] == "moderate_to_high"
    assert "Strength training" in result["plan"]


def test_active_user_gets_maintenance_plan():
    result = recommend_exercise(
        heart_rate=80,
        spo2=98,
        bp_systolic=120,
        bp_diastolic=80,
        steps=12000,
        workout_duration_minutes=30
    )

    assert result["intensity"] == "maintenance"
    assert "HIIT (if energy level is good)" in result["plan"]


# -------------------------
# ⏳ RECOVERY TEST
# -------------------------

def test_overtraining_triggers_recovery_advice():
    result = recommend_exercise(
        heart_rate=80,
        spo2=98,
        bp_systolic=120,
        bp_diastolic=80,
        steps=8000,
        workout_duration_minutes=75
    )

    assert result["recovery_advice"] == "Consider a recovery or rest day tomorrow"