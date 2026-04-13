import logging
import json
from app.agents.nutrition.prompt import build_nutrition_prompt
from app.llm.llm_client import llm

logger = logging.getLogger(__name__)

def generate_nutrition_plan(user_profile):
    """
    Generates a 7-day meal plan by calling the LLM individually for each day.
    This prevents 'Request Too Large' errors and ensures valid JSON structure.
    """
    master_meal_plan = {}

    logger.info(f"Starting 7-day nutrition plan generation for Goal: {user_profile.get('goal')}")

    for day in range(1, 8):
        logger.info(f"Generating plan for Day {day}...")
        
        # 1. Build prompt for the specific day
        # Ensure your build_nutrition_prompt function accepts 'day_number' as an argument
        prompt = build_nutrition_prompt(user_profile, day_number=day)

        try:
            # 2. Invoke LLM for the single day
            response_str = llm.invoke(prompt)

            # 3. Parse string to dictionary
            # Note: GroqLLM now uses response_format={"type": "json_object"}, 
            # so it should return a clean JSON string.
            day_data = json.loads(response_str)

            # 4. Merge into master plan
            master_meal_plan.update(day_data)
            
            logger.info(f"Successfully integrated Day {day}")

        except json.JSONDecodeError as e:
            logger.error(f"JSON Parsing failed for Day {day}: {str(e)}")
            # Optional: You could implement a single retry here if a day fails
            continue 
        except Exception as e:
            logger.error(f"Unexpected error on Day {day}: {str(e)}")
            raise RuntimeError(f"Failed to generate full plan at Day {day}")

    # Return the combined 7-day plan as a dictionary (or json.dumps if you need a string)
    logger.info("7-day nutrition plan generation complete")
    
    # so the database can save it as TEXT
    return json.dumps(master_meal_plan)