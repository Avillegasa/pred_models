/**
 * DashboardPage Component
 * Main dashboard view - shows overview or prediction form based on route
 */
import React from 'react';
import { useLocation } from 'react-router-dom';
import MainLayout from '../components/layout/MainLayout';
import { DashboardProvider } from '../context/DashboardContext';
import Dashboard from '../components/dashboard/Dashboard';
import DashboardOverview from '../components/dashboard/DashboardOverview';

function DashboardPage() {
  const location = useLocation();
  const showPredictForm = location.pathname.includes('/predict');

  return (
    <MainLayout title={showPredictForm ? 'Prediccion Manual' : 'Dashboard'}>
      {showPredictForm ? (
        <DashboardProvider>
          <Dashboard />
        </DashboardProvider>
      ) : (
        <DashboardOverview />
      )}
    </MainLayout>
  );
}

export default DashboardPage;
