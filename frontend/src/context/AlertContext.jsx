/**
 * Alert Context
 * Manages global alert state with real-time unread count
 */
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import alertService from '../services/alertService';
import { useAuth } from './AuthContext';

const AlertContext = createContext(null);

export function AlertProvider({ children }) {
  const [unreadCount, setUnreadCount] = useState(0);
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const { isAuthenticated, loading: authLoading } = useAuth();

  // Fetch unread count
  const fetchUnreadCount = useCallback(async () => {
    if (!isAuthenticated()) return;

    try {
      const data = await alertService.getUnreadCount();
      setUnreadCount(data.count);
    } catch (err) {
      console.error('Error fetching unread count:', err);
    }
  }, [isAuthenticated]);

  // Fetch alert stats
  const fetchStats = useCallback(async () => {
    if (!isAuthenticated()) return;

    try {
      const data = await alertService.getStats();
      setStats(data);
    } catch (err) {
      console.error('Error fetching alert stats:', err);
    }
  }, [isAuthenticated]);

  // Fetch alerts list
  const fetchAlerts = useCallback(async (filters = {}) => {
    if (!isAuthenticated()) return;

    setLoading(true);
    try {
      const data = await alertService.listAlerts(filters);
      setAlerts(data);
    } catch (err) {
      console.error('Error fetching alerts:', err);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  // Get single alert
  const getAlert = async (alertId) => {
    try {
      return await alertService.getAlert(alertId);
    } catch (err) {
      console.error('Error fetching alert:', err);
      throw err;
    }
  };

  // Acknowledge alert
  const acknowledgeAlert = async (alertId) => {
    try {
      await alertService.acknowledgeAlert(alertId);
      await fetchUnreadCount();
      await fetchStats();
      // Update local alerts list
      setAlerts(prev => prev.map(a =>
        a.id === alertId ? { ...a, status: 'acknowledged' } : a
      ));
    } catch (err) {
      console.error('Error acknowledging alert:', err);
      throw err;
    }
  };

  // Bulk acknowledge
  const bulkAcknowledge = async (alertIds) => {
    try {
      await alertService.bulkAcknowledge(alertIds);
      await fetchUnreadCount();
      await fetchStats();
      // Update local alerts list
      setAlerts(prev => prev.map(a =>
        alertIds.includes(a.id) ? { ...a, status: 'acknowledged' } : a
      ));
    } catch (err) {
      console.error('Error bulk acknowledging:', err);
      throw err;
    }
  };

  // Mark all as read
  const markAllAsRead = async () => {
    try {
      await alertService.markAllAsRead();
      setUnreadCount(0);
      // Update local alerts list
      setAlerts(prev => prev.map(a =>
        a.status === 'unread' ? { ...a, status: 'read' } : a
      ));
    } catch (err) {
      console.error('Error marking all as read:', err);
      throw err;
    }
  };

  // Poll for updates every 30 seconds
  useEffect(() => {
    if (!authLoading && isAuthenticated()) {
      fetchUnreadCount();

      const interval = setInterval(fetchUnreadCount, 30000);
      return () => clearInterval(interval);
    }
  }, [authLoading, isAuthenticated, fetchUnreadCount]);

  const value = {
    unreadCount,
    alerts,
    stats,
    loading,
    fetchUnreadCount,
    fetchStats,
    fetchAlerts,
    getAlert,
    acknowledgeAlert,
    bulkAcknowledge,
    markAllAsRead
  };

  return (
    <AlertContext.Provider value={value}>
      {children}
    </AlertContext.Provider>
  );
}

export function useAlerts() {
  const context = useContext(AlertContext);
  if (!context) {
    throw new Error('useAlerts must be used within an AlertProvider');
  }
  return context;
}

export default AlertContext;
