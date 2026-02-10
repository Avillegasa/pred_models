/**
 * Authentication Context
 * Manages user authentication state and provides auth methods
 */
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { jwtDecode } from 'jwt-decode';
import authService from '../services/authService';
import profileService from '../services/profileService';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  // Load full user profile from API
  const loadUserProfile = useCallback(async () => {
    try {
      const profile = await profileService.getProfile();
      setUser(prevUser => ({
        ...prevUser,
        ...profile,
        permissions: profile.permissions || {}
      }));
    } catch (error) {
      console.error('Error loading user profile:', error);
    }
  }, []);

  // Decode token and set user info
  const decodeAndSetUser = useCallback(async (tokenValue) => {
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
        exp: decoded.exp,
        permissions: {} // Will be loaded from profile
      };
      setUser(userInfo);

      // Load full profile to get permissions
      await loadUserProfile();

      return userInfo;
    } catch (error) {
      console.error('Error decoding token:', error);
      localStorage.removeItem('token');
      setToken(null);
      setUser(null);
      return null;
    }
  }, [loadUserProfile]);

  // Initialize auth state from stored token
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        await decodeAndSetUser(storedToken);
      }
      setLoading(false);
    };
    initAuth();
  }, [decodeAndSetUser]);

  // Login function
  const login = async (username, password) => {
    try {
      const response = await authService.login(username, password);
      const newToken = response.access_token;

      localStorage.setItem('token', newToken);
      setToken(newToken);
      await decodeAndSetUser(newToken);

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

  // Check if user has specific permission
  const hasPermission = useCallback((permission) => {
    if (!user) return false;
    // Admin always has all permissions
    if (user.role === 'admin') return true;
    // Check specific permission for analysts
    return user.permissions?.[permission] === true;
  }, [user]);

  // Refresh user profile (call after profile updates)
  const refreshProfile = useCallback(async () => {
    await loadUserProfile();
  }, [loadUserProfile]);

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
    hasPermission,
    refreshProfile,
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
