/**
 * PermissionsEditor Component
 * Component for editing user permissions with switches
 */
import React from 'react';
import { Form } from 'react-bootstrap';
import { FaHome, FaBrain, FaChartBar, FaBell } from 'react-icons/fa';

const PERMISSION_MODULES = [
  { key: 'dashboard', label: 'Dashboard', icon: FaHome, description: 'Ver dashboard y estadisticas' },
  { key: 'predictions', label: 'Predicciones', icon: FaBrain, description: 'Realizar predicciones manuales' },
  { key: 'reports', label: 'Reportes', icon: FaChartBar, description: 'Ver reportes mensuales' },
  { key: 'alerts', label: 'Alertas', icon: FaBell, description: 'Ver y gestionar alertas' }
];

function PermissionsEditor({ permissions, onChange, disabled = false }) {
  const handleToggle = (key) => {
    if (disabled) return;
    onChange({
      ...permissions,
      [key]: !permissions[key]
    });
  };

  return (
    <div className="permissions-editor">
      {PERMISSION_MODULES.map(({ key, label, icon: Icon, description }) => (
        <div
          key={key}
          className={`permission-item d-flex align-items-center justify-content-between p-3 rounded mb-2 ${
            disabled ? 'bg-light' : 'bg-light'
          }`}
          style={{ border: '1px solid var(--border-default)' }}
        >
          <div className="d-flex align-items-center">
            <Icon className="text-primary me-3" size={18} />
            <div>
              <div className="fw-medium">{label}</div>
              <small className="text-muted">{description}</small>
            </div>
          </div>
          <Form.Check
            type="switch"
            id={`permission-${key}`}
            checked={permissions[key] || false}
            onChange={() => handleToggle(key)}
            disabled={disabled}
            className="ms-3"
          />
        </div>
      ))}

      {disabled && (
        <small className="text-muted d-block mt-2">
          Los permisos no aplican para usuarios administradores (tienen acceso total).
        </small>
      )}

      <style>{`
        .permission-item {
          transition: all 0.2s ease;
        }
        .permission-item:hover:not(.bg-light) {
          border-color: var(--interactive-primary) !important;
        }
        .form-check-input:checked {
          background-color: var(--interactive-primary);
          border-color: var(--interactive-primary);
        }
      `}</style>
    </div>
  );
}

export default PermissionsEditor;
