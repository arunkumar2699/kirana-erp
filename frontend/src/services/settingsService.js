// frontend/src/services/settingsService.js
import api from './api';

export const settingsService = {
  getCompanyInfo: async () => {
    const response = await api.get('/settings/company-info');
    return response.data;
  },

  updateCompanyInfo: async (companyData) => {
    const response = await api.put('/settings/company-info', companyData);
    return response.data;
  },

  getPrintFormats: async () => {
    const response = await api.get('/settings/print-formats');
    return response.data;
  },

  getBillSeries: async () => {
    const response = await api.get('/settings/bill-series');
    return response.data;
  },

  updateBillSeries: async (seriesData) => {
    const response = await api.put('/settings/bill-series', seriesData);
    return response.data;
  },

  getRemoteAccessSettings: async () => {
    const response = await api.get('/settings/remote-access');
    return response.data;
  },

  updateRemoteAccessSettings: async (accessSettings) => {
    const response = await api.put('/settings/remote-access', accessSettings);
    return response.data;
  }
};