/**
 * TopBar Component
 * Top navigation bar - Swissborg dark theme
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaSignOutAlt, FaUser, FaBell, FaChevronDown } from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';
import { useAlerts } from '../../context/AlertContext';

function TopBar({ title }) {
  const { user, logout } = useAuth();
  const { unreadCount } = useAlerts();
  const navigate = useNavigate();
  const [dropdownOpen, setDropdownOpen] = React.useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="topbar">
      <div className="topbar-title">
        <h1>{title}</h1>
      </div>

      <div className="topbar-actions">
        {/* Notifications */}
        <button className="topbar-icon-btn" onClick={() => navigate('/alerts')} title="Ver alertas">
          <FaBell />
          {unreadCount > 0 && (
            <span className="notification-badge">
              {unreadCount > 99 ? '99+' : unreadCount}
            </span>
          )}
        </button>

        {/* User dropdown */}
        <div className="user-dropdown">
          <button
            className="user-dropdown-trigger"
            onClick={() => setDropdownOpen(!dropdownOpen)}
          >
            <div className="user-avatar">
              {user?.username?.charAt(0).toUpperCase()}
            </div>
            <div className="user-details">
              <span className="user-name">{user?.username}</span>
              <span className="user-role">
                {user?.role === 'admin' ? 'Administrador' : 'Analista'}
              </span>
            </div>
            <FaChevronDown className={`topbar-arrow ${dropdownOpen ? 'open' : ''}`} />
          </button>

          {dropdownOpen && (
            <>
              <div className="topbar-backdrop" onClick={() => setDropdownOpen(false)} />
              <div className="topbar-menu">
                <button className="topbar-menu-item" disabled>
                  <FaUser />
                  <span>Perfil</span>
                </button>
                <div className="topbar-menu-divider" />
                <button className="topbar-menu-item danger" onClick={handleLogout}>
                  <FaSignOutAlt />
                  <span>Cerrar Sesion</span>
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      <style>{`
        .topbar {
          height: 64px;
          background: linear-gradient(135deg, var(--interactive-accent) 0%, #E56A00 100%);
          border-bottom: none;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 1.5rem;
          box-shadow: 0 2px 8px rgba(255, 120, 0, 0.3);
          position: sticky;
          top: 0;
          z-index: 900;
        }

        .topbar-title h1 {
          color: #FFFFFF;
          font-size: 1.25rem;
          font-weight: 600;
          margin: 0;
        }

        .topbar-actions {
          display: flex;
          align-items: center;
          gap: 1rem;
        }

        .topbar-icon-btn {
          width: 40px;
          height: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: #FFFFFF;
          border: none;
          border-radius: var(--radius-md);
          color: var(--interactive-primary);
          cursor: pointer;
          position: relative;
          transition: all var(--transition-fast);
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .topbar-icon-btn:hover {
          background: #F8F9FA;
          color: var(--interactive-primary-hover);
          transform: translateY(-1px);
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
        }

        .notification-badge {
          position: absolute;
          top: -4px;
          right: -4px;
          min-width: 18px;
          height: 18px;
          padding: 0 5px;
          background: var(--status-danger);
          color: #FFFFFF;
          font-size: 0.65rem;
          font-weight: 700;
          border-radius: var(--radius-full);
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        }

        .user-dropdown {
          position: relative;
        }

        .user-dropdown-trigger {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 0.5rem 0.75rem;
          background: #FFFFFF;
          border: none;
          border-radius: var(--radius-md);
          cursor: pointer;
          transition: all var(--transition-fast);
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .user-dropdown-trigger:hover {
          background: #F8F9FA;
          transform: translateY(-1px);
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
        }

        .user-avatar {
          width: 36px;
          height: 36px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: var(--interactive-primary);
          color: #FFFFFF;
          font-weight: 600;
          border-radius: var(--radius-full);
          font-size: 0.875rem;
        }

        .user-details {
          display: flex;
          flex-direction: column;
          text-align: left;
        }

        .user-name {
          color: var(--text-primary);
          font-weight: 600;
          font-size: 0.875rem;
          line-height: 1.2;
        }

        .user-role {
          color: var(--text-muted);
          font-size: 0.75rem;
          line-height: 1.2;
        }

        .topbar-arrow {
          color: var(--text-muted);
          font-size: 0.625rem;
          transition: transform var(--transition-fast);
        }

        .topbar-arrow.open {
          transform: rotate(180deg);
        }

        .topbar-backdrop {
          position: fixed;
          inset: 0;
          z-index: 999;
        }

        .topbar-menu {
          position: absolute;
          top: calc(100% + 0.5rem);
          right: 0;
          min-width: 180px;
          background: var(--bg-elevated);
          border: 1px solid var(--border-default);
          border-radius: var(--radius-md);
          box-shadow: var(--shadow-lg);
          z-index: 1000;
          overflow: hidden;
        }

        .topbar-menu-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          width: 100%;
          padding: 0.75rem 1rem;
          background: transparent;
          border: none;
          color: var(--text-secondary);
          font-size: 0.875rem;
          cursor: pointer;
          transition: all var(--transition-fast);
        }

        .topbar-menu-item:hover:not(:disabled) {
          background: var(--bg-accent);
          color: var(--text-primary);
        }

        .topbar-menu-item:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .topbar-menu-item.danger {
          color: var(--status-danger-light);
        }

        .topbar-menu-item.danger:hover {
          background: var(--status-danger-bg);
          color: var(--status-danger-light);
        }

        .topbar-menu-divider {
          height: 1px;
          background: var(--border-subtle);
          margin: 0.25rem 0;
        }

        @media (max-width: 992px) {
          .topbar {
            padding: 0 1rem;
          }

          .topbar-title h1 {
            font-size: 1.125rem;
          }
        }

        @media (max-width: 768px) {
          .topbar {
            height: 56px;
            padding: 0 0.75rem;
          }

          .topbar-title h1 {
            font-size: 1rem;
          }

          .topbar-actions {
            gap: 0.5rem;
          }

          .topbar-icon-btn {
            width: 36px;
            height: 36px;
          }

          .user-details {
            display: none;
          }

          .user-avatar {
            width: 32px;
            height: 32px;
            font-size: 0.75rem;
          }

          .topbar-arrow {
            display: none;
          }

          .user-dropdown-trigger {
            padding: 0.25rem;
            gap: 0.5rem;
          }
        }
      `}</style>
    </header>
  );
}

export default TopBar;
