// frontend/src/components/common/Sidebar.jsx
import React from 'react';
import './Sidebar.css';

const Sidebar = ({ activeMenu, setActiveMenu, collapsed, onLogout }) => {
  const menuItems = [
    { key: 'dashboard', label: 'Dashboard', icon: '📊' },
    { key: 'billing', label: 'Billing', icon: '🛒' },
    { key: 'inventory', label: 'Inventory', icon: '📦' },
    { key: 'accounts', label: 'Accounts', icon: '👥' },
    { key: 'reports', label: 'Reports', icon: '📈' },
    { key: 'settings', label: 'Settings', icon: '⚙️' },
  ];

  return (
    <div className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        {!collapsed && <h2>Kirana ERP</h2>}
      </div>
      
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.key}
            className={`nav-item ${activeMenu === item.key ? 'active' : ''}`}
            onClick={() => setActiveMenu(item.key)}
            title={collapsed ? item.label : ''}
          >
            <span className="nav-icon">{item.icon}</span>
            {!collapsed && <span className="nav-label">{item.label}</span>}
          </button>
        ))}
      </nav>
      
      <div className="sidebar-footer">
        <button className="nav-item logout" onClick={onLogout}>
          <span className="nav-icon">🚪</span>
          {!collapsed && <span className="nav-label">Logout</span>}
        </button>
      </div>
    </div>
  );
};

export default Sidebar;