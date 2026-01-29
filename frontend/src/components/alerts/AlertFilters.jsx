/**
 * AlertFilters Component
 * Filters and bulk actions for alerts
 */
import React from 'react';
import { Row, Col, Form, Button } from 'react-bootstrap';
import { FaCheck, FaFilter } from 'react-icons/fa';

function AlertFilters({ filters, onChange, selectedCount, onBulkAcknowledge }) {
  const handleChange = (field, value) => {
    onChange({
      ...filters,
      [field]: value || undefined
    });
  };

  return (
    <Row className="align-items-center g-2">
      <Col xs={12} md={3}>
        <Form.Group>
          <Form.Label className="small text-muted mb-1">
            <FaFilter className="me-1" />Estado
          </Form.Label>
          <Form.Select
            size="sm"
            value={filters.status || ''}
            onChange={(e) => handleChange('status', e.target.value)}
          >
            <option value="">Todos</option>
            <option value="unread">Sin Leer</option>
            <option value="read">Leidos</option>
            <option value="acknowledged">Reconocidos</option>
          </Form.Select>
        </Form.Group>
      </Col>

      <Col xs={12} md={3}>
        <Form.Group>
          <Form.Label className="small text-muted mb-1">Severidad</Form.Label>
          <Form.Select
            size="sm"
            value={filters.severity || ''}
            onChange={(e) => handleChange('severity', e.target.value)}
          >
            <option value="">Todas</option>
            <option value="critical">Critica</option>
            <option value="high">Alta</option>
            <option value="medium">Media</option>
          </Form.Select>
        </Form.Group>
      </Col>

      <Col xs={12} md={3}>
        <Form.Group>
          <Form.Label className="small text-muted mb-1">Modelo</Form.Label>
          <Form.Select
            size="sm"
            value={filters.model_type || ''}
            onChange={(e) => handleChange('model_type', e.target.value)}
          >
            <option value="">Todos</option>
            <option value="phishing">Phishing</option>
            <option value="ato">Account Takeover</option>
            <option value="brute_force">Brute Force</option>
          </Form.Select>
        </Form.Group>
      </Col>

      <Col xs={12} md={3} className="d-flex align-items-end">
        {selectedCount > 0 && (
          <Button
            variant="success"
            size="sm"
            onClick={onBulkAcknowledge}
            className="w-100"
          >
            <FaCheck className="me-1" />
            Reconocer ({selectedCount})
          </Button>
        )}
      </Col>
    </Row>
  );
}

export default AlertFilters;
