/**
 * Monthly Report Service
 * Handles monthly report API calls
 */
import axios from 'axios';

const AUTH_API_URL = import.meta.env.VITE_AUTH_API_URL || 'http://localhost:8003';

const reportApi = axios.create({
  baseURL: AUTH_API_URL,
  timeout: 30000 // Longer timeout for report generation
});

// Add auth token to requests
reportApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response
reportApi.interceptors.response.use(
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

const monthlyReportService = {
  /**
   * Get monthly report for specified year and month
   * @param {number} year - Report year
   * @param {number} month - Report month (1-12)
   * @returns {Promise} Monthly report data
   */
  getMonthlyReport: async (year, month) => {
    return reportApi.get('/monthly-reports', {
      params: { year, month }
    });
  },

  /**
   * Get list of months with available data
   * @returns {Promise} Available months
   */
  getAvailableMonths: async () => {
    return reportApi.get('/monthly-reports/available');
  }
};

export default monthlyReportService;
