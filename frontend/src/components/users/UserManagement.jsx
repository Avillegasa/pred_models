/**
 * UserManagement Component
 * CRUD interface for managing users (Admin only)
 */
import React, { useState } from 'react';
import { Table, Button, Badge, Modal, Form, Alert, Spinner } from 'react-bootstrap';
import { FaEdit, FaTrash, FaUserPlus, FaUsers } from 'react-icons/fa';

function UserManagement({ users, loading, onCreate, onUpdate, onDelete }) {
  const [showModal, setShowModal] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    role: 'analyst'
  });
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  const handleOpenCreate = () => {
    setEditingUser(null);
    setFormData({
      username: '',
      email: '',
      password: '',
      full_name: '',
      role: 'analyst'
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
      role: user.role
    });
    setError('');
    setShowModal(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSaving(true);

    try {
      if (editingUser) {
        // Update existing user
        const updateData = {
          email: formData.email,
          full_name: formData.full_name
        };
        if (formData.password) {
          updateData.password = formData.password;
        }
        await onUpdate(editingUser.id, updateData);
      } else {
        // Create new user
        if (!formData.password) {
          setError('La contrasena es requerida para nuevos usuarios');
          setSaving(false);
          return;
        }
        await onCreate(formData);
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
                        : 'var(--color-slate-500)'
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
                >
                  <FaEdit />
                </Button>
                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={() => handleDelete(user.id, user.username)}
                >
                  <FaTrash />
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      {/* Create/Edit Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>
            {editingUser ? 'Editar Usuario' : 'Nuevo Usuario'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            {error && <Alert variant="danger">{error}</Alert>}

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

            <Form.Group className="mb-3">
              <Form.Label>
                Contrasena {editingUser && <small className="text-muted">(dejar vacio para no cambiar)</small>}
              </Form.Label>
              <Form.Control
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required={!editingUser}
              />
            </Form.Group>

            {!editingUser && (
              <Form.Group className="mb-3">
                <Form.Label>Rol</Form.Label>
                <Form.Select
                  value={formData.role}
                  onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                >
                  <option value="analyst">Analista SOC</option>
                  <option value="admin">Administrador</option>
                </Form.Select>
              </Form.Group>
            )}
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
    </>
  );
}

export default UserManagement;
