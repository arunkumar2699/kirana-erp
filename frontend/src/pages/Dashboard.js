// frontend/src/pages/Dashboard.js
import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import api from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    todaySales: 0,
    totalBills: 0,
    lowStockItems: 0,
    pendingPayments: 0
  });
  const [loading, setLoading] = useState(true);
  const [todaysSummary, setTodaysSummary] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

const fetchDashboardData = async () => {
  try {
    setLoading(true);
    // Fetch today's sales report
    const [salesResponse, lowStockResponse] = await Promise.all([
      api.get('/reports/daily-sales').catch(() => ({ data: { summary: {} } })),
      api.get('/inventory/low-stock-alerts').catch(() => ({ data: [] }))
    ]);
    
    setTodaysSummary(salesResponse.data);
    setStats({
      todaySales: salesResponse.data.summary?.net_amount || 0,
      totalBills: salesResponse.data.summary?.total_bills || 0,
      lowStockItems: lowStockResponse.data?.length || 0,
      pendingPayments: 0
    });
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error);
    // Set default values on error
    setStats({
      todaySales: 0,
      totalBills: 0,
      lowStockItems: 0,
      pendingPayments: 0
    });
  } finally {
    setLoading(false);
  }
};

  const StatCard = ({ title, value, color, prefix = '' }) => (
    <div className={`stat-card ${color}`}>
      <h3>{title}</h3>
      <p className="stat-value">{prefix}{value.toLocaleString()}</p>
    </div>
  );

  if (loading) {
    return <div className="dashboard loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Welcome to Kirana ERP</p>
      </div>

      <div className="stats-grid">
        <StatCard 
          title="Today's Sales" 
          value={stats.todaySales} 
          color="blue" 
          prefix="₹ "
        />
        <StatCard 
          title="Total Bills" 
          value={stats.totalBills} 
          color="green"
        />
        <StatCard 
          title="Low Stock Items" 
          value={stats.lowStockItems} 
          color="yellow"
        />
        <StatCard 
          title="Pending Payments" 
          value={stats.pendingPayments} 
          color="purple" 
          prefix="₹ "
        />
      </div>

      {todaysSummary && todaysSummary.top_selling_items && (
        <div className="dashboard-section">
          <h2>Top Selling Items Today</h2>
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Item Code</th>
                  <th>Item Name</th>
                  <th>Quantity</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                {todaysSummary.top_selling_items.map((item, index) => (
                  <tr key={index}>
                    <td>{item.code}</td>
                    <td>{item.name}</td>
                    <td>{item.quantity}</td>
                    <td>₹ {item.amount.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {todaysSummary && todaysSummary.payment_methods && (
        <div className="dashboard-section">
          <h2>Payment Methods</h2>
          <div className="payment-methods">
            {Object.entries(todaysSummary.payment_methods).map(([method, data]) => (
              <div key={method} className="payment-method-card">
                <h4>{method.toUpperCase()}</h4>
                <p>{data.count} transactions</p>
                <p className="amount">₹ {data.amount.toFixed(2)}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;