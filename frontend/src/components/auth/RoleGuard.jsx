/**
 * RoleGuard Component
 * Conditionally renders content based on user role
 */
import React from 'react';
import { useAuth } from '../../context/AuthContext';

function RoleGuard({ roles, children, fallback = null }) {
  const { user } = useAuth();

  if (!user) {
    return fallback;
  }

  // Normalize roles to array
  const allowedRoles = Array.isArray(roles) ? roles : [roles];

  if (allowedRoles.includes(user.role)) {
    return children;
  }

  return fallback;
}

export default RoleGuard;
