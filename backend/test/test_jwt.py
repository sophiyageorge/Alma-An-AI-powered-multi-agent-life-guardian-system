import pytest
from datetime import datetime, timedelta
from jose import jwt, JWTError

# Assuming the backend is in the Python Path or we use relative imports correctly
from utils.jwt import create_access_token, verify_access_token, SECRET_KEY, ALGORITHM

def test_create_access_token():
    data = {"sub": "test_user_id"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    
    # Verify the created token directly using jose
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") == "test_user_id"
    assert "exp" in payload

def test_verify_access_token_valid():
    data = {"sub": "user_abc123"}
    token = create_access_token(data)
    
    payload = verify_access_token(token)
    assert payload is not None
    assert payload.get("sub") == "user_abc123"

def test_verify_access_token_invalid_format():
    token = "invalid.token.string"
    payload = verify_access_token(token)
    assert payload is None

def test_verify_access_token_expired():
    data = {"sub": "expired_user"}
    
    # Create token manually with negative expiration
    to_encode = data.copy()
    from datetime import timezone
    expire = datetime.now(timezone.utc) + timedelta(minutes=-1)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    payload = verify_access_token(token)
    assert payload is None
