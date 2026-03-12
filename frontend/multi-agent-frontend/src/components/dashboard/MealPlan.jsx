

// export default MealPlan;
import { useState, useEffect } from "react";
import { getMealPlan, approveMealPlan } from "../../services/api";
import { Flame } from "lucide-react";
import MealPlanActions from "./UpdateMealPlan";

function MealPlan() {
  const [mealPlan, setMealPlan] = useState(null);
  const [selectedDay, setSelectedDay] = useState(null);
  const [selectedMeal, setSelectedMeal] = useState(null);
  const [mealPlanId, setMealPlanId] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    const loadMealPlan = async () => {
      try {
        const data = await getMealPlan();
        setMealPlanId(data.meal_plan_id);
        setUserId(data.user_id);


        const parsed = parseMealPlan(data.meal_plan);
        setMealPlan(parsed);

        // Select first day by default
        const firstDay = Object.keys(parsed)[0];
        setSelectedDay(firstDay);
      } catch (error) {
        console.error(error);
      }
    };

    loadMealPlan();
  }, []);

  const parseMealPlan = (text) => {
    const days = {};
    const dayBlocks = text.split(/Day\s*\d+:/i);
    const dayMatches = text.match(/Day\s*\d+/gi);

    if (!dayMatches) return {};

    dayMatches.forEach((dayLabel, index) => {
      const dayKey = dayLabel.toLowerCase().replace(" ", "");
      const mealsText = dayBlocks[index + 1];
      if (!mealsText) return;

      const mealLines = mealsText
        .split("\n")
        .map((line) => line.trim())
        .filter((line) => line.length > 0);

      days[dayKey] = mealLines.map((line) => {
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
    });

    return days;
  };

  if (!mealPlan) {
    return <p className="text-white p-6">Loading...</p>;
  }

  const days = Object.keys(mealPlan);

  return (
    <div className="p-6">
      {/* Day Selector */}
      <div className="flex gap-3 mb-6 flex-wrap">
        {days.map((day) => (
          <button
            key={day}
            onClick={() => {
              setSelectedDay(day);
              setSelectedMeal(null);
            }}
            className={`px-4 py-2 rounded-lg border transition-all duration-300 ${
              selectedDay === day
                ? "bg-amber-500 text-white border-amber-500"
                : "bg-white/10 text-gray-300 border-white/20"
            }`}
          >
            {day.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Meal Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {mealPlan[selectedDay]?.map((meal, idx) => (
          <div
            key={idx}
            onClick={() =>
              setSelectedMeal(idx === selectedMeal ? null : idx)
            }
            className={`bg-white/5 border border-white/10 rounded-xl p-4 cursor-pointer transition-all duration-300 ${
              selectedMeal === idx
                ? "ring-2 ring-amber-500/50 scale-105"
                : ""
            }`}
          >
            <div className="font-semibold text-white mb-1">{meal.name}</div>

            <div className="flex items-center gap-2 mb-3">
              <Flame className="w-4 h-4 text-orange-400" />
              <span className="text-white font-semibold">{meal.calories}</span>
              <span className="text-xs text-gray-400">cal</span>
            </div>

            {/* Expand Macros */}
            <div
              className={`overflow-hidden transition-all duration-300 ${
                selectedMeal === idx ? "max-h-20 opacity-100" : "max-h-0 opacity-0"
              }`}
            >
              <div className="grid grid-cols-3 gap-2 text-xs border-t border-white/10 pt-2">
                <div className="text-cyan-400 text-center">
                  {meal.macros.protein}g
                  <br />Protein
                </div>
                <div className="text-amber-400 text-center">
                  {meal.macros.carbs}g
                  <br />Carbs
                </div>
                <div className="text-rose-400 text-center">
                  {meal.macros.fats}g
                  <br />Fats
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

    

     
     {showModal ? (
       <MealPlanActions
      //  mealPlanId={mealPlanId}
       userId={userId}
       // currentPlan={mealPlan[selectedDay]}
       
               currentPlan={{ calories: 1800, diet: "vegetarian", goal: "weight loss", region: "Kerala", }}
               onClose={() => setShowModal(false)}
             />
       
     ) :(

  <div>
      {/* Action Buttons */}
      <div className="flex gap-3 mt-4">
        <button
          onClick={async () => {
            try {
              await approveMealPlan(mealPlanId);
            } catch (error) {
              console.error(error);
              alert("Approval failed ❌");
            }
          }}
          className="px-4 py-2 bg-green-500/20 border border-green-500/30 text-green-400 rounded-lg hover:bg-green-500/30 transition"
        >
          Approve Plan
        </button>

        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2 bg-amber-500/20 border border-amber-500/30 text-amber-400 rounded-lg hover:bg-amber-500/30 transition"
        >
          Update Plan
        </button>
      </div>
  </div>
     
     )
    }
    </div>
  );
}

export default MealPlan;