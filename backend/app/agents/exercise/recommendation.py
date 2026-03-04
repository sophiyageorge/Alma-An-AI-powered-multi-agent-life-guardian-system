"""
Exercise Agent: LLM-based recommendations for health metrics.
"""
from app.llm.llm_client import llm
from app.agents.exercise.prompt import build_exercise_prompt
from app.crud.exercise import save_exercise_entry
from app.database import get_db

def recommend_exercise(user_id: int, metrics: dict) -> dict:
    """
    Main Exercise Agent function.

    
    Generate structured exercise recommendations via LLM and store in DB.

    metrics (dict): Dictionary containing health metrics   :
        user_id (int): ID of the user
        heart_rate (int): Current heart rate
        spo2 (int): Oxygen saturation
        bp_systolic (int): Systolic blood pressure
        bp_diastolic (int): Diastolic blood pressure
        steps (int): Step count
        workout_duration_minutes (float): Duration of previous workout

    Returns:
        Dict: Structured recommendation returned by LLM
    """
    
    db = next(get_db())

    # 1️⃣ Build prompt
    prompt = build_exercise_prompt(metrics)

    # 2️⃣ Call LLM
    llm_response = llm.invoke(prompt)

    # 3️⃣ Parse recommendation
    import json
    try:
        recommendation = json.loads(llm_response)
    except json.JSONDecodeError:
        recommendation = {
            "intensity": "moderate",
            "plan": [],
            "warnings": [],
            "recovery_advice": llm_response
        }

    # 4️⃣ Save to DB
    entry = save_exercise_entry(db, user_id, metrics, llm_response, recommendation)

    return recommendation