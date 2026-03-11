
from typing import TypedDict, Optional, List, Dict
from sqlalchemy.orm import Session 


class OrchestratorState(TypedDict, total=False):

    # Core user context
    user_id: int
    user_profile: Dict

    # Inputs
    health_data: Dict
    health_metric: Dict
    journal_text: str

    daily_journal: Dict

    # Agent outputs
    nutrition_plan: Dict
    exercise_plan: Dict
    grocery_list: List[str]
    mental_insights: Dict

    # Approval flags
    meal_plan_approved: bool
    exercise_plan_approved: bool

    # Safety flags
    anomaly_detected: bool
    emergency_level: str
    compliance_passed: bool

    # Final API response
    response: Dict

     # DB session
    db: Session

