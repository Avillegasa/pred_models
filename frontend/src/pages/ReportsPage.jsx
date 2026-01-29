/**
 * ReportsPage Component
 * Reports listing and viewing page
 */
import React, { useState, useEffect, useCallback } from 'react';
import { Card } from 'react-bootstrap';
import MainLayout from '../components/layout/MainLayout';
import ReportsList from '../components/reports/ReportsList';
import ReportDetail from '../components/reports/ReportDetail';
import reportService from '../services/reportService';

function ReportsPage() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedReport, setSelectedReport] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [showDetail, setShowDetail] = useState(false);

  const loadReports = useCallback(async () => {
    try {
      setLoading(true);
      const data = await reportService.listReports();
      setReports(data);
    } catch (err) {
      console.error('Error loading reports:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadReports();
  }, [loadReports]);

  const handleView = async (reportId) => {
    setDetailLoading(true);
    setShowDetail(true);
    try {
      const report = await reportService.getReport(reportId);
      setSelectedReport(report);
    } catch (err) {
      console.error('Error loading report:', err);
    } finally {
      setDetailLoading(false);
    }
  };

  const handleDelete = async (reportId) => {
    if (window.confirm('¿Eliminar este reporte? Esta accion no se puede deshacer.')) {
      try {
        await reportService.deleteReport(reportId);
        loadReports();
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al eliminar reporte');
      }
    }
  };

  return (
    <MainLayout title="Reportes">
      <Card className="shadow-sm">
        <Card.Body>
          <ReportsList
            reports={reports}
            loading={loading}
            onView={handleView}
            onDelete={handleDelete}
          />
        </Card.Body>
      </Card>

      <ReportDetail
        show={showDetail}
        onHide={() => setShowDetail(false)}
        report={selectedReport}
        loading={detailLoading}
      />
    </MainLayout>
  );
}

export default ReportsPage;
