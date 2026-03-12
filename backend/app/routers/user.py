"""
User Authentication Router
--------------------------
Handles:
- User registration
- User login
- Initializing orchestrator workflow after login
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Schemas
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.schemas.user_profile import UserProfileCreate

# CRUD operations
from app.crud import user as crud_user
from app.crud import user_profile as crud_profile
from app.crud.user_profile import get_profile

# Database
from app.database import get_db

# Models
from app.models.user_profile import UserProfile

# JWT
from utils.jwt import create_access_token

# Orchestrator
from app.orchestrator.state import OrchestratorState
from app.orchestrator.graph import build_graph
from app.orchestrator.store import orchestrator_store

# Logging
from app.core.logging_config import setup_logger


# ---------------------------------------------------------
# Router Initialization
# ---------------------------------------------------------

router = APIRouter()

# Build LangGraph orchestrator
graph = build_graph()

# Logger
logger = setup_logger(__name__)


# ---------------------------------------------------------
# User Registration Endpoint
# ---------------------------------------------------------

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user and create a default profile.
    """

    logger.info(f"Registration attempt for email: {user.email}")

    # Check if user already exists
    db_user = crud_user.get_user_by_email(db, email=user.email)

    if db_user:
        logger.warning(f"Registration failed. Email already exists: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    new_user = crud_user.create_user(db, user)

    logger.info(
        f"User registered successfully | user_id={new_user.user_id} | email={new_user.email}"
    )

    # ---------------------------------------------------------
    # Create Default Profile
    # ---------------------------------------------------------

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

    logger.info(
        f"Default profile created for user_id={new_user.user_id}"
    )

    return new_user


# ---------------------------------------------------------
# User Login Endpoint
# ---------------------------------------------------------

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and trigger orchestrator workflow.
    """

    logger.info(f"Login attempt for email: {user.email}")

    # ---------------------------------------------------------
    # Validate Credentials
    # ---------------------------------------------------------

    db_user = crud_user.get_user_by_email(db, email=user.email)

    if not db_user or not crud_user.verify_password(user.password, db_user.password_hash):

        logger.warning(f"Invalid login attempt for email: {user.email}")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    logger.info(f"User authenticated successfully | user_id={db_user.user_id}")

    # ---------------------------------------------------------
    # Generate JWT Token
    # ---------------------------------------------------------

    access_token = create_access_token({"sub": str(db_user.user_id)})

    logger.info(f"Access token generated for user_id={db_user.user_id}")

    # ---------------------------------------------------------
    # Fetch User Profile
    # ---------------------------------------------------------

    profile = get_profile(db, db_user.user_id)

    logger.info(f"Profile fetched for user_id={db_user.user_id}")

    # ---------------------------------------------------------
    # Build User Profile State
    # ---------------------------------------------------------

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

        logger.info(
            f"Using stored profile for user_id={db_user.user_id}"
        )

    else:
        logger.warning(
            f"No profile found for user_id={db_user.user_id}. Using fallback profile"
        )

        user_profile = {
            "user_id": db_user.user_id,
            "calories": 1800,
            "diet": "vegetarian",
            "goal": "weight loss",
            "region": "Kerala",
            "restrictions": ["no dairy"],
            "meal_type": "home food"
        }

    # ---------------------------------------------------------
    # Initialize Orchestrator State
    # ---------------------------------------------------------

    state: OrchestratorState = {
        # "user_id": db_user.user_id,
        "user_profile": user_profile,
        "db": db,
        "health_data": None,
        "journal_text": None,
        "meal_plan_approved": False,
        "exercise_plan_approved": False,
        "anomaly_detected": False,
        "compliance_passed": True
    }

    logger.info(
        f"Orchestrator state initialized for user_id={db_user.user_id}"
    )

    logger.info(f"Initial orchestrator state for user_id={db_user.user_id}: {state}")

    # ---------------------------------------------------------
    # Invoke LangGraph Orchestrator
    # ---------------------------------------------------------

    try:

        logger.info(
            f"Invoking orchestrator graph for user_id={db_user.user_id}"
        )

        final_state = graph.invoke(state)

        logger.info(
            f"Orchestrator completed successfully for user_id={db_user.user_id}"
        )

        
 
    except Exception as e:

        logger.exception(
            f"Orchestrator execution failed for user_id={db_user.user_id}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to initialize wellness workflow"
        )

           # 6️⃣ Save state in memory
    orchestrator_store[db_user.user_id] = final_state
    orchestrator_store[db_user.user_id] = {
    "health_metrics": None,
    "nutrition_plan": None,
    "exercise_plan": None,
    "mental_health": None
}
    logger.info(f"Final orchestrator state for user_id {db_user.user_id}")



    # ---------------------------------------------------------
    # Return JWT Token
    # ---------------------------------------------------------

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
