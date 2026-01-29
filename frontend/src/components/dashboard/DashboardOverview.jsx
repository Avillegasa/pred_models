/**
 * DashboardOverview Component
 * Main dashboard view with statistics, charts, and recent activity
 */

import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Badge, Spinner, ProgressBar } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import {
  FaShieldAlt,
  FaExclamationTriangle,
  FaCheckCircle,
  FaChartPie,
  FaFileAlt,
  FaBrain,
  FaEnvelope,
  FaUserShield,
  FaNetworkWired
} from 'react-icons/fa';
import reportService from '../../services/reportService';
import { useAuth } from '../../context/AuthContext';

const DashboardOverview = () => {
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin';
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalPredictions: 0,
    threatsDetected: 0,
    benignCount: 0,
    avgConfidence: 0,
    byModel: {
      phishing: { total: 0, threats: 0 },
      ato: { total: 0, threats: 0 },
      brute_force: { total: 0, threats: 0 }
    }
  });
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const data = await reportService.listReports();
      setReports(data);
      calculateStats(data);
    } catch (err) {
      console.error('Error loading reports:', err);
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (reportsList) => {
    let totalPredictions = 0;
    let threatsDetected = 0;
    let benignCount = 0;
    let totalConfidence = 0;
    let confidenceCount = 0;
    const byModel = {
      phishing: { total: 0, threats: 0 },
      ato: { total: 0, threats: 0 },
      brute_force: { total: 0, threats: 0 }
    };

    reportsList.forEach(report => {
      totalPredictions += report.total_records || 0;
      threatsDetected += report.threats_detected || 0;
      benignCount += report.benign_count || 0;

      if (report.avg_confidence) {
        totalConfidence += report.avg_confidence;
        confidenceCount++;
      }

      const modelType = report.model_type?.toLowerCase() || 'unknown';
      if (byModel[modelType]) {
        byModel[modelType].total += report.total_records || 0;
        byModel[modelType].threats += report.threats_detected || 0;
      }
    });

    setStats({
      totalPredictions,
      threatsDetected,
      benignCount,
      avgConfidence: confidenceCount > 0 ? (totalConfidence / confidenceCount).toFixed(1) : 0,
      byModel
    });
  };

  const getModelIcon = (modelType) => {
    switch (modelType?.toLowerCase()) {
      case 'phishing': return <FaEnvelope />;
      case 'ato': return <FaUserShield />;
      case 'brute_force': return <FaNetworkWired />;
      default: return <FaBrain />;
    }
  };

  const getModelLabel = (modelType) => {
    switch (modelType?.toLowerCase()) {
      case 'phishing': return 'Phishing Detection';
      case 'ato': return 'Account Takeover';
      case 'brute_force': return 'Brute Force';
      default: return modelType;
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <Container fluid className="dashboard-container">
        <div className="text-center py-5">
          <Spinner animation="border" style={{ color: 'var(--interactive-primary)' }} />
          <p className="mt-3" style={{ color: 'var(--text-secondary)' }}>Cargando estadisticas...</p>
        </div>
      </Container>
    );
  }

  const threatRate = stats.totalPredictions > 0
    ? ((stats.threatsDetected / stats.totalPredictions) * 100).toFixed(1)
    : 0;

  return (
    <Container fluid className="dashboard-container">
      <div className="dashboard-content">
        {/* Stats Cards */}
        <Row className="g-4 mb-4">
          <Col xs={12} sm={6} lg={3}>
            <Card className="h-100 stat-card" style={{
              background: 'var(--surface-base)',
              border: '1px solid var(--border-subtle)',
              borderLeft: '4px solid var(--interactive-primary)'
            }}>
              <Card.Body>
                <div className="d-flex justify-content-between align-items-start">
                  <div>
                    <p className="mb-1" style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                      Total Predicciones
                    </p>
                    <h2 className="mb-0" style={{ color: 'var(--text-primary)', fontWeight: 700 }}>
                      {stats.totalPredictions.toLocaleString()}
                    </h2>
                  </div>
                  <div style={{
                    background: 'var(--bg-accent)',
                    padding: '0.75rem',
                    borderRadius: 'var(--radius-md)'
                  }}>
                    <FaChartPie size={24} style={{ color: 'var(--interactive-primary)' }} />
                  </div>
                </div>
              </Card.Body>
            </Card>
          </Col>

          <Col xs={12} sm={6} lg={3}>
            <Card className="h-100 stat-card" style={{
              background: 'var(--surface-base)',
              border: '1px solid var(--border-subtle)',
              borderLeft: '4px solid var(--status-danger)'
            }}>
              <Card.Body>
                <div className="d-flex justify-content-between align-items-start">
                  <div>
                    <p className="mb-1" style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                      Amenazas Detectadas
                    </p>
                    <h2 className="mb-0" style={{ color: 'var(--status-danger)', fontWeight: 700 }}>
                      {stats.threatsDetected.toLocaleString()}
                    </h2>
                    <small style={{ color: 'var(--text-muted)' }}>{threatRate}% del total</small>
                  </div>
                  <div style={{
                    background: 'var(--status-danger-bg)',
                    padding: '0.75rem',
                    borderRadius: 'var(--radius-md)'
                  }}>
                    <FaExclamationTriangle size={24} style={{ color: 'var(--status-danger)' }} />
                  </div>
                </div>
              </Card.Body>
            </Card>
          </Col>

          <Col xs={12} sm={6} lg={3}>
            <Card className="h-100 stat-card" style={{
              background: 'var(--surface-base)',
              border: '1px solid var(--border-subtle)',
              borderLeft: '4px solid var(--status-success)'
            }}>
              <Card.Body>
                <div className="d-flex justify-content-between align-items-start">
                  <div>
                    <p className="mb-1" style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                      Trafico Legitimo
                    </p>
                    <h2 className="mb-0" style={{ color: 'var(--status-success)', fontWeight: 700 }}>
                      {stats.benignCount.toLocaleString()}
                    </h2>
                  </div>
                  <div style={{
                    background: 'var(--status-success-bg)',
                    padding: '0.75rem',
                    borderRadius: 'var(--radius-md)'
                  }}>
                    <FaCheckCircle size={24} style={{ color: 'var(--status-success)' }} />
                  </div>
                </div>
              </Card.Body>
            </Card>
          </Col>

          <Col xs={12} sm={6} lg={3}>
            <Card className="h-100 stat-card" style={{
              background: 'var(--surface-base)',
              border: '1px solid var(--border-subtle)',
              borderLeft: '4px solid var(--status-info)'
            }}>
              <Card.Body>
                <div className="d-flex justify-content-between align-items-start">
                  <div>
                    <p className="mb-1" style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                      Confianza Promedio
                    </p>
                    <h2 className="mb-0" style={{ color: 'var(--text-primary)', fontWeight: 700 }}>
                      {stats.avgConfidence}%
                    </h2>
                  </div>
                  <div style={{
                    background: 'var(--status-info-bg)',
                    padding: '0.75rem',
                    borderRadius: 'var(--radius-md)'
                  }}>
                    <FaShieldAlt size={24} style={{ color: 'var(--status-info)' }} />
                  </div>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        {/* Model Distribution & Quick Actions */}
        <Row className="g-4 mb-4">
          <Col xs={12} lg={8}>
            <Card style={{
              background: 'var(--surface-base)',
              border: '1px solid var(--border-subtle)'
            }}>
              <Card.Header style={{
                background: 'var(--surface-raised)',
                borderBottom: '1px solid var(--border-subtle)'
              }}>
                <h5 className="mb-0" style={{ color: 'var(--text-primary)' }}>
                  <FaChartPie className="me-2" style={{ color: 'var(--text-accent)' }} />
                  Distribucion por Modelo
                </h5>
              </Card.Header>
              <Card.Body>
                {Object.entries(stats.byModel).map(([model, data]) => (
                  <div key={model} className="mb-3">
                    <div className="d-flex justify-content-between align-items-center mb-2">
                      <div className="d-flex align-items-center gap-2">
                        <span style={{ color: 'var(--text-accent)' }}>{getModelIcon(model)}</span>
                        <span style={{ color: 'var(--text-primary)', fontWeight: 500 }}>
                          {getModelLabel(model)}
                        </span>
                      </div>
                      <div className="text-end">
                        <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
                          {data.total.toLocaleString()}
                        </span>
                        <span style={{ color: 'var(--text-muted)', marginLeft: '0.5rem', fontSize: '0.875rem' }}>
                          ({data.threats} amenazas)
                        </span>
                      </div>
                    </div>
                    <ProgressBar
                      style={{ height: '8px', background: 'var(--surface-raised)' }}
                    >
                      <ProgressBar
                        variant="success"
                        now={stats.totalPredictions > 0 ? ((data.total - data.threats) / stats.totalPredictions) * 100 : 0}
                        style={{ background: 'var(--status-success)' }}
                      />
                      <ProgressBar
                        variant="danger"
                        now={stats.totalPredictions > 0 ? (data.threats / stats.totalPredictions) * 100 : 0}
                        style={{ background: 'var(--status-danger)' }}
                      />
                    </ProgressBar>
                  </div>
                ))}

                {stats.totalPredictions === 0 && (
                  <div className="text-center py-4" style={{ color: 'var(--text-muted)' }}>
                    <FaChartPie size={48} className="mb-3" style={{ opacity: 0.3 }} />
                    <p>No hay datos de predicciones aun.</p>
                    {isAdmin && (
                      <button
                        className="btn btn-primary mt-2"
                        onClick={() => navigate('/dashboard/predict')}
                      >
                        Realizar primera prediccion
                      </button>
                    )}
                  </div>
                )}
              </Card.Body>
            </Card>
          </Col>

          <Col xs={12} lg={4}>
            <Card style={{
              background: 'var(--surface-base)',
              border: '1px solid var(--border-subtle)',
              height: '100%'
            }}>
              <Card.Header style={{
                background: 'var(--surface-raised)',
                borderBottom: '1px solid var(--border-subtle)'
              }}>
                <h5 className="mb-0" style={{ color: 'var(--text-primary)' }}>
                  <FaBrain className="me-2" style={{ color: 'var(--text-accent)' }} />
                  Acciones Rapidas
                </h5>
              </Card.Header>
              <Card.Body className="d-flex flex-column gap-3">
                {isAdmin && (
                  <>
                    <button
                      className="btn btn-outline-primary w-100 d-flex align-items-center gap-2"
                      onClick={() => navigate('/dashboard/predict')}
                      style={{ borderColor: 'var(--interactive-primary)', color: 'var(--interactive-primary)' }}
                    >
                      <FaBrain /> Nueva Prediccion Manual
                    </button>
                    <button
                      className="btn btn-outline-secondary w-100 d-flex align-items-center gap-2"
                      onClick={() => navigate('/files')}
                      style={{ borderColor: 'var(--border-default)', color: 'var(--text-secondary)' }}
                    >
                      <FaFileAlt /> Subir Archivo para Analisis
                    </button>
                  </>
                )}
                <button
                  className="btn btn-outline-secondary w-100 d-flex align-items-center gap-2"
                  onClick={() => navigate('/reports')}
                  style={{ borderColor: 'var(--border-default)', color: 'var(--text-secondary)' }}
                >
                  <FaChartPie /> Ver Reportes
                </button>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        {/* Recent Reports */}
        <Row>
          <Col>
            <Card style={{
              background: 'var(--surface-base)',
              border: '1px solid var(--border-subtle)'
            }}>
              <Card.Header style={{
                background: 'var(--surface-raised)',
                borderBottom: '1px solid var(--border-subtle)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <h5 className="mb-0" style={{ color: 'var(--text-primary)' }}>
                  <FaFileAlt className="me-2" style={{ color: 'var(--text-accent)' }} />
                  Reportes Recientes
                </h5>
                <button
                  className="btn btn-sm btn-link"
                  onClick={() => navigate('/reports')}
                  style={{ color: 'var(--text-accent)', textDecoration: 'none' }}
                >
                  Ver todos
                </button>
              </Card.Header>
              <Card.Body className="p-0">
                {reports.length > 0 ? (
                  <div className="table-responsive">
                    <table className="table table-hover mb-0" style={{ color: 'var(--text-primary)' }}>
                      <thead>
                        <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                          <th style={{ color: 'var(--text-secondary)', fontWeight: 500, padding: '1rem' }}>Titulo</th>
                          <th style={{ color: 'var(--text-secondary)', fontWeight: 500, padding: '1rem' }}>Modelo</th>
                          <th style={{ color: 'var(--text-secondary)', fontWeight: 500, padding: '1rem' }}>Registros</th>
                          <th style={{ color: 'var(--text-secondary)', fontWeight: 500, padding: '1rem' }}>Amenazas</th>
                          <th style={{ color: 'var(--text-secondary)', fontWeight: 500, padding: '1rem' }}>Fecha</th>
                        </tr>
                      </thead>
                      <tbody>
                        {reports.slice(0, 5).map((report) => (
                          <tr
                            key={report.id}
                            style={{
                              borderBottom: '1px solid var(--border-subtle)',
                              cursor: 'pointer'
                            }}
                            onClick={() => navigate(`/reports/${report.id}`)}
                          >
                            <td style={{ padding: '1rem' }}>
                              <span style={{ fontWeight: 500 }}>{report.title}</span>
                            </td>
                            <td style={{ padding: '1rem' }}>
                              <Badge
                                bg="none"
                                style={{
                                  background: 'var(--bg-accent)',
                                  color: 'var(--text-accent)',
                                  fontWeight: 500
                                }}
                              >
                                {getModelIcon(report.model_type)} {getModelLabel(report.model_type)}
                              </Badge>
                            </td>
                            <td style={{ padding: '1rem' }}>{report.total_records?.toLocaleString()}</td>
                            <td style={{ padding: '1rem' }}>
                              <Badge bg={report.threats_detected > 0 ? 'danger' : 'success'}>
                                {report.threats_detected}
                              </Badge>
                            </td>
                            <td style={{ padding: '1rem', color: 'var(--text-muted)' }}>
                              {formatDate(report.created_at)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="text-center py-5" style={{ color: 'var(--text-muted)' }}>
                    <FaFileAlt size={48} className="mb-3" style={{ opacity: 0.3 }} />
                    <p>No hay reportes generados aun.</p>
                  </div>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </div>
    </Container>
  );
};

export default DashboardOverview;
