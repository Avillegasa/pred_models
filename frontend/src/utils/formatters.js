/**
 * Formatter Utilities
 * Functions for formatting data for display
 */

/**
 * Format probability/confidence as percentage
 * @param {number} value - Value between 0 and 1
 * @param {number} decimals - Number of decimal places (default: 1)
 * @returns {string} Formatted percentage string
 */
export const formatPercentage = (value, decimals = 1) => {
  if (value === undefined || value === null || isNaN(value)) return '0%';

  const percentage = value * 100;
  return `${percentage.toFixed(decimals)}%`;
};

/**
 * Format date/time to localized string
 * @param {string|Date} datetime - Datetime to format
 * @param {boolean} includeTime - Include time in output (default: true)
 * @returns {string} Formatted datetime string
 */
export const formatDatetime = (datetime, includeTime = true) => {
  if (!datetime) return 'N/A';

  const date = typeof datetime === 'string' ? new Date(datetime) : datetime;

  if (isNaN(date.getTime())) return 'Fecha invalida';

  if (includeTime) {
    return date.toLocaleString('es-ES', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  }

  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
};

/**
 * Format processing time in milliseconds
 * @param {number} ms - Time in milliseconds
 * @returns {string} Formatted time string
 */
export const formatProcessingTime = (ms) => {
  if (ms === undefined || ms === null || isNaN(ms)) return 'N/A';

  if (ms < 1000) {
    return `${Math.round(ms)}ms`;
  }

  const seconds = ms / 1000;
  return `${seconds.toFixed(2)}s`;
};

/**
 * Format large numbers with thousands separators
 * @param {number} num - Number to format
 * @returns {string} Formatted number string
 */
export const formatNumber = (num) => {
  if (num === undefined || num === null || isNaN(num)) return '0';

  return num.toLocaleString('es-ES');
};

/**
 * Truncate text with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export const truncateText = (text, maxLength = 100) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;

  return text.substring(0, maxLength) + '...';
};

/**
 * Capitalize first letter
 * @param {string} str - String to capitalize
 * @returns {string} Capitalized string
 */
export const capitalize = (str) => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

/**
 * Format prediction label for display
 * @param {string} label - Prediction label
 * @returns {string} Formatted label
 */
export const formatPredictionLabel = (label) => {
  if (!label) return 'Desconocido';

  // Convert to title case and remove underscores
  return label
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => capitalize(word))
    .join(' ');
};

/**
 * Format IP address (add zero-padding if needed)
 * @param {string} ip - IP address
 * @returns {string} Formatted IP
 */
export const formatIP = (ip) => {
  if (!ip) return '';
  return ip.trim();
};

/**
 * Format bytes to human-readable size
 * @param {number} bytes - Number of bytes
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted size string
 */
export const formatBytes = (bytes, decimals = 2) => {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

/**
 * Format severity/threat level with color code
 * Uses design tokens from theme for consistent styling
 * @param {string} level - Severity level
 * @returns {Object} Object with formatted text and color
 */
export const formatSeverityLevel = (level) => {
  // Design tokens - matching BCP theme.js primitives
  const colors = {
    danger: '#E53E3E',   // BCP red-500
    warning: '#ECC94B',  // BCP amber-500
    info: '#00498C',     // BCP blue-600 (primary)
    muted: '#808080'     // BCP gray-500
  };

  if (!level) return { text: 'Desconocido', color: colors.muted };

  const normalized = level.toLowerCase();

  const severityMap = {
    critical: { text: 'Critico', color: colors.danger, icon: '🔴' },
    critico: { text: 'Critico', color: colors.danger, icon: '🔴' },
    severe: { text: 'Severo', color: colors.danger, icon: '🔴' },
    severo: { text: 'Severo', color: colors.danger, icon: '🔴' },
    high: { text: 'Alto', color: colors.danger, icon: '🟠' },
    alto: { text: 'Alto', color: colors.danger, icon: '🟠' },
    medium: { text: 'Medio', color: colors.warning, icon: '🟡' },
    medio: { text: 'Medio', color: colors.warning, icon: '🟡' },
    moderate: { text: 'Moderado', color: colors.warning, icon: '🟡' },
    moderado: { text: 'Moderado', color: colors.warning, icon: '🟡' },
    low: { text: 'Bajo', color: colors.info, icon: '🟢' },
    bajo: { text: 'Bajo', color: colors.info, icon: '🟢' },
    minimal: { text: 'Minimo', color: colors.info, icon: '🟢' },
    minimo: { text: 'Minimo', color: colors.info, icon: '🟢' }
  };

  return severityMap[normalized] || { text: capitalize(level), color: colors.muted, icon: '⚪' };
};

/**
 * Format confidence level to text description
 * @param {number} confidence - Confidence value (0-1)
 * @returns {string} Text description
 */
export const formatConfidenceLevel = (confidence) => {
  if (confidence === undefined || confidence === null) return 'Desconocido';

  if (confidence >= 0.9) return 'Muy Alto';
  if (confidence >= 0.7) return 'Alto';
  if (confidence >= 0.5) return 'Moderado';
  if (confidence >= 0.3) return 'Bajo';
  return 'Muy Bajo';
};

/**
 * Format model name (remove parentheses and clean up)
 * @param {string} modelName - Model name
 * @returns {string} Formatted model name
 */
export const formatModelName = (modelName) => {
  if (!modelName) return 'Modelo Desconocido';

  // Remove (Mock) suffix if present
  return modelName.replace(/\s*\(Mock\)\s*/gi, '').trim();
};

/**
 * Format error message for user display
 * @param {Object|string} error - Error object or string
 * @returns {string} User-friendly error message
 */
export const formatErrorMessage = (error) => {
  if (!error) return 'Ocurrio un error desconocido';

  if (typeof error === 'string') return error;

  if (error.message) return error.message;

  if (error.detail) return error.detail;

  return 'Ocurrio un error inesperado';
};

// Export all formatters
export default {
  formatPercentage,
  formatDatetime,
  formatProcessingTime,
  formatNumber,
  truncateText,
  capitalize,
  formatPredictionLabel,
  formatIP,
  formatBytes,
  formatSeverityLevel,
  formatConfidenceLevel,
  formatModelName,
  formatErrorMessage
};
