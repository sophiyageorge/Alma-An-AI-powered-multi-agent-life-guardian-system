from typing import Dict

def build_nutrition_prompt(user_profile: Dict) -> str:
    return f"""
You are a professional dietitian and nutritionist.

Create a **7-day personalized meal plan** strictly for the user profile below, and output it in **valid JSON only**. The JSON must contain days 1 to 7, and for each day include breakfast, lunch, dinner, and snacks.

------------------------
USER PROFILE
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
1. Total calories per day must exactly equal the daily calorie target.
2. Include Breakfast, Lunch, Dinner, and 1–2 Healthy Snacks per day.
3. Each meal MUST contain these fields:
   - name: Food name
   - quantity:-  MUST be specific and food-appropriate:
          Use "number of pieces" for discrete foods (e.g., "3 idlis", "2 chapatis", "1 dosa", "2 eggs")
          Use "cups" for semi-solid/liquid foods (e.g., "1 cup sambar", "1 cup dal", "1 cup yogurt")
          Use "grams" for solid mixed dishes (e.g., "200g rice", "150g chicken curry")
          DO NOT use vague terms like "1 serving"
          EXAMPLES:
            - Idli → quantity: "3 idlis"
            - Chapati → quantity: "2 chapatis"
            - Dosa → quantity: "1 dosa"
            - Rice → quantity: "200g cooked rice"
            - Curry → quantity: "1 cup chicken curry"
            - Boiled eggs → quantity: "2 eggs"
   - ingredients: list with quantity and calories for each ingredient
   - calories: numeric value for the meal
   - steps: list of detailed preparation steps (at least 4–6 steps)
4. Follow balanced macronutrients: complex carbs, proteins, healthy fats, fiber.
5. Meals must be culturally relevant to the specified region.
6. Strictly follow dietary restrictions.
7. Avoid processed foods unless necessary.
8. Quantity must NEVER be "1 serving" or vague. It must always be measurable and food-specific.
9. Quantity must reflect realistic portion sizes aligned with calorie target.
   Example:
   - If breakfast is 300 kcal → use realistic counts like 2–3 idlis, not 6

------------------------
JSON OUTPUT FORMAT
------------------------
The final output must be valid JSON like this (all braces are escaped for Python f-string):


{{
  "day1": {{
    "breakfast": [
      {{
        "name": "Idiyappam with Egg Curry",
        "quantity": "3 idiyappam with 2 eggs curry",
        "ingredients": [
          {{ "item": "Rice flour", "quantity": "120g", "calories": 440 }},
          {{ "item": "Eggs", "quantity": "2", "calories": 140 }},
          {{ "item": "Coconut milk", "quantity": "50ml", "calories": 100 }},
          {{ "item": "Onion", "quantity": "50g", "calories": 20 }},
          {{ "item": "Oil", "quantity": "1 tsp", "calories": 45 }},
          {{ "item": "Spices", "quantity": "to taste", "calories": 5 }}
        ],
        "calories": 750,
        "steps": [
          "Step 1: Mix rice flour with warm water and a pinch of salt to form a soft dough.",
          "Step 2: Press the dough into thin strands using an idiyappam maker.",
          "Step 3: Steam the idiyappam for 8–10 minutes until soft and cooked.",
          "Step 4: Boil eggs and sauté onion, spices, and coconut milk to prepare curry.",
          "Step 5: Add boiled eggs to the curry and simmer for 5 minutes.",
          "Step 6: Serve hot idiyappam with egg curry."
        ]
      }}
    ],
    "lunch": [
      {{
        "name": "Brown Rice with Chicken Curry",
        "quantity": "200g rice with 150g chicken curry",
        "ingredients": [
          {{ "item": "Brown rice", "quantity": "200g cooked", "calories": 220 }},
          {{ "item": "Chicken", "quantity": "150g", "calories": 300 }},
          {{ "item": "Onion", "quantity": "50g", "calories": 20 }},
          {{ "item": "Tomato", "quantity": "50g", "calories": 20 }},
          {{ "item": "Oil", "quantity": "1 tbsp", "calories": 120 }},
          {{ "item": "Spices", "quantity": "to taste", "calories": 20 }}
        ],
        "calories": 700,
        "steps": [
          "Step 1: Wash and cook brown rice until soft.",
          "Step 2: Heat oil and sauté onions until golden brown.",
          "Step 3: Add tomatoes and spices, cook until soft.",
          "Step 4: Add chicken pieces and cook for 10–15 minutes.",
          "Step 5: Add water and simmer until chicken is fully cooked.",
          "Step 6: Serve hot chicken curry with brown rice."
        ]
      }}
    ],
    "dinner": [
      {{
        "name": "Vegetable Stir Fry with Chapati",
        "quantity": "2 chapatis with 150g vegetable stir fry",
        "ingredients": [
          {{ "item": "Whole wheat flour", "quantity": "60g", "calories": 200 }},
          {{ "item": "Mixed vegetables", "quantity": "150g", "calories": 80 }},
          {{ "item": "Oil", "quantity": "1 tsp", "calories": 45 }},
          {{ "item": "Spices", "quantity": "to taste", "calories": 5 }}
        ],
        "calories": 330,
        "steps": [
          "Step 1: Knead whole wheat flour into a soft dough.",
          "Step 2: Roll into chapatis and cook on a hot pan until golden.",
          "Step 3: Heat oil in a pan and add mixed vegetables.",
          "Step 4: Stir fry vegetables for 5–7 minutes.",
          "Step 5: Add spices and cook for another 2 minutes.",
          "Step 6: Serve hot chapatis with vegetable stir fry."
        ]
      }}
    ],
    "snack": [
      {{
        "name": "Banana",
        "quantity": "1 medium banana",
        "ingredients": [
          {{ "item": "Banana", "quantity": "1 medium", "calories": 90 }}
        ],
        "calories": 90,
        "steps": [
          "Step 1: Select a ripe banana.",
          "Step 2: Peel the banana.",
          "Step 3: Slice if desired.",
          "Step 4: Consume fresh."
        ]
      }}
    ]
  }},

  "day2": {{ "breakfast": [], "lunch": [], "dinner": [], "snack": [] }},
  "day3": {{ "breakfast": [], "lunch": [], "dinner": [], "snack": [] }},
  "day4": {{ "breakfast": [], "lunch": [], "dinner": [], "snack": [] }},
  "day5": {{ "breakfast": [], "lunch": [], "dinner": [], "snack": [] }},
  "day6": {{ "breakfast": [], "lunch": [], "dinner": [], "snack": [] }},
  "day7": {{ "breakfast": [], "lunch": [], "dinner": [], "snack": [] }}
}}



IMPORTANT:
- Output **JSON only**, do not include markdown, explanations, or bullet points.
- Steps must include cooking method, timing, and tips where needed.
- Repeat the same structure for all 7 days.
- Ensure the sum of calories per day equals the target.

IMPORTANT STRICT RULES:

1. The sum of calories of all meals in a day MUST exactly equal the Daily Calorie Target.
2. The calories of each meal MUST equal the sum of its ingredient calories.
3. Perform internal calculation and verification before returning output.
4. If totals do not match, regenerate internally until correct.
5. Do not approximate. Use exact numbers.

FINAL CHECK BEFORE OUTPUT:
- Verify breakfast + lunch + dinner + snacks = total calories
- Verify each meal calories = sum of ingredient calories
- Only return JSON if ALL checks pass

------------------------
DISCLAIMER
------------------------
This meal plan is generated by an AI system and is intended for general informational purposes only. It is not a substitute for professional medical or nutritional advice. Consult a qualified healthcare professional before making significant dietary changes.
"""