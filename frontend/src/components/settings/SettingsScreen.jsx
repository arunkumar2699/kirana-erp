// frontend/src/components/settings/SettingsScreen.jsx
import React from 'react';
import './SettingsScreen.css';

const SettingsScreen = () => {
  return (
    <div className="settings-screen">
      <h1>Settings</h1>
      <div className="settings-sections">
        <div className="settings-section">
          <h2>Company Information</h2>
          <form className="settings-form">
            <div className="form-group">
              <label>Company Name</label>
              <input type="text" defaultValue="Kirana Store" />
            </div>
            <div className="form-group">
              <label>Address</label>
              <textarea rows="3" defaultValue="123, Main Street, City - 123456" />
            </div>
            <div className="form-group">
              <label>Phone</label>
              <input type="text" defaultValue="9876543210" />
            </div>
            <div className="form-group">
              <label>GSTIN</label>
              <input type="text" defaultValue="27AAAAA0000A1Z5" />
            </div>
            <button type="submit" className="save-btn">Save Changes</button>
          </form>
        </div>
        
        <div className="settings-section">
          <h2>Print Settings</h2>
          <form className="settings-form">
            <div className="form-group">
              <label>Default Print Format</label>
              <select>
                <option>Thermal 58mm</option>
                <option>Thermal 80mm</option>
                <option>A4</option>
                <option>A5</option>
              </select>
            </div>
            <button type="submit" className="save-btn">Save Changes</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default SettingsScreen;
