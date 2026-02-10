/**
 * SeverityChart Component
 * Bar chart showing alerts by severity
 */
import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { theme } from '../../styles/theme';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function SeverityChart({ alertStats }) {
  const { by_severity } = alertStats;

  const data = {
    labels: ['Critico', 'Alto', 'Medio'],
    datasets: [
      {
        label: 'Alertas',
        data: [by_severity.critical, by_severity.high, by_severity.medium],
        backgroundColor: [
          theme.danger.main,
          '#FF6B6B',
          theme.warning.main,
        ],
        borderColor: [
          theme.danger.dark,
          theme.danger.main,
          theme.warning.dark,
        ],
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          afterLabel: (context) => {
            const total = alertStats.total;
            const percentage = total > 0 ? ((context.raw / total) * 100).toFixed(1) : 0;
            return `${percentage}% del total`;
          },
        },
      },
    },
    scales: {
      x: {
        grid: { display: false },
      },
      y: {
        beginAtZero: true,
        grid: { color: 'rgba(0,0,0,0.05)' },
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div style={{ height: '200px' }}>
      <Bar data={data} options={options} />
    </div>
  );
}

export default SeverityChart;
