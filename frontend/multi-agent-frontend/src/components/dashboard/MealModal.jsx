import { createPortal } from "react-dom";
import { motion, AnimatePresence } from "framer-motion";

export default function MealModal({ selectedMeal, onClose }) {
  if (!selectedMeal) return null;

  return createPortal(
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 p-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <motion.div
          className="bg-gray-900 text-white border border-gray-700 rounded-2xl p-6 max-w-2xl w-full relative overflow-y-auto max-h-[90vh] shadow-2xl"
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          exit={{ scale: 0.9 }}
        >
          {/* Close Button */}
          <button
            onClick={onClose}
            className="absolute top-3 right-3 text-gray-300 hover:text-white text-2xl font-bold"
          >
            ×
          </button>

          {/* Title */}
          <h3 className="text-2xl font-bold mb-4">{selectedMeal.name}</h3>

          {/* Calories */}
          <p className="mb-2 text-orange-400 font-semibold">
            🔥 {selectedMeal.calories} kcal
          </p>

          {/* Quantity */}
          {selectedMeal.quantity && (
            <div className="mt-3">
              <h4 className="text-lg font-semibold text-blue-400">Quantity</h4>
              <p className="text-gray-300">{selectedMeal.quantity}</p>
            </div>
          )}

          {/* Ingredients */}
          {/* Ingredients */}
            {selectedMeal.ingredients?.length > 0 && (
            <div className="mt-4">
                <h4 className="text-lg font-semibold text-green-400">Ingredients 🥗</h4>
                {selectedMeal.ingredients.map((ingredient, i) => (
                <div key={i} className="flex gap-2 mb-1 text-gray-300">
                    🥗 <span>{ingredient.item} - {ingredient.quantity} ({ingredient.calories} kcal)</span>
                </div>
                ))}
            </div>
            )}

          {/* Preparation Steps */}
          {/* Preparation Steps */}
            {selectedMeal.steps?.length > 0 && (
            <div className="mt-4">
                <h4 className="text-lg font-semibold text-purple-400">Preparation Steps</h4>
                {selectedMeal.steps.map((step, i) => (
                <div key={i} className="flex gap-2 mb-1 text-gray-300">
                    🔹 <span>{step}</span>
                </div>
                ))}
            </div>
            )}
        </motion.div>
      </motion.div>
    </AnimatePresence>,
    document.body
  );
}