/**
 * Error Alert Component
 * Displays error messages with dismissible alert
 */

import React from 'react';
import { Alert } from 'react-bootstrap';
import { FiAlertTriangle, FiWifi, FiXCircle } from 'react-icons/fi';
import { formatApiError } from '../../services/api';

const ErrorAlert = ({ error, onDismiss }) => {
  if (!error) return null;

  const formattedError = typeof error === 'object' ? formatApiError(error) : { title: 'Error', message: error };

  const getIcon = () => {
    switch (error.type) {
      case 'network':
        return <FiWifi size={20} />;
      case 'validation':
        return <FiAlertTriangle size={20} />;
      default:
        return <FiXCircle size={20} />;
    }
  };

  const getVariant = () => {
    switch (error.type) {
      case 'network':
        return 'warning';
      case 'validation':
        return 'info';
      default:
        return 'danger';
    }
  };

  return (
    <Alert
      variant={getVariant()}
      dismissible
      onClose={onDismiss}
      className="error-alert"
    >
      <Alert.Heading className="error-alert-title">
        {getIcon()}
        {formattedError.title}
      </Alert.Heading>
      <p className="error-alert-message">{formattedError.message}</p>
      {formattedError.status && (
        <small className="error-alert-details">
          Status Code: {formattedError.status}
        </small>
      )}
    </Alert>
  );
};

export default ErrorAlert;
