/**
 * Model Selector Component
 * Displays buttons for selecting prediction model
 */

import React from 'react';
import { useDashboard } from '../../context/DashboardContext';
import { getAllModels } from '../../services/modelService';
import ModelButton from './ModelButton';

const ModelSelector = () => {
  const { selectedModel, setSelectedModel } = useDashboard();
  const models = getAllModels();

  return (
    <div className="model-selector">
      <h6 className="model-selector-title">Seleccionar Modelo de Deteccion</h6>
      <div className="model-buttons">
        {models.map((model) => (
          <ModelButton
            key={model.id}
            modelType={model.id}
            metadata={model}
            isActive={selectedModel === model.id}
            onClick={setSelectedModel}
          />
        ))}
      </div>
    </div>
  );
};

export default ModelSelector;
