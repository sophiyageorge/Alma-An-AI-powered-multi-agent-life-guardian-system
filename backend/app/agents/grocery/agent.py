from app.orchestrator.state import OrchestratorState
from app.llm.llm_client import llm

def grocery_agent(state: OrchestratorState) -> OrchestratorState:

    nutrition_plan = state.get("nutrition_plan")
    if not nutrition_plan:
        state["grocery_list"] = []
        return state

    meal_plan_text = nutrition_plan.get("meal_plan_text", "")
    if not meal_plan_text:
        state["grocery_list"] = []
        return state

    prompt = f"""
You are a grocery planning assistant.

From the following 7-day meal plan, generate a WEEKLY grocery list.

Rules:
- Vegetarian and dairy-free unless stated
- Combine quantities for the whole week
- Use simple household quantities (kg, g, pieces)
- One grocery item per line
- No explanations
- Output ONLY the list items, each on a new line

Meal Plan:
{meal_plan_text}
"""

    response = llm.invoke(prompt)

    # Convert LLM output → List[str]
    grocery_items = [
        line.strip("-• ").strip()
        for line in response.split("\n")
        if line.strip()
    ]

    state["grocery_list"] = grocery_items
    return state
