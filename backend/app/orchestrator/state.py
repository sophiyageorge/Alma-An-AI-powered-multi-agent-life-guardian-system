

from typing import TypedDict, Optional, List, Dict

class OrchestratorState(TypedDict):
    user_id: str

    # Inputs
    health_data: Optional[Dict]
    health_metric:Optional[Dict]
    journal_text: Optional[str]
    user_profile: Optional[Dict]

    # Agent outputs
    nutrition_plan: Optional[Dict]
    exercise_plan: Optional[Dict]
    grocery_list: Optional[List[str]]
    mental_insights: Optional[Dict]

    # Approval flags
    meal_plan_approved: bool
    exercise_plan_approved: bool  # ✅ new for exercise

    # System flags
    anomaly_detected: bool
    emergency_level: Optional[str]
    compliance_passed: bool

    # Final output
    response: Optional[Dict]
