/**
 * ThreatDistributionChart Component
 * Pie chart showing threats vs benign distribution
 */
import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { theme } from '../../styles/theme';

ChartJS.register(ArcElement, Tooltip, Legend);

function ThreatDistributionChart({ threats, benign }) {
  const data = {
    labels: ['Amenazas Detectadas', 'Trafico Legitimo'],
    datasets: [
      {
        data: [threats, benign],
        backgroundColor: [theme.danger.main, theme.success.main],
        borderColor: [theme.danger.dark, theme.success.dark],
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: { size: 12 },
        },
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const total = threats + benign;
            const value = context.raw;
            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
            return `${context.label}: ${value} (${percentage}%)`;
          },
        },
      },
    },
  };

  return (
    <div style={{ height: '280px' }}>
      <Pie data={data} options={options} />
    </div>
  );
}

export default ThreatDistributionChart;
