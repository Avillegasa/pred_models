/**
 * Fuerza Bruta Form Component
 * Form for brute force attack detection using network traffic features
 *
 * NOTE: This model analyzes 60 network traffic features (normalized 0-1)
 * from the CSE-CIC-IDS2018 dataset to detect brute force attacks.
 */

import React, { useState, useEffect } from 'react';
import { Button, Alert, Card, Badge, Row, Col, Modal, Form, Tabs, Tab } from 'react-bootstrap';
import { FiShield, FiAlertTriangle, FiActivity, FiInfo, FiPlay, FiRefreshCw, FiEdit3, FiX } from 'react-icons/fi';
import { useDashboard } from '../../context/DashboardContext';
import { fuerzaBrutaService, EXAMPLE_FLOWS } from '../../services/fuerzaBrutaService';

// Feature groups for organized manual input
const FEATURE_GROUPS = {
  basic: {
    label: 'Basico',
    description: 'Puerto, protocolo y duracion',
    features: ['dst_port', 'protocol', 'timestamp', 'flow_duration']
  },
  packets: {
    label: 'Paquetes',
    description: 'Conteo y tamaño de paquetes',
    features: ['tot_fwd_pkts', 'tot_bwd_pkts', 'totlen_fwd_pkts']
  },
  fwdPacketLen: {
    label: 'Paquetes Fwd',
    description: 'Longitud de paquetes forward',
    features: ['fwd_pkt_len_max', 'fwd_pkt_len_min', 'fwd_pkt_len_mean', 'fwd_pkt_len_std']
  },
  bwdPacketLen: {
    label: 'Paquetes Bwd',
    description: 'Longitud de paquetes backward',
    features: ['bwd_pkt_len_max', 'bwd_pkt_len_min', 'bwd_pkt_len_mean', 'bwd_pkt_len_std']
  },
  flowRate: {
    label: 'Tasa de Flujo',
    description: 'Bytes y paquetes por segundo',
    features: ['flow_byts_s', 'flow_pkts_s', 'fwd_pkts_s', 'bwd_pkts_s']
  },
  flowIat: {
    label: 'IAT Flujo',
    description: 'Tiempo entre llegadas del flujo',
    features: ['flow_iat_mean', 'flow_iat_std', 'flow_iat_max', 'fwd_iat_std']
  },
  bwdIat: {
    label: 'IAT Backward',
    description: 'Tiempo entre llegadas backward',
    features: ['bwd_iat_tot', 'bwd_iat_mean', 'bwd_iat_std', 'bwd_iat_max', 'bwd_iat_min']
  },
  flags: {
    label: 'Flags TCP',
    description: 'Contadores de flags TCP',
    features: ['fwd_psh_flags', 'bwd_psh_flags', 'fwd_urg_flags', 'bwd_urg_flags', 'fin_flag_cnt', 'rst_flag_cnt', 'psh_flag_cnt', 'ack_flag_cnt', 'urg_flag_cnt', 'cwe_flag_count']
  },
  packetLen: {
    label: 'Longitud Pkt',
    description: 'Estadisticas de longitud de paquetes',
    features: ['pkt_len_min', 'pkt_len_max', 'pkt_len_mean', 'pkt_len_std', 'pkt_len_var']
  },
  bulk: {
    label: 'Bulk',
    description: 'Metricas de transferencia bulk',
    features: ['down_up_ratio', 'fwd_byts_b_avg', 'fwd_pkts_b_avg', 'fwd_blk_rate_avg', 'bwd_byts_b_avg', 'bwd_pkts_b_avg', 'bwd_blk_rate_avg']
  },
  window: {
    label: 'Ventana TCP',
    description: 'Tamaño de ventana inicial',
    features: ['init_fwd_win_byts', 'init_bwd_win_byts', 'fwd_act_data_pkts', 'fwd_seg_size_min']
  },
  activity: {
    label: 'Actividad',
    description: 'Tiempos activos e inactivos',
    features: ['active_mean', 'active_std', 'active_max', 'active_min', 'idle_mean', 'idle_std']
  }
};

// Feature labels for display
const FEATURE_LABELS = {
  dst_port: 'Puerto Destino',
  protocol: 'Protocolo',
  timestamp: 'Timestamp',
  flow_duration: 'Duracion Flujo',
  tot_fwd_pkts: 'Total Pkts Fwd',
  tot_bwd_pkts: 'Total Pkts Bwd',
  totlen_fwd_pkts: 'Long Total Fwd',
  fwd_pkt_len_max: 'Fwd Pkt Len Max',
  fwd_pkt_len_min: 'Fwd Pkt Len Min',
  fwd_pkt_len_mean: 'Fwd Pkt Len Mean',
  fwd_pkt_len_std: 'Fwd Pkt Len Std',
  bwd_pkt_len_max: 'Bwd Pkt Len Max',
  bwd_pkt_len_min: 'Bwd Pkt Len Min',
  bwd_pkt_len_mean: 'Bwd Pkt Len Mean',
  bwd_pkt_len_std: 'Bwd Pkt Len Std',
  flow_byts_s: 'Flow Bytes/s',
  flow_pkts_s: 'Flow Pkts/s',
  flow_iat_mean: 'Flow IAT Mean',
  flow_iat_std: 'Flow IAT Std',
  flow_iat_max: 'Flow IAT Max',
  fwd_iat_std: 'Fwd IAT Std',
  bwd_iat_tot: 'Bwd IAT Total',
  bwd_iat_mean: 'Bwd IAT Mean',
  bwd_iat_std: 'Bwd IAT Std',
  bwd_iat_max: 'Bwd IAT Max',
  bwd_iat_min: 'Bwd IAT Min',
  fwd_psh_flags: 'Fwd PSH Flags',
  bwd_psh_flags: 'Bwd PSH Flags',
  fwd_urg_flags: 'Fwd URG Flags',
  bwd_urg_flags: 'Bwd URG Flags',
  fwd_pkts_s: 'Fwd Pkts/s',
  bwd_pkts_s: 'Bwd Pkts/s',
  pkt_len_min: 'Pkt Len Min',
  pkt_len_max: 'Pkt Len Max',
  pkt_len_mean: 'Pkt Len Mean',
  pkt_len_std: 'Pkt Len Std',
  pkt_len_var: 'Pkt Len Var',
  fin_flag_cnt: 'FIN Flag Cnt',
  rst_flag_cnt: 'RST Flag Cnt',
  psh_flag_cnt: 'PSH Flag Cnt',
  ack_flag_cnt: 'ACK Flag Cnt',
  urg_flag_cnt: 'URG Flag Cnt',
  cwe_flag_count: 'CWE Flag Cnt',
  down_up_ratio: 'Down/Up Ratio',
  fwd_byts_b_avg: 'Fwd Bytes Bulk Avg',
  fwd_pkts_b_avg: 'Fwd Pkts Bulk Avg',
  fwd_blk_rate_avg: 'Fwd Bulk Rate Avg',
  bwd_byts_b_avg: 'Bwd Bytes Bulk Avg',
  bwd_pkts_b_avg: 'Bwd Pkts Bulk Avg',
  bwd_blk_rate_avg: 'Bwd Bulk Rate Avg',
  init_fwd_win_byts: 'Init Fwd Win Bytes',
  init_bwd_win_byts: 'Init Bwd Win Bytes',
  fwd_act_data_pkts: 'Fwd Act Data Pkts',
  fwd_seg_size_min: 'Fwd Seg Size Min',
  active_mean: 'Active Mean',
  active_std: 'Active Std',
  active_max: 'Active Max',
  active_min: 'Active Min',
  idle_mean: 'Idle Mean',
  idle_std: 'Idle Std'
};

// Default values (all zeros)
const getDefaultFlowData = () => {
  const data = {};
  Object.values(FEATURE_GROUPS).forEach(group => {
    group.features.forEach(feature => {
      data[feature] = 0;
    });
  });
  return data;
};

const FuerzaBrutaForm = () => {
  const { isLoading, startPrediction, setPredictionSuccess, setPredictionError, clearPrediction } = useDashboard();
  const [selectedExample, setSelectedExample] = useState(null);
  const [apiStatus, setApiStatus] = useState({ checked: false, online: false });
  const [modelInfo, setModelInfo] = useState(null);
  const [showManualModal, setShowManualModal] = useState(false);
  const [manualFlowData, setManualFlowData] = useState(getDefaultFlowData());
  const [customFlowData, setCustomFlowData] = useState(null);

  // Check API status on mount
  useEffect(() => {
    checkApiStatus();
    loadModelInfo();
  }, []);

  const checkApiStatus = async () => {
    const response = await fuerzaBrutaService.healthCheck();
    setApiStatus({ checked: true, online: response.success });
  };

  const loadModelInfo = async () => {
    const response = await fuerzaBrutaService.getModelInfo();
    if (response.success) {
      setModelInfo(response.data);
    }
  };

  const handleExampleSelect = (exampleKey) => {
    setSelectedExample(exampleKey);
    setCustomFlowData(null);
  };

  const handlePredict = async () => {
    let flowData;

    if (customFlowData) {
      flowData = customFlowData;
    } else if (selectedExample) {
      flowData = EXAMPLE_FLOWS[selectedExample].data;
    } else {
      return;
    }

    startPrediction();

    const result = await fuerzaBrutaService.predict(flowData);

    if (result.success) {
      setPredictionSuccess(result.data);
    } else {
      setPredictionError(result.error);
    }
  };

  const handleClear = () => {
    setSelectedExample(null);
    setCustomFlowData(null);
    clearPrediction();
  };

  const handleManualInputChange = (feature, value) => {
    const numValue = parseFloat(value) || 0;
    // Clamp between 0 and 1
    const clampedValue = Math.max(0, Math.min(1, numValue));
    setManualFlowData(prev => ({
      ...prev,
      [feature]: clampedValue
    }));
  };

  const handleManualSubmit = () => {
    setCustomFlowData({ ...manualFlowData });
    setSelectedExample(null);
    setShowManualModal(false);
  };

  const handleLoadExampleToModal = (exampleKey) => {
    setManualFlowData({ ...EXAMPLE_FLOWS[exampleKey].data });
  };

  const handleResetManualForm = () => {
    setManualFlowData(getDefaultFlowData());
  };

  // Key features to display (most discriminant)
  const getKeyFeatures = (data) => {
    return [
      { name: 'Bwd Pkts/s', value: data.bwd_pkts_s, description: 'Backward packets per second' },
      { name: 'Flow Pkts/s', value: data.flow_pkts_s, description: 'Flow packets per second' },
      { name: 'PSH Flag', value: data.psh_flag_cnt, description: 'PSH flag count' },
      { name: 'URG Flag', value: data.urg_flag_cnt, description: 'URG flag count' },
      { name: 'Flow Duration', value: data.flow_duration, description: 'Flow duration' },
      { name: 'Init Bwd Win', value: data.init_bwd_win_byts, description: 'Initial backward window bytes' },
    ];
  };

  // Example cards data
  const exampleCards = [
    { key: 'bruteForce', variant: 'danger', icon: FiAlertTriangle },
    { key: 'ftpBruteForce', variant: 'danger', icon: FiAlertTriangle },
    { key: 'webBruteForce', variant: 'danger', icon: FiAlertTriangle },
    { key: 'benign', variant: 'success', icon: FiActivity },
  ];

  return (
    <div className="form-card">
      <h3 className="form-card-title">
        <FiShield className="me-2" />
        Deteccion de Ataques de Fuerza Bruta
        {apiStatus.checked && (
          <Badge
            bg={apiStatus.online ? 'success' : 'danger'}
            className="ms-2"
            style={{ fontSize: '0.6rem' }}
          >
            {apiStatus.online ? 'API EN LINEA' : 'API DESCONECTADA'}
          </Badge>
        )}
      </h3>

      {/* API Status Warning */}
      {apiStatus.checked && !apiStatus.online && (
        <Alert variant="warning" className="mb-3">
          <FiAlertTriangle className="me-2" />
          API no disponible. Asegurate de que este corriendo en <code>localhost:8002</code>
        </Alert>
      )}

      {/* Model Info */}
      {modelInfo && (
        <Alert variant="info" className="mb-3">
          <small>
            <strong>Modelo:</strong> {modelInfo.model_name} |
            <strong> F1:</strong> {(modelInfo.metrics.f1_score * 100).toFixed(2)}% |
            <strong> Precision:</strong> {(modelInfo.metrics.precision * 100).toFixed(2)}%
          </small>
        </Alert>
      )}

      {/* Info about the model */}
      <Alert variant="secondary" className="mb-3">
        <FiInfo className="me-2" />
        <small>
          Este modelo analiza <strong>60 caracteristicas de trafico de red</strong> (normalizadas 0-1)
          para detectar ataques de fuerza bruta (SSH, FTP, Web, XSS).
          Selecciona un ejemplo o ingresa datos manualmente.
        </small>
      </Alert>

      {/* Manual Input Button */}
      <div className="mb-3">
        <Button
          variant="outline-primary"
          onClick={() => setShowManualModal(true)}
          className="w-100"
        >
          <FiEdit3 className="me-2" />
          Ingreso Manual de Datos (60 campos)
        </Button>
      </div>

      {/* Custom Flow Data Indicator */}
      {customFlowData && (
        <Alert variant="primary" className="mb-3">
          <strong>Datos personalizados cargados</strong>
          <br />
          <small className="text-muted">60 features de trafico de red ingresados manualmente</small>
          <Button
            variant="link"
            size="sm"
            className="p-0 ms-2"
            onClick={() => setCustomFlowData(null)}
          >
            (Limpiar)
          </Button>
        </Alert>
      )}

      {/* Example Selection */}
      <div className="mb-4">
        <label className="form-label fw-bold">O selecciona un ejemplo de trafico:</label>
        <Row className="g-3">
          {exampleCards.map(({ key, variant, icon: Icon }) => (
            <Col md={6} lg={3} key={key}>
              <Card
                className={`h-100 cursor-pointer ${selectedExample === key ? `border-${variant} border-2` : ''}`}
                onClick={() => handleExampleSelect(key)}
                style={{ cursor: 'pointer' }}
              >
                <Card.Body className="p-2">
                  <Card.Title className={`text-${variant} fs-6`}>
                    <Icon className="me-1" />
                    {EXAMPLE_FLOWS[key].name}
                  </Card.Title>
                  <Card.Text>
                    <small className="text-muted" style={{ fontSize: '0.75rem' }}>
                      {EXAMPLE_FLOWS[key].description}
                    </small>
                  </Card.Text>
                  <div className="mt-1">
                    <small style={{ fontSize: '0.7rem' }}><strong>Clave:</strong></small>
                    {getKeyFeatures(EXAMPLE_FLOWS[key].data).slice(0, 2).map((f, i) => (
                      <div key={i} className="d-flex justify-content-between" style={{ fontSize: '0.7rem' }}>
                        <small className="text-muted">{f.name}:</small>
                        <small><code>{f.value.toFixed(4)}</code></small>
                      </div>
                    ))}
                  </div>
                  {selectedExample === key && (
                    <Badge bg={variant} className="mt-2" style={{ fontSize: '0.65rem' }}>Seleccionado</Badge>
                  )}
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </div>

      {/* Selected Flow Details */}
      {selectedExample && !customFlowData && (
        <Alert variant="light" className="mb-3">
          <strong>Flujo seleccionado:</strong> {EXAMPLE_FLOWS[selectedExample].name}
          <br />
          <small className="text-muted">60 features de trafico de red seran enviadas a la API</small>
        </Alert>
      )}

      {/* Action Buttons */}
      <div className="d-flex gap-2">
        <Button
          variant="primary"
          className="form-submit-btn flex-grow-1"
          onClick={handlePredict}
          disabled={isLoading || (!selectedExample && !customFlowData) || !apiStatus.online}
        >
          {isLoading ? (
            <>
              <FiRefreshCw className="me-2 spin" />
              Analizando...
            </>
          ) : (
            <>
              <FiPlay className="me-2" />
              Predecir
            </>
          )}
        </Button>
        <Button
          variant="outline-secondary"
          onClick={handleClear}
          disabled={isLoading}
        >
          Limpiar
        </Button>
        <Button
          variant="outline-info"
          onClick={checkApiStatus}
          disabled={isLoading}
          title="Verificar conexion con API"
        >
          <FiRefreshCw />
        </Button>
      </div>

      {/* Manual Input Modal */}
      <Modal
        show={showManualModal}
        onHide={() => setShowManualModal(false)}
        size="xl"
        centered
        scrollable
      >
        <Modal.Header closeButton style={{ backgroundColor: 'var(--bs-primary)', color: 'white' }}>
          <Modal.Title>
            <FiEdit3 className="me-2" />
            Ingreso Manual de Datos de Trafico de Red
          </Modal.Title>
        </Modal.Header>
        <Modal.Body style={{ maxHeight: '70vh' }}>
          <Alert variant="info" className="mb-3">
            <small>
              Ingresa valores normalizados entre <strong>0</strong> y <strong>1</strong> para cada caracteristica.
              Puedes cargar un ejemplo como base y modificar los valores.
            </small>
          </Alert>

          {/* Quick Load Examples */}
          <div className="mb-3">
            <label className="form-label fw-bold">Cargar ejemplo como base:</label>
            <div className="d-flex gap-2 flex-wrap">
              <Button
                variant="outline-danger"
                size="sm"
                onClick={() => handleLoadExampleToModal('bruteForce')}
              >
                SSH Brute Force
              </Button>
              <Button
                variant="outline-danger"
                size="sm"
                onClick={() => handleLoadExampleToModal('ftpBruteForce')}
              >
                FTP Brute Force
              </Button>
              <Button
                variant="outline-danger"
                size="sm"
                onClick={() => handleLoadExampleToModal('webBruteForce')}
              >
                Web Brute Force
              </Button>
              <Button
                variant="outline-success"
                size="sm"
                onClick={() => handleLoadExampleToModal('benign')}
              >
                Trafico Normal
              </Button>
              <Button
                variant="outline-secondary"
                size="sm"
                onClick={handleResetManualForm}
              >
                <FiX className="me-1" />
                Resetear a Ceros
              </Button>
            </div>
          </div>

          {/* Feature Groups in Tabs */}
          <Tabs defaultActiveKey="basic" className="mb-3" fill>
            {Object.entries(FEATURE_GROUPS).map(([groupKey, group]) => (
              <Tab eventKey={groupKey} title={group.label} key={groupKey}>
                <div className="p-2">
                  <p className="text-muted mb-3">
                    <small>{group.description}</small>
                  </p>
                  <Row>
                    {group.features.map(feature => (
                      <Col md={6} lg={4} xl={3} key={feature} className="mb-2">
                        <Form.Group>
                          <Form.Label style={{ fontSize: '0.75rem' }}>
                            {FEATURE_LABELS[feature] || feature}
                          </Form.Label>
                          <Form.Control
                            type="number"
                            step="0.0001"
                            min="0"
                            max="1"
                            value={manualFlowData[feature]}
                            onChange={(e) => handleManualInputChange(feature, e.target.value)}
                            size="sm"
                            style={{ fontFamily: 'monospace' }}
                          />
                        </Form.Group>
                      </Col>
                    ))}
                  </Row>
                </div>
              </Tab>
            ))}
          </Tabs>

          {/* Preview of Key Values */}
          <Alert variant="secondary" className="mt-3">
            <strong>Vista previa de valores clave:</strong>
            <Row className="mt-2">
              {getKeyFeatures(manualFlowData).map((f, i) => (
                <Col xs={6} md={4} lg={2} key={i}>
                  <small className="text-muted d-block">{f.name}</small>
                  <code>{f.value.toFixed(4)}</code>
                </Col>
              ))}
            </Row>
          </Alert>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowManualModal(false)}>
            Cancelar
          </Button>
          <Button variant="primary" onClick={handleManualSubmit}>
            <FiPlay className="me-2" />
            Usar estos datos
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default FuerzaBrutaForm;
