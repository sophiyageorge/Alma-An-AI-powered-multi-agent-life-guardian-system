from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.crud import user as crud_user
from app.database import get_db
from utils.jwt import create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud_user.create_user(db, user)
    return new_user

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    print(f"Login attempt for email: {user.email}")
    if not db_user or not crud_user.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(db_user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}
