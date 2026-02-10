/**
 * ModelComparisonChart Component
 * Horizontal bar chart showing breakdown by model
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

const MODEL_LABELS = {
  phishing: 'Phishing',
  ato: 'Account Takeover',
  brute_force: 'Fuerza Bruta',
};

function ModelComparisonChart({ byModel }) {
  const labels = Object.keys(byModel).map((key) => MODEL_LABELS[key] || key);
  const threatData = Object.values(byModel).map((m) => m.threats);
  const benignData = Object.values(byModel).map((m) => m.benign);

  const data = {
    labels,
    datasets: [
      {
        label: 'Amenazas',
        data: threatData,
        backgroundColor: theme.danger.main,
        borderRadius: 4,
      },
      {
        label: 'Legitimos',
        data: benignData,
        backgroundColor: theme.success.main,
        borderRadius: 4,
      },
    ],
  };

  const options = {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 15,
        },
      },
      tooltip: {
        callbacks: {
          afterLabel: (context) => {
            const modelKey = Object.keys(byModel)[context.dataIndex];
            const model = byModel[modelKey];
            return `Confianza promedio: ${model.avg_confidence.toFixed(1)}%`;
          },
        },
      },
    },
    scales: {
      x: {
        stacked: true,
        grid: { display: false },
      },
      y: {
        stacked: true,
        grid: { display: false },
      },
    },
  };

  return (
    <div style={{ height: '200px' }}>
      <Bar data={data} options={options} />
    </div>
  );
}

export default ModelComparisonChart;
