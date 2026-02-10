/**
 * Account Takeover Detection Service - REAL API
 * Connects to Account Takeover Detection API
 */

const API_BASE_URL = 'http://localhost:8001';

/**
 * Map frontend field names to API field names
 * @param {Object} loginData - Login data from frontend
 * @returns {Object} Formatted data for API
 */
function formatLoginDataForAPI(loginData) {
  return {
    user_id: loginData.userId || loginData.user_id || 'unknown',
    ip_address: loginData.sourceIp || loginData.ip_address || loginData.ipAddress || '0.0.0.0',
    country: loginData.country || 'US',
    region: loginData.region || 'Unknown',
    city: loginData.city || 'Unknown',
    browser: loginData.browser || 'Unknown Browser',
    os: loginData.os || 'Unknown OS',
    device: loginData.device || 'Desktop',
    login_successful: loginData.loginSuccessful !== undefined ? (loginData.loginSuccessful ? 1 : 0) : 1,
    is_attack_ip: loginData.isAttackIp !== undefined ? (loginData.isAttackIp ? 1 : 0) : 0,
    asn: parseInt(loginData.asn) || 0,
    rtt: parseFloat(loginData.rtt) || 0.0,
    login_timestamp: loginData.timestamp || loginData.login_timestamp || new Date().toISOString()
  };
}

/**
 * Format API response for frontend
 * @param {Object} apiResponse - Response from API
 * @returns {Object} Formatted response for frontend
 */
function formatAPIResponse(apiResponse) {
  return {
    prediction: apiResponse.prediction,
    prediction_label: apiResponse.prediction_label === 'Account Takeover'
      ? 'Login Sospechoso'
      : 'Login Normal',
    confidence: apiResponse.confidence,
    probability_normal: apiResponse.probability_normal,
    probability_attack: apiResponse.probability_ato,
    risk_score: apiResponse.risk_score,
    severity: getSeverityFromRiskScore(apiResponse.risk_score),
    explanation: apiResponse.explanation,  // Pass through explanation from API
    metadata: {
      model: apiResponse.metadata.model,
      features_count: apiResponse.metadata.features_count,
      threshold: apiResponse.metadata.threshold,
      timestamp: apiResponse.metadata.timestamp,
      processing_time_ms: apiResponse.metadata.processing_time_ms
    }
  };
}

/**
 * Get severity level from risk score
 * @param {number} riskScore - Risk score (0-100)
 * @returns {string} Severity level
 */
function getSeverityFromRiskScore(riskScore) {
  if (riskScore >= 90) return 'Critico';
  if (riskScore >= 70) return 'Alto';
  if (riskScore >= 50) return 'Medio';
  if (riskScore >= 30) return 'Bajo';
  return 'Minimo';
}

export const ataquesSospechososService = {
  /**
   * Predict if a login is account takeover
   * @param {Object} loginData - Login attempt data
   * @returns {Promise<Object>} Prediction result
   */
  async predict(loginData) {
    try {
      // Format data for API
      const apiData = formatLoginDataForAPI(loginData);

      // Call real API
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(apiData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw {
          type: 'api',
          message: errorData.detail || `API request failed with status ${response.status}`,
          status: response.status,
          details: errorData
        };
      }

      const apiResponse = await response.json();
      const formattedResponse = formatAPIResponse(apiResponse);

      return {
        success: true,
        data: formattedResponse,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Account Takeover API Error:', error);

      // Handle network errors
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        return {
          success: false,
          error: {
            type: 'network',
            message: 'No se pudo conectar con la API. Verifica que el servidor esté corriendo en http://localhost:8001',
            originalError: error
          }
        };
      }

      return {
        success: false,
        error: error.type ? error : {
          type: 'unknown',
          message: error.message || 'Error desconocido al realizar la predicción',
          originalError: error
        }
      };
    }
  },

  /**
   * Get model information from API
   * @returns {Promise<Object>} Model metadata
   */
  async getModelInfo() {
    try {
      const response = await fetch(`${API_BASE_URL}/model/info`);

      if (!response.ok) {
        throw new Error(`Failed to get model info: ${response.status}`);
      }

      const data = await response.json();

      return {
        success: true,
        data: {
          model_name: data.model_name,
          version: data.model_version,
          status: 'active',
          training_date: data.training_date,
          description: 'Detecta intentos de toma de cuenta usando analisis de comportamiento',
          metrics: {
            f1_score: data.metrics.f1_score,
            accuracy: data.metrics.accuracy,
            precision: data.metrics.precision,
            recall: data.metrics.recall,
            roc_auc: data.metrics.roc_auc,
            auc_pr: data.metrics.auc_pr
          },
          features: {
            total: data.features.total,
            temporal: data.features.temporal,
            behavioral: data.features.behavioral,
            aggregated: data.features.aggregated,
            categorical: data.features.categorical,
            numeric: data.features.numeric
          },
          training_data: {
            total_samples: data.training_data.total_samples,
            train_samples: data.training_data.train_samples,
            test_samples: data.training_data.test_samples,
            ato_samples: data.training_data.ato_samples,
            normal_samples: data.training_data.normal_samples
          },
          threshold: {
            optimal: data.threshold.optimal_threshold,
            default: data.threshold.default_threshold,
            improvement: data.threshold.f1_improvement_pct
          }
        }
      };
    } catch (error) {
      console.error('Error getting model info:', error);
      return {
        success: false,
        error: {
          type: 'api',
          message: 'No se pudo obtener la informacion del modelo',
          originalError: error
        }
      };
    }
  },

  /**
   * Health check for API
   * @returns {Promise<Object>} Health status
   */
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/`);

      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }

      const data = await response.json();

      return {
        success: true,
        data: {
          status: data.status,
          message: data.message,
          model: data.model,
          version: data.version,
          is_mock: false
        }
      };
    } catch (error) {
      return {
        success: false,
        error: {
          type: 'network',
          message: 'API no disponible. Verifica que esté corriendo en http://localhost:8001',
          originalError: error
        }
      };
    }
  }
};

export default ataquesSospechososService;
