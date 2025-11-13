import React, { useState, useEffect } from 'react';
import { getStats, getMonthlyReport } from '../services/api';
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
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [monthlyData, setMonthlyData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsRes, monthlyRes] = await Promise.all([
        getStats(),
        getMonthlyReport(6)
      ]);
      
      setStats(statsRes.data);
      setMonthlyData(monthlyRes.data);
    } catch (error) {
      console.error('Error cargando datos:', error);
    } finally {
      setLoading(false);
    }
  };

  const chartData = monthlyData ? {
    labels: monthlyData.map(m => {
      const [year, month] = m.month.split('-');
      const date = new Date(year, month - 1);
      return date.toLocaleDateString('es-ES', { month: 'short', year: 'numeric' });
    }),
    datasets: [
      {
        label: 'Ingresos',
        data: monthlyData.map(m => m.total_income),
        borderColor: '#00d9a3',
        backgroundColor: 'rgba(0, 217, 163, 0.1)',
        tension: 0.4,
      },
      {
        label: 'Gastos',
        data: monthlyData.map(m => m.total_expenses),
        borderColor: '#e94560',
        backgroundColor: 'rgba(233, 69, 96, 0.1)',
        tension: 0.4,
      },
      {
        label: 'Balance',
        data: monthlyData.map(m => m.balance),
        borderColor: '#533483',
        backgroundColor: 'rgba(83, 52, 131, 0.1)',
        tension: 0.4,
      }
    ]
  } : null;

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#e8e8e8'
        }
      },
      title: {
        display: true,
        text: 'Evolución Mensual',
        color: '#e8e8e8',
        font: {
          size: 16
        }
      }
    },
    scales: {
      y: {
        ticks: {
          color: '#a8a8a8',
          callback: function(value) {
            return value.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' });
          }
        },
        grid: {
          color: '#2d2d44'
        }
      },
      x: {
        ticks: {
          color: '#a8a8a8'
        },
        grid: {
          color: '#2d2d44'
        }
      }
    }
  };

  if (loading) {
    return (
      <div className="page">
        <div className="loading">
          <div className="spinner"></div>
          <p>Cargando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Resumen de tu situación financiera</p>
      </div>

      <div className="grid grid-4">
        <div className="stat-card">
          <div className="stat-value">
            {stats?.total_transactions || 0}
          </div>
          <div className="stat-label">Transacciones</div>
        </div>

        <div className="stat-card">
          <div className="stat-value" style={{ color: '#00d9a3' }}>
            {(stats?.total_income || 0).toLocaleString('es-ES', { style: 'currency', currency: 'EUR' })}
          </div>
          <div className="stat-label">Ingresos Totales</div>
        </div>

        <div className="stat-card">
          <div className="stat-value" style={{ color: '#e94560' }}>
            {(stats?.total_expenses || 0).toLocaleString('es-ES', { style: 'currency', currency: 'EUR' })}
          </div>
          <div className="stat-label">Gastos Totales</div>
        </div>

        <div className="stat-card">
          <div className="stat-value" style={{ color: stats?.balance >= 0 ? '#00d9a3' : '#e94560' }}>
            {(stats?.balance || 0).toLocaleString('es-ES', { style: 'currency', currency: 'EUR' })}
          </div>
          <div className="stat-label">Balance</div>
        </div>
      </div>

      {stats?.uncategorized > 0 && (
        <div className="alert alert-warning">
          Tienes {stats.uncategorized} transacciones sin categorizar
        </div>
      )}

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Últimos 6 Meses</h2>
        </div>
        {chartData && <Line data={chartData} options={chartOptions} />}
      </div>
    </div>
  );
}

export default Dashboard;
