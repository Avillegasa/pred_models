/**
 * API Configuration
 * Axios instance configuration for Phishing Detection API
 */

import axios from 'axios';

// Phishing API Configuration
const PHISHING_API_URL = import.meta.env.VITE_PHISHING_API_URL || 'http://localhost:8000';
const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT || 10000;
const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true';

// Create Axios instance for Phishing API
export const phishingApi = axios.create({
  baseURL: PHISHING_API_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor
phishingApi.interceptors.request.use(
  (config) => {
    if (DEBUG_MODE) {
      console.log(`[API Request] ${config.method.toUpperCase()} ${config.baseURL}${config.url}`);
      console.log('[API Request Data]', config.data);
    }
    return config;
  },
  (error) => {
    if (DEBUG_MODE) {
      console.error('[API Request Error]', error);
    }
    return Promise.reject(error);
  }
);

// Response interceptor
phishingApi.interceptors.response.use(
  (response) => {
    if (DEBUG_MODE) {
      console.log('[API Response]', response.status, response.data);
    }
    return response.data;
  },
  (error) => {
    if (DEBUG_MODE) {
      console.error('[API Response Error]', error.response?.data || error.message);
    }

    // Handle specific error cases
    if (error.code === 'ECONNABORTED') {
      return Promise.reject({
        type: 'timeout',
        message: 'Tiempo de espera agotado. El servidor tardo demasiado en responder.',
        originalError: error
      });
    }

    if (error.code === 'ERR_NETWORK') {
      return Promise.reject({
        type: 'network',
        message: 'No se puede conectar a la API. Verifique que el servidor este en ejecucion.',
        originalError: error
      });
    }

    if (error.response) {
      // Server responded with error status
      return Promise.reject({
        type: 'api',
        message: error.response.data?.detail || error.response.data?.message || 'Error en la solicitud de API',
        status: error.response.status,
        data: error.response.data,
        originalError: error
      });
    }

    // Unknown error
    return Promise.reject({
      type: 'unknown',
      message: error.message || 'Ocurrio un error inesperado',
      originalError: error
    });
  }
);

// Helper function to format API errors for display
export const formatApiError = (error) => {
  if (!error) return { title: 'Error', message: 'Ocurrio un error desconocido' };

  const errorTypes = {
    timeout: {
      title: 'Tiempo de Espera Agotado',
      icon: '⏱️'
    },
    network: {
      title: 'Error de Conexion',
      icon: '🌐'
    },
    api: {
      title: 'Error de API',
      icon: '⚠️'
    },
    validation: {
      title: 'Error de Validacion',
      icon: '📝'
    },
    unknown: {
      title: 'Error',
      icon: '❌'
    }
  };

  const errorInfo = errorTypes[error.type] || errorTypes.unknown;

  return {
    title: errorInfo.title,
    message: error.message,
    icon: errorInfo.icon,
    status: error.status,
    details: error.data
  };
};

export default phishingApi;
