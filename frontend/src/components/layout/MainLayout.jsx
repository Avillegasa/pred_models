/**
 * MainLayout Component
 * Main layout wrapper with sidebar - Swissborg dark theme
 */
import React from 'react';
import Sidebar from './Sidebar';
import TopBar from './TopBar';

function MainLayout({ children, title = 'Dashboard' }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <TopBar title={title} />
        <main className="page-content">
          {children}
        </main>
      </div>

      <style>{`
        .app-layout {
          display: flex;
          min-height: 100vh;
          background: var(--bg-primary);
          overflow-x: hidden;
        }

        .main-content {
          flex: 1;
          margin-left: 260px;
          display: flex;
          flex-direction: column;
          min-width: 0;
          transition: margin-left 0.3s ease;
          width: calc(100% - 260px);
          height: 100vh;
        }

        .page-content {
          flex: 1;
          padding: 1.25rem;
          overflow-y: auto;
          max-width: 100%;
        }

        @media (max-width: 992px) {
          .main-content {
            margin-left: 0;
            width: 100%;
          }

          .page-content {
            padding: 1rem;
          }
        }

        @media (max-width: 768px) {
          .page-content {
            padding: 0.75rem;
          }
        }
      `}</style>
    </div>
  );
}

export default MainLayout;
