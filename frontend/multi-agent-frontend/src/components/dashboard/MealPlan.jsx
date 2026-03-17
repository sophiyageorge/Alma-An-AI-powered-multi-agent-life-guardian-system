

// export default MealPlan;
import { useState, useEffect } from "react";
import { getMealPlan, approveMealPlan } from "../../services/api";
import { Flame } from "lucide-react";
import MealPlanActions from "./UpdateMealPlan";
import toast from "react-hot-toast";


function MealPlan() {
  const [mealPlan, setMealPlan] = useState(null);
  const [selectedDay, setSelectedDay] = useState(null);
  const [openMealDetailsKey, setOpenMealDetailsKey] = useState(null);
  const [mealPlanId, setMealPlanId] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [userId, setUserId] = useState(null);
  const [error, setError] = useState(null);
  const [showApproveModal, setShowApproveModal] = useState(false);
  const [shopNumber, setShopNumber] = useState("");

  useEffect(() => {
    const loadMealPlan = async () => {
      try {
        setError(null);
        const data = await getMealPlan();
        setMealPlanId(data.meal_plan_id);
        setUserId(data.user_id);


        const parsed = parseMealPlan(data.meal_plan);
        setMealPlan(parsed);
        console.log(parsed);

        // Select first day by default
        const firstDay = Object.keys(parsed)[0];
        setSelectedDay(firstDay);
      } catch (error) {
        console.error(error);
        setError(error?.message || "Failed to load meal plan");
      }
    };

    loadMealPlan();
  }, []);


  

  const parseMealPlan = (text) => {
    if (typeof text !== "string") return {};

    const normalized = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
    // Supports formats like:
    // "**Day 1**" or "Day 1:" or "Day 1"
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
      const mealTypes = ["breakfast", "lunch", "dinner", "snacks", "snack"];

      let currentType = null;
      let buffer = [];

      const flush = () => {
        if (!currentType || buffer.length === 0) return;

        // Supports both:
        // 1) Plain:
        //    Food name (quantity + ingredients)
        //    Calories: XXX kcal
        //    Preparation tip: ...
        // 2) Markdown bullets:
        //    * **Breakfast:** Name
        //      - Food name: ...
        //      - Ingredients: ...
        //      - Calories: ...
        //      - Preparation tip: ...
        const firstLine = buffer[0] ?? "";
        const foodLine =
          buffer.find((l) => /^-?\s*food\s*name\s*:/i.test(l)) ??
          firstLine;

        const caloriesLine = buffer.find((l) => /^-?\s*calories\s*:/i.test(l));
        const prepLine = buffer.find((l) => /^-?\s*preparation\s*tip\s*:/i.test(l));
        const ingredientsLine = buffer.find((l) => /^-?\s*ingredients\s*:/i.test(l));

        const caloriesMatch = caloriesLine?.match(/(\d+)\s*(kcal|cal)/i);
        const calories = caloriesMatch ? Number(caloriesMatch[1]) : 0;

        const prepTip = prepLine
          ? prepLine.replace(/^-?\s*preparation\s*tip\s*:\s*/i, "").trim()
          : "";

        const ingredients = ingredientsLine
          ? ingredientsLine.replace(/^-?\s*ingredients\s*:\s*/i, "").trim()
          : "";

        const foodValue = foodLine
          .replace(/^-?\s*food\s*name\s*:\s*/i, "")
          .trim();

        const qtyIngMatch = foodValue.match(/\(([^)]*)\)/);
        const quantityAndIngredients = qtyIngMatch ? qtyIngMatch[1].trim() : "";

        // const name =
        //   (foodValue.split("(")[0].trim() || firstLine)
        //     .replace(/^\*+\s*/, "")
        //     .replace(/\*\*/g, "")
        //     .trim() || `${currentType}`;
        let name = foodValue || firstLine || "";

name = name
  .replace(/^\*+\s*/, "")
  .replace(/\*\*/g, "")
  .replace(/\(.+\)/, "") // remove bracket part
  .trim();

if (!name) {
  name = currentType ? `${currentType} meal` : "Meal";
}

        // Anything else in the buffer (other than calories/prep) can be treated as extra notes.
        const extra = buffer
          .slice(1)
          .filter(
            (l) =>
              !/^-?\s*calories\s*:/i.test(l) &&
              !/^-?\s*preparation\s*tip\s*:/i.test(l) &&
              !/^-?\s*ingredients\s*:/i.test(l) &&
              !/^-?\s*food\s*name\s*:/i.test(l)
          )
          .join("\n")
          .trim();

        meals.push({
          key: `${dayKey}-${currentType}-${meals.length}`,
          type: currentType,
          name,
          calories,
          quantityAndIngredients,
          preparationTip: prepTip,
          ingredients,
          extra,
        });

        buffer = [];
      };

      for (const line of lines) {
        // Markdown meal header line (tolerant):
        // "* **Breakfast:** Foo" or "- **Breakfast:** Foo" or "* Breakfast: Foo"
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

        // Plain meal header line:
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

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-white">
          <div className="font-semibold mb-1">Meal plan not available</div>
          <div className="text-sm text-gray-300">{error}</div>
          <div className="text-sm text-gray-300 mt-2">
            Please login again and try, or generate a new plan.
          </div>
        </div>
      </div>
    );
  }

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
              setOpenMealDetailsKey(null);
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
        {[...(mealPlan[selectedDay] ?? [])]
          .sort((a, b) => {
            const order = { breakfast: 1, lunch: 2, snacks: 3, snack: 3, dinner: 4 };
            const aKey = (a?.type || "").toLowerCase();
            const bKey = (b?.type || "").toLowerCase();
            const aRank = order[aKey] ?? 99;
            const bRank = order[bKey] ?? 99;
            return aRank - bRank;
          })
          .map((meal, idx) => (
          <div
            key={idx}
            className={`bg-white/5 border border-white/10 rounded-xl p-4 cursor-pointer transition-all duration-300 ${
              openMealDetailsKey === meal.key
                ? "ring-2 ring-amber-500/50 scale-105"
                : ""
            }`}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="font-semibold text-white mb-1">{meal.name}</div>
              <div className="shrink-0 px-2.5 py-1 rounded-full bg-white/10 border border-white/10 text-[11px] font-semibold text-gray-200 uppercase tracking-wide">
                {(meal.type || "meal").replace(/^snack$/i, "snacks")}
              </div>
            </div>

            <div className="flex items-center gap-2 mb-3">
              <Flame className="w-4 h-4 text-orange-400" />
              <span className="text-white font-semibold">{meal.calories}</span>
              <span className="text-xs text-gray-400">cal</span>
            </div>

            <button
              type="button"
              onClick={() =>
                setOpenMealDetailsKey((prev) => (prev === meal.key ? null : meal.key))
              }
              className="w-full mt-2 px-3 py-2 rounded-lg bg-white/10 border border-white/10 text-gray-200 hover:bg-white/15 transition text-sm"
            >
              {openMealDetailsKey === meal.key ? "Hide details" : "Show recipe & tips"}
            </button>

            <div
              className={`overflow-hidden transition-all duration-300 ${
                openMealDetailsKey === meal.key ? "max-h-96 opacity-100" : "max-h-0 opacity-0"
              }`}
            >
              <div className="mt-3 text-sm text-gray-200 border-t border-white/10 pt-3 space-y-2">
                {meal.quantityAndIngredients ? (
                  <div>
                    <div className="text-xs text-gray-400 mb-1">Quantity allowed</div>
                    <div className="text-white/90">{meal.quantityAndIngredients}</div>
                  </div>
                ) : null}

                {meal.preparationTip ? (
                  <div>
                    <div className="text-xs text-gray-400 mb-1">Preparation tip</div>
                    <div className="text-white/90">{meal.preparationTip}</div>
                  </div>
                ) : null}

                {meal.ingredients ? (
                  <div>
                    <div className="text-xs text-gray-400 mb-1">Ingredients</div>
                    <div className="text-white/90 whitespace-pre-line">{meal.ingredients}</div>
                  </div>
                ) : null}

                {meal.extra ? (
                  <div>
                    <div className="text-xs text-gray-400 mb-1">Notes</div>
                    <div className="text-white/90 whitespace-pre-line">{meal.extra}</div>
                  </div>
                ) : null}

                {!meal.quantityAndIngredients && !meal.preparationTip && !meal.ingredients && !meal.extra ? (
                  <div className="text-gray-300">
                    No extra recipe/tips found in the plan text for this meal.
                  </div>
                ) : null}
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
        {/* <button
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
        </button> */}
        <button
  onClick={() => setShowApproveModal(true)}
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
    {showApproveModal && (
  <div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
    <div className="bg-gray-900 border border-white/10 rounded-xl p-6 w-[350px]">
      
      <h2 className="text-xl font-semibold text-white mb-4">
        Enter Shop Number
      </h2>

      <input
        type="text"
        placeholder="Shop Number"
        value={shopNumber}
        onChange={(e) => setShopNumber(e.target.value)}
        className="w-full px-3 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:border-green-400"
      />

      <div className="flex justify-end gap-3 mt-5">
        
        <button
          onClick={() => {
            setShowApproveModal(false);
            setShopNumber("");
          }}
          className="px-4 py-2 bg-gray-700 text-gray-200 rounded-lg hover:bg-gray-600"
        >
          Cancel
        </button>

        <button
          onClick={async () => {
            try {
              await approveMealPlan(mealPlanId, shopNumber);

              // alert("Plan approved ✅");
              toast.success("Plan approved ✅")

              setShowApproveModal(false);
              setShopNumber("");

            } catch (error) {
              console.error(error);
              // alert("Approval failed ❌");
              toast.error("Approval")
            }
          }}
          className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
        >
          Submit
        </button>

      </div>
    </div>
  </div>
)}
    </div>
  );
}

export default MealPlan;