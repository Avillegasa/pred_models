/**
 * MetricsAnalysisSection Component
 * Displays metric comparisons between normal ranges and current values
 * with visual progress bars and anomaly indicators
 */
import React, { useState } from 'react';
import { Card, Badge, ProgressBar, Collapse, Button } from 'react-bootstrap';
import {
  FaChartBar,
  FaExclamationTriangle,
  FaCheckCircle,
  FaChevronDown,
  FaChevronUp,
  FaArrowUp,
  FaArrowDown
} from 'react-icons/fa';

/**
 * Calculate the visual position of a value within or outside a range
 * Returns a percentage (0-100) for the progress bar
 */
const calculatePosition = (value, normalMin, normalMax) => {
  // Handle edge cases
  if (normalMin === normalMax) {
    return value === normalMin ? 50 : (value > normalMin ? 100 : 0);
  }

  // Calculate position as percentage
  const range = normalMax - normalMin;
  const extendedMin = normalMin - range * 0.5;
  const extendedMax = normalMax + range * 0.5;
  const extendedRange = extendedMax - extendedMin;

  const position = ((value - extendedMin) / extendedRange) * 100;
  return Math.max(0, Math.min(100, position));
};

/**
 * Get the color variant based on anomaly status
 */
const getVariant = (isAnomalous, anomalyDirection) => {
  if (!isAnomalous) return 'success';
  return anomalyDirection === 'high' ? 'danger' : 'warning';
};

/**
 * Format a numeric value for display
 */
const formatValue = (value) => {
  if (typeof value !== 'number') return value;
  if (value === 0) return '0';
  if (Math.abs(value) < 0.001) return value.toExponential(2);
  if (Math.abs(value) < 1) return value.toFixed(4);
  if (Math.abs(value) < 100) return value.toFixed(2);
  return value.toFixed(0);
};

/**
 * Single metric card component
 */
const MetricCard = ({ metric }) => {
  const {
    metric_name,
    metric_key,
    normal_range,
    current_value,
    is_anomalous,
    anomaly_direction,
    interpretation
  } = metric;

  const position = calculatePosition(current_value, normal_range.min, normal_range.max);
  const variant = getVariant(is_anomalous, anomaly_direction);

  // Calculate normal range position for visual indicator
  const normalStartPos = calculatePosition(normal_range.min, normal_range.min, normal_range.max);
  const normalEndPos = calculatePosition(normal_range.max, normal_range.min, normal_range.max);

  return (
    <Card className={`mb-3 border-${is_anomalous ? 'danger' : 'success'} border-opacity-50`}>
      <Card.Body className="py-3">
        {/* Header with metric name and status badge */}
        <div className="d-flex justify-content-between align-items-center mb-2">
          <span className="fw-semibold text-dark">{metric_name}</span>
          <Badge
            bg={is_anomalous ? 'danger' : 'success'}
            className="d-flex align-items-center gap-1"
          >
            {is_anomalous ? (
              <>
                <FaExclamationTriangle size={10} />
                ANOMALO
                {anomaly_direction === 'high' && <FaArrowUp size={10} />}
                {anomaly_direction === 'low' && <FaArrowDown size={10} />}
              </>
            ) : (
              <>
                <FaCheckCircle size={10} />
                NORMAL
              </>
            )}
          </Badge>
        </div>

        {/* Range information */}
        <div className="d-flex justify-content-between text-muted small mb-2">
          <span>Rango Normal: {formatValue(normal_range.min)} - {formatValue(normal_range.max)}</span>
          <span className={`fw-bold text-${variant}`}>
            Valor Actual: {formatValue(current_value)}
          </span>
        </div>

        {/* Visual progress bar */}
        <div className="position-relative mb-2">
          {/* Background showing normal range */}
          <div
            className="position-absolute bg-success bg-opacity-25 rounded"
            style={{
              left: '25%',
              right: '25%',
              top: 0,
              bottom: 0,
              zIndex: 0
            }}
          />
          {/* Progress bar showing current value position */}
          <ProgressBar
            now={position}
            variant={variant}
            style={{ height: '12px', backgroundColor: 'var(--bs-gray-200)' }}
            className="position-relative"
          />
          {/* Marker for current value */}
          <div
            className={`position-absolute bg-${variant} rounded-circle border border-2 border-white`}
            style={{
              width: '16px',
              height: '16px',
              left: `calc(${position}% - 8px)`,
              top: '-2px',
              zIndex: 2,
              boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
            }}
          />
        </div>

        {/* Scale labels */}
        <div className="d-flex justify-content-between text-muted" style={{ fontSize: '0.7rem' }}>
          <span>Bajo</span>
          <span className="text-success">Normal</span>
          <span>Alto</span>
        </div>

        {/* Interpretation */}
        <div className={`mt-2 p-2 rounded bg-${is_anomalous ? 'danger' : 'success'} bg-opacity-10`}>
          <small className={`text-${is_anomalous ? 'danger' : 'success'}`}>
            {is_anomalous ? '→ ' : ''}{interpretation}
          </small>
        </div>
      </Card.Body>
    </Card>
  );
};

/**
 * Main MetricsAnalysisSection component
 * Displays all metrics with collapsible functionality
 */
const MetricsAnalysisSection = ({ metrics, modelType, isThreat }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!metrics || metrics.length === 0) {
    return null;
  }

  const anomalousCount = metrics.filter(m => m.is_anomalous).length;
  const normalCount = metrics.length - anomalousCount;

  const getModelLabel = () => {
    switch (modelType) {
      case 'phishing':
        return 'Email';
      case 'ato':
      case 'ataques_sospechosos':
        return 'Login';
      case 'brute_force':
      case 'fuerza_bruta':
        return 'Red';
      default:
        return '';
    }
  };

  return (
    <div className="mt-4">
      {/* Toggle button */}
      <Button
        variant="outline-secondary"
        size="sm"
        onClick={() => setIsExpanded(!isExpanded)}
        className="d-flex align-items-center gap-2 mb-3 w-100 justify-content-between"
        aria-expanded={isExpanded}
        aria-controls="metrics-collapse"
      >
        <span className="d-flex align-items-center gap-2">
          <FaChartBar />
          Analisis de Metricas {getModelLabel()}
          {anomalousCount > 0 && (
            <Badge bg="danger" pill>{anomalousCount} anomalo{anomalousCount > 1 ? 's' : ''}</Badge>
          )}
          {normalCount > 0 && (
            <Badge bg="success" pill>{normalCount} normal{normalCount > 1 ? 'es' : ''}</Badge>
          )}
        </span>
        {isExpanded ? <FaChevronUp /> : <FaChevronDown />}
      </Button>

      {/* Collapsible content */}
      <Collapse in={isExpanded}>
        <div id="metrics-collapse">
          {/* Summary header */}
          <div className={`alert alert-${isThreat ? 'warning' : 'info'} py-2 mb-3`}>
            <small>
              <FaChartBar className="me-2" />
              Comparacion de {metrics.length} metrica{metrics.length > 1 ? 's' : ''} contra valores normales esperados.
              {anomalousCount > 0 && (
                <span className="text-danger fw-bold ms-2">
                  {anomalousCount} valor{anomalousCount > 1 ? 'es' : ''} fuera del rango normal.
                </span>
              )}
            </small>
          </div>

          {/* Metric cards - show anomalous first */}
          {[...metrics]
            .sort((a, b) => (b.is_anomalous ? 1 : 0) - (a.is_anomalous ? 1 : 0))
            .map((metric, idx) => (
              <MetricCard key={metric.metric_key || idx} metric={metric} />
            ))}
        </div>
      </Collapse>
    </div>
  );
};

export default MetricsAnalysisSection;
