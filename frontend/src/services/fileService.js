/**
 * File Service
 * Handles file upload and management API calls
 */
import axios from 'axios';

const AUTH_API_URL = import.meta.env.VITE_AUTH_API_URL || 'http://localhost:8003';

const fileApi = axios.create({
  baseURL: AUTH_API_URL,
  timeout: 60000 // Longer timeout for file uploads
});

// Add auth token to requests
fileApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response
fileApi.interceptors.response.use(
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

const fileService = {
  /**
   * Upload a CSV or Excel file
   */
  uploadFile: async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    return fileApi.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  /**
   * List all uploaded files
   */
  listFiles: async (skip = 0, limit = 100) => {
    return fileApi.get('/files', { params: { skip, limit } });
  },

  /**
   * Get file details
   */
  getFile: async (fileId) => {
    return fileApi.get(`/files/${fileId}`);
  },

  /**
   * Get file preview (first N rows)
   */
  getFilePreview: async (fileId, rows = 5) => {
    return fileApi.get(`/files/${fileId}/preview`, { params: { rows } });
  },

  /**
   * Delete a file
   */
  deleteFile: async (fileId) => {
    return fileApi.delete(`/files/${fileId}`);
  }
};

export default fileService;
