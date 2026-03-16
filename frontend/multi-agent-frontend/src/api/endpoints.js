// src/api/endpoints.js
import { BASE_URL } from "./baseUrl";


// User related endpoints
// export const USER_API = {
//   LOGIN: `${BASE_URL}/auth/login`,
//   REGISTER: `${BASE_URL}/auth/register`,
//   PROFILE: `${BASE_URL}/user/profile`,
// };

export const AUTH_API = {
  LOGIN: `${BASE_URL}/users/login`,
  REGISTER: `${BASE_URL}/users/register`,
};

// Product related endpoints
export const API_ENDPOINTS = {
  GET_MEAL_PLAN: `${BASE_URL}/nutrition/meals`,
};


export const MEAL_APPROVAL_API = {
  APPROVE_MEAL_PLAN: (mealPlanId, shopNumber) =>
    `${BASE_URL}/meal-approval/meal-plan/${mealPlanId}/approve?shop_number=${shopNumber}`,
};

export const EXERCISE_API = {
  GET_RECOMMENDATIONS: `${BASE_URL}/exercise/recommendation`,
};

export const JOURNAL_API = {
    GET_JOURNAL: `${BASE_URL}/stt/journal/today`,
};

export const PROFILE_API = {
  UPDATE_MEAL_PLAN: (userId) => `${BASE_URL}/profile/${userId}`,
};


export const HEALTH_API = {
  CREATE_HEALTH_DATA: `${BASE_URL}/health/health-metrics/`,
  GET_TODAY_HEALTH_METRICS: (userId) =>
    `${BASE_URL}/health/health-metrics/user/${userId}/today`,
};