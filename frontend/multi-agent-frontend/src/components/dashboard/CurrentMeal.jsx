import { useState, useEffect } from "react";
import { getMealPlan } from "../../services/api";
import MealModal from "./MealModal";
import { parseMealPlan } from "../../services/parseMealPlan";

function CurrentMeal() {
  const [mealPlan, setMealPlan] = useState({});
  const [selectedMeal, setSelectedMeal] = useState(null);
  const [error, setError] = useState(null);

  const todayKey = `day${new Date().getDay() + 1}`;

  useEffect(() => {
    const loadMealPlan = async () => {
      try {
        const data = await getMealPlan();
        const text = typeof data === "string" ? data : data.meal_plan;
        const parsed = parseMealPlan(text); // returns day1 -> { breakfast: [...], ... }

        // Flatten each day's meals into an array
        const flattened = {};
        for (const day in parsed) {
          flattened[day] = [
            ...(parsed[day].breakfast || []).map(m => ({ ...m, type: "breakfast" })),
            ...(parsed[day].lunch || []).map(m => ({ ...m, type: "lunch" })),
            ...(parsed[day].dinner || []).map(m => ({ ...m, type: "dinner" })),
            ...(parsed[day].snack || []).map(m => ({ ...m, type: "snacks" }))
          ];
        }

        setMealPlan(flattened);
      } catch (err) {
        console.error(err);
        setError("Failed to load meal plan");
      }
    };

    loadMealPlan();
  }, []);

  if (error) return <p className="text-white p-6">{error}</p>;
  if (!mealPlan[todayKey] || mealPlan[todayKey].length === 0)
    return <p className="text-white p-6">Loading...</p>;

  // Group meals by type
  const mealsByType = { breakfast: [], lunch: [], snacks: [], dinner: [] };
  for (const meal of mealPlan[todayKey]) {
    const type = meal.type.toLowerCase();
    if (type.startsWith("breakfast")) mealsByType.breakfast.push(meal);
    else if (type.startsWith("lunch")) mealsByType.lunch.push(meal);
    else if (type.startsWith("dinner")) mealsByType.dinner.push(meal);
    else mealsByType.snacks.push(meal);
  }

  return (
    <div className="p-6 text-white">
      <h2 className="text-2xl font-bold mb-6">Today's Meal Plan</h2>

      <div className="grid grid-cols-2 gap-4">
        {["breakfast", "lunch", "snacks", "dinner"].map((type) => (
          <div key={type} className="bg-white/5 border border-white/10 rounded-2xl p-4">
            <h3 className="text-lg font-semibold capitalize mb-2">{type}</h3>

            {mealsByType[type]?.length ? (
              <ul className="space-y-2">
                {mealsByType[type].map((meal) => (
                  <li
                    key={meal.name + meal.calories}
                    className="cursor-pointer"
                    onClick={() => setSelectedMeal(meal)}
                  >
                    <div className="font-semibold">{meal.name}</div>
                    <div className="text-orange-400">{meal.calories} kcal</div>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-400 text-sm">No {type} listed</p>
            )}
          </div>
        ))}
      </div>

      <MealModal
        selectedMeal={selectedMeal}
        onClose={() => setSelectedMeal(null)}
      />
    </div>
  );
}

export default CurrentMeal;