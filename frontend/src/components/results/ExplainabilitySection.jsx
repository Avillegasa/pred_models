/**
 * ExplainabilitySection Component
 * Button that opens a modal with detailed prediction explanations
 */
import React, { useState } from 'react';
import { Button, Modal, Badge, ListGroup, ProgressBar, Accordion, Card } from 'react-bootstrap';
import {
  FaQuestionCircle,
  FaExclamationTriangle,
  FaShieldAlt,
  FaNetworkWired,
  FaUserSecret,
  FaCheckCircle,
  FaInfoCircle,
  FaExclamationCircle,
  FaTimesCircle,
  FaGlobe
} from 'react-icons/fa';

/**
 * Severity badge component
 */
const SeverityBadge = ({ severity }) => {
  const config = {
    critical: { bg: 'danger', icon: <FaTimesCircle />, label: 'Critico' },
    high: { bg: 'warning', text: 'dark', icon: <FaExclamationTriangle />, label: 'Alto' },
    medium: { bg: 'info', icon: <FaExclamationCircle />, label: 'Medio' },
    low: { bg: 'secondary', icon: <FaInfoCircle />, label: 'Bajo' }
  };
  const cfg = config[severity] || config.low;
  return (
    <Badge bg={cfg.bg} text={cfg.text} className="ms-2">
      {cfg.icon} {cfg.label}
    </Badge>
  );
};

/**
 * Single indicator card with evidence
 */
const IndicatorCard = ({ indicator, index }) => {
  const { indicator: title, evidence, severity } = indicator;

  return (
    <Accordion.Item eventKey={String(index)}>
      <Accordion.Header>
        <div className="d-flex align-items-center w-100">
          <span className="me-2 text-danger fw-bold">{index + 1}.</span>
          <span className="flex-grow-1">{title}</span>
          {severity && <SeverityBadge severity={severity} />}
        </div>
      </Accordion.Header>
      <Accordion.Body className="bg-light">
        {evidence && evidence.length > 0 ? (
          <ul className="mb-0 ps-3">
            {evidence.map((item, idx) => (
              <li key={idx} className="mb-1">
                <code className="bg-white px-2 py-1 rounded border small">
                  {item}
                </code>
              </li>
            ))}
          </ul>
        ) : (
          <span className="text-muted">Sin evidencia adicional</span>
        )}
      </Accordion.Body>
    </Accordion.Item>
  );
};

/**
 * Phishing explanation content
 */
const PhishingExplanationContent = ({ explanation }) => {
  const { risk_indicators, suspicious_terms, summary, total_indicators } = explanation;

  return (
    <>
      {/* Summary */}
      <div className="alert alert-secondary mb-4">
        <FaInfoCircle className="me-2" />
        {summary}
      </div>

      {/* Risk Indicators */}
      {risk_indicators && risk_indicators.length > 0 && (
        <div className="mb-4">
          <h6 className="d-flex align-items-center gap-2 mb-3">
            <FaExclamationTriangle className="text-warning" />
            Indicadores de Riesgo Detectados ({total_indicators || risk_indicators.length})
          </h6>
          <Accordion defaultActiveKey="0">
            {risk_indicators.map((indicator, idx) => (
              <IndicatorCard key={idx} indicator={indicator} index={idx} />
            ))}
          </Accordion>
        </div>
      )}

      {/* Suspicious Terms */}
      {suspicious_terms && suspicious_terms.length > 0 && (
        <div className="mb-3">
          <h6 className="d-flex align-items-center gap-2 mb-3">
            <FaShieldAlt className="text-danger" />
            Terminos Sospechosos Encontrados
          </h6>
          <div className="d-flex flex-wrap gap-2">
            {suspicious_terms.map((term, idx) => (
              <Badge key={idx} bg="warning" text="dark" className="px-2 py-2">
                "{term}"
              </Badge>
            ))}
          </div>
        </div>
      )}

      {/* No indicators message */}
      {(!risk_indicators || risk_indicators.length === 0) && (
        <div className="text-center text-muted py-4">
          <FaCheckCircle size={48} className="text-success mb-3" />
          <p>No se detectaron indicadores de riesgo especificos</p>
        </div>
      )}
    </>
  );
};

/**
 * Account Takeover explanation content
 */
const ATOExplanationContent = ({ explanation }) => {
  const { risk_indicators, risk_factors, key_features, geo_info, summary, total_indicators } = explanation;

  return (
    <>
      {/* Summary */}
      <div className="alert alert-secondary mb-4">
        <FaInfoCircle className="me-2" />
        {summary}
      </div>

      {/* Geographic & Temporal Info */}
      {(geo_info || key_features) && (
        <Card className="mb-4 border-0 bg-light">
          <Card.Body className="py-2">
            {geo_info && (
              <div className="d-flex align-items-center gap-2 small mb-2">
                <FaGlobe className="text-primary" />
                <span><strong>Ubicacion:</strong> {geo_info.city}, {geo_info.region}, {geo_info.country}</span>
                <span className="ms-3"><strong>ASN:</strong> {geo_info.asn}</span>
              </div>
            )}
            {key_features && (
              <div className="d-flex flex-wrap gap-2 small">
                {key_features.is_night !== undefined && (
                  <Badge bg={key_features.is_night ? "warning" : "secondary"} text={key_features.is_night ? "dark" : "light"}>
                    {key_features.is_night ? "🌙 Horario Nocturno" : "☀️ Horario Diurno"}
                  </Badge>
                )}
                {key_features.is_weekend !== undefined && (
                  <Badge bg={key_features.is_weekend ? "info" : "secondary"}>
                    {key_features.is_weekend ? "📅 Fin de Semana" : "💼 Dia Laboral"}
                  </Badge>
                )}
                {key_features.is_attack_ip && (
                  <Badge bg="danger">⚠️ IP de Ataque</Badge>
                )}
              </div>
            )}
          </Card.Body>
        </Card>
      )}

      {/* Risk Indicators */}
      {risk_indicators && risk_indicators.length > 0 && (
        <div className="mb-4">
          <h6 className="d-flex align-items-center gap-2 mb-3">
            <FaUserSecret className="text-danger" />
            Cambios de Comportamiento Detectados ({total_indicators || risk_indicators.length})
          </h6>
          <Accordion defaultActiveKey="0">
            {risk_indicators.map((indicator, idx) => (
              <IndicatorCard key={idx} indicator={indicator} index={idx} />
            ))}
          </Accordion>
        </div>
      )}

      {/* Risk Factors Progress */}
      {risk_factors && Object.keys(risk_factors).length > 0 && (
        <div className="mb-4">
          <h6 className="mb-3">Contribucion al Riesgo</h6>
          {Object.entries(risk_factors)
            .sort((a, b) => b[1] - a[1])
            .map(([factor, weight]) => (
              <div key={factor} className="mb-2">
                <div className="d-flex justify-content-between mb-1 small">
                  <span>{factor.replace(/_/g, ' ')}</span>
                  <span className="text-danger fw-bold">{(weight * 100).toFixed(0)}%</span>
                </div>
                <ProgressBar
                  now={weight * 100}
                  variant={weight > 0.2 ? 'danger' : weight > 0.1 ? 'warning' : 'info'}
                  style={{ height: '8px' }}
                />
              </div>
            ))}
        </div>
      )}

      {/* No indicators message */}
      {(!risk_indicators || risk_indicators.length === 0) && (
        <div className="text-center text-muted py-4">
          <FaCheckCircle size={48} className="text-success mb-3" />
          <p>No se detectaron cambios de comportamiento sospechosos</p>
        </div>
      )}
    </>
  );
};

/**
 * Brute Force explanation content
 */
const BruteForceExplanationContent = ({ explanation }) => {
  const { risk_indicators, top_features, summary, total_indicators } = explanation;

  return (
    <>
      {/* Summary */}
      <div className="alert alert-secondary mb-4">
        <FaInfoCircle className="me-2" />
        {summary}
      </div>

      {/* Risk Indicators */}
      {risk_indicators && risk_indicators.length > 0 && (
        <div className="mb-4">
          <h6 className="d-flex align-items-center gap-2 mb-3">
            <FaNetworkWired className="text-danger" />
            Anomalias de Red Detectadas ({total_indicators || risk_indicators.length})
          </h6>
          <Accordion defaultActiveKey="0">
            {risk_indicators.map((indicator, idx) => (
              <IndicatorCard key={idx} indicator={indicator} index={idx} />
            ))}
          </Accordion>
        </div>
      )}

      {/* Top Features */}
      {top_features && Object.keys(top_features).length > 0 && (
        <div className="mb-3">
          <h6 className="mb-3">Features de Red (Valores Normalizados 0-1)</h6>
          <div className="bg-dark text-light p-3 rounded">
            {Object.entries(top_features).map(([feature, value]) => (
              <div key={feature} className="d-flex justify-content-between mb-2 font-monospace small">
                <span>{feature}</span>
                <span className={value > 0.5 ? 'text-danger' : value > 0.2 ? 'text-warning' : 'text-success'}>
                  {value.toFixed(4)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No indicators message */}
      {(!risk_indicators || risk_indicators.length === 0) && (
        <div className="text-center text-muted py-4">
          <FaCheckCircle size={48} className="text-success mb-3" />
          <p>Patrones de red dentro de parametros normales</p>
        </div>
      )}
    </>
  );
};

/**
 * Main ExplainabilitySection component
 * Shows a button that opens a modal with detailed explanations
 */
const ExplainabilitySection = ({ explanation, modelType, isThreat, buttonVariant = "outline-primary", buttonSize = "sm" }) => {
  const [showModal, setShowModal] = useState(false);

  if (!explanation) {
    return null;
  }

  const handleOpen = () => setShowModal(true);
  const handleClose = () => setShowModal(false);

  const getModelSpecificContent = () => {
    switch (modelType) {
      case 'phishing':
        return <PhishingExplanationContent explanation={explanation} />;
      case 'ato':
      case 'ataques_sospechosos':
        return <ATOExplanationContent explanation={explanation} />;
      case 'brute_force':
      case 'fuerza_bruta':
        return <BruteForceExplanationContent explanation={explanation} />;
      default:
        return explanation.summary ? (
          <div className="alert alert-secondary">{explanation.summary}</div>
        ) : null;
    }
  };

  const getModelTitle = () => {
    switch (modelType) {
      case 'phishing':
        return 'Analisis de Phishing';
      case 'ato':
      case 'ataques_sospechosos':
        return 'Analisis de Account Takeover';
      case 'brute_force':
      case 'fuerza_bruta':
        return 'Analisis de Brute Force';
      default:
        return 'Analisis de Prediccion';
    }
  };

  const indicatorCount = explanation.total_indicators ||
    explanation.risk_indicators?.length ||
    0;

  return (
    <>
      {/* Trigger Button */}
      <Button
        variant={buttonVariant}
        size={buttonSize}
        onClick={handleOpen}
        className="d-flex align-items-center gap-2"
      >
        <FaQuestionCircle />
        <span>Por que esta prediccion?</span>
        {indicatorCount > 0 && (
          <Badge bg={isThreat ? "danger" : "secondary"} pill>
            {indicatorCount}
          </Badge>
        )}
      </Button>

      {/* Explanation Modal */}
      <Modal show={showModal} onHide={handleClose} size="lg" centered scrollable>
        <Modal.Header
          closeButton
          className={isThreat ? "bg-danger bg-opacity-10" : "bg-success bg-opacity-10"}
        >
          <Modal.Title className="d-flex align-items-center gap-2">
            <FaQuestionCircle className={isThreat ? "text-danger" : "text-success"} />
            {getModelTitle()}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body style={{ maxHeight: '70vh', overflowY: 'auto' }}>
          {getModelSpecificContent()}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Cerrar
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default ExplainabilitySection;
