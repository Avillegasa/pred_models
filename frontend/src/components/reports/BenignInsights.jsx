/**
 * BenignInsights Component
 * Explanation of benign/legitimate traffic patterns
 */
import React from 'react';
import { Row, Col, Card, Badge, ListGroup } from 'react-bootstrap';
import { FaCheckCircle, FaShieldAlt, FaEnvelope, FaUserShield, FaNetworkWired } from 'react-icons/fa';
import { theme } from '../../styles/theme';

const MODEL_CONFIG = {
  phishing: {
    label: 'Phishing',
    icon: FaEnvelope,
    description: 'Emails clasificados como legitimos',
  },
  ato: {
    label: 'Account Takeover',
    icon: FaUserShield,
    description: 'Logins clasificados como normales',
  },
  brute_force: {
    label: 'Fuerza Bruta',
    icon: FaNetworkWired,
    description: 'Trafico de red clasificado como legitimo',
  },
};

function BenignInsights({ insights }) {
  const { total_benign, by_model } = insights;

  if (total_benign === 0) {
    return (
      <div className="text-center py-4 text-muted">
        <FaShieldAlt size={32} className="mb-2" />
        <p>No hay datos de trafico legitimo para este periodo</p>
      </div>
    );
  }

  return (
    <div className="benign-insights">
      <div className="insights-header mb-3">
        <FaCheckCircle className="me-2" color={theme.success.main} />
        <span className="fw-bold">{total_benign.toLocaleString()}</span>
        <span className="text-muted ms-2">eventos clasificados como legitimos</span>
      </div>

      <Row className="g-3">
        {Object.entries(by_model).map(([modelType, data]) => {
          const config = MODEL_CONFIG[modelType] || {
            label: modelType,
            icon: FaShieldAlt,
            description: 'Eventos legitimos',
          };
          const IconComponent = config.icon;

          return (
            <Col key={modelType} xs={12} md={4}>
              <Card className="h-100 insight-card">
                <Card.Body>
                  <div className="d-flex align-items-center mb-3">
                    <div className="model-icon me-2">
                      <IconComponent size={18} />
                    </div>
                    <div>
                      <div className="fw-bold">{config.label}</div>
                      <small className="text-muted">{config.description}</small>
                    </div>
                  </div>

                  <div className="stats-row mb-3">
                    <div className="stat">
                      <span className="stat-value">{data.count.toLocaleString()}</span>
                      <span className="stat-label">eventos</span>
                    </div>
                    <div className="stat">
                      <Badge bg="success" className="confidence-badge">
                        {data.avg_confidence.toFixed(1)}%
                      </Badge>
                      <span className="stat-label">confianza</span>
                    </div>
                  </div>

                  {data.common_patterns && data.common_patterns.length > 0 && (
                    <div className="patterns">
                      <small className="text-muted d-block mb-2">Patrones comunes:</small>
                      <ListGroup variant="flush" className="pattern-list">
                        {data.common_patterns.map((pattern, idx) => (
                          <ListGroup.Item key={idx} className="pattern-item">
                            <FaCheckCircle size={10} className="me-2 text-success" />
                            {pattern}
                          </ListGroup.Item>
                        ))}
                      </ListGroup>
                    </div>
                  )}
                </Card.Body>
              </Card>
            </Col>
          );
        })}
      </Row>

      <style>{`
        .insights-header {
          display: flex;
          align-items: center;
          font-size: 1rem;
        }
        .insight-card {
          border: 1px solid var(--border-default);
          border-top: 3px solid var(--status-success-base);
        }
        .model-icon {
          width: 36px;
          height: 36px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: var(--status-success-bg);
          color: var(--status-success-base);
          border-radius: var(--radius-md);
        }
        .stats-row {
          display: flex;
          gap: 1.5rem;
        }
        .stat {
          display: flex;
          flex-direction: column;
          align-items: flex-start;
        }
        .stat-value {
          font-size: 1.25rem;
          font-weight: 700;
          color: var(--text-primary);
        }
        .stat-label {
          font-size: 0.75rem;
          color: var(--text-muted);
        }
        .confidence-badge {
          font-size: 0.875rem;
          padding: 0.25rem 0.5rem;
        }
        .pattern-list {
          font-size: 0.8rem;
        }
        .pattern-item {
          padding: 0.35rem 0;
          border: none;
          background: transparent;
          color: var(--text-secondary);
        }
      `}</style>
    </div>
  );
}

export default BenignInsights;
