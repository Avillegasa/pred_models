/**
 * Phishing Detection Service
 * Real API integration for phishing email prediction
 */

import { phishingApi } from './api';

export const phishingService = {
  /**
   * Health check endpoint
   * @returns {Promise<Object>} Server status
   */
  async healthCheck() {
    try {
      const response = await phishingApi.get('/');
      return { success: true, data: response };
    } catch (error) {
      return { success: false, error };
    }
  },

  /**
   * Predict if an email is phishing or legitimate
   * @param {Object} emailData - Email data to analyze
   * @param {string} emailData.sender - Sender email address (required)
   * @param {string} emailData.receiver - Receiver email address (optional)
   * @param {string} emailData.subject - Email subject (required)
   * @param {string} emailData.body - Email body content (required)
   * @param {number} emailData.urls - URL presence flag (0 or 1, optional)
   * @returns {Promise<Object>} Prediction result
   */
  async predict(emailData) {
    try {
      // Validate required fields
      if (!emailData.sender || !emailData.subject || !emailData.body) {
        throw {
          type: 'validation',
          message: 'Missing required fields: sender, subject, and body are required',
          details: { emailData }
        };
      }

      // Prepare payload
      const payload = {
        sender: emailData.sender.trim(),
        receiver: emailData.receiver?.trim() || '',
        subject: emailData.subject.trim(),
        body: emailData.body.trim(),
        urls: emailData.urls !== undefined ? parseInt(emailData.urls) : 0
      };

      // Make API request
      const response = await phishingApi.post('/predict', payload);

      return {
        success: true,
        data: response,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error };
    }
  },

  /**
   * Predict multiple emails in batch
   * @param {Array<Object>} emails - Array of email objects
   * @returns {Promise<Object>} Batch prediction results
   */
  async predictBatch(emails) {
    try {
      if (!Array.isArray(emails) || emails.length === 0) {
        throw {
          type: 'validation',
          message: 'Emails must be a non-empty array',
          details: { emails }
        };
      }

      const response = await phishingApi.post('/predict/batch', { emails });

      return {
        success: true,
        data: response,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error };
    }
  },

  /**
   * Get model information and metrics
   * @returns {Promise<Object>} Model metadata and performance metrics
   */
  async getModelInfo() {
    try {
      const response = await phishingApi.get('/model/info');
      return { success: true, data: response };
    } catch (error) {
      return { success: false, error };
    }
  }
};

export default phishingService;
