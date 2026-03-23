import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.dependencies import get_current_user

def test_get_current_user_valid_token():
    mock_db = MagicMock()
    mock_user = MagicMock()
    mock_user.user_id = "test_user_123"
    
    # Mock database to return our mock_user
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    token = HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid.token.here")
    
    # Mock the verify_access_token to return a valid payload
    with patch("app.dependencies.verify_access_token", return_value={"sub": "test_user_123"}):
        user = get_current_user(token=token, db=mock_db)
        assert user == mock_user
        mock_db.query.assert_called_once()

def test_get_current_user_invalid_token():
    mock_db = MagicMock()
    token = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid.token.here")
    
    # Mock verify_access_token to return None (invalid)
    with patch("app.dependencies.verify_access_token", return_value=None):
        with pytest.raises(HTTPException) as excinfo:
            get_current_user(token=token, db=mock_db)
        
        assert excinfo.value.status_code == 401
        assert excinfo.value.detail == "Invalid authentication credentials"

def test_get_current_user_not_found_in_db():
    mock_db = MagicMock()
    
    # Mock database to return None
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    token = HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid.token.here")
    
    # Mock verify_access_token to return a valid payload but user doesn't exist
    with patch("app.dependencies.verify_access_token", return_value={"sub": "nonexistent_user"}):
        with pytest.raises(HTTPException) as excinfo:
            get_current_user(token=token, db=mock_db)
        
        assert excinfo.value.status_code == 404
        assert excinfo.value.detail == "User not found"
