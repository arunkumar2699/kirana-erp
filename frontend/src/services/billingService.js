// frontend/src/services/billingService.js
import api from './api';

export const billingService = {
  createBill: async (billData) => {
    const response = await api.post('/billing/create', billData);
    return response.data;
  },

  getBill: async (billNumber) => {
    const response = await api.get(`/billing/retrieve/${billNumber}`);
    return response.data;
  },

  updateBill: async (billId, updateData) => {
    const response = await api.put(`/billing/update/${billId}`, updateData);
    return response.data;
  },

  holdBill: async (billId) => {
    const response = await api.post(`/billing/hold/${billId}`);
    return response.data;
  },

  getPendingBills: async () => {
    const response = await api.get('/billing/pending');
    return response.data;
  },

  searchBills: async (params) => {
    const response = await api.get('/billing/search', { params });
    return response.data;
  },

  getBillFormats: async () => {
    const response = await api.get('/billing/formats');
    return response.data;
  }
};