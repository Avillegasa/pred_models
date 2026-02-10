/**
 * LoginForm Component
 * Form for user authentication - BCP branding
 */
import React, { useState } from 'react';
import { FaUser, FaLock, FaSignInAlt } from 'react-icons/fa';

function LoginForm({ onSubmit, error, loading }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username && password) {
      onSubmit(username, password);
    }
  };

  return (
    <div className="login-card">
      {/* Header */}
      <div className="login-header">
        <img
          src="/logo-bcp.png"
          alt="BCP"
          className="login-logo-img"
        />
        <h1 className="login-title">SISTEMA DE PREDICCION</h1>
        <p className="login-subtitle">Deteccion Inteligente de Amenazas</p>
      </div>

      {/* Error message */}
      {error && (
        <div className="login-error">
          {error}
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label className="form-label">
            <FaUser className="label-icon" />
            Usuario
          </label>
          <input
            type="text"
            className="form-input"
            placeholder="Ingrese su usuario"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            disabled={loading}
            autoComplete="username"
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">
            <FaLock className="label-icon" />
            Contrasena
          </label>
          <input
            type="password"
            className="form-input"
            placeholder="Ingrese su contrasena"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
            autoComplete="current-password"
            required
          />
        </div>

        <button
          type="submit"
          className="login-button"
          disabled={loading || !username || !password}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Iniciando sesion...
            </>
          ) : (
            <>
              <FaSignInAlt className="button-icon" />
              Iniciar Sesion
            </>
          )}
        </button>
      </form>

      {/* Footer */}
      <div className="login-footer">
        <span>Usuarios de prueba:</span>
        <code>admin / admin123</code>
        <code>analyst / analyst123</code>
      </div>

      <style>{`
        .login-card {
          background: var(--surface-base);
          border: 1px solid var(--border-default);
          border-radius: var(--radius-lg);
          padding: 2.5rem;
          box-shadow: var(--shadow-xl);
        }

        .login-header {
          text-align: center;
          margin-bottom: 2rem;
        }

        .login-logo-img {
          width: 120px;
          height: auto;
          margin-bottom: 1.25rem;
          object-fit: contain;
        }

        .login-title {
          color: var(--text-primary);
          font-size: 1.5rem;
          font-weight: 700;
          margin: 0 0 0.5rem;
          letter-spacing: 1px;
        }

        .login-subtitle {
          color: var(--text-secondary);
          font-size: 0.875rem;
          margin: 0;
        }

        .login-error {
          background: var(--status-danger-bg);
          border: 1px solid var(--status-danger);
          border-radius: var(--radius-md);
          color: var(--status-danger-light);
          padding: 0.75rem 1rem;
          margin-bottom: 1.5rem;
          font-size: 0.875rem;
        }

        .login-form {
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
        }

        .form-group {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .form-label {
          color: var(--text-secondary);
          font-size: 0.875rem;
          font-weight: 500;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .label-icon {
          color: var(--text-muted);
        }

        .form-input {
          background: var(--surface-raised);
          border: 1px solid var(--border-default);
          border-radius: var(--radius-md);
          color: var(--text-primary);
          padding: 0.75rem 1rem;
          font-size: 1rem;
          width: 100%;
          transition: all var(--transition-fast);
        }

        .form-input::placeholder {
          color: var(--text-muted);
        }

        .form-input:focus {
          outline: none;
          border-color: var(--border-focus);
          box-shadow: 0 0 0 3px var(--bg-accent);
        }

        .form-input:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .login-button {
          background: linear-gradient(135deg, #004B8E 0%, #0066B8 100%);
          border: none;
          border-radius: var(--radius-md);
          color: #ffffff;
          padding: 0.875rem 1.5rem;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          margin-top: 0.5rem;
          transition: all var(--transition-fast);
        }

        .login-button:hover:not(:disabled) {
          background: linear-gradient(135deg, #003d75 0%, #0055a3 100%);
          box-shadow: 0 4px 15px rgba(0, 75, 142, 0.4);
          transform: translateY(-1px);
        }

        .login-button:active:not(:disabled) {
          transform: translateY(0);
        }

        .login-button:disabled {
          background: var(--surface-raised);
          color: var(--text-muted);
          cursor: not-allowed;
        }

        .button-icon {
          font-size: 1rem;
        }

        .spinner {
          width: 18px;
          height: 18px;
          border: 2px solid transparent;
          border-top-color: currentColor;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        .login-footer {
          margin-top: 2rem;
          padding-top: 1.5rem;
          border-top: 1px solid var(--border-default);
          text-align: center;
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .login-footer span {
          color: var(--text-muted);
          font-size: 0.75rem;
        }

        .login-footer code {
          background: var(--surface-raised);
          padding: 0.25rem 0.5rem;
          border-radius: var(--radius-sm);
          color: var(--text-accent);
          font-size: 0.75rem;
        }
      `}</style>
    </div>
  );
}

export default LoginForm;
