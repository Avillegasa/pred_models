/**
 * Dashboard Context
 * Global state management for the cybersecurity dashboard
 */

import React, { createContext, useContext, useState, useCallback } from 'react';
import { MODEL_TYPES } from '../services/modelService';

// Create Context
const DashboardContext = createContext(undefined);

/**
 * Dashboard Provider Component
 * Wraps the application and provides global state
 */
export const DashboardProvider = ({ children }) => {
  // Selected model state
  const [selectedModel, setSelectedModel] = useState(MODEL_TYPES.PHISHING);

  // Prediction state
  const [prediction, setPrediction] = useState({
    loading: false,
    data: null,
    error: null
  });

  /**
   * Update selected model
   * Clears prediction when model changes
   */
  const handleSelectModel = useCallback((modelType) => {
    setSelectedModel(modelType);
    // Clear previous prediction when switching models
    setPrediction({
      loading: false,
      data: null,
      error: null
    });
  }, []);

  /**
   * Start prediction (loading state)
   */
  const startPrediction = useCallback(() => {
    setPrediction({
      loading: true,
      data: null,
      error: null
    });
  }, []);

  /**
   * Set prediction success
   */
  const setPredictionSuccess = useCallback((data) => {
    setPrediction({
      loading: false,
      data,
      error: null
    });
  }, []);

  /**
   * Set prediction error
   */
  const setPredictionError = useCallback((error) => {
    setPrediction({
      loading: false,
      data: null,
      error
    });
  }, []);

  /**
   * Clear prediction
   */
  const clearPrediction = useCallback(() => {
    setPrediction({
      loading: false,
      data: null,
      error: null
    });
  }, []);

  /**
   * Reset dashboard state
   */
  const resetDashboard = useCallback(() => {
    setSelectedModel(MODEL_TYPES.PHISHING);
    setPrediction({
      loading: false,
      data: null,
      error: null
    });
  }, []);

  // Context value
  const value = {
    // Model selection
    selectedModel,
    setSelectedModel: handleSelectModel,

    // Prediction state
    prediction,
    startPrediction,
    setPredictionSuccess,
    setPredictionError,
    clearPrediction,

    // Utility
    resetDashboard,

    // Computed values
    isLoading: prediction.loading,
    hasError: !!prediction.error,
    hasData: !!prediction.data,
    isEmpty: !prediction.loading && !prediction.data && !prediction.error
  };

  return (
    <DashboardContext.Provider value={value}>
      {children}
    </DashboardContext.Provider>
  );
};

/**
 * Custom hook to use Dashboard context
 * Throws error if used outside of DashboardProvider
 */
export const useDashboard = () => {
  const context = useContext(DashboardContext);

  if (context === undefined) {
    throw new Error('useDashboard must be used within a DashboardProvider');
  }

  return context;
};

export default DashboardContext;
