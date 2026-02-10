/**
 * Metadata Info Component
 * Displays prediction metadata (model, timestamp, processing time, etc.)
 */

import React from 'react';
import { Badge } from 'react-bootstrap';
import { formatDatetime, formatProcessingTime, formatNumber, formatModelName } from '../../utils/formatters';

const MetadataInfo = ({ prediction }) => {
  if (!prediction || !prediction.metadata) return null;

  const { metadata, model_type, is_mock } = prediction;
  const {
    model,
    features_count,
    timestamp,
    processing_time_ms
  } = metadata;

  return (
    <div className="metadata-section">
      <h6 className="metadata-title">Informacion del Modelo</h6>

      <div className="metadata-grid">
        <div className="metadata-item">
          <span className="metadata-item-label">Modelo</span>
          <span className="metadata-item-value">
            {formatModelName(model)}
            {is_mock && (
              <Badge bg="secondary" className="ms-2">MOCK</Badge>
            )}
          </span>
        </div>

        {features_count && (
          <div className="metadata-item">
            <span className="metadata-item-label">Caracteristicas</span>
            <span className="metadata-item-value">{formatNumber(features_count)}</span>
          </div>
        )}

        {processing_time_ms && (
          <div className="metadata-item">
            <span className="metadata-item-label">Tiempo de Proceso</span>
            <span className="metadata-item-value">{formatProcessingTime(processing_time_ms)}</span>
          </div>
        )}

        {timestamp && (
          <div className="metadata-item">
            <span className="metadata-item-label">Marca de Tiempo</span>
            <span className="metadata-item-value">{formatDatetime(timestamp)}</span>
          </div>
        )}
      </div>

      {/* Additional model-specific information */}
      {prediction.attack_type && (
        <div className="mt-3">
          <div className="metadata-item">
            <span className="metadata-item-label">Tipo de Ataque</span>
            <span className="metadata-item-value">
              <Badge bg="danger">{prediction.attack_type}</Badge>
            </span>
          </div>
        </div>
      )}

      {prediction.severity && (
        <div className="mt-2">
          <div className="metadata-item">
            <span className="metadata-item-label">Severidad</span>
            <span className="metadata-item-value">
              <Badge bg="warning">{prediction.severity}</Badge>
            </span>
          </div>
        </div>
      )}

      {prediction.threat_level && (
        <div className="mt-2">
          <div className="metadata-item">
            <span className="metadata-item-label">Nivel de Amenaza</span>
            <span className="metadata-item-value">
              <Badge bg="danger">{prediction.threat_level}</Badge>
            </span>
          </div>
        </div>
      )}

      {prediction.blocked_recommendation !== undefined && (
        <div className="mt-2">
          <div className="metadata-item">
            <span className="metadata-item-label">Se Recomienda Bloquear</span>
            <span className="metadata-item-value">
              <Badge bg={prediction.blocked_recommendation ? 'danger' : 'success'}>
                {prediction.blocked_recommendation ? 'Si' : 'No'}
              </Badge>
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default MetadataInfo;
