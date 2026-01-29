/**
 * Prediction Card Component
 * Displays the main prediction result with visual indicators
 */

import React from 'react';
import { FiCheckCircle, FiAlertTriangle, FiShield } from 'react-icons/fi';
import { formatPredictionLabel } from '../../utils/formatters';

const PredictionCard = ({ prediction }) => {
  if (!prediction) return null;

  const {
    prediction: predictionValue,
    prediction_label,
    confidence
  } = prediction;

  const isLegitimate = predictionValue === 0;
  const isThreat = predictionValue === 1;

  const cardClass = isLegitimate ? 'prediction-safe' : 'prediction-threat';
  const iconClass = isLegitimate ? 'safe' : 'threat';

  const getIcon = () => {
    if (isLegitimate) return <FiCheckCircle className={`prediction-icon ${iconClass}`} />;
    if (isThreat) return <FiAlertTriangle className={`prediction-icon ${iconClass}`} />;
    return <FiShield className="prediction-icon" />;
  };

  const getDescription = () => {
    if (isLegitimate) {
      return 'This appears to be legitimate activity. No immediate threat detected.';
    }
    if (isThreat) {
      return 'This activity shows characteristics of a security threat. Review carefully.';
    }
    return 'Analysis complete.';
  };

  return (
    <div className={`prediction-card ${cardClass}`}>
      <div className="prediction-header">
        {getIcon()}
        <div>
          <h2 className="prediction-label">
            {formatPredictionLabel(prediction_label)}
          </h2>
          <p className="prediction-description">
            {getDescription()}
          </p>
        </div>
      </div>
    </div>
  );
};

export default PredictionCard;
