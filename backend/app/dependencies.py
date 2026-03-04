# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from utils.jwt import verify_access_token  # ✅ use your utils/jwt.py
from app.models.user import User

security = HTTPBearer()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    token = token.credentials
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    user_id = payload.get("sub")
    print(f"Decoded token payload: {payload}")
    print(f"Extracted user_id: {user_id}")
    user = db.query(User).filter(User.user_id == user_id).first()
    print("Current User:", user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user




