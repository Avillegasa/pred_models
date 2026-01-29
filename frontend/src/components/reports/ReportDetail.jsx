/**
 * ReportDetail Component
 * Detailed view of a report with results
 */
import React, { useState } from 'react';
import { Modal, Table, Badge, ProgressBar, Row, Col, Card, Spinner, Button } from 'react-bootstrap';
import { FaShieldAlt, FaCheckCircle, FaExclamationTriangle, FaQuestionCircle } from 'react-icons/fa';
import ExplainabilitySection from '../results/ExplainabilitySection';

function ReportDetail({ show, onHide, report, loading }) {
  const [selectedExplanation, setSelectedExplanation] = useState(null);
  const [showExplanationModal, setShowExplanationModal] = useState(false);
  const getModelBadge = (modelType) => {
    const badges = {
      phishing: <Badge bg="info" className="fs-6">Phishing Detection</Badge>,
      ato: <Badge bg="warning" text="dark" className="fs-6">Account Takeover</Badge>,
      brute_force: <Badge bg="danger" className="fs-6">Brute Force</Badge>
    };
    return badges[modelType] || <Badge bg="secondary" className="fs-6">Unknown</Badge>;
  };

  const getThreatPercentage = () => {
    if (!report?.total_records) return 0;
    return ((report.threats_detected / report.total_records) * 100).toFixed(1);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleShowExplanation = (result, idx) => {
    setSelectedExplanation({ ...result, index: idx, modelType: report?.model_type });
    setShowExplanationModal(true);
  };

  const handleCloseExplanation = () => {
    setShowExplanationModal(false);
    setSelectedExplanation(null);
  };

  // Check if any result has explanation
  const hasExplanations = report?.results?.some(r => r.explanation);

  return (
    <Modal show={show} onHide={onHide} size="xl" centered>
      <Modal.Header closeButton>
        <Modal.Title>
          Reporte: {report?.title || 'Cargando...'}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {loading ? (
          <div className="text-center py-5">
            <Spinner animation="border" variant="primary" />
            <p className="mt-2 text-muted">Cargando detalles del reporte...</p>
          </div>
        ) : report ? (
          <>
            {/* Summary Cards */}
            <Row className="mb-4">
              <Col md={3}>
                <Card className="text-center h-100 border-0 shadow-sm">
                  <Card.Body>
                    <FaShieldAlt size={32} className="text-primary mb-2" />
                    <h3 className="mb-0">{report.total_records?.toLocaleString()}</h3>
                    <small className="text-muted">Total Registros</small>
                  </Card.Body>
                </Card>
              </Col>
              <Col md={3}>
                <Card className="text-center h-100 border-0 shadow-sm bg-danger bg-opacity-10">
                  <Card.Body>
                    <FaExclamationTriangle size={32} className="text-danger mb-2" />
                    <h3 className="mb-0 text-danger">{report.threats_detected?.toLocaleString()}</h3>
                    <small className="text-muted">Amenazas Detectadas</small>
                  </Card.Body>
                </Card>
              </Col>
              <Col md={3}>
                <Card className="text-center h-100 border-0 shadow-sm bg-success bg-opacity-10">
                  <Card.Body>
                    <FaCheckCircle size={32} className="text-success mb-2" />
                    <h3 className="mb-0 text-success">{report.benign_count?.toLocaleString()}</h3>
                    <small className="text-muted">Benignos</small>
                  </Card.Body>
                </Card>
              </Col>
              <Col md={3}>
                <Card className="text-center h-100 border-0 shadow-sm">
                  <Card.Body>
                    <div className="fw-bold text-primary mb-2" style={{ fontSize: '2rem' }}>
                      {report.avg_confidence?.toFixed(1)}%
                    </div>
                    <small className="text-muted">Confianza Promedio</small>
                  </Card.Body>
                </Card>
              </Col>
            </Row>

            {/* Report Info */}
            <Card className="mb-4 border-0 shadow-sm">
              <Card.Body>
                <Row>
                  <Col md={6}>
                    <p><strong>Modelo:</strong> {getModelBadge(report.model_type)}</p>
                    <p><strong>Archivo:</strong> {report.file_name || 'N/A'}</p>
                    <p><strong>Creado por:</strong> {report.created_by_name}</p>
                  </Col>
                  <Col md={6}>
                    <p><strong>Fecha:</strong> {formatDate(report.created_at)}</p>
                    <p><strong>Estado:</strong> <Badge bg="success">{report.status}</Badge></p>
                    <p>
                      <strong>Tasa de amenazas:</strong>{' '}
                      <span className={getThreatPercentage() > 50 ? 'text-danger fw-bold' : ''}>
                        {getThreatPercentage()}%
                      </span>
                    </p>
                  </Col>
                </Row>

                {/* Threat distribution bar */}
                <div className="mt-3">
                  <small className="text-muted">Distribucion de resultados:</small>
                  <ProgressBar className="mt-1" style={{ height: '24px' }}>
                    <ProgressBar
                      variant="danger"
                      now={getThreatPercentage()}
                      label={`${report.threats_detected} amenazas`}
                      key={1}
                    />
                    <ProgressBar
                      variant="success"
                      now={100 - getThreatPercentage()}
                      label={`${report.benign_count} benignos`}
                      key={2}
                    />
                  </ProgressBar>
                </div>
              </Card.Body>
            </Card>

            {/* Results Table */}
            {report.results && Array.isArray(report.results) && report.results.length > 0 && (
              <Card className="border-0 shadow-sm">
                <Card.Header className="bg-white">
                  <strong>Resultados Detallados</strong>
                  <small className="text-muted ms-2">
                    (Mostrando {Math.min(report.results.length, 100)} de {report.results.length})
                  </small>
                </Card.Header>
                <Card.Body className="p-0">
                  <div style={{ maxHeight: '400px', overflow: 'auto' }}>
                    <Table striped hover size="sm" className="mb-0">
                      <thead className="sticky-top bg-light">
                        <tr>
                          <th>#</th>
                          <th>Resultado</th>
                          <th>Etiqueta</th>
                          <th>Confianza</th>
                          {report.model_type === 'phishing' && <th>Nivel de Riesgo</th>}
                          {report.model_type === 'brute_force' && <th>Tipo de Ataque</th>}
                          {hasExplanations && <th>Explicacion</th>}
                        </tr>
                      </thead>
                      <tbody>
                        {report.results.slice(0, 100).map((result, idx) => (
                          <tr key={idx}>
                            <td>{idx + 1}</td>
                            <td>
                              {result.is_threat ? (
                                <Badge bg="danger">Amenaza</Badge>
                              ) : (
                                <Badge bg="success">Benigno</Badge>
                              )}
                            </td>
                            <td>{result.label}</td>
                            <td>
                              <ProgressBar
                                now={result.confidence}
                                variant={result.is_threat ? 'danger' : 'success'}
                                style={{ height: '6px', minWidth: '80px' }}
                              />
                              <small>{result.confidence?.toFixed(1)}%</small>
                            </td>
                            {report.model_type === 'phishing' && (
                              <td>
                                <Badge
                                  bg={
                                    result.risk_level === 'high' ? 'danger' :
                                    result.risk_level === 'medium' ? 'warning' : 'secondary'
                                  }
                                >
                                  {result.risk_level}
                                </Badge>
                              </td>
                            )}
                            {report.model_type === 'brute_force' && (
                              <td>{result.attack_type || '-'}</td>
                            )}
                            {hasExplanations && (
                              <td>
                                {result.explanation ? (
                                  <Button
                                    variant="link"
                                    size="sm"
                                    className="p-0 text-primary"
                                    onClick={() => handleShowExplanation(result, idx)}
                                    title="Ver explicacion"
                                  >
                                    <FaQuestionCircle />
                                  </Button>
                                ) : (
                                  <span className="text-muted">-</span>
                                )}
                              </td>
                            )}
                          </tr>
                        ))}
                      </tbody>
                    </Table>
                  </div>
                </Card.Body>
              </Card>
            )}
          </>
        ) : (
          <p className="text-muted text-center">No hay datos disponibles</p>
        )}
      </Modal.Body>

      {/* Explanation Detail Modal */}
      <Modal
        show={showExplanationModal}
        onHide={handleCloseExplanation}
        centered
        size="lg"
      >
        <Modal.Header closeButton>
          <Modal.Title className="d-flex align-items-center gap-2">
            <FaQuestionCircle className={selectedExplanation?.is_threat ? 'text-danger' : 'text-success'} />
            Explicacion del Registro #{selectedExplanation?.index + 1}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedExplanation && (
            <>
              <div className="mb-3">
                <Badge bg={selectedExplanation.is_threat ? 'danger' : 'success'} className="me-2">
                  {selectedExplanation.is_threat ? 'Amenaza' : 'Benigno'}
                </Badge>
                <span className="text-muted">
                  Confianza: <strong>{selectedExplanation.confidence?.toFixed(1)}%</strong>
                </span>
              </div>
              <ExplainabilitySection
                explanation={selectedExplanation.explanation}
                modelType={selectedExplanation.modelType}
                isThreat={selectedExplanation.is_threat}
              />
            </>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseExplanation}>
            Cerrar
          </Button>
        </Modal.Footer>
      </Modal>
    </Modal>
  );
}

export default ReportDetail;
