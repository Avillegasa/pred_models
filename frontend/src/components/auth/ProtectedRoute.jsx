/**
 * ProtectedRoute Component
 * Wrapper for routes that require authentication
 */
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import LoadingSpinner from '../common/LoadingSpinner';

function ProtectedRoute({ children, requiredRole = null }) {
  const { isAuthenticated, hasRole, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '100vh' }}>
        <LoadingSpinner message="Loading..." />
      </div>
    );
  }

  if (!isAuthenticated()) {
    // Redirect to login, saving the attempted location
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Check for required role
  if (requiredRole && !hasRole(requiredRole)) {
    // User doesn't have required role, redirect to dashboard
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

export default ProtectedRoute;
