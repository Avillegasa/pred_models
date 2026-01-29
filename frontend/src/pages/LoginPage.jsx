/**
 * LoginPage Component
 * Full page login view - Swissborg dark theme
 */
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import LoginForm from '../components/auth/LoginForm';

function LoginPage() {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Clear any stale auth state when login page mounts
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token && !isAuthenticated()) {
      localStorage.removeItem('token');
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated()) {
      const from = location.state?.from?.pathname || '/dashboard';
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, location]);

  const handleLogin = async (username, password) => {
    setError('');
    setLoading(true);

    try {
      const result = await login(username, password);

      if (result.success) {
        const from = location.state?.from?.pathname || '/dashboard';
        navigate(from, { replace: true });
      } else {
        setError(result.error || 'Error al iniciar sesion');
      }
    } catch (err) {
      setError('Error de conexion. Verifique que el servidor este activo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <LoginForm
          onSubmit={handleLogin}
          error={error}
          loading={loading}
        />
      </div>

      <style>{`
        .login-page {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          background: var(--bg-primary);
          padding: 2rem;
        }

        .login-container {
          width: 100%;
          max-width: 420px;
        }
      `}</style>
    </div>
  );
}

export default LoginPage;
