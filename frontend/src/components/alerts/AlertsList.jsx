/**
 * AlertsList Component
 * Display list of alerts with selection and actions
 */
import React from 'react';
import { Table, Button, Badge, Spinner, Form } from 'react-bootstrap';
import { FaEye, FaCheck, FaExclamationTriangle, FaShieldAlt, FaBell, FaUserSecret } from 'react-icons/fa';

function AlertsList({ alerts, loading, onView, onAcknowledge, selectedIds, onSelectionChange }) {

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getSeverityBadge = (severity) => {
    const badges = {
      critical: <Badge bg="danger"><FaExclamationTriangle className="me-1" />Critico</Badge>,
      high: <Badge bg="warning" text="dark">Alto</Badge>,
      medium: <Badge bg="info">Medio</Badge>
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

  const getModelIcon = (modelType) => {
    const icons = {
      phishing: <FaShieldAlt className="text-info" title="Phishing" />,
      ato: <FaUserSecret className="text-warning" title="Account Takeover" />,
      brute_force: <FaExclamationTriangle className="text-danger" title="Brute Force" />
    };
    return icons[modelType] || <FaShieldAlt />;
  };

  const getModelLabel = (modelType) => {
    const labels = {
      phishing: 'Phishing',
      ato: 'ATO',
      brute_force: 'Brute Force'
    };
    return labels[modelType] || modelType;
  };

  const handleSelectAll = (e) => {
    if (e.target.checked) {
      onSelectionChange(alerts.map(a => a.id));
    } else {
      onSelectionChange([]);
    }
  };

  const handleSelectOne = (alertId) => {
    if (selectedIds.includes(alertId)) {
      onSelectionChange(selectedIds.filter(id => id !== alertId));
    } else {
      onSelectionChange([...selectedIds, alertId]);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2 text-muted">Cargando alertas...</p>
      </div>
    );
  }

  if (!alerts || alerts.length === 0) {
    return (
      <div className="text-center py-5 text-muted">
        <FaBell size={48} className="mb-3 opacity-50" />
        <p>No hay alertas que mostrar</p>
      </div>
    );
  }

  return (
    <Table responsive hover className="align-middle">
      <thead className="bg-light">
        <tr>
          <th style={{ width: '40px' }}>
            <Form.Check
              type="checkbox"
              onChange={handleSelectAll}
              checked={selectedIds.length === alerts.length && alerts.length > 0}
            />
          </th>
          <th>Severidad</th>
          <th>Alerta</th>
          <th>Modelo</th>
          <th>Confianza</th>
          <th>Estado</th>
          <th>Fecha</th>
          <th className="text-end">Acciones</th>
        </tr>
      </thead>
      <tbody>
        {alerts.map((alert) => (
          <tr
            key={alert.id}
            className={alert.status === 'unread' ? 'table-warning' : ''}
            style={{ cursor: 'pointer' }}
          >
            <td onClick={(e) => e.stopPropagation()}>
              <Form.Check
                type="checkbox"
                checked={selectedIds.includes(alert.id)}
                onChange={() => handleSelectOne(alert.id)}
              />
            </td>
            <td>{getSeverityBadge(alert.severity)}</td>
            <td onClick={() => onView(alert.id)}>
              <div className="fw-semibold">{alert.title}</div>
              <small className="text-muted">{alert.prediction_label}</small>
            </td>
            <td>
              {getModelIcon(alert.model_type)}
              <span className="ms-2">{getModelLabel(alert.model_type)}</span>
            </td>
            <td>
              <span className={`fw-bold ${alert.confidence >= 90 ? 'text-danger' : alert.confidence >= 80 ? 'text-warning' : 'text-info'}`}>
                {alert.confidence?.toFixed(1)}%
              </span>
            </td>
            <td>{getStatusBadge(alert.status)}</td>
            <td>
              <small>{formatDate(alert.created_at)}</small>
            </td>
            <td className="text-end" onClick={(e) => e.stopPropagation()}>
              <Button
                variant="outline-primary"
                size="sm"
                className="me-1"
                onClick={() => onView(alert.id)}
                title="Ver detalles"
              >
                <FaEye />
              </Button>
              {alert.status !== 'acknowledged' && (
                <Button
                  variant="outline-success"
                  size="sm"
                  onClick={() => onAcknowledge(alert.id)}
                  title="Reconocer"
                >
                  <FaCheck />
                </Button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}

export default AlertsList;
