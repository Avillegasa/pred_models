/**
 * TopThreatsTable Component
 * Table showing top 10 threats by confidence
 */
import React from 'react';
import { Table, Badge } from 'react-bootstrap';
import { FaExclamationCircle } from 'react-icons/fa';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';

dayjs.extend(utc);
dayjs.extend(timezone);

const MODEL_LABELS = {
  phishing: 'Phishing',
  ato: 'Account Takeover',
  brute_force: 'Fuerza Bruta',
};

const MODEL_COLORS = {
  phishing: 'danger',
  ato: 'warning',
  brute_force: 'info',
};

function TopThreatsTable({ threats }) {
  if (!threats || threats.length === 0) {
    return (
      <div className="text-center py-4 text-muted">
        <FaExclamationCircle size={32} className="mb-2" />
        <p>No se detectaron amenazas en este periodo</p>
      </div>
    );
  }

  return (
    <div className="table-responsive">
      <Table hover className="threats-table mb-0">
        <thead>
          <tr>
            <th style={{ width: '50px' }}>#</th>
            <th>Modelo</th>
            <th>Clasificacion</th>
            <th style={{ width: '100px' }}>Confianza</th>
            <th>Fecha</th>
            <th>Resumen</th>
          </tr>
        </thead>
        <tbody>
          {threats.map((threat, idx) => (
            <tr key={threat.id}>
              <td className="text-center fw-bold">{idx + 1}</td>
              <td>
                <Badge bg={MODEL_COLORS[threat.model_type] || 'secondary'}>
                  {MODEL_LABELS[threat.model_type] || threat.model_type}
                </Badge>
              </td>
              <td className="fw-medium">{threat.prediction_label}</td>
              <td>
                <span
                  className={`confidence-badge ${
                    threat.confidence >= 95
                      ? 'critical'
                      : threat.confidence >= 85
                      ? 'high'
                      : 'medium'
                  }`}
                >
                  {threat.confidence.toFixed(1)}%
                </span>
              </td>
              <td className="text-muted">
                {dayjs(threat.created_at).tz('America/La_Paz').format('DD/MM HH:mm')}
              </td>
              <td className="explanation-cell">
                {threat.explanation_summary || '-'}
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      <style>{`
        .threats-table {
          font-size: 0.875rem;
        }
        .threats-table th {
          background: var(--bg-secondary);
          font-weight: 600;
          color: var(--text-secondary);
          border-bottom: 2px solid var(--border-default);
        }
        .threats-table td {
          vertical-align: middle;
        }
        .confidence-badge {
          display: inline-block;
          padding: 0.25rem 0.5rem;
          border-radius: var(--radius-sm);
          font-weight: 600;
          font-size: 0.8rem;
        }
        .confidence-badge.critical {
          background: var(--status-danger-bg);
          color: var(--status-danger-base);
        }
        .confidence-badge.high {
          background: rgba(255, 107, 107, 0.15);
          color: #dc3545;
        }
        .confidence-badge.medium {
          background: var(--status-warning-bg);
          color: var(--status-warning-base);
        }
        .explanation-cell {
          max-width: 250px;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          color: var(--text-muted);
          font-size: 0.8rem;
        }
      `}</style>
    </div>
  );
}

export default TopThreatsTable;
