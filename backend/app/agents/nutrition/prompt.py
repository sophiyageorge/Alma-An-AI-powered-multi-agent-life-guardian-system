from typing import Dict

def build_nutrition_prompt(user_profile: Dict, day_number: int) -> str:
    """
    Builds a prompt for a single day to stay within token limits 
    and ensure valid JSON output.
    """
    return f"""
You are a professional dietitian and nutritionist.
Create a personalized meal plan for **DAY {day_number} ONLY** based on the profile below.

------------------------
USER PROFILE (Target Day: {day_number})
------------------------
Daily Calorie Target: {user_profile.get('calories')} kcal
Diet Type: {user_profile.get('diet')}
Goal: {user_profile.get('goal')}
Cuisine Region: {user_profile.get('region')}
Dietary Restrictions: {user_profile.get('restrictions')}
Meal Preference: {user_profile.get('meal_type')}

------------------------
MEAL PLAN REQUIREMENTS
------------------------
1. Total calories for Day {day_number} must exactly equal {user_profile.get('calories')} kcal.
2. Include Breakfast, Lunch, Dinner and Snacks.
3. Each meal MUST contain these specific fields:
   - "name": Food name
   - "quantity": Measurable amount (e.g., "3 idlis", "200g rice", "1 cup dal"). NEVER use "1 serving".
   - "ingredients": List of items with specific quantity and calories.
   - "calories": Numeric total for that meal.
   - "steps": List of 4-6 detailed cooking steps.
4. Meals must be culturally relevant to {user_profile.get('region')} and respect all dietary restrictions.

------------------------
STRICT JSON OUTPUT FORMAT
------------------------
Return ONLY valid JSON. No conversational text, no markdown code blocks.
The structure must be:

{{
  "day_{day_number}": {{
    "breakfast": [
      {{
        "name": "Example Name",
        "quantity": "3 pieces",
        "ingredients": [
          {{ "item": "Ingredient A", "quantity": "50g", "calories": 100 }}
        ],
        "calories": 100,
        "steps": ["Step 1...", "Step 2..."]
      }}
    ],
    "lunch": [],
    "dinner": [],
    "snacks": []
  }}
}}

# FINAL VERIFICATION RULES:
# - Day {day_number} total (Breakfast + Lunch + Dinner) MUST = {user_profile.get('calories')}.
# - Each meal's calorie field MUST = the sum of its ingredients' calories.
# - If the math is wrong, recalculate before outputting.
# - Output ONLY the JSON object.
"""