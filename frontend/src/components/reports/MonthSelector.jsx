/**
 * MonthSelector Component
 * Selector for year and month with available months indicator
 */
import React from 'react';
import { Row, Col, Form, Badge } from 'react-bootstrap';
import { FaCalendarAlt } from 'react-icons/fa';

const MONTH_NAMES = {
  1: 'Enero',
  2: 'Febrero',
  3: 'Marzo',
  4: 'Abril',
  5: 'Mayo',
  6: 'Junio',
  7: 'Julio',
  8: 'Agosto',
  9: 'Septiembre',
  10: 'Octubre',
  11: 'Noviembre',
  12: 'Diciembre',
};

function MonthSelector({ year, month, availableMonths, onChange, loading }) {
  // Get unique years from available months
  const years = [...new Set(availableMonths.map((m) => m.year))].sort((a, b) => b - a);

  // If no years available, use current year
  const currentYear = new Date().getFullYear();
  const displayYears = years.length > 0 ? years : [currentYear, currentYear - 1];

  // Get months available for selected year
  const monthsForYear = availableMonths.filter((m) => m.year === year);

  // Check if a month has data
  const hasData = (y, m) => {
    return availableMonths.some(
      (am) => am.year === y && am.month === m && (am.prediction_count > 0 || am.alert_count > 0)
    );
  };

  const handleYearChange = (e) => {
    const newYear = parseInt(e.target.value);
    onChange(newYear, month);
  };

  const handleMonthChange = (e) => {
    const newMonth = parseInt(e.target.value);
    onChange(year, newMonth);
  };

  return (
    <div className="month-selector">
      <Row className="align-items-center g-3">
        <Col xs="auto">
          <FaCalendarAlt className="text-primary" size={20} />
        </Col>
        <Col xs={12} sm="auto">
          <Form.Select
            value={year}
            onChange={handleYearChange}
            disabled={loading}
            style={{ minWidth: '120px' }}
          >
            {displayYears.map((y) => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </Form.Select>
        </Col>
        <Col xs={12} sm="auto">
          <Form.Select
            value={month}
            onChange={handleMonthChange}
            disabled={loading}
            style={{ minWidth: '150px' }}
          >
            {Object.entries(MONTH_NAMES).map(([m, name]) => {
              const monthNum = parseInt(m);
              const monthHasData = hasData(year, monthNum);
              return (
                <option key={m} value={m}>
                  {name} {monthHasData ? '' : '(sin datos)'}
                </option>
              );
            })}
          </Form.Select>
        </Col>
        {monthsForYear.length > 0 && (
          <Col xs="auto">
            <Badge bg="info" className="ms-2">
              {monthsForYear[0]?.prediction_count || 0} predicciones
            </Badge>
          </Col>
        )}
      </Row>

      <style>{`
        .month-selector {
          padding: 1rem;
          background: var(--bg-secondary);
          border-radius: var(--radius-md);
          margin-bottom: 1.5rem;
        }
      `}</style>
    </div>
  );
}

export default MonthSelector;
