/**
 * UsersPage Component
 * User management page (Admin only)
 */
import React, { useState, useEffect, useCallback } from 'react';
import { Card } from 'react-bootstrap';
import MainLayout from '../components/layout/MainLayout';
import UserManagement from '../components/users/UserManagement';
import userService from '../services/userService';

function UsersPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadUsers = useCallback(async () => {
    try {
      setLoading(true);
      const data = await userService.listUsers();
      setUsers(data);
    } catch (err) {
      console.error('Error loading users:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  const handleCreate = async (userData) => {
    await userService.createUser(userData);
    loadUsers();
  };

  const handleUpdate = async (userId, userData) => {
    await userService.updateUser(userId, userData);
    loadUsers();
  };

  const handleDelete = async (userId) => {
    await userService.deleteUser(userId);
    loadUsers();
  };

  const handleUpdateRole = async (userId, role) => {
    await userService.updateRole(userId, role);
    loadUsers();
  };

  const handleUpdatePermissions = async (userId, permissions) => {
    await userService.updatePermissions(userId, permissions);
    loadUsers();
  };

  const handleResetPassword = async (userId, newPassword) => {
    await userService.resetPassword(userId, newPassword);
    // No need to reload users for password reset
  };

  return (
    <MainLayout title="Gestion de Usuarios">
      <Card className="shadow-sm">
        <Card.Body>
          <UserManagement
            users={users}
            loading={loading}
            onCreate={handleCreate}
            onUpdate={handleUpdate}
            onDelete={handleDelete}
            onUpdateRole={handleUpdateRole}
            onUpdatePermissions={handleUpdatePermissions}
            onResetPassword={handleResetPassword}
          />
        </Card.Body>
      </Card>
    </MainLayout>
  );
}

export default UsersPage;
