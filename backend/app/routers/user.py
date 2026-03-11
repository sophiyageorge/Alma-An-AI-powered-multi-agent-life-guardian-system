from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.schemas.user_profile import UserProfileCreate, UserProfileResponse
from app.crud import user as crud_user
from app.database import get_db
from utils.jwt import create_access_token
from app.models.user_profile import UserProfile
from app.crud import user_profile as crud_profile
from app.orchestrator.state import OrchestratorState
from app.orchestrator.graph import build_graph
# from app.orchestrator.store import orchestrator_store
from app.crud.user_profile import get_profile
from app.core.logging_config import setup_logger

logger = setup_logger(__name__)

router = APIRouter()
graph = build_graph() 

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud_user.create_user(db, user)

    logger.info(f"New user registered: {new_user.email} with user_id: {new_user.user_id}")  

    
    # Create default profile
    default_profile = UserProfileCreate(
    user_id=new_user.user_id,
    calories=1800,
    diet="vegetarian",
    goal="maintain weight",
    region="Unknown",
    restrictions=[],
    meal_type="home food"
)
    crud_profile.create_profile(db, default_profile)

    logger.info(f"Default profile created for user_id: {new_user.user_id}")

    return new_user

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    print(f"Login attempt for email: {user.email}")
    if not db_user or not crud_user.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(db_user.user_id)})

    # 2️⃣ Fetch latest profile from DB
    profile = get_profile(db, db_user.user_id)
    logger.info(f"Fetched profile for user_id: {db_user.user_id}: {profile}")

    # 3️⃣ Fallback to default if profile not found
    if profile:
        user_profile = {
            "user_id": db_user.user_id,
            "calories": profile.calories,
            "diet": profile.diet,
            "goal": profile.goal,
            "region": profile.region,
            "restrictions": profile.restrictions or [],
            "meal_type": profile.meal_type
        }
        logger.info(f"Using profile from DB for user_id: {db_user.user_id}")
    else:
        user_profile = {
            "user_id": db_user.user_id,
            "calories": 1800,
            "diet": "vegetarian",
            "goal": "weight loss",
            "region": "Kerala",
            "restrictions": ["no dairy"],
            "meal_type": "home food"
        }
        logger.warning(f"No profile found for user_id: {db_user.user_id}. Using default profile.")


    db = next(get_db())
    # 4️⃣ Initialize orchestrator state
   
#     state: OrchestratorState = {
#     "user_id": user.id,
#     "user_profile": user_profile,
#     "nutrition_plan": None,
#     "exercise_response": None,
#     "daily_journal": None
# }
    state: OrchestratorState = {
    "user_id": db_user.user_id,
    "user_profile": user_profile,
    "db": db,
    "health_data": None,
    "journal_text": None,
    "meal_plan_approved": False,
    "exercise_plan_approved": False,
    "anomaly_detected": False,
    "compliance_passed": True
}
    logger.info(f"Initial orchestrator state for user_id {db_user.user_id}: {state}")

    logger.info("Initial state before graph invocation:", state.get("user_profile"))

    # 5️⃣ Invoke orchestrator once
    final_state = graph.invoke(state)

    # 6️⃣ Save state in memory
    # orchestrator_store[db_user.user_id] = final_state
#     orchestrator_store[db_user.user_id] = {
#     "health_metrics": None,
#     "nutrition_plan": None,
#     "exercise_plan": None,
#     "mental_health": None
# }
    logger.info(f"Final orchestrator state for user_id {db_user.user_id}: {final_state}")

    return {"access_token": access_token, "token_type": "bearer"}
