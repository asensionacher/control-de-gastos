import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para añadir el token a las peticiones
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth
export const register = (username, password) => {
  return api.post('/api/auth/register', { username, password });
};

export const login = (username, password) => {
  return api.post('/api/auth/login', { username, password });
};

export const getCurrentUser = () => {
  return api.get('/api/auth/me');
};

// Transactions
export const getTransactions = (params = {}) => {
  return api.get('/api/transactions/', { params });
};

export const getTransaction = (id) => {
  return api.get(`/api/transactions/${id}`);
};

export const getSimilarTransactionsCount = (params) => {
  return api.get('/api/transactions/', { params });
};

export const updateTransaction = (id, data) => {
  return api.put(`/api/transactions/${id}`, data);
};

export const bulkCategorize = (transactionIds, categoryId, subcategoryId = null) => {
  return api.post('/api/transactions/bulk-categorize', {
    transaction_ids: transactionIds,
    category_id: categoryId,
    subcategory_id: subcategoryId
  });
};

export const bulkDelete = (transactionIds) => {
  return api.post('/api/transactions/bulk-delete', transactionIds);
};

export const exportTransactions = async () => {
  const response = await api.get('/api/transactions/export', {
    responseType: 'blob'
  });

  // Crear un blob URL y disparar la descarga
  const blob = new Blob([response.data], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;

  // Obtener el nombre del archivo de los headers o usar uno por defecto
  const contentDisposition = response.headers['content-disposition'];
  let filename = 'transacciones.csv';
  if (contentDisposition) {
    const filenameMatch = contentDisposition.match(/filename="(.+)"/);
    if (filenameMatch) {
      filename = filenameMatch[1];
    }
  }

  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);

  return response;
};

export const importTransactions = (file) => {
  const formData = new FormData();
  formData.append('file', file);

  return api.post('/api/transactions/import', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }).then(response => response.data);
};

export const deleteTransaction = (id) => {
  return api.delete(`/api/transactions/${id}`);
};

export const getUncategorizedCount = () => {
  return api.get('/api/transactions/uncategorized/count');
};

// Categories
export const getCategories = () => {
  return api.get('/api/categories/');
};

export const createCategory = (data) => {
  return api.post('/api/categories/', data);
};

export const updateCategory = (id, data) => {
  return api.put(`/api/categories/${id}`, data);
};

export const deleteCategory = (id) => {
  return api.delete(`/api/categories/${id}`);
};

export const getSubcategories = (categoryId) => {
  return api.get(`/api/categories/${categoryId}/subcategories`);
};

export const createSubcategory = (categoryId, data) => {
  return api.post(`/api/categories/${categoryId}/subcategories`, data);
};

export const updateSubcategory = (id, data) => {
  return api.put(`/api/categories/subcategories/${id}`, data);
};

export const deleteSubcategory = (id) => {
  return api.delete(`/api/categories/subcategories/${id}`);
};

export const initDefaultCategories = () => {
  return api.post('/api/categories/init-default');
};

// Upload
export const uploadCSV = (files, bankType = null) => {
  const formData = new FormData();

  // Soportar múltiples archivos o un solo archivo
  if (Array.isArray(files)) {
    files.forEach(file => {
      formData.append('files', file);
    });
  } else {
    formData.append('files', files);
  }

  if (bankType) {
    formData.append('bank_type', bankType);
  }

  return api.post('/api/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const getBankTypes = () => {
  return api.get('/api/upload/bank-types');
};

export const detectBank = (file) => {
  const formData = new FormData();
  formData.append('file', file);

  return api.post('/api/upload/detect-bank', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Reports
export const getMonthlyReport = (months = 12) => {
  return api.get('/api/reports/monthly', { params: { months } });
};

export const getCategoryReport = (startDate, endDate) => {
  return api.get('/api/reports/by-category', {
    params: { start_date: startDate, end_date: endDate }
  });
};

export const getTopExpenses = (limit = 10, startDate, endDate) => {
  return api.get('/api/reports/top-expenses', {
    params: { limit, start_date: startDate, end_date: endDate }
  });
};

export const getReportSummary = (months = 6) => {
  return api.get('/api/reports/summary', { params: { months } });
};

export const getStats = () => {
  return api.get('/api/reports/stats');
};

export default api;
