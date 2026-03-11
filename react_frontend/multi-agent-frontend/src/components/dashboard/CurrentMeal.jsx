import { useState, useEffect } from "react";
import { getMealPlan } from "../../services/api";
import { Apple, Sparkles, Flame } from "lucide-react";

function CurrentMeal({ mounted }) {
  const [meals, setMeals] = useState([]);
  const [selectedMeal, setSelectedMeal] = useState(null);

useEffect(() => {
  const loadMealPlan = async () => {
    try {
      const data = await getMealPlan();

      const text = typeof data === "string" ? data : data.meal_plan;

      const parsedMeals = extractTodayMeals(text);
      setMeals(parsedMeals);

    } catch (error) {
      console.error(error);
    }
  };

  loadMealPlan();
}, []);

const extractTodayMeals = (text) => {
  const todayIndex = new Date().getDay();
  const dayNumber = todayIndex === 0 ? 7 : todayIndex;
  const todayLabel = `Day ${dayNumber}`;

  // Split text into day sections
  const sections = text.split(/Day\s*\d+:/i);
  const dayMatches = text.match(/Day\s*\d+/gi);

  if (!dayMatches) return [];

  let todaySection = "";

  dayMatches.forEach((label, index) => {
    if (label.toLowerCase() === todayLabel.toLowerCase()) {
      todaySection = sections[index + 1];
    }
  });

  if (!todaySection) return [];

  const mealLines = todaySection
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0);

  return mealLines.map((line) => {
    const calorieMatch = line.match(/(\d+)\s*cal/i);
    const proteinMatch = line.match(/protein\s*(\d+)g/i);
    const carbsMatch = line.match(/carbs?\s*(\d+)g/i);
    const fatsMatch = line.match(/fats?\s*(\d+)g/i);

    return {
      name: line.split("(")[0],
      time: "",
      calories: calorieMatch ? calorieMatch[1] : 0,
      macros: {
        protein: proteinMatch ? proteinMatch[1] : 0,
        carbs: carbsMatch ? carbsMatch[1] : 0,
        fats: fatsMatch ? fatsMatch[1] : 0,
      },
    };
  });
};

  return (
  
    
      <div className="relative">
        <div className="flex flex-wrap items-center gap-3 mb-6">
          <div className="p-3 bg-amber-500/20 rounded-xl">
            <Apple className="w-6 h-6 text-amber-400" />
          </div>

          <h2 className="text-xl font-bold text-white">
            Today's Meal Plan
          </h2>

          <div className="ml-auto flex items-center gap-1 px-3 py-1 bg-amber-500/20 border border-amber-500/30 rounded-full">
            <Sparkles className="w-3 h-3 text-amber-400 animate-pulse" />
            <span className="text-xs text-amber-300">
              AI Personalized
            </span>
          </div>
        </div>

        {/* Meals */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {meals.length === 0 ? (
            <p className="text-gray-400">No meal data available</p>
          ) : (
            meals.map((meal, idx) => (
              <div
                key={idx}
                onClick={() =>
                  setSelectedMeal(idx === selectedMeal ? null : idx)
                }
                className={`group relative bg-white/5 border border-white/10 rounded-xl p-4 cursor-pointer transition-all duration-300 hover:scale-105 ${
                  selectedMeal === idx
                    ? "ring-2 ring-amber-500/50 scale-105"
                    : ""
                }`}
              >
                <div className="text-4xl mb-3">
                  {meal.icon || "🍽️"}
                </div>

                <div className="font-semibold text-white mb-1">
                  {meal.name}
                </div>

                <div className="text-xs text-gray-400 mb-3">
                  {meal.time}
                </div>

                <div className="flex items-center gap-2 mb-3">
                  <Flame className="w-4 h-4 text-orange-400" />
                  <span className="font-semibold text-white">
                    {meal.calories}
                  </span>
                  <span className="text-xs text-gray-400">cal</span>
                </div>

                {/* Expand Macros */}
                <div
                  className={`overflow-hidden transition-all duration-300 ${
                    selectedMeal === idx
                      ? "max-h-20 opacity-100"
                      : "max-h-0 opacity-0"
                  }`}
                >
                  <div className="pt-3 border-t border-white/10 grid grid-cols-3 gap-2 text-xs">
                    <div className="text-center">
                      <div className="text-cyan-400 font-semibold">
                        {meal.macros?.protein}g
                      </div>
                      <div className="text-gray-400">Protein</div>
                    </div>

                    <div className="text-center">
                      <div className="text-amber-400 font-semibold">
                        {meal.macros?.carbs}g
                      </div>
                      <div className="text-gray-400">Carbs</div>
                    </div>

                    <div className="text-center">
                      <div className="text-rose-400 font-semibold">
                        {meal.macros?.fats}g
                      </div>
                      <div className="text-gray-400">Fats</div>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

  );
}

export default CurrentMeal;