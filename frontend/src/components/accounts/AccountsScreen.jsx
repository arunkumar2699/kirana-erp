// frontend/src/components/accounts/AccountsScreen.jsx
import React from 'react';
import './AccountsScreen.css';

const AccountsScreen = () => {
  return (
    <div className="accounts-screen">
      <h1>Accounts & Ledgers</h1>
      <div className="accounts-sections">
        <div className="section-card">
          <h2>Customers</h2>
          <p>Manage customer accounts and outstanding balances</p>
          <button className="section-btn">View Customers</button>
        </div>
        <div className="section-card">
          <h2>Suppliers</h2>
          <p>Manage supplier accounts and payments</p>
          <button className="section-btn">View Suppliers</button>
        </div>
        <div className="section-card">
          <h2>Ledgers</h2>
          <p>View and manage all ledger accounts</p>
          <button className="section-btn">View Ledgers</button>
        </div>
      </div>
    </div>
  );
};

export default AccountsScreen;
