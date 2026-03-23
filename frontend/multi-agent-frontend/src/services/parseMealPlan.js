export const parseMealPlan = (input) => {
  if (!input) return {};

  // If input is already an object, return it
  if (typeof input === "object") return input;

  try {
    // Try parsing JSON
    const data = JSON.parse(input);

    // Optional: Normalize field names to lowercase
    const normalized = {};
    for (const [dayKey, meals] of Object.entries(data)) {
      normalized[dayKey.toLowerCase()] = {};
      for (const [mealType, mealArray] of Object.entries(meals)) {
        normalized[dayKey.toLowerCase()][mealType.toLowerCase()] = mealArray.map((meal) => ({
          name: meal.name || "Unnamed Meal",
          quantity: meal.quantity || "N/A",
          ingredients: meal.ingredients || [],
          calories: meal.calories || 0,
          steps: meal.steps || [],
        }));
      }
    }

    return normalized;
  } catch (err) {
    console.error("Invalid JSON input:", err);
    return {};
  }
};