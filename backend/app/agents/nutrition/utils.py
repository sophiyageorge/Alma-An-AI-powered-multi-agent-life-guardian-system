"""
Utility functions for Nutrition Agent.
"""

from typing import Dict


def validate_user_profile(user_profile: Dict) -> None:
    """
    Validates required user profile fields.

    Raises:
        ValueError: If required fields are missing.
    """
    required_fields = ["calories", "diet", "goal"]

    missing = [field for field in required_fields if not user_profile.get(field)]
    if missing:
        raise ValueError(f"Missing required user profile fields: {missing}")
