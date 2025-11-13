import React, { useState, useEffect } from 'react';
import {
  getCategories,
  createCategory,
  updateCategory,
  deleteCategory,
  createSubcategory,
  deleteSubcategory,
  initDefaultCategories
} from '../services/api';

function Categories() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newCategory, setNewCategory] = useState('');
  const [newSubcategory, setNewSubcategory] = useState({});
  const [editingId, setEditingId] = useState(null);
  const [editingName, setEditingName] = useState('');

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      setLoading(true);
      const response = await getCategories();
      setCategories(response.data);
    } catch (error) {
      console.error('Error cargando categorías:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCategory = async (e) => {
    e.preventDefault();
    if (!newCategory.trim()) return;

    try {
      await createCategory({ name: newCategory.trim() });
      setNewCategory('');
      loadCategories();
    } catch (error) {
      console.error('Error creando categoría:', error);
      alert('Error al crear la categoría. Puede que ya exista.');
    }
  };

  const handleUpdateCategory = async (id) => {
    if (!editingName.trim()) return;

    try {
      await updateCategory(id, { name: editingName.trim() });
      setEditingId(null);
      setEditingName('');
      loadCategories();
    } catch (error) {
      console.error('Error actualizando categoría:', error);
      alert('Error al actualizar la categoría');
    }
  };

  const handleDeleteCategory = async (id) => {
    if (window.confirm('¿Estás seguro? Esto eliminará la categoría y todas sus subcategorías.')) {
      try {
        await deleteCategory(id);
        loadCategories();
      } catch (error) {
        console.error('Error eliminando categoría:', error);
        alert('Error al eliminar la categoría');
      }
    }
  };

  const handleCreateSubcategory = async (categoryId) => {
    const name = newSubcategory[categoryId];
    if (!name?.trim()) return;

    try {
      await createSubcategory(categoryId, { 
        name: name.trim(),
        category_id: categoryId 
      });
      setNewSubcategory({ ...newSubcategory, [categoryId]: '' });
      loadCategories();
    } catch (error) {
      console.error('Error creando subcategoría:', error);
      alert('Error al crear la subcategoría');
    }
  };

  const handleDeleteSubcategory = async (subcategoryId) => {
    if (window.confirm('¿Estás seguro de eliminar esta subcategoría?')) {
      try {
        await deleteSubcategory(subcategoryId);
        loadCategories();
      } catch (error) {
        console.error('Error eliminando subcategoría:', error);
        alert('Error al eliminar la subcategoría');
      }
    }
  };

  const handleInitDefaults = async () => {
    if (window.confirm('¿Quieres inicializar las categorías por defecto?')) {
      try {
        await initDefaultCategories();
        loadCategories();
      } catch (error) {
        console.error('Error inicializando categorías:', error);
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
        <h1 className="page-title">Categorías</h1>
        <p className="page-subtitle">Gestiona las categorías y subcategorías de tus gastos</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Nueva Categoría</h2>
        </div>
        <form onSubmit={handleCreateCategory} style={{ display: 'flex', gap: '1rem' }}>
          <input
            type="text"
            className="form-control"
            placeholder="Nombre de la categoría..."
            value={newCategory}
            onChange={(e) => setNewCategory(e.target.value)}
            style={{ flex: 1 }}
          />
          <button type="submit" className="btn btn-primary">
            Añadir Categoría
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleInitDefaults}
          >
            Cargar Por Defecto
          </button>
        </form>
      </div>

      <div className="grid grid-2">
        {categories.map(category => (
          <div key={category.id} className="card">
            <div className="card-header">
              {editingId === category.id ? (
                <div style={{ display: 'flex', gap: '0.5rem', width: '100%' }}>
                  <input
                    type="text"
                    className="form-control"
                    value={editingName}
                    onChange={(e) => setEditingName(e.target.value)}
                    autoFocus
                  />
                  <button
                    className="btn btn-small btn-success"
                    onClick={() => handleUpdateCategory(category.id)}
                  >
                    ✓
                  </button>
                  <button
                    className="btn btn-small btn-secondary"
                    onClick={() => {
                      setEditingId(null);
                      setEditingName('');
                    }}
                  >
                    ✗
                  </button>
                </div>
              ) : (
                <>
                  <h3 className="card-title">{category.name}</h3>
                  <div>
                    <button
                      className="btn btn-small btn-secondary"
                      onClick={() => {
                        setEditingId(category.id);
                        setEditingName(category.name);
                      }}
                      style={{ marginRight: '0.5rem' }}
                    >
                      Editar
                    </button>
                    <button
                      className="btn btn-small btn-danger"
                      onClick={() => handleDeleteCategory(category.id)}
                    >
                      Eliminar
                    </button>
                  </div>
                </>
              )}
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <h4 style={{ fontSize: '0.875rem', color: '#a8a8a8', marginBottom: '0.5rem' }}>
                Subcategorías ({category.subcategories?.length || 0})
              </h4>
              
              {category.subcategories && category.subcategories.length > 0 && (
                <ul style={{ listStyle: 'none', padding: 0 }}>
                  {category.subcategories.map(sub => (
                    <li
                      key={sub.id}
                      style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        padding: '0.5rem',
                        marginBottom: '0.25rem',
                        backgroundColor: 'var(--bg-tertiary)',
                        borderRadius: '5px'
                      }}
                    >
                      <span>{sub.name}</span>
                      <button
                        className="btn btn-small btn-danger"
                        onClick={() => handleDeleteSubcategory(sub.id)}
                      >
                        ✗
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input
                type="text"
                className="form-control"
                placeholder="Nueva subcategoría..."
                value={newSubcategory[category.id] || ''}
                onChange={(e) => setNewSubcategory({
                  ...newSubcategory,
                  [category.id]: e.target.value
                })}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleCreateSubcategory(category.id);
                  }
                }}
              />
              <button
                className="btn btn-small btn-primary"
                onClick={() => handleCreateSubcategory(category.id)}
              >
                Añadir
              </button>
            </div>
          </div>
        ))}
      </div>

      {categories.length === 0 && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: '#a8a8a8', marginBottom: '1rem' }}>
            No hay categorías creadas
          </p>
          <button className="btn btn-primary" onClick={handleInitDefaults}>
            Cargar Categorías Por Defecto
          </button>
        </div>
      )}
    </div>
  );
}

export default Categories;
