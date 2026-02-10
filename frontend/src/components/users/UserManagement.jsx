/**
 * UserManagement Component
 * CRUD interface for managing users (Admin only)
 */
import React, { useState } from 'react';
import { Table, Button, Badge, Modal, Form, Alert, Spinner, Tabs, Tab } from 'react-bootstrap';
import { FaEdit, FaTrash, FaUserPlus, FaUsers, FaKey, FaShieldAlt, FaHome, FaBrain, FaChartBar, FaBell } from 'react-icons/fa';
import PermissionsEditor from './PermissionsEditor';

const DEFAULT_PERMISSIONS = {
  dashboard: true,
  predictions: false,
  reports: true,
  alerts: true
};

function UserManagement({ users, loading, onCreate, onUpdate, onDelete, onUpdateRole, onUpdatePermissions, onResetPassword }) {
  const [showModal, setShowModal] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    role: 'analyst',
    permissions: { ...DEFAULT_PERMISSIONS }
  });
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  // Password reset modal state
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [passwordUser, setPasswordUser] = useState(null);
  const [newPassword, setNewPassword] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [passwordSaving, setPasswordSaving] = useState(false);

  const handleOpenCreate = () => {
    setEditingUser(null);
    setFormData({
      username: '',
      email: '',
      password: '',
      full_name: '',
      role: 'analyst',
      permissions: { ...DEFAULT_PERMISSIONS }
    });
    setError('');
    setShowModal(true);
  };

  const handleOpenEdit = (user) => {
    setEditingUser(user);
    setFormData({
      username: user.username,
      email: user.email,
      password: '',
      full_name: user.full_name || '',
      role: user.role,
      permissions: user.permissions || { ...DEFAULT_PERMISSIONS }
    });
    setError('');
    setShowModal(true);
  };

  const handleOpenPasswordReset = (user) => {
    setPasswordUser(user);
    setNewPassword('');
    setPasswordError('');
    setShowPasswordModal(true);
  };

  const handlePasswordReset = async (e) => {
    e.preventDefault();
    if (newPassword.length < 6) {
      setPasswordError('La contrasena debe tener al menos 6 caracteres');
      return;
    }
    setPasswordSaving(true);
    setPasswordError('');

    try {
      await onResetPassword(passwordUser.id, newPassword);
      setShowPasswordModal(false);
    } catch (err) {
      setPasswordError(err.response?.data?.detail || 'Error al resetear contrasena');
    } finally {
      setPasswordSaving(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSaving(true);

    try {
      if (editingUser) {
        // Update existing user basic info
        const updateData = {
          email: formData.email,
          full_name: formData.full_name
        };
        if (formData.password) {
          updateData.password = formData.password;
        }
        await onUpdate(editingUser.id, updateData);

        // Update role if changed
        if (formData.role !== editingUser.role && onUpdateRole) {
          await onUpdateRole(editingUser.id, formData.role);
        }

        // Update permissions if analyst and permissions changed
        if (formData.role === 'analyst' && onUpdatePermissions) {
          await onUpdatePermissions(editingUser.id, formData.permissions);
        }
      } else {
        // Create new user
        if (!formData.password) {
          setError('La contrasena es requerida para nuevos usuarios');
          setSaving(false);
          return;
        }
        await onCreate({
          ...formData,
          permissions: formData.role === 'analyst' ? formData.permissions : undefined
        });
      }
      setShowModal(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al guardar usuario');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (userId, username) => {
    if (window.confirm(`¿Eliminar usuario "${username}"? Esta accion no se puede deshacer.`)) {
      try {
        await onDelete(userId);
      } catch (err) {
        alert(err.response?.data?.detail || 'Error al eliminar usuario');
      }
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-ES');
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2 text-muted">Cargando usuarios...</p>
      </div>
    );
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h5 className="mb-0">
          <FaUsers className="me-2" />
          Usuarios del Sistema
        </h5>
        <Button
          variant="primary"
          onClick={handleOpenCreate}
        >
          <FaUserPlus className="me-2" />
          Nuevo Usuario
        </Button>
      </div>

      <Table responsive hover className="align-middle">
        <thead className="bg-light">
          <tr>
            <th>Usuario</th>
            <th>Email</th>
            <th>Nombre</th>
            <th>Rol</th>
            <th>Permisos</th>
            <th>Estado</th>
            <th>Creado</th>
            <th className="text-end">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>
                <div className="d-flex align-items-center">
                  <div
                    className="d-flex align-items-center justify-content-center rounded-circle text-white me-2"
                    style={{
                      width: '32px',
                      height: '32px',
                      background: user.role === 'admin'
                        ? 'var(--interactive-primary)'
                        : 'var(--color-slate-500, #64748b)'
                    }}
                  >
                    {user.username.charAt(0).toUpperCase()}
                  </div>
                  <strong>{user.username}</strong>
                </div>
              </td>
              <td>{user.email}</td>
              <td>{user.full_name || '-'}</td>
              <td>
                <Badge bg={user.role === 'admin' ? 'primary' : 'secondary'}>
                  {user.role === 'admin' ? 'Administrador' : 'Analista'}
                </Badge>
              </td>
              <td>
                {user.role === 'admin' ? (
                  <Badge bg="primary">Acceso Total</Badge>
                ) : (
                  <div className="d-flex flex-wrap gap-1">
                    {user.permissions?.dashboard && (
                      <Badge bg="info" title="Dashboard"><FaHome size={10} /></Badge>
                    )}
                    {user.permissions?.predictions && (
                      <Badge bg="info" title="Predicciones"><FaBrain size={10} /></Badge>
                    )}
                    {user.permissions?.reports && (
                      <Badge bg="info" title="Reportes"><FaChartBar size={10} /></Badge>
                    )}
                    {user.permissions?.alerts && (
                      <Badge bg="info" title="Alertas"><FaBell size={10} /></Badge>
                    )}
                  </div>
                )}
              </td>
              <td>
                <Badge bg={user.is_active ? 'success' : 'danger'}>
                  {user.is_active ? 'Activo' : 'Inactivo'}
                </Badge>
              </td>
              <td>
                <small>{formatDate(user.created_at)}</small>
              </td>
              <td className="text-end">
                <Button
                  variant="outline-primary"
                  size="sm"
                  className="me-1"
                  onClick={() => handleOpenEdit(user)}
                  title="Editar usuario"
                >
                  <FaEdit />
                </Button>
                <Button
                  variant="outline-warning"
                  size="sm"
                  className="me-1"
                  onClick={() => handleOpenPasswordReset(user)}
                  title="Resetear contrasena"
                >
                  <FaKey />
                </Button>
                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={() => handleDelete(user.id, user.username)}
                  title="Eliminar usuario"
                >
                  <FaTrash />
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      {/* Create/Edit Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)} centered size="lg">
        <Modal.Header closeButton>
          <Modal.Title>
            {editingUser ? 'Editar Usuario' : 'Nuevo Usuario'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            {error && <Alert variant="danger">{error}</Alert>}

            <Tabs defaultActiveKey="info" className="mb-3">
              <Tab eventKey="info" title="Informacion">
                <Form.Group className="mb-3">
                  <Form.Label>Usuario</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    disabled={!!editingUser}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Nombre Completo</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.full_name}
                    onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                  />
                </Form.Group>

                {!editingUser && (
                  <Form.Group className="mb-3">
                    <Form.Label>Contrasena</Form.Label>
                    <Form.Control
                      type="password"
                      value={formData.password}
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                      required
                      minLength={6}
                    />
                    <Form.Text className="text-muted">Minimo 6 caracteres</Form.Text>
                  </Form.Group>
                )}

                <Form.Group className="mb-3">
                  <Form.Label>Rol</Form.Label>
                  <Form.Select
                    value={formData.role}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                  >
                    <option value="analyst">Analista SOC</option>
                    <option value="admin">Administrador</option>
                  </Form.Select>
                  <Form.Text className="text-muted">
                    {formData.role === 'admin'
                      ? 'Los administradores tienen acceso total al sistema.'
                      : 'Los analistas tienen acceso segun los permisos configurados.'}
                  </Form.Text>
                </Form.Group>
              </Tab>

              <Tab eventKey="permissions" title={<><FaShieldAlt className="me-1" />Permisos</>}>
                <PermissionsEditor
                  permissions={formData.permissions}
                  onChange={(perms) => setFormData({ ...formData, permissions: perms })}
                  disabled={formData.role === 'admin'}
                />
              </Tab>
            </Tabs>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Cancelar
            </Button>
            <Button
              type="submit"
              variant="primary"
              disabled={saving}
            >
              {saving ? 'Guardando...' : 'Guardar'}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>

      {/* Password Reset Modal */}
      <Modal show={showPasswordModal} onHide={() => setShowPasswordModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>
            <FaKey className="me-2" />
            Resetear Contrasena
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handlePasswordReset}>
          <Modal.Body>
            {passwordError && <Alert variant="danger">{passwordError}</Alert>}

            <p className="text-muted">
              Resetear la contrasena de <strong>{passwordUser?.username}</strong>
            </p>

            <Form.Group className="mb-3">
              <Form.Label>Nueva Contrasena</Form.Label>
              <Form.Control
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                minLength={6}
                placeholder="Ingrese nueva contrasena"
              />
              <Form.Text className="text-muted">Minimo 6 caracteres</Form.Text>
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowPasswordModal(false)}>
              Cancelar
            </Button>
            <Button
              type="submit"
              variant="warning"
              disabled={passwordSaving}
            >
              {passwordSaving ? 'Reseteando...' : 'Resetear Contrasena'}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </>
  );
}

export default UserManagement;
