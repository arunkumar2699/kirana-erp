// frontend/src/components/inventory/InventoryScreen.jsx
import React, { useState, useEffect } from 'react';
import { inventoryService } from '../../services/inventoryService';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';
import './InventoryScreen.css';

const InventoryScreen = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchItems();
    fetchCategories();
  }, [selectedCategory]);

  const fetchItems = async () => {
    try {
      setLoading(true);
      const params = {
        limit: 100,
        category: selectedCategory || undefined
      };
      const data = await inventoryService.getItems(params);
      setItems(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const data = await inventoryService.getCategories();
      setCategories(data);
    } catch (err) {
      console.error('Failed to fetch categories:', err);
    }
  };

  const filteredItems = items.filter(item =>
    item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.item_code.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={fetchItems} />;

  return (
    <div className="inventory-screen">
      <div className="inventory-header">
        <h1>Inventory Management</h1>
        <button className="add-item-btn">+ Add New Item</button>
      </div>

      <div className="inventory-filters">
        <input
          type="text"
          placeholder="Search items..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="category-filter"
        >
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      <div className="inventory-table-container">
        <table className="inventory-table">
          <thead>
            <tr>
              <th>Code</th>
              <th>Name</th>
              <th>Category</th>
              <th>Stock</th>
              <th>Price</th>
              <th>MRP</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredItems.map(item => (
              <tr key={item.id} className={item.current_stock <= item.min_stock_alert ? 'low-stock' : ''}>
                <td>{item.item_code}</td>
                <td>{item.name}</td>
                <td>{item.category}</td>
                <td>{item.current_stock} {item.unit}</td>
                <td>₹{item.selling_price}</td>
                <td>₹{item.mrp}</td>
                <td>
                  <button className="action-btn edit">Edit</button>
                  <button className="action-btn stock">Update Stock</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default InventoryScreen;
