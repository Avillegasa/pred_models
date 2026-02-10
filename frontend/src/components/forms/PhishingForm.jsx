/**
 * Phishing Form Component
 * Form for phishing email detection
 */

import React from 'react';
import { Button } from 'react-bootstrap';
import { FiMail, FiInbox, FiFileText, FiLink } from 'react-icons/fi';
import FormInput from './FormInput';
import { useFormValidation } from '../../hooks/useFormValidation';
import { usePrediction } from '../../hooks/usePrediction';
import { isValidEmail } from '../../utils/validators';

const PhishingForm = () => {
  const { predict, isLoading } = usePrediction();

  const initialState = {
    sender: '',
    receiver: '',
    subject: '',
    body: '',
    urls: '0'
  };

  const validationRules = {
    sender: {
      label: 'Email del Remitente',
      required: true,
      validator: (value) => {
        if (!isValidEmail(value)) {
          return 'Por favor ingrese una direccion de email valida';
        }
        return null;
      }
    },
    receiver: {
      label: 'Email del Destinatario',
      required: false,
      validator: (value) => {
        if (value && !isValidEmail(value)) {
          return 'Por favor ingrese una direccion de email valida';
        }
        return null;
      }
    },
    subject: {
      label: 'Asunto',
      required: true,
      min: 3,
      minMessage: 'El asunto debe tener al menos 3 caracteres'
    },
    body: {
      label: 'Cuerpo',
      required: true,
      min: 10,
      minMessage: 'El cuerpo debe tener al menos 10 caracteres'
    },
    urls: {
      label: 'URLs',
      required: true
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
      ...formData,
      urls: parseInt(formData.urls)
    });

    if (result.success) {
      // Form stays filled for comparison
      console.log('Prediction success:', result.data);
    }
  };

  const handleClear = () => {
    reset();
  };

  return (
    <div className="form-card">
      <h3 className="form-card-title">Deteccion de Email de Phishing</h3>
      <form onSubmit={handleSubmit}>
        <FormInput
          label="Direccion de Email del Remitente"
          name="sender"
          type="email"
          value={formData.sender}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="sospechoso@ejemplo.com"
          required
          error={errors.sender}
          icon={<FiMail />}
        />

        <FormInput
          label="Direccion de Email del Destinatario"
          name="receiver"
          type="email"
          value={formData.receiver}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="victima@empresa.com (opcional)"
          error={errors.receiver}
          icon={<FiInbox />}
        />

        <FormInput
          label="Asunto del Email"
          name="subject"
          type="text"
          value={formData.subject}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="URGENTE: Verifique su cuenta"
          required
          error={errors.subject}
          icon={<FiFileText />}
        />

        <FormInput
          label="Cuerpo del Email"
          name="body"
          as="textarea"
          rows={6}
          value={formData.body}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="Ingrese el contenido del email aqui..."
          required
          error={errors.body}
        />

        <FormInput
          label="Contiene URLs"
          name="urls"
          type="select"
          value={formData.urls}
          onChange={handleChange}
          onBlur={handleBlur}
          required
          error={errors.urls}
          options={[
            { value: '0', label: 'No' },
            { value: '1', label: 'Si' }
          ]}
          icon={<FiLink />}
        />

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

export default PhishingForm;
