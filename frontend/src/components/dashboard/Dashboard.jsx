/**
 * Dashboard Component
 * Main container for the prediction dashboard
 */

import React from 'react';
import { Container } from 'react-bootstrap';
import { useDashboard } from '../../context/DashboardContext';
import ModelSelector from './ModelSelector';
import PredictionForm from '../forms/PredictionForm';
import ResultsDisplay from '../results/ResultsDisplay';

const Dashboard = () => {
  const { selectedModel } = useDashboard();

  return (
    <Container fluid className="dashboard-container">
      <div className="dashboard-content">
        {/* Model Selector */}
        <ModelSelector />

        {/* Forms and Results Grid */}
        <div className="dashboard-grid">
          {/* Form Section */}
          <div className="form-section">
            <PredictionForm />
          </div>

          {/* Results Section */}
          <div className="results-section">
            <ResultsDisplay />
          </div>
        </div>
      </div>
    </Container>
  );
};

export default Dashboard;
