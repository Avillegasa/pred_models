/**
 * Results Display Component
 * Container for displaying prediction results
 */

import React from 'react';
import { FiTarget } from 'react-icons/fi';
import { useDashboard } from '../../context/DashboardContext';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorAlert from './ErrorAlert';
import PredictionCard from './PredictionCard';
import ConfidenceMetrics from './ConfidenceMetrics';
import MetadataInfo from './MetadataInfo';
import ExplainabilitySection from './ExplainabilitySection';
import MetricsAnalysisSection from './MetricsAnalysisSection';

const ResultsDisplay = () => {
  const { prediction, isLoading, hasError, hasData, isEmpty, clearPrediction, selectedModel } = useDashboard();

  // Loading state
  if (isLoading) {
    return (
      <div className="results-card">
        <LoadingSpinner message="Analizando amenaza..." />
      </div>
    );
  }

  // Error state
  if (hasError) {
    return (
      <div className="results-card">
        <h3 className="form-card-title">Resultados de Prediccion</h3>
        <ErrorAlert error={prediction.error} onDismiss={clearPrediction} />
      </div>
    );
  }

  // Empty state
  if (isEmpty) {
    return (
      <div className="results-card">
        <div className="results-card-empty">
          <FiTarget className="results-card-empty-icon" />
          <p className="results-card-empty-text">Sin resultados aun</p>
          <small className="text-muted">
            Complete el formulario y haga clic en Predecir para analizar los datos
          </small>
        </div>
      </div>
    );
  }

  // Results state
  if (hasData) {
    const isThreat = prediction.data?.prediction === 1;

    return (
      <div className="results-card">
        <h3 className="form-card-title">Resultados de Prediccion</h3>

        {/* Main Prediction */}
        <PredictionCard prediction={prediction.data} />

        {/* Confidence Metrics */}
        <ConfidenceMetrics prediction={prediction.data} />

        {/* Explainability Section */}
        {prediction.data?.explanation && (
          <ExplainabilitySection
            explanation={prediction.data.explanation}
            modelType={selectedModel}
            isThreat={isThreat}
          />
        )}

        {/* Metrics Analysis Section */}
        {prediction.data?.metrics_analysis && (
          <MetricsAnalysisSection
            metrics={prediction.data.metrics_analysis}
            modelType={selectedModel}
            isThreat={isThreat}
          />
        )}

        {/* Metadata */}
        <MetadataInfo prediction={prediction.data} />
      </div>
    );
  }

  return null;
};

export default ResultsDisplay;
