"""
Prompt template builder for Excercise Advisor Agent.
"""


from typing import Dict


def build_exercise_prompt(metrics: Dict) -> str:
    """
    Build a structured LLM prompt for Exercise Agent.
    """
    return f"""
You are a professional exercise and fitness advisor.
A user provides the following health metrics:

- Heart Rate: {metrics.get('heart_rate')} bpm
- SPO2: {metrics.get('spo2')}%
- Blood Pressure: {metrics.get('bp_systolic')}/{metrics.get('bp_diastolic')} mmHg
- Steps Today: {metrics.get('steps')}
- Workout Duration Today: {metrics.get('workout_duration_minutes')} minutes

Please generate a **structured exercise recommendation**. Return in JSON format with keys:
- intensity (very_low, low, moderate, moderate_to_high, high, maintenance)
- plan (list of recommended exercises)
- warnings (list of health warnings if any)
- recovery_advice (string, optional)

Ensure recommendations are **safe, practical, and personalized**.
"""
