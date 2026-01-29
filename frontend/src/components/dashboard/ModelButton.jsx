/**
 * Model Button Component
 * Reusable button for model selection
 */

import React from 'react';
import { Badge } from 'react-bootstrap';

const ModelButton = ({ modelType, metadata, isActive, onClick }) => {
  const { name, shortName, icon, status, color } = metadata;

  return (
    <button
      className={`model-button ${isActive ? 'active' : ''}`}
      onClick={() => onClick(modelType)}
      style={{
        borderColor: isActive ? color : undefined,
        backgroundColor: isActive ? color : undefined
      }}
    >
      <span className="model-button-icon">{icon}</span>
      <span className="model-button-label">{shortName}</span>
      {status === 'mock' && (
        <Badge bg="secondary" className="model-button-badge">
          MOCK
        </Badge>
      )}
    </button>
  );
};

export default ModelButton;
