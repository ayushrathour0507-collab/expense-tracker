import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { expenseAPI } from '../services/api';

export default function Dashboard() {
  const [expenses, setExpenses] = useState([]);
  const [summary, setSummary] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchExpenses();
    fetchSummary();
  }, []);

  const fetchExpenses = async () => {
    try {
      const response = await expenseAPI.getExpenses();
      setExpenses(response.data);
    } catch (err) {
      setError('Failed to fetch expenses');
      if (err.response?.status === 401) {
        navigate('/login');
      }
    }
  };

  const fetchSummary = async () => {
    try {
      const response = await expenseAPI.getExpenseSummary();
      setSummary(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch summary');
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this expense?')) {
      try {
        await expenseAPI.deleteExpense(id);
        setExpenses(expenses.filter((exp) => exp.id !== id));
        // Refetch summary
        fetchSummary();
      } catch (err) {
        setError('Failed to delete expense');
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  const totalAmount = expenses.reduce((sum, exp) => sum + exp.amount, 0);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-500 text-lg">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-800">
            Expense Tracker
          </h1>
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
          >
            Logout
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Total Amount Card */}
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow p-6 text-white">
            <h2 className="text-lg font-semibold mb-2">Total Expenses</h2>
            <p className="text-4xl font-bold">₹{totalAmount.toFixed(2)}</p>
          </div>

          {/* Category Summary */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
              Category Breakdown
            </h2>
            {summary.length > 0 ? (
              <div className="space-y-2">
                {summary.map((item) => (
                  <div key={item.category} className="flex justify-between items-center">
                    <span className="text-gray-600">{item.category}</span>
                    <span className="font-semibold text-gray-800">
                      ₹{item.total_amount.toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No expenses yet</p>
            )}
          </div>
        </div>

        {/* Add Expense Button */}
        <button
          onClick={() => navigate('/add-expense')}
          className="mb-6 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-6 rounded-lg transition duration-200"
        >
          + Add New Expense
        </button>

        {/* Expenses List */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-800">
              Recent Expenses
            </h2>
          </div>

          {expenses.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">
                      Category
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">
                      Amount
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">
                      Note
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">
                      Action
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {expenses.map((expense) => (
                    <tr
                      key={expense.id}
                      className="hover:bg-gray-50 transition duration-200"
                    >
                      <td className="px-6 py-4 text-sm text-gray-800">
                        {new Date(expense.date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold">
                          {expense.category}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm font-semibold text-gray-800">
                        ₹{expense.amount.toFixed(2)}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600 max-w-xs truncate">
                        {expense.note || '-'}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <button
                          onClick={() => handleDelete(expense.id)}
                          className="text-red-500 hover:text-red-700 font-semibold transition duration-200"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="px-6 py-12 text-center">
              <p className="text-gray-500 text-lg">
                No expenses yet. Click "Add New Expense" to get started!
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
