/**
 * User Service
 * Handles user management API calls (Admin only)
 */
import { authApi } from './authService';

const userService = {
  /**
   * List all users
   */
  listUsers: async (skip = 0, limit = 100) => {
    return authApi.get('/users', { params: { skip, limit } });
  },

  /**
   * Get user by ID
   */
  getUser: async (userId) => {
    return authApi.get(`/users/${userId}`);
  },

  /**
   * Create a new user
   */
  createUser: async (userData) => {
    return authApi.post('/users', userData);
  },

  /**
   * Update a user
   */
  updateUser: async (userId, userData) => {
    return authApi.put(`/users/${userId}`, userData);
  },

  /**
   * Delete a user
   */
  deleteUser: async (userId) => {
    return authApi.delete(`/users/${userId}`);
  },

  /**
   * Update user role (Admin only)
   */
  updateRole: async (userId, role) => {
    return authApi.put(`/users/${userId}/role`, { role });
  },

  /**
   * Update user permissions (Admin only, for analysts)
   */
  updatePermissions: async (userId, permissions) => {
    return authApi.put(`/users/${userId}/permissions`, { permissions });
  },

  /**
   * Reset user password (Admin only)
   */
  resetPassword: async (userId, newPassword) => {
    return authApi.put(`/users/${userId}/password`, { new_password: newPassword });
  }
};

export default userService;
