/**
 * Authentication Context
 * Manages user authentication state and provides auth methods
 */
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { jwtDecode } from 'jwt-decode';
import authService from '../services/authService';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  // Decode token and set user info
  const decodeAndSetUser = useCallback((tokenValue) => {
    if (!tokenValue) {
      setUser(null);
      return null;
    }

    try {
      const decoded = jwtDecode(tokenValue);

      // Check if token is expired
      if (decoded.exp * 1000 < Date.now()) {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        return null;
      }

      const userInfo = {
        username: decoded.sub,
        role: decoded.role,
        exp: decoded.exp
      };
      setUser(userInfo);
      return userInfo;
    } catch (error) {
      console.error('Error decoding token:', error);
      localStorage.removeItem('token');
      setToken(null);
      setUser(null);
      return null;
    }
  }, []);

  // Initialize auth state from stored token
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      decodeAndSetUser(storedToken);
    }
    setLoading(false);
  }, [decodeAndSetUser]);

  // Login function
  const login = async (username, password) => {
    try {
      const response = await authService.login(username, password);
      const newToken = response.access_token;

      localStorage.setItem('token', newToken);
      setToken(newToken);
      decodeAndSetUser(newToken);

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed'
      };
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  // Check if user has specific role
  const hasRole = (role) => {
    return user?.role === role;
  };

  // Check if user is admin
  const isAdmin = () => {
    return user?.role === 'admin';
  };

  // Check if user is authenticated
  const isAuthenticated = useCallback(() => {
    return !!user && !!token;
  }, [user, token]);

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    hasRole,
    isAdmin,
    isAuthenticated
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthContext;
