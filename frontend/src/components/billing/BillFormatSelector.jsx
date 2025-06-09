// frontend/src/components/billing/BillFormatSelector.jsx
import React from 'react';
import './BillFormatSelector.css';

const BillFormatSelector = ({ value, onChange }) => {
  const formats = [
    { value: 'gst_invoice', label: 'GST Invoice' },
    { value: 'sale_challan', label: 'Sale Challan' },
    { value: 'quotation', label: 'Quotation' },
    { value: 'purchase', label: 'Purchase' }
  ];

  return (
    <div className="bill-format-selector">
      <label>Bill Format:</label>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        {formats.map(format => (
          <option key={format.value} value={format.value}>
            {format.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default BillFormatSelector;
