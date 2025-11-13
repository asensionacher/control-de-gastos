import React, { useState, useEffect } from 'react';
import { getReportSummary, getCategoryReport } from '../services/api';
import { Bar, Doughnut, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function Reports() {
  const [summary, setSummary] = useState(null);
  const [categoryData, setCategoryData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [months, setMonths] = useState(6);

  useEffect(() => {
    loadReports();
  }, [months]);

  const loadReports = async () => {
    try {
      setLoading(true);
      const [summaryRes, categoryRes] = await Promise.all([
        getReportSummary(months),
        getCategoryReport()
      ]);
      
      setSummary(summaryRes.data);
      setCategoryData(categoryRes.data);
    } catch (error) {
      console.error('Error cargando reportes:', error);
    } finally {
      setLoading(false);
    }
  };

  // Gráfico de evolución mensual
  const monthlyChartData = summary ? {
    labels: summary.monthly_reports.map(m => {
      const [year, month] = m.month.split('-');
      const date = new Date(year, month - 1);
      return date.toLocaleDateString('es-ES', { month: 'short', year: 'numeric' });
    }),
    datasets: [
      {
        label: 'Ingresos',
        data: summary.monthly_reports.map(m => m.total_income),
        backgroundColor: 'rgba(0, 217, 163, 0.6)',
        borderColor: '#00d9a3',
        borderWidth: 2,
      },
      {
        label: 'Gastos',
        data: summary.monthly_reports.map(m => m.total_expenses),
        backgroundColor: 'rgba(233, 69, 96, 0.6)',
        borderColor: '#e94560',
        borderWidth: 2,
      }
    ]
  } : null;

  // Gráfico de categorías (Doughnut)
  const categoryChartData = categoryData ? {
    labels: categoryData.map(c => c.category_name),
    datasets: [{
      data: categoryData.map(c => c.total),
      backgroundColor: [
        '#e94560',
        '#533483',
        '#0f3460',
        '#00d9a3',
        '#ff9f1c',
        '#16213e',
        '#e84545',
        '#903749',
        '#53354a',
        '#2b2e4a',
        '#f38181',
        '#aa96da'
      ],
      borderColor: '#1a1a2e',
      borderWidth: 2,
    }]
  } : null;

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#e8e8e8',
          padding: 15,
        }
      },
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

  const doughnutOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          color: '#e8e8e8',
          padding: 15,
          font: {
            size: 12
          }
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.parsed || 0;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${label}: ${value.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' })} (${percentage}%)`;
          }
        }
      }
    }
  };

  if (loading) {
    return (
      <div className="page">
        <div className="loading">
          <div className="spinner"></div>
          <p>Cargando reportes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">Reportes</h1>
        <p className="page-subtitle">Análisis detallado de tus finanzas</p>
      </div>

      <div className="card">
        <div className="form-group">
          <label className="form-label">Período de análisis</label>
          <select
            className="form-control"
            value={months}
            onChange={(e) => setMonths(parseInt(e.target.value))}
            style={{ maxWidth: '200px' }}
          >
            <option value={3}>Últimos 3 meses</option>
            <option value={6}>Últimos 6 meses</option>
            <option value={12}>Últimos 12 meses</option>
            <option value={24}>Últimos 24 meses</option>
          </select>
        </div>
      </div>

      {/* Evolución mensual */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">📊 Evolución Mensual</h2>
        </div>
        {monthlyChartData && (
          <Bar data={monthlyChartData} options={chartOptions} />
        )}
      </div>

      <div className="grid grid-2">
        {/* Distribución por categorías */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">🎯 Gastos por Categoría</h2>
          </div>
          {categoryChartData && (
            <Doughnut data={categoryChartData} options={doughnutOptions} />
          )}
        </div>

        {/* Detalle de categorías */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">📋 Detalle de Categorías</h2>
          </div>
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            {categoryData && categoryData.map((cat, index) => (
              <div
                key={index}
                style={{
                  padding: '1rem',
                  marginBottom: '0.5rem',
                  backgroundColor: 'var(--bg-tertiary)',
                  borderRadius: '5px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}
              >
                <div>
                  <div style={{ fontWeight: 600, marginBottom: '0.25rem' }}>
                    {cat.category_name}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#a8a8a8' }}>
                    {cat.count} transacciones
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontWeight: 600, color: '#e94560' }}>
                    {cat.total.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' })}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#a8a8a8' }}>
                    {cat.percentage}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Top gastos */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">💸 Mayores Gastos</h2>
        </div>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Descripción</th>
                <th>Categoría</th>
                <th>Importe</th>
              </tr>
            </thead>
            <tbody>
              {summary?.top_expenses.map((expense, index) => (
                <tr key={index}>
                  <td>
                    {new Date(expense.date).toLocaleDateString('es-ES', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric'
                    })}
                  </td>
                  <td>{expense.description}</td>
                  <td>{expense.category?.name || 'Sin categoría'}</td>
                  <td>
                    <span className="badge badge-expense">
                      {Math.abs(expense.amount).toLocaleString('es-ES', { 
                        style: 'currency', 
                        currency: 'EUR' 
                      })}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Resumen mensual en tabla */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">📅 Resumen Mensual</h2>
        </div>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Mes</th>
                <th>Ingresos</th>
                <th>Gastos</th>
                <th>Balance</th>
              </tr>
            </thead>
            <tbody>
              {summary?.monthly_reports.map((month, index) => {
                const [year, monthNum] = month.month.split('-');
                const date = new Date(year, monthNum - 1);
                const monthName = date.toLocaleDateString('es-ES', { 
                  month: 'long', 
                  year: 'numeric' 
                });
                
                return (
                  <tr key={index}>
                    <td style={{ textTransform: 'capitalize' }}>{monthName}</td>
                    <td style={{ color: '#00d9a3' }}>
                      {month.total_income.toLocaleString('es-ES', { 
                        style: 'currency', 
                        currency: 'EUR' 
                      })}
                    </td>
                    <td style={{ color: '#e94560' }}>
                      {month.total_expenses.toLocaleString('es-ES', { 
                        style: 'currency', 
                        currency: 'EUR' 
                      })}
                    </td>
                    <td style={{ 
                      color: month.balance >= 0 ? '#00d9a3' : '#e94560',
                      fontWeight: 600 
                    }}>
                      {month.balance.toLocaleString('es-ES', { 
                        style: 'currency', 
                        currency: 'EUR' 
                      })}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Reports;
