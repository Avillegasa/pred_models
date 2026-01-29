/**
 * Account Takeover Detection Form Component
 * Form for detecting suspicious login attempts
 */

import React from 'react';
import { Button } from 'react-bootstrap';
import { FiUser, FiGlobe, FiMapPin, FiChrome, FiMonitor, FiCheckCircle, FiAlertCircle, FiActivity, FiClock, FiCalendar } from 'react-icons/fi';
import FormInput from './FormInput';
import { useFormValidation } from '../../hooks/useFormValidation';
import { usePrediction } from '../../hooks/usePrediction';
import { isValidIP } from '../../utils/validators';

const AtaquesSospechososForm = () => {
  const { predict, isLoading } = usePrediction();

  // Get current datetime for default value (format for datetime-local input)
  const getCurrentDatetimeLocal = () => {
    const now = new Date();
    // Format: YYYY-MM-DDTHH:MM (for datetime-local input)
    return now.toISOString().slice(0, 16);
  };

  // Convert datetime-local to ISO string for API
  const toISOTimestamp = (datetimeLocal) => {
    if (!datetimeLocal) return new Date().toISOString();
    return new Date(datetimeLocal).toISOString();
  };

  const initialState = {
    userId: '',
    ipAddress: '',
    country: 'US',
    region: '',
    city: '',
    browser: '',
    os: '',
    device: 'Desktop',
    loginSuccessful: true,
    isAttackIp: false,
    asn: '',
    rtt: '',
    loginTimestamp: getCurrentDatetimeLocal()
  };

  const validationRules = {
    userId: {
      label: 'User ID',
      required: true
    },
    ipAddress: {
      label: 'IP Address',
      required: true,
      validator: (value) => {
        if (!isValidIP(value)) {
          return 'Please enter a valid IP address';
        }
        return null;
      }
    },
    country: {
      label: 'Country',
      required: true
    },
    region: {
      label: 'Region',
      required: true
    },
    city: {
      label: 'City',
      required: true
    },
    browser: {
      label: 'Browser',
      required: true
    },
    os: {
      label: 'Operating System',
      required: true
    },
    device: {
      label: 'Device Type',
      required: true
    },
    asn: {
      label: 'ASN',
      required: true,
      min: 0,
      minMessage: 'ASN must be a positive number'
    },
    rtt: {
      label: 'RTT',
      required: true,
      min: 0,
      minMessage: 'RTT must be a positive number'
    }
  };

  const {
    formData,
    errors,
    handleChange,
    handleBlur,
    validate,
    reset
  } = useFormValidation(initialState, validationRules);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    const result = await predict({
      userId: formData.userId,
      ipAddress: formData.ipAddress,
      country: formData.country,
      region: formData.region,
      city: formData.city,
      browser: formData.browser,
      os: formData.os,
      device: formData.device,
      loginSuccessful: formData.loginSuccessful,
      isAttackIp: formData.isAttackIp,
      asn: parseInt(formData.asn),
      rtt: parseFloat(formData.rtt),
      timestamp: toISOTimestamp(formData.loginTimestamp)
    });

    if (result.success) {
      console.log('Prediction success:', result.data);
    }
  };

  const handleClear = () => {
    reset();
  };

  // Examples for quick testing
  const loadNormalExample = () => {
    // Normal login during business hours
    const businessHour = new Date();
    businessHour.setHours(10, 30, 0, 0); // 10:30 AM

    handleChange({ target: { name: 'userId', value: 'user123' } });
    handleChange({ target: { name: 'ipAddress', value: '192.168.1.100' } });
    handleChange({ target: { name: 'country', value: 'US' } });
    handleChange({ target: { name: 'region', value: 'California' } });
    handleChange({ target: { name: 'city', value: 'San Francisco' } });
    handleChange({ target: { name: 'browser', value: 'Chrome 120.0' } });
    handleChange({ target: { name: 'os', value: 'Windows 10' } });
    handleChange({ target: { name: 'device', value: 'Desktop' } });
    handleChange({ target: { name: 'loginSuccessful', value: true } });
    handleChange({ target: { name: 'isAttackIp', value: false } });
    handleChange({ target: { name: 'asn', value: '15169' } });
    handleChange({ target: { name: 'rtt', value: '45.5' } });
    handleChange({ target: { name: 'loginTimestamp', value: businessHour.toISOString().slice(0, 16) } });
  };

  const loadATOExample = () => {
    // Suspicious login at 3 AM (night time)
    const nightTime = new Date();
    nightTime.setHours(3, 15, 0, 0); // 3:15 AM

    handleChange({ target: { name: 'userId', value: 'user456' } });
    handleChange({ target: { name: 'ipAddress', value: '89.46.23.10' } });
    handleChange({ target: { name: 'country', value: 'RO' } });
    handleChange({ target: { name: 'region', value: 'Bucharest' } });
    handleChange({ target: { name: 'city', value: 'Bucharest' } });
    handleChange({ target: { name: 'browser', value: 'Firefox 115.0' } });
    handleChange({ target: { name: 'os', value: 'Linux' } });
    handleChange({ target: { name: 'device', value: 'Desktop' } });
    handleChange({ target: { name: 'loginSuccessful', value: true } });
    handleChange({ target: { name: 'isAttackIp', value: true } });
    handleChange({ target: { name: 'asn', value: '9050' } });
    handleChange({ target: { name: 'rtt', value: '890' } });
    handleChange({ target: { name: 'loginTimestamp', value: nightTime.toISOString().slice(0, 16) } });
  };

  return (
    <div className="form-card">
      <h3 className="form-card-title">
        Account Takeover Detection
        <span className="badge badge-active ms-2">ACTIVE</span>
      </h3>

      {/* Quick examples */}
      <div className="mb-3 d-flex gap-2">
        <Button
          size="sm"
          variant="outline-success"
          onClick={loadNormalExample}
          disabled={isLoading}
        >
          📋 Load Normal Example
        </Button>
        <Button
          size="sm"
          variant="outline-danger"
          onClick={loadATOExample}
          disabled={isLoading}
        >
          🚨 Load ATO Example
        </Button>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="row">
          <div className="col-md-6">
            <FormInput
              label="User ID"
              name="userId"
              type="text"
              value={formData.userId}
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="user123"
              required
              error={errors.userId}
              icon={<FiUser />}
            />
          </div>
          <div className="col-md-6">
            <FormInput
              label="IP Address"
              name="ipAddress"
              type="text"
              value={formData.ipAddress}
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="192.168.1.100"
              required
              error={errors.ipAddress}
              icon={<FiGlobe />}
            />
          </div>
        </div>

        <div className="row">
          <div className="col-md-4">
            <FormInput
              label="Country"
              name="country"
              type="text"
              value={formData.country}
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="US"
              required
              maxLength="2"
              error={errors.country}
              icon={<FiMapPin />}
            />
          </div>
          <div className="col-md-4">
            <FormInput
              label="Region"
              name="region"
              type="text"
              value={formData.region}
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="California"
              required
              error={errors.region}
              icon={<FiMapPin />}
            />
          </div>
          <div className="col-md-4">
            <FormInput
              label="City"
              name="city"
              type="text"
              value={formData.city}
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="San Francisco"
              required
              error={errors.city}
              icon={<FiMapPin />}
            />
          </div>
        </div>

        <div className="row">
          <div className="col-md-6">
            <FormInput
              label="Browser"
              name="browser"
              type="text"
              value={formData.browser}
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="Chrome 120.0"
              required
              error={errors.browser}
              icon={<FiChrome />}
            />
          </div>
          <div className="col-md-6">
            <FormInput
              label="Operating System"
              name="os"
              type="text"
              value={formData.os}
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="Windows 10"
              required
              error={errors.os}
              icon={<FiMonitor />}
            />
          </div>
        </div>

        <div className="row">
          <div className="col-md-4">
            <FormInput
              label="Device Type"
              name="device"
              type="select"
              value={formData.device}
              onChange={handleChange}
              onBlur={handleBlur}
              required
              error={errors.device}
              options={['Desktop', 'Mobile', 'Tablet']}
              icon={<FiMonitor />}
            />
          </div>
          <div className="col-md-4">
            <FormInput
              label="ASN"
              name="asn"
              type="number"
              value={formData.asn}
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="15169"
              required
              min="0"
              error={errors.asn}
              icon={<FiActivity />}
            />
          </div>
          <div className="col-md-4">
            <FormInput
              label="RTT (ms)"
              name="rtt"
              type="number"
              step="0.1"
              value={formData.rtt}
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="45.5"
              required
              min="0"
              error={errors.rtt}
              icon={<FiClock />}
            />
          </div>
        </div>

        {/* Login Timestamp */}
        <div className="row">
          <div className="col-12">
            <div className="mb-3">
              <label htmlFor="loginTimestamp" className="form-label">
                <FiCalendar className="me-1" /> Fecha y Hora del Login
              </label>
              <input
                type="datetime-local"
                className="form-control"
                id="loginTimestamp"
                name="loginTimestamp"
                value={formData.loginTimestamp}
                onChange={handleChange}
              />
              <small className="text-muted">
                Horario nocturno (22:00-06:00) se considera sospechoso
              </small>
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col-md-6">
            <div className="form-check mb-3">
              <input
                className="form-check-input"
                type="checkbox"
                id="loginSuccessful"
                name="loginSuccessful"
                checked={formData.loginSuccessful}
                onChange={(e) => handleChange({ target: { name: 'loginSuccessful', value: e.target.checked } })}
              />
              <label className="form-check-label" htmlFor="loginSuccessful">
                <FiCheckCircle className="me-1" /> Login Successful
              </label>
            </div>
          </div>
          <div className="col-md-6">
            <div className="form-check mb-3">
              <input
                className="form-check-input"
                type="checkbox"
                id="isAttackIp"
                name="isAttackIp"
                checked={formData.isAttackIp}
                onChange={(e) => handleChange({ target: { name: 'isAttackIp', value: e.target.checked } })}
              />
              <label className="form-check-label" htmlFor="isAttackIp">
                <FiAlertCircle className="me-1" /> Is Attack IP
              </label>
            </div>
          </div>
        </div>

        <div className="d-flex gap-2">
          <Button
            type="submit"
            variant="primary"
            className="form-submit-btn flex-grow-1"
            disabled={isLoading}
          >
            {isLoading ? 'Analyzing...' : 'Predict'}
          </Button>
          <Button
            type="button"
            variant="outline-secondary"
            onClick={handleClear}
            disabled={isLoading}
          >
            Clear
          </Button>
        </div>
      </form>
    </div>
  );
};

export default AtaquesSospechososForm;
