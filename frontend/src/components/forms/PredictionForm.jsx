/**
 * Prediction Form Container
 * Dynamically displays the appropriate form based on selected model
 */

import React from 'react';
import { useDashboard } from '../../context/DashboardContext';
import { MODEL_TYPES } from '../../services/modelService';
import PhishingForm from './PhishingForm';
import AtaquesSospechososForm from './AtaquesSospechososForm';
import FuerzaBrutaForm from './FuerzaBrutaForm';

const PredictionForm = () => {
  const { selectedModel } = useDashboard();

  // Render appropriate form based on selected model
  switch (selectedModel) {
    case MODEL_TYPES.PHISHING:
      return <PhishingForm />;

    case MODEL_TYPES.ATAQUES_SOSPECHOSOS:
      return <AtaquesSospechososForm />;

    case MODEL_TYPES.FUERZA_BRUTA:
      return <FuerzaBrutaForm />;

    default:
      return <PhishingForm />;
  }
};

export default PredictionForm;
