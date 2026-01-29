/**
 * ReportsList Component
 * Display list of generated reports
 */
import React from 'react';
import { Table, Button, Badge, Spinner, ProgressBar } from 'react-bootstrap';
import { FaEye, FaTrash, FaChartBar } from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';

function ReportsList({ reports, loading, onView, onDelete }) {
  const { isAdmin } = useAuth();

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getModelBadge = (modelType) => {
    const badges = {
      phishing: <Badge bg="info">Phishing</Badge>,
      ato: <Badge bg="warning" text="dark">ATO</Badge>,
      brute_force: <Badge bg="danger">Brute Force</Badge>
    };
    return badges[modelType] || <Badge bg="secondary">Desconocido</Badge>;
  };

  const getStatusBadge = (status) => {
    const badges = {
      completed: <Badge bg="success">Completado</Badge>,
      processing: <Badge bg="warning">Procesando</Badge>,
      failed: <Badge bg="danger">Error</Badge>,
      pending: <Badge bg="secondary">Pendiente</Badge>
    };
    return badges[status] || <Badge bg="secondary">{status}</Badge>;
  };

  const getThreatPercentage = (threats, total) => {
    if (!total) return 0;
    return ((threats / total) * 100).toFixed(1);
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2 text-muted">Cargando reportes...</p>
      </div>
    );
  }

  if (!reports || reports.length === 0) {
    return (
      <div className="text-center py-5 text-muted">
        <FaChartBar size={48} className="mb-3 opacity-50" />
        <p>No hay reportes generados</p>
      </div>
    );
  }

  return (
    <Table responsive hover className="align-middle">
      <thead className="bg-light">
        <tr>
          <th>Titulo</th>
          <th>Modelo</th>
          <th>Resultados</th>
          <th>Confianza</th>
          <th>Estado</th>
          <th>Creado Por</th>
          <th>Fecha</th>
          <th className="text-end">Acciones</th>
        </tr>
      </thead>
      <tbody>
        {reports.map((report) => (
          <tr key={report.id}>
            <td>
              <div className="fw-semibold">{report.title}</div>
              <small className="text-muted">{report.total_records?.toLocaleString()} registros</small>
            </td>
            <td>{getModelBadge(report.model_type)}</td>
            <td>
              <div className="d-flex align-items-center gap-2">
                <div style={{ minWidth: '100px' }}>
                  <ProgressBar style={{ height: '8px' }}>
                    <ProgressBar
                      variant="danger"
                      now={getThreatPercentage(report.threats_detected, report.total_records)}
                      key={1}
                    />
                    <ProgressBar
                      variant="success"
                      now={getThreatPercentage(report.benign_count, report.total_records)}
                      key={2}
                    />
                  </ProgressBar>
                </div>
                <small>
                  <span className="text-danger">{report.threats_detected}</span>
                  {' / '}
                  <span className="text-success">{report.benign_count}</span>
                </small>
              </div>
            </td>
            <td>
              {report.avg_confidence ? `${report.avg_confidence.toFixed(1)}%` : '-'}
            </td>
            <td>{getStatusBadge(report.status)}</td>
            <td>
              <small>{report.created_by_name || 'Sistema'}</small>
            </td>
            <td>
              <small>{formatDate(report.created_at)}</small>
            </td>
            <td className="text-end">
              <Button
                variant="outline-primary"
                size="sm"
                className="me-1"
                onClick={() => onView(report.id)}
                title="Ver detalles"
              >
                <FaEye />
              </Button>
              {isAdmin() && (
                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={() => onDelete(report.id)}
                  title="Eliminar"
                >
                  <FaTrash />
                </Button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}

export default ReportsList;
