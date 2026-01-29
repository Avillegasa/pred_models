/**
 * Error Boundary Component
 * Catches JavaScript errors anywhere in child component tree
 */

import React from 'react';
import { Alert, Container } from 'react-bootstrap';
import { FiAlertTriangle } from 'react-icons/fi';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error Boundary caught error:', error, errorInfo);
    this.state = {
      hasError: true,
      error,
      errorInfo
    };
  }

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <Container className="py-5">
          <Alert variant="danger">
            <Alert.Heading>
              <FiAlertTriangle className="me-2" />
              Something went wrong
            </Alert.Heading>
            <p>
              An unexpected error occurred. Please try reloading the page.
            </p>
            <hr />
            {this.state.error && (
              <details className="mb-3">
                <summary style={{ cursor: 'pointer' }}>Error details</summary>
                <pre className="mt-2" style={{ fontSize: '0.875rem' }}>
                  {this.state.error.toString()}
                  {this.state.errorInfo && this.state.errorInfo.componentStack}
                </pre>
              </details>
            )}
            <button className="btn btn-danger" onClick={this.handleReload}>
              Reload Page
            </button>
          </Alert>
        </Container>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
