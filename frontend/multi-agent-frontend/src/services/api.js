import { API_ENDPOINTS,AUTH_API, } from "../api/endpoints";


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



export const authenticateUser = async (mode, payload) => {
  const endpoint =
    mode === "signin" ? AUTH_API.LOGIN : AUTH_API.REGISTER;

  const body =
    mode === "signin"
      ? JSON.stringify({
          email: payload.email,
          password: payload.password,
        })
      : JSON.stringify({
          name: payload.name,
          email: payload.email,
          date_of_birth: payload.dateOfBirth,
          gender: payload.gender,
          password: payload.password,
        });

  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: body,
  });

  const data = await response.json();

  return { response, data };
};


export const getMealPlan = async () => {
  const response = await fetch(API_ENDPOINTS.GET_MEAL_PLAN, {
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

export const approveMealPlan = async (mealPlanId, shopNumber) => {
  try {
    const response = await fetch(
      API_ENDPOINTS.MEAL_APPROVAL_API.APPROVE_MEAL_PLAN(mealPlanId, shopNumber),
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
  const response = await fetch(API_ENDPOINTS.EXERCISE_API.GET_RECOMMENDATIONS, {
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
  const response = await fetch(API_ENDPOINTS.JOURNAL_API.GET_JOURNAL, {
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
    const response = await fetch(API_ENDPOINTS.PROFILE_API.UPDATE_MEAL_PLAN(user_id), {
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

export const HealthDailyUpdate = async (payload) => {
  try {
    const response = await fetch(`${API_BASE_URL}/health-data`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData?.detail || `Server error ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("HealthDailyUpdate error:", error);
    throw error;
  }
};

