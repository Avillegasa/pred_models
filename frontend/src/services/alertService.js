/**
 * Alert Service
 * Handles alert management API calls
 */
import axios from 'axios';

const AUTH_API_URL = import.meta.env.VITE_AUTH_API_URL || 'http://localhost:8003';

const alertApi = axios.create({
  baseURL: AUTH_API_URL,
  timeout: 10000
});

// Add auth token to requests
alertApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response
alertApi.interceptors.response.use(
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

const alertService = {
  /**
   * List alerts with optional filters
   */
  listAlerts: async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.status) params.append('status', filters.status);
    if (filters.severity) params.append('severity', filters.severity);
    if (filters.model_type) params.append('model_type', filters.model_type);
    if (filters.skip) params.append('skip', filters.skip);
    if (filters.limit) params.append('limit', filters.limit);

    const queryString = params.toString();
    return alertApi.get(`/alerts${queryString ? '?' + queryString : ''}`);
  },

  /**
   * Get unread alert count
   */
  getUnreadCount: async () => {
    return alertApi.get('/alerts/unread/count');
  },

  /**
   * Get alert statistics
   */
  getStats: async () => {
    return alertApi.get('/alerts/stats');
  },

  /**
   * Get alert thresholds configuration
   */
  getThresholds: async () => {
    return alertApi.get('/alerts/thresholds');
  },

  /**
   * Get single alert details
   */
  getAlert: async (alertId) => {
    return alertApi.get(`/alerts/${alertId}`);
  },

  /**
   * Acknowledge a single alert
   */
  acknowledgeAlert: async (alertId) => {
    return alertApi.post(`/alerts/${alertId}/acknowledge`);
  },

  /**
   * Bulk acknowledge alerts
   */
  bulkAcknowledge: async (alertIds) => {
    return alertApi.post('/alerts/acknowledge/bulk', { alert_ids: alertIds });
  },

  /**
   * Mark all alerts as read
   */
  markAllAsRead: async () => {
    return alertApi.post('/alerts/mark-all-read');
  }
};

export default alertService;
