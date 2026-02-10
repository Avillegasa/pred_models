/**
 * Account Takeover Detection Form Component
 * Form for detecting suspicious login attempts
 */

import React from 'react';
import { Button, Form } from 'react-bootstrap';
import { FiUser, FiGlobe, FiMapPin, FiChrome, FiMonitor, FiCheckCircle, FiAlertCircle, FiActivity, FiClock, FiCalendar, FiFlag } from 'react-icons/fi';
import FormInput from './FormInput';
import { useFormValidation } from '../../hooks/useFormValidation';
import { usePrediction } from '../../hooks/usePrediction';
import { isValidIP } from '../../utils/validators';

// Lista completa de paises organizados por nivel de riesgo
// El valor es el codigo ISO de 2 letras que espera el modelo
const COUNTRIES_BY_RISK = {
  low: {
    label: 'BAJO RIESGO - Bolivia y Sudamerica',
    countries: [
      { code: 'BO', name: 'Bolivia' },
      { code: 'AR', name: 'Argentina' },
      { code: 'BR', name: 'Brasil' },
      { code: 'CL', name: 'Chile' },
      { code: 'CO', name: 'Colombia' },
      { code: 'EC', name: 'Ecuador' },
      { code: 'GF', name: 'Guayana Francesa' },
      { code: 'GY', name: 'Guyana' },
      { code: 'PE', name: 'Peru' },
      { code: 'PY', name: 'Paraguay' },
      { code: 'SR', name: 'Surinam' },
      { code: 'UY', name: 'Uruguay' },
      { code: 'VE', name: 'Venezuela' },
    ]
  },
  medium: {
    label: 'RIESGO MEDIO - Norteamerica, Europa, Asia desarrollada',
    countries: [
      // Norteamerica
      { code: 'US', name: 'Estados Unidos' },
      { code: 'CA', name: 'Canada' },
      { code: 'MX', name: 'Mexico' },
      // Europa Occidental
      { code: 'DE', name: 'Alemania' },
      { code: 'AT', name: 'Austria' },
      { code: 'BE', name: 'Belgica' },
      { code: 'DK', name: 'Dinamarca' },
      { code: 'ES', name: 'Espana' },
      { code: 'FI', name: 'Finlandia' },
      { code: 'FR', name: 'Francia' },
      { code: 'GR', name: 'Grecia' },
      { code: 'IE', name: 'Irlanda' },
      { code: 'IT', name: 'Italia' },
      { code: 'NL', name: 'Paises Bajos' },
      { code: 'NO', name: 'Noruega' },
      { code: 'PT', name: 'Portugal' },
      { code: 'GB', name: 'Reino Unido' },
      { code: 'SE', name: 'Suecia' },
      { code: 'CH', name: 'Suiza' },
      // Europa Central/Sur
      { code: 'AL', name: 'Albania' },
      { code: 'BA', name: 'Bosnia' },
      { code: 'BG', name: 'Bulgaria' },
      { code: 'HR', name: 'Croacia' },
      { code: 'SK', name: 'Eslovaquia' },
      { code: 'SI', name: 'Eslovenia' },
      { code: 'HU', name: 'Hungria' },
      { code: 'MK', name: 'Macedonia' },
      { code: 'PL', name: 'Polonia' },
      { code: 'CZ', name: 'Republica Checa' },
      { code: 'RO', name: 'Rumania' },
      { code: 'RS', name: 'Serbia' },
      // Oceania
      { code: 'AU', name: 'Australia' },
      { code: 'NZ', name: 'Nueva Zelanda' },
      // Asia desarrollada
      { code: 'KR', name: 'Corea del Sur' },
      { code: 'HK', name: 'Hong Kong' },
      { code: 'JP', name: 'Japon' },
      { code: 'SG', name: 'Singapur' },
      { code: 'TW', name: 'Taiwan' },
    ]
  },
  high: {
    label: 'ALTO RIESGO - Historial de ciberataques',
    countries: [
      // Ex-URSS / Europa del Este
      { code: 'AM', name: 'Armenia' },
      { code: 'AZ', name: 'Azerbaiyan' },
      { code: 'BY', name: 'Bielorrusia' },
      { code: 'GE', name: 'Georgia' },
      { code: 'KZ', name: 'Kazajistan' },
      { code: 'KG', name: 'Kirguistan' },
      { code: 'MD', name: 'Moldavia' },
      { code: 'MN', name: 'Mongolia' },
      { code: 'RU', name: 'Rusia' },
      { code: 'TJ', name: 'Tayikistan' },
      { code: 'TM', name: 'Turkmenistan' },
      { code: 'UA', name: 'Ucrania' },
      { code: 'UZ', name: 'Uzbekistan' },
      // Asia Oriental
      { code: 'CN', name: 'China' },
      { code: 'KP', name: 'Corea del Norte' },
      // Medio Oriente
      { code: 'AF', name: 'Afganistan' },
      { code: 'IR', name: 'Iran' },
      { code: 'IQ', name: 'Irak' },
      { code: 'LB', name: 'Libano' },
      { code: 'SY', name: 'Siria' },
      { code: 'YE', name: 'Yemen' },
      // Africa
      { code: 'DZ', name: 'Argelia' },
      { code: 'CM', name: 'Camerun' },
      { code: 'CI', name: 'Costa de Marfil' },
      { code: 'EG', name: 'Egipto' },
      { code: 'GH', name: 'Ghana' },
      { code: 'KE', name: 'Kenia' },
      { code: 'MA', name: 'Marruecos' },
      { code: 'NG', name: 'Nigeria' },
      { code: 'SN', name: 'Senegal' },
      { code: 'ZA', name: 'Sudafrica' },
      { code: 'TN', name: 'Tunez' },
      // Sudeste Asiatico
      { code: 'BD', name: 'Bangladesh' },
      { code: 'KH', name: 'Camboya' },
      { code: 'PH', name: 'Filipinas' },
      { code: 'IN', name: 'India' },
      { code: 'ID', name: 'Indonesia' },
      { code: 'LA', name: 'Laos' },
      { code: 'MY', name: 'Malasia' },
      { code: 'MM', name: 'Myanmar' },
      { code: 'NP', name: 'Nepal' },
      { code: 'PK', name: 'Pakistan' },
      { code: 'LK', name: 'Sri Lanka' },
      { code: 'TH', name: 'Tailandia' },
      { code: 'VN', name: 'Vietnam' },
    ]
  }
};

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
    country: 'BO',  // Default to Bolivia
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
      label: 'ID de Usuario',
      required: true
    },
    ipAddress: {
      label: 'Direccion IP',
      required: true,
      validator: (value) => {
        if (!isValidIP(value)) {
          return 'Por favor ingrese una direccion IP valida';
        }
        return null;
      }
    },
    country: {
      label: 'Pais',
      required: true
    },
    region: {
      label: 'Region (opcional)',
      required: false
    },
    city: {
      label: 'Ciudad',
      required: true
    },
    browser: {
      label: 'Navegador',
      required: true
    },
    os: {
      label: 'Sistema Operativo',
      required: true
    },
    device: {
      label: 'Tipo de Dispositivo',
      required: true
    },
    asn: {
      label: 'ASN',
      required: true,
      min: 0,
      minMessage: 'El ASN debe ser un numero positivo'
    },
    rtt: {
      label: 'RTT',
      required: true,
      min: 0,
      minMessage: 'El RTT debe ser un numero positivo'
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
    // Normal login from Bolivia during business hours
    const businessHour = new Date();
    businessHour.setHours(10, 30, 0, 0); // 10:30 AM

    handleChange({ target: { name: 'userId', value: 'user123' } });
    handleChange({ target: { name: 'ipAddress', value: '190.186.45.100' } });
    handleChange({ target: { name: 'country', value: 'BO' } });
    handleChange({ target: { name: 'region', value: 'Santa Cruz' } });
    handleChange({ target: { name: 'city', value: 'Santa Cruz de la Sierra' } });
    handleChange({ target: { name: 'browser', value: 'Chrome 120.0' } });
    handleChange({ target: { name: 'os', value: 'Windows 10' } });
    handleChange({ target: { name: 'device', value: 'Desktop' } });
    handleChange({ target: { name: 'loginSuccessful', value: true } });
    handleChange({ target: { name: 'isAttackIp', value: false } });
    handleChange({ target: { name: 'asn', value: '27839' } });
    handleChange({ target: { name: 'rtt', value: '45.5' } });
    handleChange({ target: { name: 'loginTimestamp', value: businessHour.toISOString().slice(0, 16) } });
  };

  const loadATOExample = () => {
    // Suspicious login from Russia at 3 AM (night time)
    const nightTime = new Date();
    nightTime.setHours(3, 15, 0, 0); // 3:15 AM

    handleChange({ target: { name: 'userId', value: 'user456' } });
    handleChange({ target: { name: 'ipAddress', value: '89.46.23.10' } });
    handleChange({ target: { name: 'country', value: 'RU' } });
    handleChange({ target: { name: 'region', value: 'Moscow' } });
    handleChange({ target: { name: 'city', value: 'Moscow' } });
    handleChange({ target: { name: 'browser', value: 'Firefox 115.0' } });
    handleChange({ target: { name: 'os', value: 'Linux' } });
    handleChange({ target: { name: 'device', value: 'Desktop' } });
    handleChange({ target: { name: 'loginSuccessful', value: true } });
    handleChange({ target: { name: 'isAttackIp', value: true } });
    handleChange({ target: { name: 'asn', value: '9050' } });
    handleChange({ target: { name: 'rtt', value: '890' } });
    handleChange({ target: { name: 'loginTimestamp', value: nightTime.toISOString().slice(0, 16) } });
  };

  // Get risk level badge color
  const getCountryRiskBadge = (countryCode) => {
    if (COUNTRIES_BY_RISK.low.countries.find(c => c.code === countryCode)) {
      return { color: 'success', text: 'Bajo riesgo' };
    }
    if (COUNTRIES_BY_RISK.medium.countries.find(c => c.code === countryCode)) {
      return { color: 'warning', text: 'Riesgo medio' };
    }
    if (COUNTRIES_BY_RISK.high.countries.find(c => c.code === countryCode)) {
      return { color: 'danger', text: 'Alto riesgo' };
    }
    return { color: 'secondary', text: 'Desconocido' };
  };

  const riskBadge = getCountryRiskBadge(formData.country);

  return (
    <div className="form-card">
      <h3 className="form-card-title">
        Deteccion de Toma de Cuenta (ATO)
        <span className="badge badge-active ms-2">ACTIVO</span>
      </h3>

      {/* Quick examples */}
      <div className="mb-3 d-flex gap-2">
        <Button
          size="sm"
          variant="outline-success"
          onClick={loadNormalExample}
          disabled={isLoading}
        >
          Cargar Ejemplo Normal (Bolivia)
        </Button>
        <Button
          size="sm"
          variant="outline-danger"
          onClick={loadATOExample}
          disabled={isLoading}
        >
          Cargar Ejemplo ATO (Rusia)
        </Button>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="row">
          <div className="col-md-6">
            <FormInput
              label="ID de Usuario"
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
              label="Direccion IP"
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
            <div className="mb-3">
              <label htmlFor="country" className="form-label">
                <FiFlag className="me-1" /> Pais <span className="text-danger">*</span>
                <span className={`badge bg-${riskBadge.color} ms-2`} style={{ fontSize: '0.7rem' }}>
                  {riskBadge.text}
                </span>
              </label>
              <Form.Select
                id="country"
                name="country"
                value={formData.country}
                onChange={handleChange}
                onBlur={handleBlur}
                className={errors.country ? 'is-invalid' : ''}
              >
                <optgroup label={COUNTRIES_BY_RISK.low.label}>
                  {COUNTRIES_BY_RISK.low.countries.map(c => (
                    <option key={c.code} value={c.code}>
                      {c.name} ({c.code})
                    </option>
                  ))}
                </optgroup>
                <optgroup label={COUNTRIES_BY_RISK.medium.label}>
                  {COUNTRIES_BY_RISK.medium.countries.map(c => (
                    <option key={c.code} value={c.code}>
                      {c.name} ({c.code})
                    </option>
                  ))}
                </optgroup>
                <optgroup label={COUNTRIES_BY_RISK.high.label}>
                  {COUNTRIES_BY_RISK.high.countries.map(c => (
                    <option key={c.code} value={c.code}>
                      {c.name} ({c.code})
                    </option>
                  ))}
                </optgroup>
              </Form.Select>
              {errors.country && (
                <div className="invalid-feedback">{errors.country}</div>
              )}
            </div>
          </div>
          <div className="col-md-4">
            <FormInput
              label="Region (opcional)"
              name="region"
              type="text"
              value={formData.region}
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="Santa Cruz"
              error={errors.region}
              icon={<FiMapPin />}
            />
          </div>
          <div className="col-md-4">
            <FormInput
              label="Ciudad"
              name="city"
              type="text"
              value={formData.city}
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="Santa Cruz de la Sierra"
              required
              error={errors.city}
              icon={<FiMapPin />}
            />
          </div>
        </div>

        <div className="row">
          <div className="col-md-6">
            <FormInput
              label="Navegador"
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
              label="Sistema Operativo"
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
              label="Tipo de Dispositivo"
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
                <FiCheckCircle className="me-1" /> Login Exitoso
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
                <FiAlertCircle className="me-1" /> Es IP de Ataque
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
            {isLoading ? 'Analizando...' : 'Predecir'}
          </Button>
          <Button
            type="button"
            variant="outline-secondary"
            onClick={handleClear}
            disabled={isLoading}
          >
            Limpiar
          </Button>
        </div>
      </form>
    </div>
  );
};

export default AtaquesSospechososForm;
