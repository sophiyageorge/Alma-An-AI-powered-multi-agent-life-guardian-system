import { useState, useEffect } from "react";
import { getMealPlan } from "../../services/api";



  
function MealPlan() {

  console.log("MealPlan component loaded");

  const [mealPlan, setMealPlan] = useState(null);

  useEffect(() => {
    const loadMealPlan = async () => {
      try {
        const data = await getMealPlan();
        setMealPlan(data);
      } catch (error) {
        console.error(error);
      }
    };

    loadMealPlan();
  }, []);

  return (
    <div style={{ padding: "20px", background: "yellow" }}>
      <h1>Today's Meal Plan</h1>
      {mealPlan ? (
        <pre>{mealPlan.meal_plan}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default MealPlan;