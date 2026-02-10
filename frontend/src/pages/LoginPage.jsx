/**
 * LoginPage Component
 * Split layout with animated visual panel - BCP branding
 */
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import LoginForm from '../components/auth/LoginForm';
import { FaShieldAlt, FaBrain, FaLock, FaNetworkWired } from 'react-icons/fa';

function LoginPage() {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, isAuthenticated } = useAuth();
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
      {/* Visual Panel - Left Side */}
      <div className="login-visual-panel">
        <div className="visual-overlay"></div>

        {/* Floating Icons */}
        <div className="floating-icons">
          <div className="floating-icon icon-1"><FaShieldAlt /></div>
          <div className="floating-icon icon-2"><FaBrain /></div>
          <div className="floating-icon icon-3"><FaLock /></div>
          <div className="floating-icon icon-4"><FaNetworkWired /></div>
        </div>

        <div className="visual-content">
          <h2 className="visual-title">Protegiendo el futuro digital del BCP</h2>
          <p className="visual-description">
            Sistema inteligente de deteccion de amenazas en tiempo real
            con Machine Learning
          </p>

          <div className="model-badges">
            <div className="model-badge">
              <FaShieldAlt className="badge-icon" />
              <span>Phishing Detection</span>
            </div>
            <div className="model-badge">
              <FaBrain className="badge-icon" />
              <span>Account Takeover</span>
            </div>
            <div className="model-badge">
              <FaNetworkWired className="badge-icon" />
              <span>Brute Force</span>
            </div>
          </div>

        </div>
      </div>

      {/* Login Form Panel - Right Side */}
      <div className="login-form-panel">
        <div className="login-container">
          <LoginForm
            onSubmit={handleLogin}
            error={error}
            loading={loading}
          />
        </div>
      </div>

      <style>{`
        .login-page {
          min-height: 100vh;
          display: flex;
          background: var(--bg-primary);
        }

        /* Visual Panel - Left Side */
        .login-visual-panel {
          flex: 1;
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(-45deg, #004B8E, #0066B8, #F26E29, #E56A00);
          background-size: 400% 400%;
          animation: gradientShift 15s ease infinite;
          overflow: hidden;
        }

        @keyframes gradientShift {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }

        .visual-overlay {
          position: absolute;
          inset: 0;
          background: rgba(0, 0, 0, 0.3);
          backdrop-filter: blur(1px);
        }

        /* Floating Icons Animation */
        .floating-icons {
          position: absolute;
          inset: 0;
          pointer-events: none;
        }

        .floating-icon {
          position: absolute;
          color: rgba(255, 255, 255, 0.15);
          font-size: 3rem;
          animation: float 6s ease-in-out infinite;
        }

        .icon-1 {
          top: 15%;
          left: 10%;
          animation-delay: 0s;
        }

        .icon-2 {
          top: 25%;
          right: 15%;
          animation-delay: 1.5s;
          font-size: 2.5rem;
        }

        .icon-3 {
          bottom: 25%;
          left: 20%;
          animation-delay: 3s;
          font-size: 2rem;
        }

        .icon-4 {
          bottom: 15%;
          right: 10%;
          animation-delay: 4.5s;
          font-size: 2.5rem;
        }

        @keyframes float {
          0%, 100% {
            transform: translateY(0) rotate(0deg);
            opacity: 0.15;
          }
          50% {
            transform: translateY(-20px) rotate(5deg);
            opacity: 0.25;
          }
        }

        /* Visual Content */
        .visual-content {
          position: relative;
          z-index: 1;
          text-align: center;
          padding: 2rem;
          max-width: 500px;
        }

        .visual-title {
          color: #ffffff;
          font-size: 2rem;
          font-weight: 700;
          margin: 0 0 1rem;
          text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }

        .visual-description {
          color: rgba(255, 255, 255, 0.9);
          font-size: 1rem;
          margin: 0 0 2rem;
          line-height: 1.6;
        }

        /* Model Badges */
        .model-badges {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .model-badge {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.75rem;
          background: rgba(255, 255, 255, 0.15);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.25);
          border-radius: 50px;
          padding: 0.75rem 1.5rem;
          color: #ffffff;
          font-size: 0.875rem;
          font-weight: 500;
          transition: all 0.3s ease;
        }

        .model-badge:hover {
          background: rgba(255, 255, 255, 0.25);
          transform: translateX(5px);
        }

        .badge-icon {
          font-size: 1rem;
        }

        /* Login Form Panel - Right Side */
        .login-form-panel {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem;
          background: var(--bg-primary);
        }

        .login-container {
          width: 100%;
          max-width: 420px;
        }

        /* Responsive Design */
        @media (max-width: 968px) {
          .login-page {
            flex-direction: column;
          }

          .login-visual-panel {
            padding: 2rem;
            min-height: auto;
          }

          .visual-title {
            font-size: 1.5rem;
          }

          .visual-description {
            margin-bottom: 1.5rem;
          }

          .model-badges {
            flex-direction: row;
            flex-wrap: wrap;
            justify-content: center;
          }

          .model-badge {
            padding: 0.5rem 1rem;
            font-size: 0.75rem;
          }

          .floating-icons {
            display: none;
          }
        }

        @media (max-width: 600px) {
          .login-visual-panel {
            padding: 1.5rem;
          }

          .visual-title {
            font-size: 1.25rem;
          }

          .visual-description {
            display: none;
          }

          .login-form-panel {
            padding: 1.5rem;
          }
        }
      `}</style>
    </div>
  );
}

export default LoginPage;
