/**
 * Validation Utilities
 * Reusable validators for form inputs
 */

/**
 * Validate email address
 * @param {string} email - Email address to validate
 * @returns {boolean} True if valid
 */
export const isValidEmail = (email) => {
  if (!email) return false;

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate IPv4 address
 * @param {string} ip - IP address to validate
 * @returns {boolean} True if valid
 */
export const isValidIPv4 = (ip) => {
  if (!ip) return false;

  const ipv4Regex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  return ipv4Regex.test(ip);
};

/**
 * Validate IPv6 address
 * @param {string} ip - IP address to validate
 * @returns {boolean} True if valid
 */
export const isValidIPv6 = (ip) => {
  if (!ip) return false;

  const ipv6Regex = /^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$/;
  return ipv6Regex.test(ip);
};

/**
 * Validate IP address (IPv4 or IPv6)
 * @param {string} ip - IP address to validate
 * @returns {boolean} True if valid
 */
export const isValidIP = (ip) => {
  return isValidIPv4(ip) || isValidIPv6(ip);
};

/**
 * Validate port number
 * @param {number|string} port - Port number to validate
 * @returns {boolean} True if valid
 */
export const isValidPort = (port) => {
  const portNum = parseInt(port);
  return !isNaN(portNum) && portNum >= 1 && portNum <= 65535;
};

/**
 * Validate URL
 * @param {string} url - URL to validate
 * @returns {boolean} True if valid
 */
export const isValidURL = (url) => {
  if (!url) return false;

  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

/**
 * Validate username (alphanumeric, underscore, hyphen, 3-30 chars)
 * @param {string} username - Username to validate
 * @returns {boolean} True if valid
 */
export const isValidUsername = (username) => {
  if (!username) return false;

  const usernameRegex = /^[a-zA-Z0-9_-]{3,30}$/;
  return usernameRegex.test(username);
};

/**
 * Validate required field (not empty)
 * @param {any} value - Value to validate
 * @returns {boolean} True if not empty
 */
export const isRequired = (value) => {
  if (value === undefined || value === null) return false;
  if (typeof value === 'string') return value.trim().length > 0;
  if (typeof value === 'number') return true;
  if (typeof value === 'boolean') return true;
  return false;
};

/**
 * Validate minimum length
 * @param {string} value - Value to validate
 * @param {number} min - Minimum length
 * @returns {boolean} True if meets minimum
 */
export const hasMinLength = (value, min) => {
  if (!value) return false;
  return value.length >= min;
};

/**
 * Validate maximum length
 * @param {string} value - Value to validate
 * @param {number} max - Maximum length
 * @returns {boolean} True if within maximum
 */
export const hasMaxLength = (value, max) => {
  if (!value) return true; // Empty is valid for max length
  return value.length <= max;
};

/**
 * Validate number range
 * @param {number|string} value - Value to validate
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {boolean} True if within range
 */
export const isInRange = (value, min, max) => {
  const num = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(num)) return false;
  return num >= min && num <= max;
};

/**
 * Validate datetime-local format (YYYY-MM-DDTHH:MM)
 * @param {string} datetime - Datetime string to validate
 * @returns {boolean} True if valid
 */
export const isValidDatetime = (datetime) => {
  if (!datetime) return false;

  const datetimeRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/;
  if (!datetimeRegex.test(datetime)) return false;

  const date = new Date(datetime);
  return !isNaN(date.getTime());
};

/**
 * Validate hexadecimal string
 * @param {string} hex - Hex string to validate
 * @returns {boolean} True if valid
 */
export const isValidHex = (hex) => {
  if (!hex) return false;

  const hexRegex = /^[0-9A-Fa-f]+$/;
  return hexRegex.test(hex);
};

// Export validators as default object
export default {
  isValidEmail,
  isValidIPv4,
  isValidIPv6,
  isValidIP,
  isValidPort,
  isValidURL,
  isValidUsername,
  isRequired,
  hasMinLength,
  hasMaxLength,
  isInRange,
  isValidDatetime,
  isValidHex
};
