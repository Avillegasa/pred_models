/**
 * Model Service Factory
 * Provides unified interface for all prediction models
 */

import { phishingService } from './phishingService';
import { ataquesSospechososService } from './ataquesSospechososService';
import { fuerzaBrutaService } from './fuerzaBrutaService';

// Model type constants
export const MODEL_TYPES = {
  PHISHING: 'phishing',
  ATAQUES_SOSPECHOSOS: 'ataques_sospechosos',
  FUERZA_BRUTA: 'fuerza_bruta'
};

// Design tokens - matching BCP theme.js primitives
const THEME_COLORS = {
  info: '#00498C',     // BCP blue-600 - Phishing (primary/informational)
  danger: '#E53E3E',   // BCP red-500 - Account Takeover (high risk)
  warning: '#FF7800'   // BCP orange-500 (accent) - Brute Force (attack detection)
};

// Model metadata
export const MODEL_METADATA = {
  [MODEL_TYPES.PHISHING]: {
    id: MODEL_TYPES.PHISHING,
    name: 'Deteccion de Phishing',
    shortName: 'Phishing',
    description: 'Detecta emails de phishing usando aprendizaje automatico',
    icon: '📧',
    status: 'active', // 'active' or 'mock'
    color: THEME_COLORS.info,
    service: phishingService
  },
  [MODEL_TYPES.ATAQUES_SOSPECHOSOS]: {
    id: MODEL_TYPES.ATAQUES_SOSPECHOSOS,
    name: 'Deteccion de Toma de Cuenta',
    shortName: 'Logins Sospechosos',
    description: 'Detecta intentos de toma de cuenta usando analisis de comportamiento',
    icon: '🔐',
    status: 'active', // 'active' or 'mock'
    color: THEME_COLORS.danger,
    service: ataquesSospechososService
  },
  [MODEL_TYPES.FUERZA_BRUTA]: {
    id: MODEL_TYPES.FUERZA_BRUTA,
    name: 'Deteccion de Fuerza Bruta',
    shortName: 'Fuerza Bruta',
    description: 'Detecta ataques de fuerza bruta usando analisis de trafico de red (Random Forest)',
    icon: '🌐',
    status: 'active', // 'active' or 'mock'
    color: THEME_COLORS.warning,
    service: fuerzaBrutaService
  }
};

/**
 * Get service for a specific model type
 * @param {string} modelType - Model type constant
 * @returns {Object} Service object
 */
export const getModelService = (modelType) => {
  const metadata = MODEL_METADATA[modelType];

  if (!metadata) {
    console.error(`Unknown model type: ${modelType}`);
    return phishingService; // Fallback to phishing service
  }

  return metadata.service;
};

/**
 * Get metadata for a specific model
 * @param {string} modelType - Model type constant
 * @returns {Object} Model metadata
 */
export const getModelMetadata = (modelType) => {
  return MODEL_METADATA[modelType] || MODEL_METADATA[MODEL_TYPES.PHISHING];
};

/**
 * Get all available models
 * @returns {Array<Object>} Array of model metadata
 */
export const getAllModels = () => {
  return Object.values(MODEL_METADATA);
};

/**
 * Check if a model is in mock mode
 * @param {string} modelType - Model type constant
 * @returns {boolean} True if model is mock
 */
export const isModelMock = (modelType) => {
  const metadata = MODEL_METADATA[modelType];
  return metadata?.status === 'mock';
};

/**
 * Unified prediction function for any model
 * @param {string} modelType - Model type constant
 * @param {Object} data - Input data for prediction
 * @returns {Promise<Object>} Prediction result
 */
export const predictWithModel = async (modelType, data) => {
  try {
    const service = getModelService(modelType);
    const result = await service.predict(data);

    // Add model type to result metadata
    if (result.success && result.data) {
      result.data.model_type = modelType;
      result.data.is_mock = isModelMock(modelType);
    }

    return result;
  } catch (error) {
    console.error(`Error predicting with model ${modelType}:`, error);
    return {
      success: false,
      error: {
        type: 'service',
        message: `Error al obtener prediccion del modelo ${modelType}`,
        originalError: error
      }
    };
  }
};

/**
 * Get model information for any model
 * @param {string} modelType - Model type constant
 * @returns {Promise<Object>} Model information
 */
export const getModelInfo = async (modelType) => {
  try {
    const service = getModelService(modelType);

    // Check if service has getModelInfo method
    if (typeof service.getModelInfo === 'function') {
      return await service.getModelInfo();
    }

    // Fallback: return static metadata
    const metadata = getModelMetadata(modelType);
    return {
      success: true,
      data: {
        model_name: metadata.name,
        description: metadata.description,
        status: metadata.status,
        model_type: modelType
      }
    };
  } catch (error) {
    console.error(`Error getting model info for ${modelType}:`, error);
    return {
      success: false,
      error: {
        type: 'service',
        message: `Error al obtener informacion del modelo ${modelType}`,
        originalError: error
      }
    };
  }
};

/**
 * Health check for a specific model
 * @param {string} modelType - Model type constant
 * @returns {Promise<Object>} Health check result
 */
export const healthCheck = async (modelType) => {
  try {
    const service = getModelService(modelType);

    // Only phishing service has real health check
    if (modelType === MODEL_TYPES.PHISHING && typeof service.healthCheck === 'function') {
      return await service.healthCheck();
    }

    // Mock services always healthy
    return {
      success: true,
      data: {
        status: 'ok',
        model: getModelMetadata(modelType).name,
        is_mock: isModelMock(modelType)
      }
    };
  } catch (error) {
    return {
      success: false,
      error: {
        type: 'service',
        message: `Verificacion de estado fallida para ${modelType}`,
        originalError: error
      }
    };
  }
};

export default {
  MODEL_TYPES,
  MODEL_METADATA,
  getModelService,
  getModelMetadata,
  getAllModels,
  isModelMock,
  predictWithModel,
  getModelInfo,
  healthCheck
};
