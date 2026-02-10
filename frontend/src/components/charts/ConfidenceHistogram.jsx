/**
 * ConfidenceHistogram Component
 * Bar chart showing confidence distribution
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

function ConfidenceHistogram({ distribution }) {
  const labels = distribution.map((d) => d.range);
  const counts = distribution.map((d) => d.count);

  // Color gradient from yellow to green based on confidence
  const colors = [
    theme.warning.main,  // 50-60%
    '#D4A017',           // 60-70%
    '#7CB342',           // 70-80%
    theme.success.light, // 80-90%
    theme.success.main,  // 90-100%
  ];

  const data = {
    labels,
    datasets: [
      {
        label: 'Predicciones',
        data: counts,
        backgroundColor: colors,
        borderColor: colors.map((c) => c),
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
          label: (context) => {
            const total = counts.reduce((a, b) => a + b, 0);
            const percentage = total > 0 ? ((context.raw / total) * 100).toFixed(1) : 0;
            return `${context.raw} predicciones (${percentage}%)`;
          },
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Rango de Confianza',
        },
        grid: { display: false },
      },
      y: {
        title: {
          display: true,
          text: 'Cantidad',
        },
        beginAtZero: true,
        grid: { color: 'rgba(0,0,0,0.05)' },
      },
    },
  };

  return (
    <div style={{ height: '250px' }}>
      <Bar data={data} options={options} />
    </div>
  );
}

export default ConfidenceHistogram;
