/**
 * DailyTrendChart Component
 * Line chart showing daily trend for the month
 */
import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { theme } from '../../styles/theme';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

function DailyTrendChart({ dailyTrend }) {
  const labels = dailyTrend.map((d) => d.day);
  const threatData = dailyTrend.map((d) => d.threats);
  const benignData = dailyTrend.map((d) => d.benign);

  const data = {
    labels,
    datasets: [
      {
        label: 'Amenazas',
        data: threatData,
        borderColor: theme.danger.main,
        backgroundColor: theme.danger.bg,
        fill: true,
        tension: 0.3,
        pointRadius: 3,
        pointHoverRadius: 6,
      },
      {
        label: 'Legitimos',
        data: benignData,
        borderColor: theme.success.main,
        backgroundColor: theme.success.bg,
        fill: true,
        tension: 0.3,
        pointRadius: 3,
        pointHoverRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
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
          title: (context) => {
            const dayData = dailyTrend[context[0].dataIndex];
            return `Dia ${dayData.day} - ${dayData.date}`;
          },
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Dia del mes',
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
    <div style={{ height: '300px' }}>
      <Line data={data} options={options} />
    </div>
  );
}

export default DailyTrendChart;
