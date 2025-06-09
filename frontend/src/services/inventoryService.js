// frontend/src/services/inventoryService.js
import api from './api';

export const inventoryService = {
  getItems: async (params) => {
    const response = await api.get('/inventory/items', { params });
    return response.data;
  },

  createItem: async (itemData) => {
    const response = await api.post('/inventory/items', itemData);
    return response.data;
  },

  updateItem: async (itemId, updateData) => {
    const response = await api.put(`/inventory/items/${itemId}`, updateData);
    return response.data;
  },

  deleteItem: async (itemId) => {
    const response = await api.delete(`/inventory/items/${itemId}`);
    return response.data;
  },

  searchItems: async (searchData) => {
    const response = await api.post('/inventory/items/search', searchData);
    return response.data;
  },

  updateStock: async (itemId, quantityChange, reason) => {
    const response = await api.put('/inventory/stock/update', {
      item_id: itemId,
      quantity_change: quantityChange,
      reason
    });
    return response.data;
  },

  getLowStockAlerts: async () => {
    const response = await api.get('/inventory/low-stock-alerts');
    return response.data;
  },

  getCategories: async () => {
    const response = await api.get('/inventory/categories');
    return response.data;
  }
};