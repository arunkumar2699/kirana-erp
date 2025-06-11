import React, { useState } from 'react';
import './App.css';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import BillingScreen from './components/billing/BillingScreen';
import InventoryScreen from './components/inventory/InventoryScreen';
import AccountsScreen from './components/accounts/AccountsScreen';
import ReportsScreen from './components/reports/ReportsScreen';
import SettingsScreen from './components/settings/SettingsScreen';
import Sidebar from './components/common/Sidebar';
import Header from './components/common/Header';
import LoadingSpinner from './components/common/LoadingSpinner';
import { AuthProvider, useAuth } from './context/AuthContext';

function AppContent() {
  const { isAuthenticated, user, logout, loading } = useAuth();
  const [activeMenu, setActiveMenu] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Handle loading state
  if (loading) {
    return <LoadingSpinner size="large" message="Loading..." />;
  }

  // Handle unauthenticated state
  if (!isAuthenticated) {
    return <Login />;
  }

  const renderContent = () => {
    switch (activeMenu) {
      case 'dashboard':
        return <Dashboard />;
      case 'billing':
        return <BillingScreen />;
      case 'inventory':
        return <InventoryScreen />;
      case 'accounts':
        return <AccountsScreen />;
      case 'reports':
        return <ReportsScreen />;
      case 'settings':
        return <SettingsScreen />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="app">
      <Sidebar 
        activeMenu={activeMenu} 
        setActiveMenu={setActiveMenu}
        collapsed={sidebarCollapsed}
        onLogout={logout}
      />
      <div className="main-content">
        <Header 
          user={user}
          onToggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)}
        />
        <div className="content-area">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;