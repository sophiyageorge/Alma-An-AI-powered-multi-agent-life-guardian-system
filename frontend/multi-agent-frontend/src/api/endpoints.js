// src/api/endpoints.js
// import { BASE_URL } from "./baseUrl";
const BASE_URL = import.meta.env.VITE_API_BASE_URL;


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
  UPDATE_MEAL_PLAN: (userId) => `${BASE_URL}/profile/${userId}`,
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
    TRANSCRIBE_AUDIO: `${BASE_URL}/stt/transcribe`,
};

export const PROFILE_API = {
  UPDATE_MEAL_PLAN: (userId) => `${BASE_URL}/profile/${userId}`,
};


export const HEALTH_API = {
  CREATE_HEALTH_DATA: `${BASE_URL}/health/health-metrics/`,
  GET_TODAY_HEALTH_METRICS: (userId) =>
    `${BASE_URL}/health/health-metrics/user/${userId}/today`,
  GET_LAST_WEEK_HEALTH: (userId) =>
    `${BASE_URL}/health/health-metrics/health/last-week?user_id=${userId}`,
  GET_LAST_MONTH_HEALTH: (userId) =>
    `${BASE_URL}/health/health-metrics/health/last-month?user_id=${userId}`,
  GET_HEALTH:`${BASE_URL}/health/health-metrics/user/{user_id}/today`,
};

