/**
 * Sidebar Component
 * Navigation sidebar - Swissborg dark theme
 */
import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  FaHome,
  FaFileUpload,
  FaChartBar,
  FaUsers,
  FaShieldAlt,
  FaBrain,
  FaBell
} from 'react-icons/fa';
import { Badge } from 'react-bootstrap';
import { useAuth } from '../../context/AuthContext';
import { useAlerts } from '../../context/AlertContext';
import RoleGuard from '../auth/RoleGuard';

function Sidebar() {
  const { user } = useAuth();
  const { unreadCount } = useAlerts();

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <FaShieldAlt size={20} />
        </div>
        <div className="sidebar-brand">
          <span className="brand-name">SOC Portal</span>
          <span className="brand-role">
            {user?.role === 'admin' ? 'Administrador' : 'Analista'}
          </span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <NavLink to="/dashboard" end className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <FaHome className="nav-icon" />
          <span>Dashboard</span>
        </NavLink>

        <RoleGuard roles="admin">
          <NavLink to="/dashboard/predict" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <FaBrain className="nav-icon" />
            <span>Prediccion Manual</span>
          </NavLink>
        </RoleGuard>

        <RoleGuard roles="admin">
          <NavLink to="/files" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <FaFileUpload className="nav-icon" />
            <span>Archivos</span>
          </NavLink>
        </RoleGuard>

        <NavLink to="/reports" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <FaChartBar className="nav-icon" />
          <span>Reportes</span>
        </NavLink>

        <NavLink to="/alerts" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <FaBell className="nav-icon" />
          <span>Alertas</span>
          {unreadCount > 0 && (
            <Badge bg="danger" className="ms-auto" pill>
              {unreadCount > 99 ? '99+' : unreadCount}
            </Badge>
          )}
        </NavLink>

        <RoleGuard roles="admin">
          <NavLink to="/users" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <FaUsers className="nav-icon" />
            <span>Usuarios</span>
          </NavLink>
        </RoleGuard>
      </nav>

      {/* User info */}
      <div className="sidebar-footer">
        <div className="user-avatar">
          {user?.username?.charAt(0).toUpperCase()}
        </div>
        <div className="user-info">
          <span className="user-name">{user?.username}</span>
          <span className="user-role">{user?.role}</span>
        </div>
      </div>

      <style>{`
        .sidebar {
          width: 260px;
          height: 100vh;
          position: fixed;
          left: 0;
          top: 0;
          background: var(--bg-secondary);
          border-right: 1px solid var(--border-subtle);
          display: flex;
          flex-direction: column;
          z-index: 1000;
        }

        .sidebar-header {
          padding: 1.25rem;
          display: flex;
          align-items: center;
          gap: 0.75rem;
          border-bottom: 1px solid var(--border-subtle);
        }

        .sidebar-logo {
          width: 40px;
          height: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: var(--interactive-primary);
          color: var(--text-inverse);
          border-radius: var(--radius-md);
        }

        .sidebar-brand {
          display: flex;
          flex-direction: column;
        }

        .brand-name {
          color: var(--text-primary);
          font-weight: 600;
          font-size: 1rem;
        }

        .brand-role {
          color: var(--text-muted);
          font-size: 0.75rem;
        }

        .sidebar-nav {
          flex: 1;
          padding: 1rem 0.75rem;
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        .nav-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 0.75rem 1rem;
          color: var(--text-secondary);
          text-decoration: none;
          border-radius: var(--radius-md);
          transition: all var(--transition-fast);
          font-size: 0.9rem;
        }

        .nav-item:hover {
          background: var(--bg-elevated);
          color: var(--text-primary);
        }

        .nav-item.active {
          background: var(--bg-accent);
          color: var(--text-accent);
        }

        .nav-item.active .nav-icon {
          color: var(--text-accent);
        }

        .nav-icon {
          font-size: 1rem;
          opacity: 0.8;
        }

        .sidebar-footer {
          padding: 1rem 1.25rem;
          border-top: 1px solid var(--border-subtle);
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }

        .user-avatar {
          width: 36px;
          height: 36px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: var(--bg-elevated);
          color: var(--text-accent);
          font-weight: 600;
          border-radius: var(--radius-full);
          font-size: 0.875rem;
        }

        .user-info {
          display: flex;
          flex-direction: column;
        }

        .user-name {
          color: var(--text-primary);
          font-weight: 500;
          font-size: 0.875rem;
        }

        .user-role {
          color: var(--text-muted);
          font-size: 0.75rem;
          text-transform: capitalize;
        }

        @media (max-width: 992px) {
          .sidebar {
            transform: translateX(-100%);
            transition: transform 0.3s ease;
          }

          .sidebar.open {
            transform: translateX(0);
          }
        }
      `}</style>
    </aside>
  );
}

export default Sidebar;
