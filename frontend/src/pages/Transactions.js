import React, { useState, useEffect } from 'react';
import { getTransactions, getCategories, updateTransaction, deleteTransaction, bulkCategorize, bulkDelete } from '../services/api';

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState(null);
  const [selectedIds, setSelectedIds] = useState([]);
  const [bulkCategory, setBulkCategory] = useState('');
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const itemsPerPage = 100;
  const [filters, setFilters] = useState({
    bank_type: '',
    category_id: '',
    transaction_type: '',
    description: '',
    start_date: '',
    end_date: ''
  });

  useEffect(() => {
    loadCategories();
    loadTransactions();
  }, [page]);

  useEffect(() => {
    // Reset to page 1 when filters change
    setPage(1);
  }, [filters]);

  const loadCategories = async () => {
    try {
      const response = await getCategories();
      setCategories(response.data);
    } catch (error) {
      console.error('Error cargando categorías:', error);
    }
  };

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const params = {
        skip: (page - 1) * itemsPerPage,
        limit: itemsPerPage
      };
      if (filters.bank_type) params.bank_type = filters.bank_type;
      if (filters.category_id) {
        // Si es "null", enviar como parámetro especial para filtrar sin categoría
        params.category_id = filters.category_id === 'null' ? 'null' : filters.category_id;
      }
      if (filters.transaction_type) params.transaction_type = filters.transaction_type;
      if (filters.description && filters.description.length >= 3) params.description = filters.description;
      if (filters.start_date) params.start_date = filters.start_date;
      if (filters.end_date) params.end_date = filters.end_date;
      
      const response = await getTransactions(params);
      setTransactions(response.data);
      
      // Get total count for pagination
      const countParams = { ...params };
      delete countParams.skip;
      delete countParams.limit;
      const countResponse = await getTransactions({ ...countParams, limit: 1000000 });
      setTotalCount(countResponse.data.length);
    } catch (error) {
      console.error('Error cargando transacciones:', error);
    } finally {
      setLoading(false);
    }
  };

  const reloadTransactionsWithoutScroll = async () => {
    try {
      const params = {
        skip: (page - 1) * itemsPerPage,
        limit: itemsPerPage
      };
      if (filters.bank_type) params.bank_type = filters.bank_type;
      if (filters.category_id) {
        // Si es "null", enviar como parámetro especial para filtrar sin categoría
        params.category_id = filters.category_id === 'null' ? 'null' : filters.category_id;
      }
      if (filters.transaction_type) params.transaction_type = filters.transaction_type;
      if (filters.description && filters.description.length >= 3) params.description = filters.description;
      if (filters.start_date) params.start_date = filters.start_date;
      if (filters.end_date) params.end_date = filters.end_date;
      
      const response = await getTransactions(params);
      setTransactions(response.data);
      
      // Update total count
      const countParams = { ...params };
      delete countParams.skip;
      delete countParams.limit;
      const countResponse = await getTransactions({ ...countParams, limit: 1000000 });
      setTotalCount(countResponse.data.length);
    } catch (error) {
      console.error('Error cargando transacciones:', error);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const handleApplyFilters = () => {
    setPage(1);
    loadTransactions();
  };

  const handleClearFilters = () => {
    setFilters({
      bank_type: '',
      category_id: '',
      transaction_type: '',
      description: '',
      start_date: '',
      end_date: ''
    });
    setPage(1);
    // Recargar inmediatamente con filtros limpios
    setTimeout(() => loadTransactions(), 0);
  };

  const handleUpdateCategory = async (transactionId, categoryId, subcategoryId) => {
    try {
      await updateTransaction(transactionId, {
        category_id: categoryId ? parseInt(categoryId) : null,
        subcategory_id: subcategoryId ? parseInt(subcategoryId) : null
      });
      setEditingId(null);
      reloadTransactionsWithoutScroll();
    } catch (error) {
      console.error('Error actualizando transacción:', error);
      alert('Error al actualizar la transacción');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar esta transacción?')) {
      try {
        await deleteTransaction(id);
        reloadTransactionsWithoutScroll();
      } catch (error) {
        console.error('Error eliminando transacción:', error);
        alert('Error al eliminar la transacción');
      }
    }
  };

  const handleSelectTransaction = (id) => {
    setSelectedIds(prev => {
      if (prev.includes(id)) {
        return prev.filter(i => i !== id);
      } else {
        return [...prev, id];
      }
    });
  };

  const handleSelectAll = () => {
    if (selectedIds.length === transactions.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(transactions.map(t => t.id));
    }
  };

  const handleBulkCategorize = async () => {
    if (selectedIds.length === 0) {
      alert('Selecciona al menos una transacción');
      return;
    }
    
    if (bulkCategory === '') {
      alert('Selecciona una categoría');
      return;
    }

    try {
      // Si es "null" (string), enviar null real, sino el valor parseado
      const categoryValue = bulkCategory === 'null' ? null : parseInt(bulkCategory);
      await bulkCategorize(selectedIds, categoryValue);
      setSelectedIds([]);
      setBulkCategory('');
      reloadTransactionsWithoutScroll();
    } catch (error) {
      console.error('Error categorizando transacciones:', error);
      alert('Error al categorizar las transacciones');
    }
  };

  const handleBulkDelete = async () => {
    if (selectedIds.length === 0) {
      alert('Selecciona al menos una transacción');
      return;
    }

    if (window.confirm(`¿Estás seguro de eliminar ${selectedIds.length} transacción${selectedIds.length !== 1 ? 'es' : ''}?`)) {
      try {
        await bulkDelete(selectedIds);
        setSelectedIds([]);
        reloadTransactionsWithoutScroll();
      } catch (error) {
        console.error('Error eliminando transacciones:', error);
        alert('Error al eliminar las transacciones');
      }
    }
  };

  const handleQuickCategorize = async (transactionId, categoryId) => {
    try {
      // Find the transaction to get its description
      const transaction = transactions.find(t => t.id === transactionId);
      if (!transaction) return;
      
      // Convertir vacío a null
      const categoryValue = categoryId === '' ? null : parseInt(categoryId);
      
      // Count how many transactions have the same description
      const similarTransactions = transactions.filter(
        t => t.description === transaction.description
      );
      
      let applyToAll = false;
      
      // If there are more transactions with the same description, ask
      if (similarTransactions.length > 1) {
        const categoryName = categoryValue === null ? 'Sin categoría' : 
          categories.find(c => c.id === categoryValue)?.name || 'esta categoría';
        
        const confirmed = window.confirm(
          `Hay ${similarTransactions.length} transacciones con la descripción "${transaction.description}".\n\n` +
          `¿Deseas aplicar "${categoryName}" a todas ellas?`
        );
        applyToAll = confirmed;
      }
      
      await updateTransaction(transactionId, {
        category_id: categoryValue,
        apply_to_all: applyToAll
      });
      reloadTransactionsWithoutScroll();
    } catch (error) {
      console.error('Error actualizando transacción:', error);
      alert('Error al actualizar la transacción');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const formatAmount = (amount) => {
    return amount.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' });
  };

  const totalPages = Math.ceil(totalCount / itemsPerPage);

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleGoToPage = (pageNum) => {
    setPage(pageNum);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">Transacciones</h1>
        <p className="page-subtitle">Gestiona tus movimientos bancarios</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Filtros</h2>
        </div>
        <div className="grid grid-4">
          <div className="form-group">
            <label className="form-label">Descripción</label>
            <input
              type="text"
              name="description"
              className="form-control"
              value={filters.description}
              onChange={handleFilterChange}
              placeholder="Buscar por descripción (min. 3 caracteres)"
            />
            {filters.description && filters.description.length > 0 && filters.description.length < 3 && (
              <p style={{ color: '#ff9f1c', fontSize: '0.875rem', marginTop: '0.25rem' }}>
                Escribe al menos 3 caracteres
              </p>
            )}
          </div>

          <div className="form-group">
            <label className="form-label">Tipo</label>
            <select
              name="transaction_type"
              className="form-control"
              value={filters.transaction_type}
              onChange={handleFilterChange}
            >
              <option value="">Todos</option>
              <option value="expense">Gastos</option>
              <option value="income">Ingresos</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Banco</label>
            <select
              name="bank_type"
              className="form-control"
              value={filters.bank_type}
              onChange={handleFilterChange}
            >
              <option value="">Todos</option>
              <option value="kutxabank_account">Kutxabank - Cuenta</option>
              <option value="kutxabank_card">Kutxabank - Tarjeta</option>
              <option value="openbank">Openbank</option>
              <option value="imaginbank">Imaginbank</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Categoría</label>
            <select
              name="category_id"
              className="form-control"
              value={filters.category_id}
              onChange={handleFilterChange}
            >
              <option value="">Todas</option>
              <option value="null">Sin categoría</option>
              {categories.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="grid grid-4">
          <div className="form-group">
            <label className="form-label">Desde</label>
            <input
              type="date"
              name="start_date"
              className="form-control"
              value={filters.start_date}
              onChange={handleFilterChange}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Hasta</label>
            <input
              type="date"
              name="end_date"
              className="form-control"
              value={filters.end_date}
              onChange={handleFilterChange}
            />
          </div>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button className="btn btn-primary" onClick={handleApplyFilters}>
            Aplicar Filtros
          </button>
          <button className="btn btn-secondary" onClick={handleClearFilters}>
            Limpiar Filtros
          </button>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">
            Lista de Transacciones ({totalCount})
          </h2>
          <p style={{ color: '#a8a8a8', fontSize: '0.9rem', marginTop: '0.5rem' }}>
            Página {page} de {totalPages} - Mostrando {transactions.length} de {totalCount}
          </p>
        </div>

        {/* Bulk actions */}
        {selectedIds.length > 0 && (
          <div style={{ 
            padding: '1rem', 
            background: 'rgba(0, 217, 163, 0.1)', 
            borderBottom: '1px solid #333',
            display: 'flex',
            alignItems: 'center',
            gap: '1rem'
          }}>
            <span style={{ color: '#00d9a3', fontWeight: 'bold' }}>
              {selectedIds.length} seleccionada{selectedIds.length !== 1 ? 's' : ''}
            </span>
            <select
              className="form-control"
              value={bulkCategory}
              onChange={(e) => setBulkCategory(e.target.value)}
              style={{ maxWidth: '200px' }}
            >
              <option value="">Seleccionar categoría...</option>
              <option value="null">Sin categoría</option>
              {categories.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
            <button 
              className="btn btn-primary btn-small"
              onClick={handleBulkCategorize}
              disabled={!bulkCategory}
            >
              Categorizar
            </button>
            <button 
              className="btn btn-danger btn-small"
              onClick={handleBulkDelete}
            >
              Eliminar
            </button>
            <button 
              className="btn btn-secondary btn-small"
              onClick={() => setSelectedIds([])}
            >
              Cancelar
            </button>
          </div>
        )}

        {loading ? (
          <div className="loading">
            <div className="spinner"></div>
            <p>Cargando...</p>
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th style={{ width: '40px' }}>
                    <input
                      type="checkbox"
                      checked={selectedIds.length === transactions.length && transactions.length > 0}
                      onChange={handleSelectAll}
                      style={{ cursor: 'pointer' }}
                    />
                  </th>
                  <th>Fecha</th>
                  <th>Descripción</th>
                  <th>Banco</th>
                  <th>Importe</th>
                  <th>Categoría</th>
                  <th>Subcategoría</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map(transaction => (
                  <tr 
                    key={transaction.id}
                    style={{ 
                      background: selectedIds.includes(transaction.id) 
                        ? 'rgba(0, 217, 163, 0.05)' 
                        : 'transparent'
                    }}
                  >
                    <td>
                      <input
                        type="checkbox"
                        checked={selectedIds.includes(transaction.id)}
                        onChange={() => handleSelectTransaction(transaction.id)}
                        style={{ cursor: 'pointer' }}
                      />
                    </td>
                    <td>{formatDate(transaction.date)}</td>
                    <td>{transaction.description}</td>
                    <td>
                      <span style={{ fontSize: '0.875rem', color: '#a8a8a8' }}>
                        {transaction.bank_type.replace('_', ' ')}
                      </span>
                    </td>
                    <td>
                      <span className={transaction.amount >= 0 ? 'badge badge-income' : 'badge badge-expense'}>
                        {formatAmount(transaction.amount)}
                      </span>
                    </td>
                    <td>
                      {editingId === transaction.id ? (
                        <select
                          className="form-control"
                          defaultValue={transaction.category_id || ''}
                          onChange={(e) => {
                            const categoryId = e.target.value;
                            handleUpdateCategory(transaction.id, categoryId, null);
                          }}
                        >
                          <option value="">Sin categoría</option>
                          {categories.map(cat => (
                            <option key={cat.id} value={cat.id}>{cat.name}</option>
                          ))}
                        </select>
                      ) : (
                        <select
                          className="form-control"
                          value={transaction.category_id || ''}
                          onChange={(e) => handleQuickCategorize(transaction.id, e.target.value)}
                          style={{ 
                            background: transaction.category_id ? '#1a1a1a' : 'rgba(255, 159, 28, 0.1)',
                            border: transaction.category_id ? '1px solid #333' : '1px solid rgba(255, 159, 28, 0.3)'
                          }}
                        >
                          <option value="">Sin categoría</option>
                          {categories.map(cat => (
                            <option key={cat.id} value={cat.id}>{cat.name}</option>
                          ))}
                        </select>
                      )}
                    </td>
                    <td>
                      {transaction.subcategory?.name || '-'}
                    </td>
                    <td>
                      {editingId === transaction.id ? (
                        <button
                          className="btn btn-small btn-secondary"
                          onClick={() => setEditingId(null)}
                        >
                          Cancelar
                        </button>
                      ) : (
                        <>
                          <button
                            className="btn btn-small btn-danger"
                            onClick={() => handleDelete(transaction.id)}
                          >
                            Eliminar
                          </button>
                        </>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Paginación */}
        {!loading && totalPages > 1 && (
          <div style={{ 
            padding: '1rem', 
            borderTop: '1px solid #333',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <button 
              className="btn btn-small btn-secondary"
              onClick={handlePreviousPage}
              disabled={page === 1}
            >
              ← Anterior
            </button>
            
            <div style={{ display: 'flex', gap: '0.25rem' }}>
              {/* First page */}
              {page > 3 && (
                <>
                  <button
                    className="btn btn-small btn-secondary"
                    onClick={() => handleGoToPage(1)}
                  >
                    1
                  </button>
                  {page > 4 && <span style={{ padding: '0.5rem', color: '#a8a8a8' }}>...</span>}
                </>
              )}
              
              {/* Pages around current */}
              {Array.from({ length: totalPages }, (_, i) => i + 1)
                .filter(p => p >= page - 2 && p <= page + 2)
                .map(p => (
                  <button
                    key={p}
                    className={`btn btn-small ${p === page ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => handleGoToPage(p)}
                    disabled={p === page}
                  >
                    {p}
                  </button>
                ))}
              
              {/* Last page */}
              {page < totalPages - 2 && (
                <>
                  {page < totalPages - 3 && <span style={{ padding: '0.5rem', color: '#a8a8a8' }}>...</span>}
                  <button
                    className="btn btn-small btn-secondary"
                    onClick={() => handleGoToPage(totalPages)}
                  >
                    {totalPages}
                  </button>
                </>
              )}
            </div>
            
            <button 
              className="btn btn-small btn-secondary"
              onClick={handleNextPage}
              disabled={page === totalPages}
            >
              Siguiente →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default Transactions;
