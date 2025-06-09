// frontend/src/components/reports/ReportsScreen.jsx
import React from 'react';
import './ReportsScreen.css';

const ReportsScreen = () => {
  const reports = [
    { id: 'daily-sales', title: 'Daily Sales Report', description: 'View today\'s sales summary' },
    { id: 'item-wise', title: 'Item-wise Sales', description: 'Sales analysis by items' },
    { id: 'customer-wise', title: 'Customer-wise Sales', description: 'Sales analysis by customers' },
    { id: 'gst-summary', title: 'GST Summary', description: 'GST collection and payment summary' },
    { id: 'profit-loss', title: 'Profit & Loss', description: 'Profit and loss statement' },
    { id: 'stock-report', title: 'Stock Report', description: 'Current stock valuation' },
  ];

  return (
    <div className="reports-screen">
      <h1>Reports</h1>
      <div className="reports-grid">
        {reports.map(report => (
          <div key={report.id} className="report-card">
            <h3>{report.title}</h3>
            <p>{report.description}</p>
            <button className="generate-btn">Generate Report</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ReportsScreen;
