/**
 * useFormValidation Hook
 * Custom hook for form state management and validation
 */

import { useState, useCallback } from 'react';

/**
 * Custom hook for form validation
 * @param {Object} initialState - Initial form state
 * @param {Object} validationRules - Validation rules for each field
 * @returns {Object} Form state and methods
 */
export const useFormValidation = (initialState, validationRules = {}) => {
  const [formData, setFormData] = useState(initialState);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  /**
   * Validate a single field
   * @param {string} name - Field name
   * @param {any} value - Field value
   * @returns {string|null} Error message or null
   */
  const validateField = useCallback((name, value) => {
    const rule = validationRules[name];
    if (!rule) return null;

    // Required check
    if (rule.required && (value === undefined || value === null || value === '')) {
      return rule.requiredMessage || `${rule.label || name} is required`;
    }

    // Skip other validations if value is empty and not required
    if (!value && !rule.required) {
      return null;
    }

    // Pattern validation (regex)
    if (rule.pattern) {
      const regex = typeof rule.pattern === 'string' ? new RegExp(rule.pattern) : rule.pattern;
      if (!regex.test(value)) {
        return rule.patternMessage || `Invalid format for ${rule.label || name}`;
      }
    }

    // Minimum value/length
    if (rule.min !== undefined) {
      if (typeof value === 'number' && value < rule.min) {
        return rule.minMessage || `Minimum value is ${rule.min}`;
      }
      if (typeof value === 'string' && value.length < rule.min) {
        return rule.minMessage || `Minimum length is ${rule.min} characters`;
      }
    }

    // Maximum value/length
    if (rule.max !== undefined) {
      if (typeof value === 'number' && value > rule.max) {
        return rule.maxMessage || `Maximum value is ${rule.max}`;
      }
      if (typeof value === 'string' && value.length > rule.max) {
        return rule.maxMessage || `Maximum length is ${rule.max} characters`;
      }
    }

    // Custom validator function
    if (rule.validator && typeof rule.validator === 'function') {
      const customError = rule.validator(value, formData);
      if (customError) {
        return customError;
      }
    }

    return null;
  }, [validationRules, formData]);

  /**
   * Handle input change
   */
  const handleChange = useCallback((e) => {
    const { name, value, type, checked } = e.target;
    const fieldValue = type === 'checkbox' ? checked : value;

    setFormData(prev => ({ ...prev, [name]: fieldValue }));

    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }
  }, [errors]);

  /**
   * Handle input blur
   */
  const handleBlur = useCallback((e) => {
    const { name, value } = e.target;

    // Mark field as touched
    setTouched(prev => ({ ...prev, [name]: true }));

    // Validate field
    const error = validateField(name, value);
    if (error) {
      setErrors(prev => ({ ...prev, [name]: error }));
    }
  }, [validateField]);

  /**
   * Validate all fields
   * @returns {boolean} True if form is valid
   */
  const validate = useCallback(() => {
    const newErrors = {};

    Object.keys(validationRules).forEach(fieldName => {
      const error = validateField(fieldName, formData[fieldName]);
      if (error) {
        newErrors[fieldName] = error;
      }
    });

    setErrors(newErrors);

    // Mark all fields as touched
    const allTouched = Object.keys(validationRules).reduce((acc, key) => {
      acc[key] = true;
      return acc;
    }, {});
    setTouched(allTouched);

    return Object.keys(newErrors).length === 0;
  }, [validationRules, formData, validateField]);

  /**
   * Reset form to initial state
   */
  const reset = useCallback(() => {
    setFormData(initialState);
    setErrors({});
    setTouched({});
  }, [initialState]);

  /**
   * Set form data programmatically
   */
  const setFormValues = useCallback((values) => {
    setFormData(prev => ({ ...prev, ...values }));
  }, []);

  /**
   * Set specific field value
   */
  const setFieldValue = useCallback((name, value) => {
    setFormData(prev => ({ ...prev, [name]: value }));

    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }
  }, [errors]);

  /**
   * Set specific field error
   */
  const setFieldError = useCallback((name, error) => {
    setErrors(prev => ({ ...prev, [name]: error }));
  }, []);

  /**
   * Clear errors
   */
  const clearErrors = useCallback(() => {
    setErrors({});
  }, []);

  /**
   * Check if form is valid (no errors)
   */
  const isValid = Object.keys(errors).length === 0;

  /**
   * Check if form has been modified
   */
  const isDirty = JSON.stringify(formData) !== JSON.stringify(initialState);

  return {
    // State
    formData,
    errors,
    touched,

    // Handlers
    handleChange,
    handleBlur,

    // Methods
    validate,
    reset,
    setFormValues,
    setFieldValue,
    setFieldError,
    clearErrors,

    // Computed
    isValid,
    isDirty
  };
};

export default useFormValidation;
