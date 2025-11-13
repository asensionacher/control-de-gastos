import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import './App.css';
import Dashboard from './pages/Dashboard';
import Transactions from './pages/Transactions';
import Upload from './pages/Upload';
import Categories from './pages/Categories';
import Reports from './pages/Reports';
import Login from './pages/Login';
import Register from './pages/Register';

// Componente para rutas protegidas
function PrivateRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
}

// Componente de navegación
function Navigation() {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="nav-container">
        <h1 className="nav-logo">💰 Control de Gastos</h1>
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-link">Dashboard</Link>
          </li>
          <li className="nav-item">
            <Link to="/transactions" className="nav-link">Transacciones</Link>
          </li>
          <li className="nav-item">
            <Link to="/upload" className="nav-link">Subir CSV/XLS</Link>
          </li>
          <li className="nav-item">
            <Link to="/categories" className="nav-link">Categorías</Link>
          </li>
          <li className="nav-item">
            <Link to="/reports" className="nav-link">Reportes</Link>
          </li>
          <li className="nav-item" style={{ marginLeft: 'auto' }}>
            <span className="nav-link" style={{ color: '#666' }}>👤 {username}</span>
          </li>
          <li className="nav-item">
            <button onClick={handleLogout} className="nav-link" style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              color: '#dc3545'
            }}>
              Cerrar Sesión
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route path="/*" element={
            <PrivateRoute>
              <Navigation />
              <main className="main-content">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/transactions" element={<Transactions />} />
                  <Route path="/upload" element={<Upload />} />
                  <Route path="/categories" element={<Categories />} />
                  <Route path="/reports" element={<Reports />} />
                </Routes>
              </main>
            </PrivateRoute>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
