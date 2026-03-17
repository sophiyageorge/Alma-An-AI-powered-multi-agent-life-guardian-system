import { useState, useEffect } from "react";
import { getMealPlan } from "../../services/api";
import { Apple, Sparkles, Flame } from "lucide-react";

function CurrentMeal({ mounted }) {
  const [mealsByType, setMealsByType] = useState({});
  const [error, setError] = useState(null);

useEffect(() => {
  const loadMealPlan = async () => {
    try {
      setError(null);
      const data = await getMealPlan();

      const text = typeof data === "string" ? data : data.meal_plan;

      const parsedMeals = parseMealPlan(text);

      // Plan day numbering is Day 1..7 while JS getDay() is 0..6.
      // Treat Sunday as Day 1, Monday as Day 2, ... Saturday as Day 7.
      const todayKey = `day${new Date().getDay() + 1}`;

      const todayMeals = parsedMeals?.[todayKey] ?? [];
      setMealsByType(groupMealsByType(todayMeals));

    } catch (error) {
      console.error(error);
      setError(error?.message || "Failed to load today's meal plan");
    }
  };

  loadMealPlan();
}, []);

const groupMealsByType = (meals) => {
  const grouped = { breakfast: [], lunch: [], dinner: [], snacks: [] };
  for (const m of meals) {
    const t = (m?.type || "").toLowerCase();
    if (t.startsWith("breakfast")) grouped.breakfast.push(m);
    else if (t.startsWith("lunch")) grouped.lunch.push(m);
    else if (t.startsWith("dinner")) grouped.dinner.push(m);
    else grouped.snacks.push(m);
  }
  return grouped;
};

const parseMealPlan = (text) => {
  if (typeof text !== "string") return {};
  const normalized = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n");

  const dayMatches = [
    ...normalized.matchAll(/(?:\*\*)?\bDay\s*(\d+)\b(?:\*\*)?\s*:?\s*/gi),
  ];
  if (dayMatches.length === 0) return {};

  const days = {};

  for (let i = 0; i < dayMatches.length; i++) {
    const dayNumber = dayMatches[i][1];
    const dayKey = `day${dayNumber}`;
    const startIdx = dayMatches[i].index + dayMatches[i][0].length;
    const endIdx = i + 1 < dayMatches.length ? dayMatches[i + 1].index : normalized.length;
    const block = normalized.slice(startIdx, endIdx).trim();

    const lines = block
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);

    const meals = [];
    let currentType = null;
    let buffer = [];

    const flush = () => {
      if (!currentType || buffer.length === 0) return;

      const firstLine = buffer[0] ?? "";
      const foodLine =
        buffer.find((l) => /^-?\s*food\s*name\s*:/i.test(l)) ?? firstLine;
      const ingredientsLine = buffer.find((l) => /^-?\s*ingredients\s*:/i.test(l));
      const caloriesLine = buffer.find((l) => /^-?\s*calories\s*:/i.test(l));
      const prepLine = buffer.find((l) => /^-?\s*preparation\s*tip\s*:/i.test(l));

      const foodValue = foodLine.replace(/^-?\s*food\s*name\s*:\s*/i, "").trim();
      const name = (foodValue.split("(")[0].trim() || firstLine)
        .replace(/^\*+\s*/, "")
        .replace(/\*\*/g, "")
        .trim();

      const qtyMatch = foodValue.match(/\(([^)]*)\)/);
      const quantityAndIngredients = qtyMatch ? qtyMatch[1].trim() : "";

      const caloriesMatch = caloriesLine?.match(/(\d+)\s*(kcal|cal)/i);
      const calories = caloriesMatch ? Number(caloriesMatch[1]) : 0;

      const ingredients = ingredientsLine
        ? ingredientsLine.replace(/^-?\s*ingredients\s*:\s*/i, "").trim()
        : "";

      const preparationTip = prepLine
        ? prepLine.replace(/^-?\s*preparation\s*tip\s*:\s*/i, "").trim()
        : "";

      meals.push({
        key: `${dayKey}-${currentType}-${meals.length}`,
        type: currentType,
        name: name || currentType,
        calories,
        quantityAndIngredients,
        ingredients,
        preparationTip,
      });

      buffer = [];
    };

    for (const line of lines) {
      const mdHeader = line.match(
        /^([*-])\s*(?:\*\*)?(Breakfast|Lunch|Dinner|Snacks?|Snack)(?:\*\*)?\s*:\s*(.+)?$/i
      );
      if (mdHeader) {
        flush();
        currentType = mdHeader[2].toLowerCase();
        buffer = [];
        const maybeTitle = (mdHeader[3] ?? "").trim();
        if (maybeTitle) buffer.push(maybeTitle);
        continue;
      }

      const headingMatch = line.match(/^(Breakfast|Lunch|Dinner|Snacks|Snack)\s*:\s*$/i);
      if (headingMatch) {
        flush();
        currentType = headingMatch[1].toLowerCase();
        buffer = [];
        continue;
      }

      if (/^daily\s+total\s+calories\s*:/i.test(line)) {
        flush();
        currentType = null;
        buffer = [];
        continue;
      }

      if (currentType) buffer.push(line);
    }

    flush();
    days[dayKey] = meals;
  }

  return days;
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
        {error ? (
          <div className="text-gray-300 bg-white/5 border border-white/10 rounded-xl p-4">
            {error}
          </div>
        ) : Object.values(mealsByType).every((arr) => (arr?.length ?? 0) === 0) ? (
          <div className="text-gray-300 bg-white/5 border border-white/10 rounded-xl p-4">
            Please enter your health data daily to keep your meal plan personalized and up to date.
          </div>
        ) : (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
              {["breakfast", "lunch", "snacks", "dinner"].map((type) => (
                <div
                  key={type}
                  className="bg-white/5 border border-white/10 rounded-2xl p-4"
                >
                  <div className="text-white font-semibold mb-3 capitalize">
                    {type}
                  </div>
                  <div className="space-y-3">
                    {(mealsByType[type] ?? []).length === 0 ? (
                      <div className="text-sm text-gray-300">
                        No {type} listed for today.
                      </div>
                    ) : (
                      (mealsByType[type] ?? []).map((meal) => (
                        <div
                          key={meal.key}
                          className="group relative bg-black/10 border border-white/10 rounded-xl p-4 transition-all duration-300 hover:bg-black/20"
                        >
                          <div className="font-semibold text-white mb-1">
                            {meal.name}
                          </div>

                          <div className="flex items-center gap-2 mb-2">
                            <Flame className="w-4 h-4 text-orange-400" />
                            <span className="font-semibold text-white">
                              {meal.calories || "--"}
                            </span>
                            <span className="text-xs text-gray-400">kcal</span>
                          </div>

                          {meal.quantityAndIngredients ? (
                            <div className="text-sm text-gray-200">
                              <span className="text-gray-400">Quantity:</span>{" "}
                              {meal.quantityAndIngredients}
                            </div>
                          ) : null}

                          {meal.preparationTip ? (
                            <div className="text-sm text-gray-200 mt-2">
                              <span className="text-gray-400">Tip:</span>{" "}
                              {meal.preparationTip}
                            </div>
                          ) : null}
                        </div>
                      ))
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

  );
}

export default CurrentMeal;