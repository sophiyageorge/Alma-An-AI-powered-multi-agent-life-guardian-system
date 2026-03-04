from sqlalchemy.orm import Session
from app.models.user import User
import bcrypt
import hashlib

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto",bcrypt__rounds=12,bcrypt__ident=None)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user):
    # truncated = user.password[:72]
    # hashed_password = pwd_context.hash(truncated)
    sha256_pw = hashlib.sha256(user.password.encode()).digest()
    hashed_password = bcrypt.hashpw(sha256_pw, bcrypt.gensalt())
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        date_of_birth=user.date_of_birth,
        gender=user.gender
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    sha256_pw = hashlib.sha256(plain_password.encode()).digest()
    return bcrypt.checkpw(sha256_pw, hashed_password)
    # truncated = plain_password[:72]
    # return pwd_context.verify(truncated, hashed_password)