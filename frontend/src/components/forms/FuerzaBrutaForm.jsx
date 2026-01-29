/**
 * Fuerza Bruta Form Component
 * Form for brute force attack detection using network traffic features
 *
 * NOTE: This model analyzes 60 network traffic features (normalized 0-1)
 * from the CSE-CIC-IDS2018 dataset to detect brute force attacks.
 */

import React, { useState, useEffect } from 'react';
import { Button, Alert, Card, Badge, Row, Col } from 'react-bootstrap';
import { FiShield, FiAlertTriangle, FiActivity, FiInfo, FiPlay, FiRefreshCw } from 'react-icons/fi';
import { useDashboard } from '../../context/DashboardContext';
import { fuerzaBrutaService, EXAMPLE_FLOWS } from '../../services/fuerzaBrutaService';

const FuerzaBrutaForm = () => {
  const { isLoading, startPrediction, setPredictionSuccess, setPredictionError, clearPrediction } = useDashboard();
  const [selectedExample, setSelectedExample] = useState(null);
  const [apiStatus, setApiStatus] = useState({ checked: false, online: false });
  const [modelInfo, setModelInfo] = useState(null);

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
  };

  const handlePredict = async () => {
    if (!selectedExample) return;

    startPrediction();

    const flowData = EXAMPLE_FLOWS[selectedExample].data;
    const result = await fuerzaBrutaService.predict(flowData);

    if (result.success) {
      setPredictionSuccess(result.data);
    } else {
      setPredictionError(result.error);
    }
  };

  const handleClear = () => {
    setSelectedExample(null);
    clearPrediction();
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

  return (
    <div className="form-card">
      <h3 className="form-card-title">
        <FiShield className="me-2" />
        Brute Force Attack Detection
        {apiStatus.checked && (
          <Badge
            bg={apiStatus.online ? 'success' : 'danger'}
            className="ms-2"
            style={{ fontSize: '0.6rem' }}
          >
            {apiStatus.online ? 'API ONLINE' : 'API OFFLINE'}
          </Badge>
        )}
      </h3>

      {/* API Status Warning */}
      {apiStatus.checked && !apiStatus.online && (
        <Alert variant="warning" className="mb-3">
          <FiAlertTriangle className="me-2" />
          API no disponible. Asegúrate de que esté corriendo en <code>localhost:8002</code>
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
          Este modelo analiza <strong>60 características de tráfico de red</strong> (normalizadas 0-1)
          para detectar ataques de fuerza bruta (SSH, FTP, Web, XSS).
          Selecciona un ejemplo para probar.
        </small>
      </Alert>

      {/* Example Selection */}
      <div className="mb-4">
        <label className="form-label fw-bold">Selecciona un ejemplo de tráfico:</label>
        <Row className="g-3">
          {/* Brute Force Example */}
          <Col md={6}>
            <Card
              className={`h-100 cursor-pointer ${selectedExample === 'bruteForce' ? 'border-danger border-2' : ''}`}
              onClick={() => handleExampleSelect('bruteForce')}
              style={{ cursor: 'pointer' }}
            >
              <Card.Body>
                <Card.Title className="text-danger">
                  <FiAlertTriangle className="me-2" />
                  {EXAMPLE_FLOWS.bruteForce.name}
                </Card.Title>
                <Card.Text>
                  <small className="text-muted">{EXAMPLE_FLOWS.bruteForce.description}</small>
                </Card.Text>
                <div className="mt-2">
                  <small><strong>Key Features:</strong></small>
                  {getKeyFeatures(EXAMPLE_FLOWS.bruteForce.data).slice(0, 3).map((f, i) => (
                    <div key={i} className="d-flex justify-content-between">
                      <small className="text-muted">{f.name}:</small>
                      <small><code>{f.value.toFixed(4)}</code></small>
                    </div>
                  ))}
                </div>
                {selectedExample === 'bruteForce' && (
                  <Badge bg="danger" className="mt-2">Seleccionado</Badge>
                )}
              </Card.Body>
            </Card>
          </Col>

          {/* Benign Example */}
          <Col md={6}>
            <Card
              className={`h-100 cursor-pointer ${selectedExample === 'benign' ? 'border-success border-2' : ''}`}
              onClick={() => handleExampleSelect('benign')}
              style={{ cursor: 'pointer' }}
            >
              <Card.Body>
                <Card.Title className="text-success">
                  <FiActivity className="me-2" />
                  {EXAMPLE_FLOWS.benign.name}
                </Card.Title>
                <Card.Text>
                  <small className="text-muted">{EXAMPLE_FLOWS.benign.description}</small>
                </Card.Text>
                <div className="mt-2">
                  <small><strong>Key Features:</strong></small>
                  {getKeyFeatures(EXAMPLE_FLOWS.benign.data).slice(0, 3).map((f, i) => (
                    <div key={i} className="d-flex justify-content-between">
                      <small className="text-muted">{f.name}:</small>
                      <small><code>{f.value.toFixed(4)}</code></small>
                    </div>
                  ))}
                </div>
                {selectedExample === 'benign' && (
                  <Badge bg="success" className="mt-2">Seleccionado</Badge>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </div>

      {/* Selected Flow Details */}
      {selectedExample && (
        <Alert variant="light" className="mb-3">
          <strong>Flujo seleccionado:</strong> {EXAMPLE_FLOWS[selectedExample].name}
          <br />
          <small className="text-muted">60 features de tráfico de red serán enviadas a la API</small>
        </Alert>
      )}

      {/* Action Buttons */}
      <div className="d-flex gap-2">
        <Button
          variant="primary"
          className="form-submit-btn flex-grow-1"
          onClick={handlePredict}
          disabled={isLoading || !selectedExample || !apiStatus.online}
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
          title="Verificar conexión con API"
        >
          <FiRefreshCw />
        </Button>
      </div>
    </div>
  );
};

export default FuerzaBrutaForm;
