// frontend/src/services/reportsService.js
import api from './api';

export const reportsService = {
  getDailySales: async (date) => {
    const params = date ? { report_date: date } : {};
    const response = await api.get('/reports/daily-sales', { params });
    return response.data;
  },

  getItemWiseReport: async (fromDate, toDate, category) => {
    const params = {
      from_date: fromDate,
      to_date: toDate,
      ...(category && { category })
    };
    const response = await api.get('/reports/item-wise', { params });
    return response.data;
  },

  getCustomerWiseReport: async (fromDate, toDate) => {
    const params = {
      from_date: fromDate,
      to_date: toDate
    };
    const response = await api.get('/reports/customer-wise', { params });
    return response.data;
  },

  getGSTSummary: async (fromDate, toDate) => {
    const params = {
      from_date: fromDate,
      to_date: toDate
    };
    const response = await api.get('/reports/gst-summary', { params });
    return response.data;
  },

  getProfitLossReport: async (fromDate, toDate) => {
    const params = {
      from_date: fromDate,
      to_date: toDate
    };
    const response = await api.get('/reports/profit-loss', { params });
    return response.data;
  },

  getStockReport: async (category, lowStockOnly) => {
    const params = {
      ...(category && { category }),
      ...(lowStockOnly && { low_stock_only: lowStockOnly })
    };
    const response = await api.get('/reports/stock-report', { params });
    return response.data;
  }
};