// frontend/src/services/accountsService.js
import api from './api';

export const accountsService = {
  // Customer APIs
  getCustomers: async (params) => {
    const response = await api.get('/accounts/customers', { params });
    return response.data;
  },

  createCustomer: async (customerData) => {
    const response = await api.post('/accounts/customers', customerData);
    return response.data;
  },

  updateCustomer: async (customerId, updateData) => {
    const response = await api.put(`/accounts/customers/${customerId}`, updateData);
    return response.data;
  },

  getCustomer: async (customerId) => {
    const response = await api.get(`/accounts/customers/${customerId}`);
    return response.data;
  },

  // Supplier APIs
  getSuppliers: async (params) => {
    const response = await api.get('/accounts/suppliers', { params });
    return response.data;
  },

  createSupplier: async (supplierData) => {
    const response = await api.post('/accounts/suppliers', supplierData);
    return response.data;
  },

  updateSupplier: async (supplierId, updateData) => {
    const response = await api.put(`/accounts/suppliers/${supplierId}`, updateData);
    return response.data;
  },

  // Ledger APIs
  getLedgers: async (params) => {
    const response = await api.get('/accounts/ledgers', { params });
    return response.data;
  },

  getLedgerDetails: async (ledgerId, params) => {
    const response = await api.get(`/accounts/ledgers/${ledgerId}`, { params });
    return response.data;
  }
};