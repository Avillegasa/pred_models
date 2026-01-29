/**
 * AlertsPage Component
 * Alert listing and management page
 */
import React, { useState, useEffect, useCallback } from 'react';
import { Card } from 'react-bootstrap';
import MainLayout from '../components/layout/MainLayout';
import AlertsList from '../components/alerts/AlertsList';
import AlertDetail from '../components/alerts/AlertDetail';
import AlertFilters from '../components/alerts/AlertFilters';
import AlertStatsCards from '../components/alerts/AlertStatsCards';
import { useAlerts } from '../context/AlertContext';

function AlertsPage() {
  const {
    alerts,
    stats,
    loading,
    fetchAlerts,
    fetchStats,
    acknowledgeAlert,
    bulkAcknowledge
  } = useAlerts();

  const [selectedAlertId, setSelectedAlertId] = useState(null);
  const [showDetail, setShowDetail] = useState(false);
  const [filters, setFilters] = useState({});
  const [selectedIds, setSelectedIds] = useState([]);

  // Load alerts and stats on mount and filter change
  useEffect(() => {
    fetchAlerts(filters);
    fetchStats();
  }, [filters, fetchAlerts, fetchStats]);

  const handleView = useCallback((alertId) => {
    setSelectedAlertId(alertId);
    setShowDetail(true);
  }, []);

  const handleAcknowledge = useCallback(async (alertId) => {
    try {
      await acknowledgeAlert(alertId);
    } catch (err) {
      console.error('Error acknowledging alert:', err);
    }
  }, [acknowledgeAlert]);

  const handleBulkAcknowledge = useCallback(async () => {
    if (selectedIds.length > 0) {
      try {
        await bulkAcknowledge(selectedIds);
        setSelectedIds([]);
      } catch (err) {
        console.error('Error bulk acknowledging:', err);
      }
    }
  }, [selectedIds, bulkAcknowledge]);

  const handleFilterChange = useCallback((newFilters) => {
    setFilters(newFilters);
    setSelectedIds([]);
  }, []);

  const handleCloseDetail = useCallback(() => {
    setShowDetail(false);
    setSelectedAlertId(null);
    // Refresh alerts after viewing (in case it was marked as read)
    fetchAlerts(filters);
  }, [fetchAlerts, filters]);

  return (
    <MainLayout title="Alertas">
      {/* Stats Cards */}
      <AlertStatsCards stats={stats} />

      {/* Filters */}
      <Card className="shadow-sm mb-3">
        <Card.Body>
          <AlertFilters
            filters={filters}
            onChange={handleFilterChange}
            selectedCount={selectedIds.length}
            onBulkAcknowledge={handleBulkAcknowledge}
          />
        </Card.Body>
      </Card>

      {/* Alerts List */}
      <Card className="shadow-sm">
        <Card.Body>
          <AlertsList
            alerts={alerts}
            loading={loading}
            onView={handleView}
            onAcknowledge={handleAcknowledge}
            selectedIds={selectedIds}
            onSelectionChange={setSelectedIds}
          />
        </Card.Body>
      </Card>

      {/* Alert Detail Modal */}
      <AlertDetail
        show={showDetail}
        onHide={handleCloseDetail}
        alertId={selectedAlertId}
        onAcknowledge={handleAcknowledge}
      />
    </MainLayout>
  );
}

export default AlertsPage;
