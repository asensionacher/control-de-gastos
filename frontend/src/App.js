import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Dashboard from './pages/Dashboard';
import Transactions from './pages/Transactions';
import Upload from './pages/Upload';
import Categories from './pages/Categories';
import Reports from './pages/Reports';

function App() {
  return (
    <Router>
      <div className="App">
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
            </ul>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/transactions" element={<Transactions />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/categories" element={<Categories />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
