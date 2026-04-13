import { useState, useEffect } from "react";
import { getMealPlan } from "../../services/api";
import MealModal from "./MealModal";

function CurrentMeal() {
  const [mealPlan, setMealPlan] = useState(null);
  const [selectedMeal, setSelectedMeal] = useState(null);
  const [error, setError] = useState(null);

  const todayIndex = new Date().getDay() + 1;
  const todayKey = `day_${todayIndex}`;

  useEffect(() => {
    const loadMealPlan = async () => {
      try {
        const data = await getMealPlan();
        setMealPlan(data?.meal_plan || {});
      } catch (err) {
        console.error(err);
        setError("Failed to load meal plan");
      }
    };

    loadMealPlan();
  }, []);

  if (error) {
    return <p className="text-white p-6">{error}</p>;
  }

  if (!mealPlan || !mealPlan[todayKey]) {
    return <p className="text-white p-6">Loading meal plan...</p>;
  }

  const todayMeals = mealPlan[todayKey];

  const mealsByType = {
    breakfast: todayMeals.breakfast || [],
    lunch: todayMeals.lunch || [],
    snacks: todayMeals.snacks || [],
    dinner: todayMeals.dinner || [],
  };

  return (
    <div className="p-6 text-white">
      <h2 className="text-2xl font-bold mb-6">Today's Meal Plan</h2>

      <div className="grid grid-cols-2 gap-4">
        {["breakfast", "lunch", "snacks", "dinner"].map((type) => (
          <div
            key={type}
            className="bg-white/5 border border-white/10 rounded-2xl p-4"
          >
            <h3 className="text-lg font-semibold capitalize mb-2">
              {type}
            </h3>

            {mealsByType[type].length > 0 ? (
              <ul className="space-y-2">
                {mealsByType[type].map((meal, i) => (
                  <li
                    key={meal.name + i}
                    className="cursor-pointer"
                    onClick={() => setSelectedMeal(meal)}
                  >
                    <div className="font-semibold">{meal.name}</div>
                    <div className="text-orange-400">
                      {meal.calories} kcal
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-400 text-sm">
                No {type} listed
              </p>
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