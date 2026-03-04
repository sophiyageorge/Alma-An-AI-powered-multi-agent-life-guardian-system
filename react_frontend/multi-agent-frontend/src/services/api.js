const BASE_URL = "http://localhost:8000"; // your FastAPI backend

export const getAuthHeaders = () => {
  const token = localStorage.getItem("token");

  return {
    "Content-Type": "application/json",
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

