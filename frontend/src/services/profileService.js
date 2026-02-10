/**
 * Profile Service
 * Handles profile-related API calls for the current user
 */
import { authApi } from './authService';

const profileService = {
  /**
   * Get current user's profile
   */
  getProfile: async () => {
    return authApi.get('/profile');
  },

  /**
   * Update current user's profile (email and full_name)
   */
  updateProfile: async (profileData) => {
    return authApi.put('/profile', profileData);
  },

  /**
   * Change current user's password
   */
  changePassword: async (currentPassword, newPassword) => {
    return authApi.put('/profile/password', {
      current_password: currentPassword,
      new_password: newPassword
    });
  }
};

export default profileService;
