import { useState, useEffect } from "react";
import { getMealPlan, approveMealPlan,getUserProfile } from "../../services/api";
import MealPlanActions from "./UpdateMealPlan";
import toast from "react-hot-toast";
import { motion } from "framer-motion";
import MealModal from "./MealModal";
import { parseMealPlan } from "../../services/parseMealPlan";

function MealPlan() {
  const [mealPlan, setMealPlan] = useState(null);
  const [selectedDay, setSelectedDay] = useState("");
  const [mealPlanId, setMealPlanId] = useState(null);
  const [approved, setApproved] = useState(null);
  const [userId, setUserId] = useState(null);
  const [error, setError] = useState(null);

  const [showModal, setShowModal] = useState(false);
  const [showApproveModal, setShowApproveModal] = useState(false);
  const [shopNumber, setShopNumber] = useState("");
  const [selectedMeal, setSelectedMeal] = useState(null);
  const [targetCalories, setTargetCalories] = useState(1800);
  

  // Load meal plan on mount
  useEffect(() => {
    const loadMealPlan = async () => {
      try {
        const data = await getMealPlan();
        setMealPlanId(data.meal_plan_id);
        setUserId(data.user_id);
        setApproved(data.approved);

        const parsed = parseMealPlan(data.meal_plan);
        setMealPlan(parsed);

        const firstDay = Object.keys(parsed)[0];
        setSelectedDay(firstDay);
        
        // get user profile
        const profile = await getUserProfile(data.user_id);
         setTargetCalories(profile.calories || 1800);
      } catch (err) {
        console.error(err);
        setError("Failed to load meal plan");
      }
    };

    loadMealPlan();
  }, []);

  if (error) return <p className="text-white p-6">{error}</p>;
  if (!mealPlan) return <p className="text-white p-6">Loading...</p>;

  // Calculate total calories for selected day
  const totalCalories = Object.values(mealPlan[selectedDay] || {}).reduce(
    (sum, meals) =>
      sum + meals.reduce((mealSum, m) => mealSum + (m.calories || 0), 0),
    0
  );

 
  const progress = Math.min((totalCalories / targetCalories) * 100, 100);

  return (
    <div className="p-6 text-white">

      {/* HEADER */}
      <div className="mb-6 bg-gradient-to-r from-amber-500/10 to-orange-500/10 border border-white/10 rounded-2xl p-5">
        <div className="flex justify-between">
         
          <h2 className="text-xl font-semibold">{selectedDay ? selectedDay.toUpperCase() : "Loading..."}</h2>
          <span>{totalCalories} / {targetCalories} kcal</span>
        </div>

        <div className="w-full h-3 bg-white/10 rounded-full mt-3">
          <div
            className="h-full bg-gradient-to-r from-amber-400 to-orange-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* DAY SELECTOR */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {Object.keys(mealPlan).map((day) => (
          <button
            key={day}
            onClick={() => setSelectedDay(day)}
            className={`px-3 py-1 rounded ${
              selectedDay === day ? "bg-amber-500" : "bg-white/10"
            }`}
          >
            {day}
          </button>
        ))}
      </div>

      {/* MEALS */}
      <div className="space-y-6">
        {Object.entries(mealPlan[selectedDay] || {}).map(([mealType, meals]) => (
          <div key={mealType}>
            <h3 className="text-lg font-semibold mb-2">{mealType ? mealType.toUpperCase() : ""}</h3>
            <div className="space-y-4">
              {meals.map((meal, idx) => (
                <motion.div
                  key={`${mealType}-${idx}`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white/5 border border-white/10 rounded-2xl p-5"
                >
                  <h4 className="text-md font-semibold">{meal.name}</h4>
                  <div className="text-orange-400">🔥 {meal.calories} kcal</div>
                  <button
                    onClick={() => setSelectedMeal(meal)}
                    className="mt-2 px-3 py-2 bg-amber-500 rounded"
                  >
                    View Details
                  </button>
                </motion.div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* MODAL */}
      <MealModal selectedMeal={selectedMeal} onClose={() => setSelectedMeal(null)} />

      {/* ACTIONS */}
      {showModal ? (
        <MealPlanActions
          userId={userId}
          currentPlan={{ calories: 1800, diet: "vegetarian", goal: "weight loss", region: "Kerala" }}
          onClose={() => setShowModal(false)}
        />
      ) : (
        <div className="flex gap-3 mt-4">
          {!approved && (
            <button
              onClick={() => setShowApproveModal(true)}
              className="px-4 py-2 bg-green-500/20 border border-green-500/30 text-green-400 rounded-lg hover:bg-green-500/30 transition"
            >
              Approve Plan
            </button>
          )}
          <button
            onClick={() => setShowModal(true)}
            className="px-4 py-2 bg-amber-500/20 border border-amber-500/30 text-amber-400 rounded-lg hover:bg-amber-500/30 transition"
          >
            Update Plan
          </button>
        </div>
      )}

      {/* APPROVE MODAL */}
      {showApproveModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
          <div className="bg-gray-900 border border-white/10 rounded-xl p-6 w-[350px]">
            <h2 className="text-xl font-semibold text-white mb-4">Enter Shop Number</h2>
            <input
              type="text"
              placeholder="Grocery Shop Number"
              value={shopNumber}
              onChange={(e) => setShopNumber(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:border-green-400"
            />
            <div className="flex justify-end gap-3 mt-5">
              <button
                onClick={() => { setShowApproveModal(false); setShopNumber(""); }}
                className="px-4 py-2 bg-gray-700 text-gray-200 rounded-lg hover:bg-gray-600"
              >
                Cancel
              </button>
              <button
                onClick={async () => {
                  try {
                    await approveMealPlan(mealPlanId, shopNumber);
                    toast.success("Plan approved ✅");
                    setShowApproveModal(false);
                    setShopNumber("");
                    setApproved(true);
                  } catch (error) {
                    console.error(error);
                    toast.error("Approval failed ❌");
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