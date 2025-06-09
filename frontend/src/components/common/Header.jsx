// frontend/src/components/common/Header.jsx
import React from 'react';
import './Header.css';

const Header = ({ user, onToggleSidebar }) => {
  return (
    <header className="app-header">
      <button className="menu-toggle" onClick={onToggleSidebar}>
        ☰
      </button>
      
      <div className="header-info">
        <span className="user-info">Welcome, {user?.full_name || user?.username}</span>
        <span className="separator">|</span>
        <span className="year-info">2024-2025</span>
      </div>
    </header>
  );
};

export default Header;