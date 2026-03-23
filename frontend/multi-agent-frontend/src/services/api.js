import { API_ENDPOINTS, 
  AUTH_API, 
  HEALTH_API,
   MEAL_APPROVAL_API,
    EXERCISE_API,
    JOURNAL_API,
    PROFILE_API
   } from "../api/endpoints";
   import toast from "react-hot-toast";


export const getAuthHeaders = () => {
  const token = localStorage.getItem("token");

  return {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "",
  };
};

const getUserIdFromToken = () => {
  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    const payloadPart = token.split(".")[1];
    if (!payloadPart) return null;

    const base64 = payloadPart.replace(/-/g, "+").replace(/_/g, "/");
    const padded = base64.padEnd(base64.length + ((4 - (base64.length % 4)) % 4), "=");
    const payloadJson = atob(padded);
    const payload = JSON.parse(payloadJson);

    const sub = payload?.sub;
    const asNum = typeof sub === "string" ? Number(sub) : Number(sub);
    return Number.isFinite(asNum) ? asNum : null;
  } catch {
    return null;
  }
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
          phone:payload.phone
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

  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.reload();  // forces login again
  }

  if (!response.ok) {
    throw new Error("Failed to fetch meal plan");
  }
  console.log("inside getMealplan")
  return response.json();
};

export const approveMealPlan = async (mealPlanId, shopNumber) => {
  try {
    const response = await fetch(
      MEAL_APPROVAL_API.APPROVE_MEAL_PLAN(mealPlanId, shopNumber),
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
    // alert(data.message || "Operation completed");
    // toast.success(data.message || "Operation completed")
    

    return data;

    // return await response.json();
  } catch (error) {
    console.error("Error approving meal plan:", error);
    throw error;
  }
};
export const getRecommendations = async () => {
  const response = await fetch(EXERCISE_API.GET_RECOMMENDATIONS, {
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
  const response = await fetch(JOURNAL_API.GET_JOURNAL, {
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
    const response = await fetch(API_ENDPOINTS.UPDATE_MEAL_PLAN(user_id), {
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
    getMealPlan();

    return await response.json();
  } catch (error) {
    console.error("Failed to update meal plan:", error);
    throw error;
  }
};

export const HealthDailyUpdate = async (payload) => {
  try {
    const response = await fetch(HEALTH_API.CREATE_HEALTH_DATA, {
      method: "POST",
      headers: 
      
        getAuthHeaders()

      ,
      body: JSON.stringify(payload),
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      let message = "Unknown error";

      if (Array.isArray(data?.detail)) {
        message = data.detail.map((e) => e.msg).join(", ");
      } else if (typeof data?.detail === "string") {
        message = data.detail;
      } else {
        message = `Server error ${response.status}`;
      }

      throw new Error(message);
    }

    return data;
  } catch (error) {
    console.error("HealthDailyUpdate error:", error);
    throw error;
  }
};



export const getHealth = async () => {
  const userId = getUserIdFromToken();
  if (!userId) {
    throw new Error("Missing user id (please login again)");
  }

  const response = await fetch(HEALTH_API.GET_TODAY_HEALTH_METRICS(userId), {
    method: "GET",
    headers: getAuthHeaders(),
  });

  console.log("Response status:", response.status);

  

  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.reload();  // forces login again
  }

  if (!response.ok) {
    throw new Error("Failed to fetch health metrics");
  }
   const data = await response.json();
  return data;
};

export const getLastWeekHealth = async (userIdOverride) => {
  const userId = userIdOverride ?? getUserIdFromToken();
  if (!userId) {
    throw new Error("Missing user id (please login again)");
  }

  const response = await fetch(HEALTH_API.GET_LAST_WEEK_HEALTH(userId), {
    method: "GET",
    headers: getAuthHeaders(),
  });

  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.reload(); // forces login again
  }

  if (!response.ok) {
    throw new Error("Failed to fetch last week health metrics");
  }

  return response.json();
};

export const getLastMonthHealth = async (userIdOverride) => {
  const userId = userIdOverride ?? getUserIdFromToken();
  if (!userId) {
    throw new Error("Missing user id (please login again)");
  }

  const response = await fetch(HEALTH_API.GET_LAST_MONTH_HEALTH(userId), {
    method: "GET",
    headers: getAuthHeaders(),
  });

  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.reload(); // forces login again
  }

  if (!response.ok) {
    throw new Error("Failed to fetch last month health metrics");
  }

  return response.json();
};

// src/services/sttService.js
export const transcribeAudio = async (audioBlob) => {
  try {
    const formData = new FormData();
    formData.append("file", audioBlob, "recording.mp4");

    const response = await fetch(JOURNAL_API.TRANSCRIBE_AUDIO, {
      method: "POST",
      body: formData,
      headers: getAuthHeadersform(), // your auth headers function
    });

    if (!response.ok) {
      throw new Error(`STT API error: ${response.statusText}`);
    }

    const data = await response.json();
    return data.text; // return only the transcription
  } catch (error) {
    console.error("Error in transcribeAudio:", error);
    throw error;
  }
};

export const getUserProfile = async (userIdOverride) => {
  const userId = userIdOverride ?? getUserIdFromToken();

  if (!userId) {
    throw new Error("Missing user id (please login again)");
  }

  const response = await fetch(PROFILE_API.GET_USER_PROFILE(userId), {
    method: "GET",
    headers: getAuthHeaders(),
  });

  // Handle unauthorized
  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.reload();
  }

  // Handle other errors
  if (!response.ok) {
    throw new Error("Failed to fetch user profile");
  }

  return response.json();
};