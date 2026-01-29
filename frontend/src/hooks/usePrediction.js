/**
 * usePrediction Hook
 * Custom hook for managing prediction logic
 */

import { useCallback } from 'react';
import { useDashboard } from '../context/DashboardContext';
import { predictWithModel } from '../services/modelService';

/**
 * Custom hook for handling predictions
 * @returns {Object} Prediction state and methods
 */
export const usePrediction = () => {
  const {
    selectedModel,
    prediction,
    startPrediction,
    setPredictionSuccess,
    setPredictionError,
    clearPrediction,
    isLoading,
    hasError,
    hasData,
    isEmpty
  } = useDashboard();

  /**
   * Make a prediction with the selected model
   * @param {Object} data - Input data for prediction
   * @returns {Promise<Object>} Prediction result
   */
  const predict = useCallback(async (data) => {
    try {
      // Start loading state
      startPrediction();

      // Call prediction service
      const result = await predictWithModel(selectedModel, data);

      // Handle result
      if (result.success) {
        setPredictionSuccess(result.data);
        return { success: true, data: result.data };
      } else {
        setPredictionError(result.error);
        return { success: false, error: result.error };
      }
    } catch (error) {
      console.error('Prediction error:', error);

      const errorObj = {
        type: 'unknown',
        message: error.message || 'An unexpected error occurred during prediction',
        originalError: error
      };

      setPredictionError(errorObj);
      return { success: false, error: errorObj };
    }
  }, [selectedModel, startPrediction, setPredictionSuccess, setPredictionError]);

  /**
   * Retry last prediction (if data is available)
   * @param {Object} data - Input data for prediction
   * @returns {Promise<Object>} Prediction result
   */
  const retry = useCallback(async (data) => {
    if (!data) {
      console.error('Cannot retry: no data provided');
      return { success: false, error: { type: 'validation', message: 'No data to retry' } };
    }

    return await predict(data);
  }, [predict]);

  /**
   * Clear prediction and reset state
   */
  const clear = useCallback(() => {
    clearPrediction();
  }, [clearPrediction]);

  return {
    // State
    prediction,
    isLoading,
    hasError,
    hasData,
    isEmpty,

    // Methods
    predict,
    retry,
    clear,

    // Current model
    selectedModel
  };
};

export default usePrediction;
