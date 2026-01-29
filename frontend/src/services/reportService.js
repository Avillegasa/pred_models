/**
 * Report Service
 * Handles report generation and viewing API calls
 */
import axios from 'axios';

const AUTH_API_URL = import.meta.env.VITE_AUTH_API_URL || 'http://localhost:8003';

const reportApi = axios.create({
  baseURL: AUTH_API_URL,
  timeout: 120000 // Longer timeout for report generation
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

const reportService = {
  /**
   * Generate a new report from a file
   */
  generateReport: async (title, fileId) => {
    return reportApi.post('/reports/generate', {
      title,
      file_id: fileId
    });
  },

  /**
   * List all reports
   */
  listReports: async (skip = 0, limit = 100) => {
    return reportApi.get('/reports', { params: { skip, limit } });
  },

  /**
   * Get report details
   */
  getReport: async (reportId) => {
    return reportApi.get(`/reports/${reportId}`);
  },

  /**
   * Delete a report
   */
  deleteReport: async (reportId) => {
    return reportApi.delete(`/reports/${reportId}`);
  }
};

export default reportService;
