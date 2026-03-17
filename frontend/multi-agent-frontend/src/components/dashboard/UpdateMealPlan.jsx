
import { useState } from "react";
import { updateMealPlan } from "../../services/api";
import { createPortal } from "react-dom";
import toast from "react-hot-toast";

function MealPlanActions({ userId, currentPlan, onClose }) {
  const [formData, setFormData] = useState({
    calories: currentPlan?.calories || "",
    diet: currentPlan?.diet || "",
    goal: currentPlan?.goal || "",
    region: currentPlan?.region || "",
    restrictions: currentPlan?.restrictions?.join(", ") || "",
    meal_type: currentPlan?.meal_type || ""
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (key, value) => {
    setFormData((prev) => ({
      ...prev,
      [key]: value
    }));
  };

  const handleUpdate = async () => {
    try {
      setLoading(true);

      const payload = {
        calories: Number(formData.calories),
        diet: formData.diet,
        goal: formData.goal,
        region: formData.region,
        meal_type: formData.meal_type,
        restrictions: formData.restrictions
          ? formData.restrictions.split(",").map((r) => r.trim())
          : []
      };

      await updateMealPlan(userId, payload);

      // alert("Meal plan updated successfully ✅");
      toast.success("Meal plan updated successfully ✅")
      window.location.href="/home"
      
      onClose();
    } catch (err) {
      console.error(err);
      // alert("Update failed ❌");
      // toast.error("Update failed ❌")
    } finally {
      setLoading(false);
    }
  };

  return createPortal(
    <div
      className="fixed inset-0 bg-black/60 flex items-center justify-center z-[9999]"
      onClick={onClose}
    >
      <div
        className="bg-gray-900 p-6 rounded-2xl w-full max-w-md border border-white/10"
        onClick={(e) => e.stopPropagation()}
      >
        <h3 className="text-xl font-bold text-white mb-5">
          Update Meal Plan Preferences
        </h3>

        <div className="space-y-4">

          <div>
            <label className="text-sm text-gray-400">Calories</label>
            <input
              type="number"
              value={formData.calories}
              onChange={(e) => handleChange("calories", e.target.value)}
              className="w-full mt-1 p-2 rounded-lg bg-white/5 border border-white/10 text-white"
            />
          </div>

          <div>
            <label className="text-sm text-gray-400">Diet</label>
            <input
              type="text"
              value={formData.diet}
              onChange={(e) => handleChange("diet", e.target.value)}
              className="w-full mt-1 p-2 rounded-lg bg-white/5 border border-white/10 text-white"
            />
          </div>

          <div>
            <label className="text-sm text-gray-400">Goal</label>
            <input
              type="text"
              value={formData.goal}
              onChange={(e) => handleChange("goal", e.target.value)}
              className="w-full mt-1 p-2 rounded-lg bg-white/5 border border-white/10 text-white"
            />
          </div>

          <div>
            <label className="text-sm text-gray-400">Region</label>
            <input
              type="text"
              value={formData.region}
              onChange={(e) => handleChange("region", e.target.value)}
              className="w-full mt-1 p-2 rounded-lg bg-white/5 border border-white/10 text-white"
            />
          </div>

          <div>
            <label className="text-sm text-gray-400">Meal Type</label>
            <input
              type="text"
              value={formData.meal_type}
              onChange={(e) => handleChange("meal_type", e.target.value)}
              className="w-full mt-1 p-2 rounded-lg bg-white/5 border border-white/10 text-white"
            />
          </div>

          <div>
            <label className="text-sm text-gray-400">
              Restrictions (comma separated)
            </label>
            <input
              type="text"
              placeholder="eg: no dairy, no sugar"
              value={formData.restrictions}
              onChange={(e) =>
                handleChange("restrictions", e.target.value)
              }
              className="w-full mt-1 p-2 rounded-lg bg-white/5 border border-white/10 text-white"
            />
          </div>

        </div>

        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg"
          >
            Cancel
          </button>

          <button
            onClick={handleUpdate}
            disabled={loading}
            className="px-4 py-2 bg-amber-500 text-white rounded-lg"
          >
            {loading ? "Updating..." : "Submit"}
          </button>
        </div>
      </div>
    </div>,
    document.body
  );
}

export default MealPlanActions;

