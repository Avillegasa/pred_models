/**
 * Prediction Service
 * Handles storing and retrieving manual predictions
 */
import axios from 'axios';

const AUTH_API_URL = import.meta.env.VITE_AUTH_API_URL || 'http://localhost:8003';

const predictionApi = axios.create({
  baseURL: AUTH_API_URL,
  timeout: 30000
});

// Add auth token to requests
predictionApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response
predictionApi.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

const predictionService = {
  /**
   * Save a manual prediction result
   */
  savePrediction: async (predictionData) => {
    return predictionApi.post('/predictions/', predictionData);
  },

  /**
   * List manual predictions
   */
  listPredictions: async (skip = 0, limit = 100, modelType = null) => {
    const params = { skip, limit };
    if (modelType) {
      params.model_type = modelType;
    }
    return predictionApi.get('/predictions/', { params });
  },

  /**
   * Get prediction statistics for dashboard
   */
  getStats: async () => {
    return predictionApi.get('/predictions/stats');
  }
};

export default predictionService;
