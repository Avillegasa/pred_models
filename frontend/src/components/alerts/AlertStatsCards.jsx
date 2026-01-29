/**
 * AlertStatsCards Component
 * Display alert statistics in card format
 */
import React from 'react';
import { Row, Col, Card } from 'react-bootstrap';
import { FaBell, FaExclamationTriangle, FaExclamationCircle, FaInfoCircle } from 'react-icons/fa';

function AlertStatsCards({ stats }) {
  if (!stats) return null;

  const cards = [
    {
      title: 'Sin Leer',
      value: stats.unread,
      icon: <FaBell />,
      color: 'primary',
      bgColor: 'rgba(0, 73, 140, 0.1)'
    },
    {
      title: 'Criticas',
      value: stats.by_severity?.critical || 0,
      icon: <FaExclamationTriangle />,
      color: 'danger',
      bgColor: 'rgba(229, 62, 62, 0.1)'
    },
    {
      title: 'Altas',
      value: stats.by_severity?.high || 0,
      icon: <FaExclamationCircle />,
      color: 'warning',
      bgColor: 'rgba(236, 201, 75, 0.1)'
    },
    {
      title: 'Medias',
      value: stats.by_severity?.medium || 0,
      icon: <FaInfoCircle />,
      color: 'info',
      bgColor: 'rgba(49, 151, 149, 0.1)'
    }
  ];

  return (
    <Row className="g-3 mb-4">
      {cards.map((card, index) => (
        <Col key={index} xs={6} lg={3}>
          <Card className="h-100 border-0 shadow-sm">
            <Card.Body className="d-flex align-items-center gap-3">
              <div
                className={`d-flex align-items-center justify-content-center rounded-circle text-${card.color}`}
                style={{
                  width: '48px',
                  height: '48px',
                  background: card.bgColor,
                  fontSize: '1.25rem'
                }}
              >
                {card.icon}
              </div>
              <div>
                <div className="text-muted small">{card.title}</div>
                <div className={`h4 mb-0 text-${card.color}`}>{card.value}</div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      ))}
    </Row>
  );
}

export default AlertStatsCards;
