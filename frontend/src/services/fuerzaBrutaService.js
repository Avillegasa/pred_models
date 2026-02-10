/**
 * Fuerza Bruta (Brute Force) Service - REAL API
 * Connects to Brute Force Detection API (Random Forest model)
 *
 * NOTE: This model uses NETWORK TRAFFIC FEATURES (60 features)
 * NOT login attempt data. It analyzes network packets to detect brute force attacks.
 */

const API_BASE_URL = import.meta.env.VITE_BRUTE_FORCE_API_URL || 'http://localhost:8002';

// Simulate API delay for mock fallback
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Pre-loaded example network flows for testing
 */
export const EXAMPLE_FLOWS = {
  bruteForce: {
    name: "Ataque de Fuerza Bruta SSH",
    description: "Patron tipico de ataque de fuerza bruta SSH del dataset CSE-CIC-IDS2018",
    data: {
      dst_port: 0.0003,
      protocol: 0.3529,
      timestamp: 0.0432,
      flow_duration: 0.0000,
      tot_fwd_pkts: 0.0000,
      tot_bwd_pkts: 0.0000,
      totlen_fwd_pkts: 0.0000,
      fwd_pkt_len_max: 0.0000,
      fwd_pkt_len_min: 0.0000,
      fwd_pkt_len_mean: 0.0000,
      fwd_pkt_len_std: 0.0000,
      bwd_pkt_len_max: 0.0000,
      bwd_pkt_len_min: 0.0000,
      bwd_pkt_len_mean: 0.0000,
      bwd_pkt_len_std: 0.0000,
      flow_byts_s: 0.0000,
      flow_pkts_s: 0.5000,
      flow_iat_mean: 0.0000,
      flow_iat_std: 0.0000,
      flow_iat_max: 0.0000,
      fwd_iat_std: 0.0000,
      bwd_iat_tot: 0.0000,
      bwd_iat_mean: 0.0000,
      bwd_iat_std: 0.0000,
      bwd_iat_max: 0.0000,
      bwd_iat_min: 0.0000,
      fwd_psh_flags: 0.0000,
      bwd_psh_flags: 0.0000,
      fwd_urg_flags: 0.0000,
      bwd_urg_flags: 0.0000,
      fwd_pkts_s: 0.2500,
      bwd_pkts_s: 0.5000,
      pkt_len_min: 0.0000,
      pkt_len_max: 0.0000,
      pkt_len_mean: 0.0000,
      pkt_len_std: 0.0000,
      pkt_len_var: 0.0000,
      fin_flag_cnt: 0.0000,
      rst_flag_cnt: 0.0000,
      psh_flag_cnt: 1.0000,
      ack_flag_cnt: 0.0000,
      urg_flag_cnt: 0.0000,
      cwe_flag_count: 0.0000,
      down_up_ratio: 0.0119,
      fwd_byts_b_avg: 0.0000,
      fwd_pkts_b_avg: 0.0000,
      fwd_blk_rate_avg: 0.0000,
      bwd_byts_b_avg: 0.0000,
      bwd_pkts_b_avg: 0.0000,
      bwd_blk_rate_avg: 0.0000,
      init_fwd_win_byts: 0.4102,
      init_bwd_win_byts: 0.0000,
      fwd_act_data_pkts: 0.0000,
      fwd_seg_size_min: 0.8333,
      active_mean: 0.0000,
      active_std: 0.0000,
      active_max: 0.0000,
      active_min: 0.0000,
      idle_mean: 0.0000,
      idle_std: 0.0000
    }
  },
  benign: {
    name: "Trafico Web Normal",
    description: "Trafico de navegacion web legitimo",
    data: {
      dst_port: 0.7967,
      protocol: 0.3529,
      timestamp: 0.9500,
      flow_duration: 0.0000,
      tot_fwd_pkts: 0.0000,
      tot_bwd_pkts: 0.0000,
      totlen_fwd_pkts: 0.0000,
      fwd_pkt_len_max: 0.0000,
      fwd_pkt_len_min: 0.0000,
      fwd_pkt_len_mean: 0.0000,
      fwd_pkt_len_std: 0.0000,
      bwd_pkt_len_max: 0.0000,
      bwd_pkt_len_min: 0.0000,
      bwd_pkt_len_mean: 0.0000,
      bwd_pkt_len_std: 0.0000,
      flow_byts_s: 0.0000,
      flow_pkts_s: 0.0385,
      flow_iat_mean: 0.0000,
      flow_iat_std: 0.0000,
      flow_iat_max: 0.0000,
      fwd_iat_std: 0.0000,
      bwd_iat_tot: 0.0000,
      bwd_iat_mean: 0.0000,
      bwd_iat_std: 0.0000,
      bwd_iat_max: 0.0000,
      bwd_iat_min: 0.0000,
      fwd_psh_flags: 0.0000,
      bwd_psh_flags: 0.0000,
      fwd_urg_flags: 0.0000,
      bwd_urg_flags: 0.0000,
      fwd_pkts_s: 0.0192,
      bwd_pkts_s: 0.0385,
      pkt_len_min: 0.0000,
      pkt_len_max: 0.0000,
      pkt_len_mean: 0.0000,
      pkt_len_std: 0.0000,
      pkt_len_var: 0.0000,
      fin_flag_cnt: 0.0000,
      rst_flag_cnt: 0.0000,
      psh_flag_cnt: 0.0000,
      ack_flag_cnt: 1.0000,
      urg_flag_cnt: 1.0000,
      cwe_flag_count: 0.0000,
      down_up_ratio: 0.0119,
      fwd_byts_b_avg: 0.0000,
      fwd_pkts_b_avg: 0.0000,
      fwd_blk_rate_avg: 0.0000,
      bwd_byts_b_avg: 0.0000,
      bwd_pkts_b_avg: 0.0000,
      bwd_blk_rate_avg: 0.0000,
      init_fwd_win_byts: 0.2372,
      init_bwd_win_byts: 0.9695,
      fwd_act_data_pkts: 0.0000,
      fwd_seg_size_min: 0.4167,
      active_mean: 0.0000,
      active_std: 0.0000,
      active_max: 0.0000,
      active_min: 0.0000,
      idle_mean: 0.0000,
      idle_std: 0.0000
    }
  },
  ftpBruteForce: {
    name: "Ataque de Fuerza Bruta FTP",
    description: "Patron de ataque brute force contra servidor FTP (puerto 21)",
    data: {
      dst_port: 0.0003,
      protocol: 0.3529,
      timestamp: 0.1200,
      flow_duration: 0.0001,
      tot_fwd_pkts: 0.0010,
      tot_bwd_pkts: 0.0010,
      totlen_fwd_pkts: 0.0005,
      fwd_pkt_len_max: 0.0010,
      fwd_pkt_len_min: 0.0000,
      fwd_pkt_len_mean: 0.0005,
      fwd_pkt_len_std: 0.0000,
      bwd_pkt_len_max: 0.0010,
      bwd_pkt_len_min: 0.0000,
      bwd_pkt_len_mean: 0.0005,
      bwd_pkt_len_std: 0.0000,
      flow_byts_s: 0.0100,
      flow_pkts_s: 0.7000,
      flow_iat_mean: 0.0001,
      flow_iat_std: 0.0000,
      flow_iat_max: 0.0001,
      fwd_iat_std: 0.0000,
      bwd_iat_tot: 0.0001,
      bwd_iat_mean: 0.0001,
      bwd_iat_std: 0.0000,
      bwd_iat_max: 0.0001,
      bwd_iat_min: 0.0000,
      fwd_psh_flags: 0.0000,
      bwd_psh_flags: 0.0000,
      fwd_urg_flags: 0.0000,
      bwd_urg_flags: 0.0000,
      fwd_pkts_s: 0.6500,
      bwd_pkts_s: 0.7500,
      pkt_len_min: 0.0000,
      pkt_len_max: 0.0010,
      pkt_len_mean: 0.0005,
      pkt_len_std: 0.0000,
      pkt_len_var: 0.0000,
      fin_flag_cnt: 0.0000,
      rst_flag_cnt: 0.4000,
      psh_flag_cnt: 0.8500,
      ack_flag_cnt: 0.2000,
      urg_flag_cnt: 0.0000,
      cwe_flag_count: 0.0000,
      down_up_ratio: 0.0150,
      fwd_byts_b_avg: 0.0000,
      fwd_pkts_b_avg: 0.0000,
      fwd_blk_rate_avg: 0.0000,
      bwd_byts_b_avg: 0.0000,
      bwd_pkts_b_avg: 0.0000,
      bwd_blk_rate_avg: 0.0000,
      init_fwd_win_byts: 0.3500,
      init_bwd_win_byts: 0.0000,
      fwd_act_data_pkts: 0.0010,
      fwd_seg_size_min: 0.7500,
      active_mean: 0.0000,
      active_std: 0.0000,
      active_max: 0.0000,
      active_min: 0.0000,
      idle_mean: 0.0000,
      idle_std: 0.0000
    }
  },
  webBruteForce: {
    name: "Ataque de Fuerza Bruta Web (Login)",
    description: "Patron de ataque brute force contra formulario web de login",
    data: {
      dst_port: 0.0068,
      protocol: 0.3529,
      timestamp: 0.5500,
      flow_duration: 0.0002,
      tot_fwd_pkts: 0.0015,
      tot_bwd_pkts: 0.0012,
      totlen_fwd_pkts: 0.0020,
      fwd_pkt_len_max: 0.0050,
      fwd_pkt_len_min: 0.0000,
      fwd_pkt_len_mean: 0.0025,
      fwd_pkt_len_std: 0.0010,
      bwd_pkt_len_max: 0.0030,
      bwd_pkt_len_min: 0.0000,
      bwd_pkt_len_mean: 0.0015,
      bwd_pkt_len_std: 0.0005,
      flow_byts_s: 0.0200,
      flow_pkts_s: 0.6000,
      flow_iat_mean: 0.0002,
      flow_iat_std: 0.0001,
      flow_iat_max: 0.0003,
      fwd_iat_std: 0.0001,
      bwd_iat_tot: 0.0002,
      bwd_iat_mean: 0.0001,
      bwd_iat_std: 0.0000,
      bwd_iat_max: 0.0002,
      bwd_iat_min: 0.0000,
      fwd_psh_flags: 0.5000,
      bwd_psh_flags: 0.0000,
      fwd_urg_flags: 0.0000,
      bwd_urg_flags: 0.0000,
      fwd_pkts_s: 0.5500,
      bwd_pkts_s: 0.6000,
      pkt_len_min: 0.0000,
      pkt_len_max: 0.0050,
      pkt_len_mean: 0.0020,
      pkt_len_std: 0.0010,
      pkt_len_var: 0.0001,
      fin_flag_cnt: 0.1000,
      rst_flag_cnt: 0.3000,
      psh_flag_cnt: 0.7500,
      ack_flag_cnt: 0.5000,
      urg_flag_cnt: 0.0000,
      cwe_flag_count: 0.0000,
      down_up_ratio: 0.0200,
      fwd_byts_b_avg: 0.0000,
      fwd_pkts_b_avg: 0.0000,
      fwd_blk_rate_avg: 0.0000,
      bwd_byts_b_avg: 0.0000,
      bwd_pkts_b_avg: 0.0000,
      bwd_blk_rate_avg: 0.0000,
      init_fwd_win_byts: 0.4000,
      init_bwd_win_byts: 0.3000,
      fwd_act_data_pkts: 0.0015,
      fwd_seg_size_min: 0.6000,
      active_mean: 0.0001,
      active_std: 0.0000,
      active_max: 0.0001,
      active_min: 0.0000,
      idle_mean: 0.0000,
      idle_std: 0.0000
    }
  }
};

/**
 * Feature descriptions for user understanding
 */
export const FEATURE_DESCRIPTIONS = {
  dst_port: "Puerto de destino (normalizado 0-1)",
  protocol: "Protocolo de red (normalizado 0-1)",
  timestamp: "Marca de tiempo (normalizado 0-1)",
  flow_duration: "Duración del flujo (normalizado 0-1)",
  flow_pkts_s: "Paquetes por segundo (normalizado 0-1)",
  bwd_pkts_s: "Paquetes backward por segundo (normalizado 0-1) - KEY FEATURE",
  psh_flag_cnt: "Contador de flags PSH (normalizado 0-1) - KEY FEATURE",
  urg_flag_cnt: "Contador de flags URG (normalizado 0-1) - KEY FEATURE",
  // ... (60 features total)
};

export const fuerzaBrutaService = {
  /**
   * Predict if network flow is a brute force attack
   * @param {Object} flowData - Network flow data (60 normalized features)
   * @returns {Promise<Object>} Prediction result
   */
  async predict(flowData) {
    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(flowData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw {
          type: 'api',
          message: `API request failed: ${response.status} ${response.statusText}`,
          details: errorData
        };
      }

      const apiResponse = await response.json();

      // Transform API response to match frontend expectations
      return {
        success: true,
        data: {
          prediction: apiResponse.prediction,
          prediction_label: apiResponse.prediction_label,
          confidence: apiResponse.confidence,
          probability_normal: apiResponse.probabilities.Benign,
          probability_bruteforce: apiResponse.probabilities['Brute Force'],
          explanation: apiResponse.explanation,  // Pass through explanation from API
          metadata: {
            model: apiResponse.model_name,
            features_count: 60,
            timestamp: new Date().toISOString(),
            processing_time_ms: apiResponse.processing_time_ms
          },
          // Add brute force specific info
          is_brute_force: apiResponse.prediction === 1,
          threat_level: apiResponse.prediction === 1 ?
            (apiResponse.confidence > 0.9 ? 'Severo' :
             apiResponse.confidence > 0.7 ? 'Alto' :
             apiResponse.confidence > 0.5 ? 'Moderado' : 'Bajo') : 'Minimo',
          attack_type: apiResponse.prediction === 1 ? 'Fuerza Bruta Basada en Red' : null,
          recommendations: apiResponse.prediction === 1 ? [
            'Analizar tráfico de red en detalle',
            'Verificar logs del sistema objetivo',
            'Implementar rate limiting',
            'Configurar firewall para bloquear IPs sospechosas',
            'Habilitar detección de intrusos (IDS/IPS)'
          ] : null
        },
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Brute Force API Error:', error);
      return {
        success: false,
        error: {
          type: error.type || 'network',
          message: error.message || 'No se pudo conectar a la API de Deteccion de Fuerza Bruta',
          details: error.details || error
        }
      };
    }
  },

  /**
   * Batch prediction for multiple network flows
   * @param {Array<Object>} flows - Array of network flow data
   * @returns {Promise<Object>} Batch prediction results
   */
  async predictBatch(flows) {
    try {
      const response = await fetch(`${API_BASE_URL}/predict/batch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ flows }),
      });

      if (!response.ok) {
        throw new Error(`Batch prediction failed: ${response.statusText}`);
      }

      const data = await response.json();
      return {
        success: true,
        data
      };
    } catch (error) {
      console.error('Batch prediction error:', error);
      return { success: false, error };
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
        throw new Error('Failed to fetch model info');
      }

      const data = await response.json();

      return {
        success: true,
        data: {
          model_name: data.model_name,
          version: data.model_version,
          status: 'active',
          description: 'Modelo Random Forest entrenado con el dataset CSE-CIC-IDS2018',
          training_date: data.training_date,
          metrics: {
            f1_score: data.metrics.f1_score,
            accuracy: data.metrics.accuracy,
            precision: data.metrics.precision,
            recall: data.metrics.recall,
            roc_auc: data.metrics.roc_auc
          },
          features: {
            total: data.features.total,
            feature_names: data.features.feature_names
          },
          training_data: {
            total_samples: data.training_data.total_samples,
            train_samples: data.training_data.train_samples,
            test_samples: data.training_data.test_samples,
            balance: data.training_data.balance
          },
          attack_types: [
            'FTP Brute Force',
            'SSH Brute Force',
            'Web Brute Force',
            'XSS Brute Force'
          ]
        }
      };
    } catch (error) {
      console.error('Model info error:', error);
      return {
        success: false,
        error: {
          type: 'api',
          message: 'Failed to get model info',
          details: error
        }
      };
    }
  },

  /**
   * Health check for Brute Force API
   * @returns {Promise<Object>} Health status
   */
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/`);

      if (!response.ok) {
        throw new Error('Health check failed');
      }

      const data = await response.json();

      return {
        success: true,
        data: {
          status: data.status,
          model: data.model,
          version: data.version,
          message: data.message
        }
      };
    } catch (error) {
      return {
        success: false,
        error: {
          type: 'network',
          message: 'La API de Fuerza Bruta no esta disponible',
          details: error
        }
      };
    }
  },

  /**
   * Get example flows for testing
   * @returns {Object} Example flows
   */
  getExamples() {
    return EXAMPLE_FLOWS;
  }
};

export default fuerzaBrutaService;
