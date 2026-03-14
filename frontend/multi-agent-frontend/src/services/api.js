const BASE_URL = "http://backend-service:8000"; // your FastAPI backend

export const getAuthHeaders = () => {
  const token = localStorage.getItem("token");

  return {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "",
  };
};

export const getAuthHeadersform = () => {
  const token = localStorage.getItem("token");

  return {
    // "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "",
  };
};


// uncomment this


export const getMealPlan = async () => {
  const response = await fetch(`${BASE_URL}/nutrition/meals`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch meal plan");
  }

  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.reload();  // forces login again
  }

  if (!response.ok) {
    throw new Error("Failed to fetch meal plan");
  }

  return response.json();
};

export const approveMealPlan = async (mealPlanId) => {
  try {
    const response = await fetch(
      `${BASE_URL}/meal-approval/meal-plan/${mealPlanId}/approve`,
      {
        method: "POST",
        headers: getAuthHeaders(), // includes JWT token
      }
    );

    // Handle unauthorized
    if (response.status === 401) {
      localStorage.removeItem("token");
      window.location.reload(); // forces login
      return; // stop execution
    }

    // Handle other errors
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to approve meal plan: ${errorText}`);
    }

    // Successful response
    const data = await response.json();

    // Show API message in alert
    alert(data.message || "Operation completed");

    return data;

    // return await response.json();
  } catch (error) {
    console.error("Error approving meal plan:", error);
    throw error;
  }
};
export const getRecommendations = async () => {
  const response = await fetch(`${BASE_URL}/exercise/recommendation`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch meal plan");
  }

  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.reload();  // forces login again
  }

  if (!response.ok) {
    throw new Error("Failed to fetch meal plan");
  }

  return response.json();
};

export const getJournal = async () => {
  const response = await fetch(`${BASE_URL}/stt/journal/today`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch meal plan");
  }

  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.reload();  // forces login again
  }

  if (!response.ok) {
    throw new Error("Failed to fetch meal plan");
  }

  return response.json();
};

export const updateMealPlan = async (user_id, payload) => {
  try {
    const response = await fetch(`http://localhost:8000/profile/${user_id}`, {
      method: "PUT", // Use PUT as per API spec
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        calories: payload.calories || 0,
        diet: payload.diet || "",
        goal: payload.goal || "",
        region: payload.region || "",
        restrictions: Array.isArray(payload.restrictions)
          ? payload.restrictions
          : payload.restrictions
          ? [payload.restrictions]
          : [],
        meal_type: payload.meal_type || "",
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Failed to update meal plan:", error);
    throw error;
  }
};

