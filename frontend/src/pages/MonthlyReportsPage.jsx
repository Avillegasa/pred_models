/**
 * MonthlyReportsPage Component
 * Main page for monthly reports with charts and PDF generation
 */
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Row, Col, Card, Alert, Spinner } from 'react-bootstrap';
import { FaChartBar, FaExclamationTriangle, FaShieldAlt } from 'react-icons/fa';
import MainLayout from '../components/layout/MainLayout';
import MonthSelector from '../components/reports/MonthSelector';
import MonthlySummaryCards from '../components/reports/MonthlySummaryCards';
import TopThreatsTable from '../components/reports/TopThreatsTable';
import BenignInsights from '../components/reports/BenignInsights';
import PDFGenerator from '../components/reports/PDFGenerator';
import ThreatDistributionChart from '../components/charts/ThreatDistributionChart';
import ModelComparisonChart from '../components/charts/ModelComparisonChart';
import DailyTrendChart from '../components/charts/DailyTrendChart';
import ConfidenceHistogram from '../components/charts/ConfidenceHistogram';
import SeverityChart from '../components/charts/SeverityChart';
import monthlyReportService from '../services/monthlyReportService';

function MonthlyReportsPage() {
  const [report, setReport] = useState(null);
  const [availableMonths, setAvailableMonths] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const chartsRef = useRef(null);

  // Current date for initial selection
  const now = new Date();
  const [selectedYear, setSelectedYear] = useState(now.getFullYear());
  const [selectedMonth, setSelectedMonth] = useState(now.getMonth() + 1);

  // Load available months on mount
  useEffect(() => {
    const loadAvailableMonths = async () => {
      try {
        const data = await monthlyReportService.getAvailableMonths();
        setAvailableMonths(data.months || []);

        // If there are available months, select the most recent one
        if (data.months && data.months.length > 0) {
          setSelectedYear(data.months[0].year);
          setSelectedMonth(data.months[0].month);
        }
      } catch (err) {
        console.error('Error loading available months:', err);
      }
    };

    loadAvailableMonths();
  }, []);

  // Load report when selection changes
  const loadReport = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await monthlyReportService.getMonthlyReport(selectedYear, selectedMonth);
      setReport(data);
    } catch (err) {
      console.error('Error loading report:', err);
      setError(err.response?.data?.detail || 'Error al cargar el reporte');
      setReport(null);
    } finally {
      setLoading(false);
    }
  }, [selectedYear, selectedMonth]);

  useEffect(() => {
    loadReport();
  }, [loadReport]);

  const handleMonthChange = (year, month) => {
    setSelectedYear(year);
    setSelectedMonth(month);
  };

  const hasData = report && report.summary.total_predictions > 0;

  return (
    <MainLayout title="Reportes Mensuales">
      {/* Header with selector and PDF button */}
      <div className="d-flex flex-wrap justify-content-between align-items-start gap-3 mb-4">
        <MonthSelector
          year={selectedYear}
          month={selectedMonth}
          availableMonths={availableMonths}
          onChange={handleMonthChange}
          loading={loading}
        />
        {report && <PDFGenerator report={report} chartsRef={chartsRef} />}
      </div>

      {/* Loading state */}
      {loading && (
        <div className="text-center py-5">
          <Spinner animation="border" variant="primary" />
          <p className="mt-3 text-muted">Cargando reporte...</p>
        </div>
      )}

      {/* Error state */}
      {error && !loading && (
        <Alert variant="danger">
          <FaExclamationTriangle className="me-2" />
          {error}
        </Alert>
      )}

      {/* No data state */}
      {!loading && !error && !hasData && (
        <Card className="text-center py-5">
          <Card.Body>
            <FaChartBar size={48} className="text-muted mb-3" />
            <h5>No hay datos disponibles</h5>
            <p className="text-muted">
              No se encontraron predicciones para {report?.month_name} {report?.year}.
              <br />
              Seleccione otro mes o realice predicciones para generar datos.
            </p>
          </Card.Body>
        </Card>
      )}

      {/* Report content */}
      {!loading && !error && hasData && (
        <>
          {/* Summary Cards */}
          <MonthlySummaryCards summary={report.summary} />

          {/* Charts Section - wrapped in ref for PDF capture */}
          <div ref={chartsRef}>
            <Row className="g-4 mb-4">
              {/* Threat Distribution Pie */}
              <Col xs={12} lg={4}>
                <Card className="h-100">
                  <Card.Header className="bg-white">
                    <h6 className="mb-0">
                      <FaShieldAlt className="me-2 text-primary" />
                      Distribucion de Resultados
                    </h6>
                  </Card.Header>
                  <Card.Body>
                    <ThreatDistributionChart
                      threats={report.summary.threats_detected}
                      benign={report.summary.benign_count}
                    />
                  </Card.Body>
                </Card>
              </Col>

              {/* Model Comparison Bar */}
              <Col xs={12} lg={8}>
                <Card className="h-100">
                  <Card.Header className="bg-white">
                    <h6 className="mb-0">Desglose por Modelo</h6>
                  </Card.Header>
                  <Card.Body>
                    <ModelComparisonChart byModel={report.by_model} />
                  </Card.Body>
                </Card>
              </Col>
            </Row>

            <Row className="g-4 mb-4">
              {/* Daily Trend Line */}
              <Col xs={12}>
                <Card>
                  <Card.Header className="bg-white">
                    <h6 className="mb-0">Tendencia Diaria - {report.month_name} {report.year}</h6>
                  </Card.Header>
                  <Card.Body>
                    <DailyTrendChart dailyTrend={report.daily_trend} />
                  </Card.Body>
                </Card>
              </Col>
            </Row>

            <Row className="g-4 mb-4">
              {/* Confidence Histogram */}
              <Col xs={12} md={6}>
                <Card className="h-100">
                  <Card.Header className="bg-white">
                    <h6 className="mb-0">Distribucion de Confianza</h6>
                  </Card.Header>
                  <Card.Body>
                    <ConfidenceHistogram distribution={report.confidence_distribution} />
                  </Card.Body>
                </Card>
              </Col>

              {/* Severity Chart */}
              <Col xs={12} md={6}>
                <Card className="h-100">
                  <Card.Header className="bg-white">
                    <h6 className="mb-0">Alertas por Severidad</h6>
                  </Card.Header>
                  <Card.Body>
                    <SeverityChart alertStats={report.alerts} />
                  </Card.Body>
                </Card>
              </Col>
            </Row>
          </div>

          {/* Top Threats Table */}
          <Card className="mb-4">
            <Card.Header className="bg-white">
              <h6 className="mb-0">
                <FaExclamationTriangle className="me-2 text-danger" />
                Top 10 Amenazas Detectadas
              </h6>
            </Card.Header>
            <Card.Body className="p-0">
              <TopThreatsTable threats={report.top_threats} />
            </Card.Body>
          </Card>

          {/* Benign Insights */}
          <Card>
            <Card.Header className="bg-white">
              <h6 className="mb-0">
                <FaShieldAlt className="me-2 text-success" />
                Analisis de Trafico Legitimo
              </h6>
            </Card.Header>
            <Card.Body>
              <BenignInsights insights={report.benign_insights} />
            </Card.Body>
          </Card>
        </>
      )}
    </MainLayout>
  );
}

export default MonthlyReportsPage;
