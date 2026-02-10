/**
 * Form Input Component
 * Reusable input field with validation and error display
 */

import React from 'react';
import { Form } from 'react-bootstrap';
import { FiAlertCircle } from 'react-icons/fi';

const FormInput = ({
  label,
  name,
  type = 'text',
  value,
  onChange,
  onBlur,
  placeholder,
  required = false,
  error,
  as,
  rows,
  options,
  icon,
  ...rest
}) => {
  const inputId = `input-${name}`;
  const hasError = !!error;

  // Render select dropdown
  if (type === 'select' && options) {
    return (
      <Form.Group className="form-group" controlId={inputId}>
        <Form.Label className={required ? 'form-label-required' : ''}>
          {label}
        </Form.Label>
        <Form.Select
          name={name}
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          isInvalid={hasError}
          {...rest}
        >
          <option value="">Seleccionar {label}...</option>
          {options.map((option) => (
            <option key={option.value || option} value={option.value || option}>
              {option.label || option}
            </option>
          ))}
        </Form.Select>
        {hasError && (
          <div className="form-error-message">
            <FiAlertCircle size={14} />
            {error}
          </div>
        )}
      </Form.Group>
    );
  }

  // Render textarea
  if (as === 'textarea') {
    return (
      <Form.Group className="form-group" controlId={inputId}>
        <Form.Label className={required ? 'form-label-required' : ''}>
          {label}
        </Form.Label>
        <Form.Control
          as="textarea"
          name={name}
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          placeholder={placeholder}
          isInvalid={hasError}
          rows={rows || 4}
          {...rest}
        />
        {hasError && (
          <div className="form-error-message">
            <FiAlertCircle size={14} />
            {error}
          </div>
        )}
      </Form.Group>
    );
  }

  // Render regular input
  return (
    <Form.Group className="form-group" controlId={inputId}>
      <Form.Label className={required ? 'form-label-required' : ''}>
        {label}
      </Form.Label>
      <div className={icon ? 'form-input-group' : ''}>
        {icon && <span className="form-input-icon">{icon}</span>}
        <Form.Control
          type={type}
          name={name}
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          placeholder={placeholder}
          isInvalid={hasError}
          {...rest}
        />
      </div>
      {hasError && (
        <div className="form-error-message">
          <FiAlertCircle size={14} />
          {error}
        </div>
      )}
    </Form.Group>
  );
};

export default FormInput;
