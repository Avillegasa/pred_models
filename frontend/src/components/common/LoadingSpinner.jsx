/**
 * Loading Spinner Component
 * Displays loading animation with optional message
 */

import React from 'react';
import { Spinner } from 'react-bootstrap';

const LoadingSpinner = ({ message = 'Processing...', size = 'lg', variant = 'primary' }) => {
  return (
    <div className="loading-container">
      <Spinner animation="border" variant={variant} size={size} role="status">
        <span className="visually-hidden">Loading...</span>
      </Spinner>
      {message && <p className="loading-text">{message}</p>}
    </div>
  );
};

export default LoadingSpinner;
