/**
 * Confidence Metrics Component
 * Displays confidence scores and probability breakdown
 */

import React from 'react';
import { ProgressBar } from 'react-bootstrap';
import { formatPercentage } from '../../utils/formatters';

const ConfidenceMetrics = ({ prediction }) => {
  if (!prediction) return null;

  const {
    prediction: predictionValue,
    confidence,
    probability_legitimate,
    probability_phishing,
    probability_normal,
    probability_attack,
    probability_bruteforce
  } = prediction;

  // Determine which probabilities to display based on prediction type
  const legitProb = probability_legitimate ?? probability_normal ?? 0;
  const threatProb = probability_phishing ?? probability_attack ?? probability_bruteforce ?? 0;

  const legitLabel = probability_legitimate !== undefined ? 'Legitimo' :
                     probability_normal !== undefined ? 'Normal' : 'Seguro';

  const threatLabel = probability_phishing !== undefined ? 'Phishing' :
                      probability_attack !== undefined ? 'Ataque' :
                      probability_bruteforce !== undefined ? 'Fuerza Bruta' : 'Amenaza';

  const isLegitimate = predictionValue === 0;
  const progressVariant = isLegitimate ? 'success' : 'danger';

  return (
    <div className="confidence-section">
      <h6 className="confidence-title">Analisis de Confianza</h6>

      <div className="confidence-score">
        <span className="confidence-label">Confianza</span>
        <span className="confidence-value">{formatPercentage(confidence)}</span>
      </div>

      <ProgressBar
        now={confidence * 100}
        variant={progressVariant}
        className="confidence-progress"
        label={formatPercentage(confidence)}
      />

      <div className="probability-breakdown">
        <div className="probability-item">
          <span className="probability-label">
            <span className="probability-dot safe" />
            {legitLabel}
          </span>
          <span className="probability-value">{formatPercentage(legitProb)}</span>
        </div>

        <div className="probability-item">
          <span className="probability-label">
            <span className="probability-dot threat" />
            {threatLabel}
          </span>
          <span className="probability-value">{formatPercentage(threatProb)}</span>
        </div>
      </div>
    </div>
  );
};

export default ConfidenceMetrics;
