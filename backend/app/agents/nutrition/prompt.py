"""
Prompt templates for Nutrition Agent.
"""

from typing import Dict


def build_nutrition_prompt(user_profile: Dict) -> str:
    """
    Builds the nutrition agent prompt dynamically.

    Args:
        user_profile (Dict): User profile containing dietary preferences and goals.

    Returns:
        str: Formatted prompt string.
    """
    return f"""
Create a 7-day meal plan.

Daily calories: {user_profile.get('calories')}
Diet: {user_profile.get('diet')}
Goal: {user_profile.get('goal')}
Region: {user_profile.get('region')}
Restrictions: {user_profile.get('restrictions')}
Meal preference: {user_profile.get('meal_type')}

Instructions:
- Include breakfast, lunch, dinner, snacks
- Mention calories per meal
- Keep food culturally relevant
- Output as a single readable paragraph
"""
 