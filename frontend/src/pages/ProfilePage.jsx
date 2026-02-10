/**
 * ProfilePage Component
 * User profile management page
 */
import React, { useState, useEffect } from 'react';
import { Card, Form, Button, Alert, Row, Col, Badge, Spinner } from 'react-bootstrap';
import { FaUser, FaEnvelope, FaIdCard, FaCalendar, FaShieldAlt, FaKey, FaSave, FaHome, FaBrain, FaChartBar, FaBell } from 'react-icons/fa';
import MainLayout from '../components/layout/MainLayout';
import { useAuth } from '../context/AuthContext';
import profileService from '../services/profileService';

function ProfilePage() {
  const { user, refreshProfile } = useAuth();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);

  // Edit profile state
  const [editForm, setEditForm] = useState({ email: '', full_name: '' });
  const [editError, setEditError] = useState('');
  const [editSuccess, setEditSuccess] = useState('');
  const [editSaving, setEditSaving] = useState(false);

  // Password change state
  const [passwordForm, setPasswordForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [passwordError, setPasswordError] = useState('');
  const [passwordSuccess, setPasswordSuccess] = useState('');
  const [passwordSaving, setPasswordSaving] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const data = await profileService.getProfile();
      setProfile(data);
      setEditForm({
        email: data.email || '',
        full_name: data.full_name || ''
      });
    } catch (err) {
      console.error('Error loading profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    setEditError('');
    setEditSuccess('');
    setEditSaving(true);

    try {
      await profileService.updateProfile(editForm);
      setEditSuccess('Perfil actualizado correctamente');
      await refreshProfile();
      await loadProfile();
    } catch (err) {
      setEditError(err.response?.data?.detail || 'Error al actualizar perfil');
    } finally {
      setEditSaving(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setPasswordError('');
    setPasswordSuccess('');

    if (passwordForm.new_password !== passwordForm.confirm_password) {
      setPasswordError('Las contrasenas no coinciden');
      return;
    }

    if (passwordForm.new_password.length < 6) {
      setPasswordError('La nueva contrasena debe tener al menos 6 caracteres');
      return;
    }

    setPasswordSaving(true);

    try {
      await profileService.changePassword(
        passwordForm.current_password,
        passwordForm.new_password
      );
      setPasswordSuccess('Contrasena cambiada correctamente');
      setPasswordForm({
        current_password: '',
        new_password: '',
        confirm_password: ''
      });
    } catch (err) {
      setPasswordError(err.response?.data?.detail || 'Error al cambiar contrasena');
    } finally {
      setPasswordSaving(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const permissionLabels = {
    dashboard: { label: 'Dashboard', icon: FaHome },
    predictions: { label: 'Predicciones', icon: FaBrain },
    reports: { label: 'Reportes', icon: FaChartBar },
    alerts: { label: 'Alertas', icon: FaBell }
  };

  if (loading) {
    return (
      <MainLayout title="Mi Perfil">
        <div className="text-center py-5">
          <Spinner animation="border" variant="primary" />
          <p className="mt-2 text-muted">Cargando perfil...</p>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout title="Mi Perfil">
      <Row className="g-4">
        {/* User Info Card */}
        <Col lg={4}>
          <Card className="shadow-sm h-100">
            <Card.Body className="text-center">
              <div
                className="d-inline-flex align-items-center justify-content-center rounded-circle mb-3"
                style={{
                  width: '80px',
                  height: '80px',
                  background: 'var(--interactive-primary)',
                  color: 'white',
                  fontSize: '2rem',
                  fontWeight: 'bold'
                }}
              >
                {profile?.username?.charAt(0).toUpperCase()}
              </div>

              <h4 className="mb-1">{profile?.username}</h4>
              <Badge bg={profile?.role === 'admin' ? 'primary' : 'secondary'} className="mb-3">
                {profile?.role === 'admin' ? 'Administrador' : 'Analista'}
              </Badge>

              <hr />

              <div className="text-start">
                <div className="d-flex align-items-center mb-2">
                  <FaEnvelope className="text-muted me-2" />
                  <span>{profile?.email}</span>
                </div>
                <div className="d-flex align-items-center mb-2">
                  <FaIdCard className="text-muted me-2" />
                  <span>{profile?.full_name || 'Sin nombre'}</span>
                </div>
                <div className="d-flex align-items-center mb-2">
                  <FaCalendar className="text-muted me-2" />
                  <span>Miembro desde {formatDate(profile?.created_at)}</span>
                </div>
                <div className="d-flex align-items-center">
                  <FaShieldAlt className="text-muted me-2" />
                  <Badge bg={profile?.is_active ? 'success' : 'danger'}>
                    {profile?.is_active ? 'Activo' : 'Inactivo'}
                  </Badge>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>

        {/* Edit Profile & Password Cards */}
        <Col lg={8}>
          {/* Edit Profile */}
          <Card className="shadow-sm mb-4">
            <Card.Header className="bg-white">
              <h5 className="mb-0">
                <FaUser className="me-2" />
                Editar Informacion
              </h5>
            </Card.Header>
            <Card.Body>
              {editError && <Alert variant="danger">{editError}</Alert>}
              {editSuccess && <Alert variant="success">{editSuccess}</Alert>}

              <Form onSubmit={handleEditSubmit}>
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Email</Form.Label>
                      <Form.Control
                        type="email"
                        value={editForm.email}
                        onChange={(e) => setEditForm({ ...editForm, email: e.target.value })}
                        required
                      />
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Nombre Completo</Form.Label>
                      <Form.Control
                        type="text"
                        value={editForm.full_name}
                        onChange={(e) => setEditForm({ ...editForm, full_name: e.target.value })}
                      />
                    </Form.Group>
                  </Col>
                </Row>
                <Button type="submit" variant="primary" disabled={editSaving}>
                  <FaSave className="me-2" />
                  {editSaving ? 'Guardando...' : 'Guardar Cambios'}
                </Button>
              </Form>
            </Card.Body>
          </Card>

          {/* Change Password */}
          <Card className="shadow-sm mb-4">
            <Card.Header className="bg-white">
              <h5 className="mb-0">
                <FaKey className="me-2" />
                Cambiar Contrasena
              </h5>
            </Card.Header>
            <Card.Body>
              {passwordError && <Alert variant="danger">{passwordError}</Alert>}
              {passwordSuccess && <Alert variant="success">{passwordSuccess}</Alert>}

              <Form onSubmit={handlePasswordSubmit}>
                <Row>
                  <Col md={4}>
                    <Form.Group className="mb-3">
                      <Form.Label>Contrasena Actual</Form.Label>
                      <Form.Control
                        type="password"
                        value={passwordForm.current_password}
                        onChange={(e) => setPasswordForm({ ...passwordForm, current_password: e.target.value })}
                        required
                      />
                    </Form.Group>
                  </Col>
                  <Col md={4}>
                    <Form.Group className="mb-3">
                      <Form.Label>Nueva Contrasena</Form.Label>
                      <Form.Control
                        type="password"
                        value={passwordForm.new_password}
                        onChange={(e) => setPasswordForm({ ...passwordForm, new_password: e.target.value })}
                        required
                        minLength={6}
                      />
                    </Form.Group>
                  </Col>
                  <Col md={4}>
                    <Form.Group className="mb-3">
                      <Form.Label>Confirmar Contrasena</Form.Label>
                      <Form.Control
                        type="password"
                        value={passwordForm.confirm_password}
                        onChange={(e) => setPasswordForm({ ...passwordForm, confirm_password: e.target.value })}
                        required
                      />
                    </Form.Group>
                  </Col>
                </Row>
                <Button type="submit" variant="warning" disabled={passwordSaving}>
                  <FaKey className="me-2" />
                  {passwordSaving ? 'Cambiando...' : 'Cambiar Contrasena'}
                </Button>
              </Form>
            </Card.Body>
          </Card>

          {/* Permissions (only for analysts) */}
          {profile?.role !== 'admin' && (
            <Card className="shadow-sm">
              <Card.Header className="bg-white">
                <h5 className="mb-0">
                  <FaShieldAlt className="me-2" />
                  Mis Permisos
                </h5>
              </Card.Header>
              <Card.Body>
                <p className="text-muted small mb-3">
                  Estos permisos son gestionados por el administrador. Contacte al administrador si necesita cambios.
                </p>
                <div className="d-flex flex-wrap gap-3">
                  {Object.entries(permissionLabels).map(([key, { label, icon: Icon }]) => {
                    const hasPermission = profile?.permissions?.[key] === true;
                    return (
                      <div
                        key={key}
                        className={`d-flex align-items-center px-3 py-2 rounded ${
                          hasPermission ? 'bg-success bg-opacity-10' : 'bg-secondary bg-opacity-10'
                        }`}
                      >
                        <Icon className={`me-2 ${hasPermission ? 'text-success' : 'text-muted'}`} />
                        <span className={hasPermission ? 'text-success' : 'text-muted'}>
                          {label}
                        </span>
                        <Badge
                          bg={hasPermission ? 'success' : 'secondary'}
                          className="ms-2"
                        >
                          {hasPermission ? 'SI' : 'NO'}
                        </Badge>
                      </div>
                    );
                  })}
                </div>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </MainLayout>
  );
}

export default ProfilePage;
