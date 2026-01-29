/**
 * Header Component
 * Dashboard header with logo and title
 */

import React from 'react';
import { FiShield } from 'react-icons/fi';

const Header = () => {
  return (
    <header className="dashboard-header">
      <div className="dashboard-header-content">
        <h1 className="dashboard-header-title">
          <FiShield className="dashboard-header-icon" />
          Cybersecurity Incident Prediction Dashboard
        </h1>
        <p className="dashboard-header-subtitle">
          Real-time threat detection powered by machine learning
        </p>
      </div>
    </header>
  );
};

export default Header;
