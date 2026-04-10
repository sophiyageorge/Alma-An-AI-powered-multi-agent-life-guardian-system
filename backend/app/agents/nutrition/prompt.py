from typing import Dict

def build_nutrition_prompt(user_profile: Dict) -> str:
    return f"""
You are a professional dietitian and nutritionist.

Create a **1-day personalized meal plan** for the user below and output in **valid JSON only**. Include **Breakfast, Lunch, Dinner, and Snack**.

USER PROFILE:
Daily Calories: {user_profile.get('calories')} kcal
Diet Type: {user_profile.get('diet')}
Goal: {user_profile.get('goal')}
Cuisine Region: {user_profile.get('region')}
Dietary Restrictions: {user_profile.get('restrictions')}
Meal Preference: {user_profile.get('meal_type')}

MEAL REQUIREMENTS:
- Total calories must exactly equal daily target.
- Each meal must include:
  * name: Food name
  * quantity: specific and measurable (e.g., "2 chapatis", "1 cup dal", "150g chicken")
  * ingredients: list of {{"item": <name>, "quantity": <quantity>, "calories": <calories>}}
  * calories: numeric, sum of ingredients
  * steps: list of 4-6 detailed cooking steps with methods, timings, and tips
- Use realistic portion sizes.
- Follow dietary restrictions and culturally relevant foods.
- Avoid vague terms like "1 serving".

OUTPUT FORMAT:
{{
  "day1": {{
    "breakfast": [
      {{
        "name": "",
        "quantity": "",
        "ingredients": [],
        "calories": 0,
        "steps": []
      }}
    ],
    "lunch": [
      {{
        "name": "",
        "quantity": "",
        "ingredients": [],
        "calories": 0,
        "steps": []
      }}
    ],
    "dinner": [
      {{
        "name": "",
        "quantity": "",
        "ingredients": [],
        "calories": 0,
        "steps": []
      }}
    ],
    "snack": [
      {{
        "name": "",
        "quantity": "",
        "ingredients": [],
        "calories": 0,
        "steps": []
      }}
    ]
  }}
}}

IMPORTANT:
- Output **JSON only**, no explanations or markdown.
- Calories must exactly match daily target.
- Ingredients calories must sum to meal calories.
"""