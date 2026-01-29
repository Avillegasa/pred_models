/**
 * AlertDetail Component
 * Modal showing alert details with explainability
 */
import React, { useState, useEffect } from 'react';
import { Modal, Button, Badge, Row, Col, Spinner, Accordion } from 'react-bootstrap';
import { FaCheck, FaExclamationTriangle, FaShieldAlt, FaUserSecret, FaClock, FaUser, FaCode } from 'react-icons/fa';
import { useAlerts } from '../../context/AlertContext';
import ExplainabilitySection from '../results/ExplainabilitySection';

function AlertDetail({ show, onHide, alertId, onAcknowledge }) {
  const { getAlert } = useAlerts();
  const [alert, setAlert] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (show && alertId) {
      setLoading(true);
      getAlert(alertId)
        .then(data => setAlert(data))
        .catch(err => console.error('Error loading alert:', err))
        .finally(() => setLoading(false));
    }
  }, [show, alertId, getAlert]);

  const getSeverityBadge = (severity) => {
    const badges = {
      critical: <Badge bg="danger" className="fs-6"><FaExclamationTriangle className="me-1" />Critico</Badge>,
      high: <Badge bg="warning" text="dark" className="fs-6">Alto</Badge>,
      medium: <Badge bg="info" className="fs-6">Medio</Badge>
    };
    return badges[severity] || <Badge bg="secondary">{severity}</Badge>;
  };

  const getStatusBadge = (status) => {
    const badges = {
      unread: <Badge bg="primary">No Leido</Badge>,
      read: <Badge bg="secondary">Leido</Badge>,
      acknowledged: <Badge bg="success">Reconocido</Badge>
    };
    return badges[status] || <Badge bg="secondary">{status}</Badge>;
  };

  const getModelInfo = (modelType) => {
    const info = {
      phishing: { icon: <FaShieldAlt className="text-info" />, label: 'Phishing Detection' },
      ato: { icon: <FaUserSecret className="text-warning" />, label: 'Account Takeover Detection' },
      brute_force: { icon: <FaExclamationTriangle className="text-danger" />, label: 'Brute Force Detection' }
    };
    return info[modelType] || { icon: <FaShieldAlt />, label: modelType };
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  if (loading) {
    return (
      <Modal show={show} onHide={onHide} centered>
        <Modal.Body className="text-center py-5">
          <Spinner animation="border" variant="primary" />
          <p className="mt-2 text-muted">Cargando detalles...</p>
        </Modal.Body>
      </Modal>
    );
  }

  if (!alert) return null;

  const modelInfo = getModelInfo(alert.model_type);

  return (
    <Modal show={show} onHide={onHide} size="lg" centered>
      <Modal.Header closeButton className="border-0 pb-0">
        <Modal.Title className="d-flex align-items-center gap-2">
          {getSeverityBadge(alert.severity)}
          {getStatusBadge(alert.status)}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <h5 className="mb-3">{alert.title}</h5>

        <Row className="mb-4">
          <Col md={6}>
            <div className="mb-3">
              <small className="text-muted d-block">Modelo</small>
              <div className="d-flex align-items-center gap-2 mt-1">
                {modelInfo.icon}
                <span className="fw-semibold">{modelInfo.label}</span>
              </div>
            </div>
          </Col>
          <Col md={6}>
            <div className="mb-3">
              <small className="text-muted d-block">Confianza</small>
              <div className="mt-1">
                <span className={`h4 ${alert.confidence >= 90 ? 'text-danger' : alert.confidence >= 80 ? 'text-warning' : 'text-info'}`}>
                  {alert.confidence?.toFixed(1)}%
                </span>
              </div>
            </div>
          </Col>
        </Row>

        {alert.description && (
          <div className="mb-4">
            <small className="text-muted d-block mb-1">Descripcion</small>
            <p className="mb-0 bg-light p-3 rounded" style={{ whiteSpace: 'pre-wrap' }}>
              {alert.description}
            </p>
          </div>
        )}

        {alert.prediction_label && (
          <div className="mb-4">
            <small className="text-muted d-block mb-1">Etiqueta de Prediccion</small>
            <p className="mb-0 fw-semibold">{alert.prediction_label}</p>
          </div>
        )}

        <Row className="mb-4">
          <Col md={6}>
            <div className="d-flex align-items-center gap-2 text-muted">
              <FaClock />
              <small>Creado: {formatDate(alert.created_at)}</small>
            </div>
          </Col>
          {alert.report_title && (
            <Col md={6}>
              <div className="d-flex align-items-center gap-2 text-muted">
                <small>Reporte: {alert.report_title}</small>
              </div>
            </Col>
          )}
        </Row>

        {alert.status === 'acknowledged' && (
          <div className="bg-success bg-opacity-10 p-3 rounded">
            <div className="d-flex align-items-center gap-2 text-success">
              <FaCheck />
              <span className="fw-semibold">Reconocido</span>
            </div>
            <small className="text-muted d-block mt-1">
              <FaUser className="me-1" />
              {alert.acknowledger_name || 'Usuario'} - {formatDate(alert.acknowledged_at)}
            </small>
          </div>
        )}

        {/* Explainability Section */}
        {alert.raw_data?.explanation && (
          <ExplainabilitySection
            explanation={alert.raw_data.explanation}
            modelType={alert.model_type}
            isThreat={true}
          />
        )}

        {/* Raw Data (collapsible) */}
        {alert.raw_data && (
          <div className="mt-4">
            <Accordion>
              <Accordion.Item eventKey="0">
                <Accordion.Header>
                  <FaCode className="me-2" />
                  <small>Datos Tecnicos de Prediccion (JSON)</small>
                </Accordion.Header>
                <Accordion.Body className="p-0">
                  <pre className="bg-dark text-light p-3 rounded-0 small mb-0" style={{ maxHeight: '200px', overflow: 'auto' }}>
                    {JSON.stringify(alert.raw_data, null, 2)}
                  </pre>
                </Accordion.Body>
              </Accordion.Item>
            </Accordion>
          </div>
        )}
      </Modal.Body>
      <Modal.Footer className="border-0">
        <Button variant="secondary" onClick={onHide}>
          Cerrar
        </Button>
        {alert.status !== 'acknowledged' && (
          <Button
            variant="success"
            onClick={() => {
              onAcknowledge(alert.id);
              onHide();
            }}
          >
            <FaCheck className="me-1" />
            Reconocer Alerta
          </Button>
        )}
      </Modal.Footer>
    </Modal>
  );
}

export default AlertDetail;
