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
      label: 'Sender Email',
      required: true,
      validator: (value) => {
        if (!isValidEmail(value)) {
          return 'Please enter a valid email address';
        }
        return null;
      }
    },
    receiver: {
      label: 'Receiver Email',
      required: false,
      validator: (value) => {
        if (value && !isValidEmail(value)) {
          return 'Please enter a valid email address';
        }
        return null;
      }
    },
    subject: {
      label: 'Subject',
      required: true,
      min: 3,
      minMessage: 'Subject must be at least 3 characters'
    },
    body: {
      label: 'Body',
      required: true,
      min: 10,
      minMessage: 'Body must be at least 10 characters'
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
      <h3 className="form-card-title">Phishing Email Detection</h3>
      <form onSubmit={handleSubmit}>
        <FormInput
          label="Sender Email Address"
          name="sender"
          type="email"
          value={formData.sender}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="suspicious@example.com"
          required
          error={errors.sender}
          icon={<FiMail />}
        />

        <FormInput
          label="Receiver Email Address"
          name="receiver"
          type="email"
          value={formData.receiver}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="victim@company.com (optional)"
          error={errors.receiver}
          icon={<FiInbox />}
        />

        <FormInput
          label="Email Subject"
          name="subject"
          type="text"
          value={formData.subject}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="URGENT: Verify your account"
          required
          error={errors.subject}
          icon={<FiFileText />}
        />

        <FormInput
          label="Email Body"
          name="body"
          as="textarea"
          rows={6}
          value={formData.body}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="Enter the email content here..."
          required
          error={errors.body}
        />

        <FormInput
          label="Contains URLs"
          name="urls"
          type="select"
          value={formData.urls}
          onChange={handleChange}
          onBlur={handleBlur}
          required
          error={errors.urls}
          options={[
            { value: '0', label: 'No' },
            { value: '1', label: 'Yes' }
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

export default PhishingForm;
