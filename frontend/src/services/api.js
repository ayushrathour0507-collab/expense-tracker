import axios from 'axios';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_URL ||
  'http://127.0.0.1:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add token to headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth API calls
export const authAPI = {
  register: (email, password) =>
    api.post('/auth/register', { email, password }),
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
};

// Expense API calls
export const expenseAPI = {
  createExpense: (amount, category, date, note) =>
    api.post('/expenses', { amount, category, date, note }),
  getExpenses: () =>
    api.get('/expenses'),
  deleteExpense: (id) =>
    api.delete(`/expenses/${id}`),
  getExpenseSummary: () =>
    api.get('/expenses/summary'),
  updateExpense: (id, data) =>
    api.put(`/expenses/${id}`, data),
};

export default api;
