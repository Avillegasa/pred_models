/**
 * MonthlySummaryCards Component
 * Summary cards showing key metrics
 */
import React from 'react';
import { Row, Col, Card } from 'react-bootstrap';
import { FaChartLine, FaExclamationTriangle, FaCheckCircle, FaPercentage } from 'react-icons/fa';
import { theme } from '../../styles/theme';

function MonthlySummaryCards({ summary }) {
  const {
    total_predictions,
    threats_detected,
    benign_count,
    threat_rate_percent,
    avg_confidence,
  } = summary;

  const cards = [
    {
      title: 'Predicciones Analizadas',
      value: total_predictions.toLocaleString(),
      icon: FaChartLine,
      color: theme.primary.medium,
      bg: theme.info.bg,
    },
    {
      title: 'Amenazas Detectadas',
      value: threats_detected.toLocaleString(),
      subtitle: `${threat_rate_percent.toFixed(1)}% del total`,
      icon: FaExclamationTriangle,
      color: theme.danger.main,
      bg: theme.danger.bg,
    },
    {
      title: 'Trafico Legitimo',
      value: benign_count.toLocaleString(),
      subtitle: `${(100 - threat_rate_percent).toFixed(1)}% del total`,
      icon: FaCheckCircle,
      color: theme.success.main,
      bg: theme.success.bg,
    },
    {
      title: 'Confianza Promedio',
      value: `${avg_confidence.toFixed(1)}%`,
      icon: FaPercentage,
      color: theme.warning.main,
      bg: theme.warning.bg,
    },
  ];

  return (
    <Row className="g-3 mb-4">
      {cards.map((card, idx) => (
        <Col key={idx} xs={12} sm={6} lg={3}>
          <Card className="h-100 summary-card" style={{ borderLeft: `4px solid ${card.color}` }}>
            <Card.Body className="d-flex align-items-center gap-3">
              <div
                className="icon-wrapper"
                style={{ background: card.bg }}
              >
                <card.icon size={24} color={card.color} />
              </div>
              <div>
                <div className="card-value" style={{ color: card.color }}>
                  {card.value}
                </div>
                <div className="card-title">{card.title}</div>
                {card.subtitle && (
                  <div className="card-subtitle">{card.subtitle}</div>
                )}
              </div>
            </Card.Body>
          </Card>
        </Col>
      ))}

      <style>{`
        .summary-card {
          border: 1px solid var(--border-default);
          transition: transform 0.2s, box-shadow 0.2s;
        }
        .summary-card:hover {
          transform: translateY(-2px);
          box-shadow: var(--shadow-md);
        }
        .icon-wrapper {
          width: 48px;
          height: 48px;
          border-radius: var(--radius-md);
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
        }
        .card-value {
          font-size: 1.5rem;
          font-weight: 700;
          line-height: 1.2;
        }
        .card-title {
          font-size: 0.875rem;
          color: var(--text-secondary);
          font-weight: 500;
        }
        .card-subtitle {
          font-size: 0.75rem;
          color: var(--text-muted);
        }
      `}</style>
    </Row>
  );
}

export default MonthlySummaryCards;
