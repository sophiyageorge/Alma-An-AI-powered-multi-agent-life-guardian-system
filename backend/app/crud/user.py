"""
User CRUD operations and password utilities
-------------------------------------------

Provides functions to create users, fetch by email, and verify passwords.
Uses secure SHA-256 + bcrypt hashing for password storage.
"""

from sqlalchemy.orm import Session
from app.models.user import User
import bcrypt
import hashlib
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


# --------------------------
# Fetch User by Email
# --------------------------
def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Retrieve a user by email.

    Args:
        db (Session): SQLAlchemy DB session
        email (str): User email

    Returns:
        User | None: User object if found, else None
    """
    user = db.query(User).filter(User.email == email).first()
    if user:
        logger.info(f"User found by email: {email} | user_id={user.user_id}")
    else:
        logger.warning(f"No user found with email: {email}")
    return user


# --------------------------
# Create User
# --------------------------
def create_user(db: Session, user) -> User:
    """
    Create a new user with hashed password.

    Uses SHA-256 pre-hashing and bcrypt for secure password storage.

    Args:
        db (Session): SQLAlchemy DB session
        user: Pydantic UserCreate object with password

    Returns:
        User: Newly created user object
    """
    try:
        # Pre-hash with SHA-256
        sha256_pw = hashlib.sha256(user.password.encode()).digest()
        # bcrypt hash
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

        logger.info(f"Created new user | user_id={db_user.user_id} | email={db_user.email}")
        return db_user

    except Exception as e:
        db.rollback()
        logger.exception(f"Failed to create user | email={user.email}")
        raise e


# --------------------------
# Verify Password
# --------------------------
def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    """
    Verify a plaintext password against the stored hash.

    Args:
        plain_password (str): User-provided password
        hashed_password (bytes): Stored SHA-256 + bcrypt hashed password

    Returns:
        bool: True if password matches, else False
    """
    sha256_pw = hashlib.sha256(plain_password.encode()).digest()
    result = bcrypt.checkpw(sha256_pw, hashed_password)

    if result:
        logger.info("Password verification successful")
    else:
        logger.warning("Password verification failed")
    return result
