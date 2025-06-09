// frontend/src/components/billing/PrintPreview.jsx
import React from 'react';
import './PrintPreview.css';

const PrintPreview = ({ billData, onClose }) => {
  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="print-preview-overlay">
      <div className="print-preview-container">
        <div className="print-preview-header">
          <h2>Print Preview</h2>
          <button onClick={onClose} className="close-btn">✕</button>
        </div>
        
        <div className="print-content" id="printable-area">
          <div className="bill-header">
            <h1>KIRANA STORE</h1>
            <p>123, Main Street, City - 123456</p>
            <p>Phone: 9876543210 | GSTIN: 27AAAAA0000A1Z5</p>
          </div>
          
          <div className="bill-type">
            {billData.billType === 'gst_invoice' ? 'TAX INVOICE' : 'SALE CHALLAN'}
          </div>
          
          <div className="bill-details">
            <div>
              <strong>Bill No:</strong> {billData.billNumber}<br />
              <strong>Date:</strong> {billData.date.toLocaleDateString()}
            </div>
            {billData.customer.name && (
              <div>
                <strong>Customer:</strong> {billData.customer.name}<br />
                <strong>Phone:</strong> {billData.customer.phone}
              </div>
            )}
          </div>
          
          <table className="bill-items">
            <thead>
              <tr>
                <th>S.No</th>
                <th>Item</th>
                <th>Qty</th>
                <th>Rate</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              {billData.items.map((item, index) => (
                <tr key={item.id}>
                  <td>{index + 1}</td>
                  <td>{item.name}</td>
                  <td>{item.quantity}</td>
                  <td>₹{item.rate}</td>
                  <td>₹{item.amount.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          
          <div className="bill-summary">
            <div className="summary-row">
              <span>Subtotal:</span>
              <span>₹{billData.totals.subtotal.toFixed(2)}</span>
            </div>
            {billData.totals.gstAmount > 0 && (
              <div className="summary-row">
                <span>GST:</span>
                <span>₹{billData.totals.gstAmount.toFixed(2)}</span>
              </div>
            )}
            {billData.totals.discount > 0 && (
              <div className="summary-row">
                <span>Discount:</span>
                <span>₹{billData.totals.discount.toFixed(2)}</span>
              </div>
            )}
            <div className="summary-row total">
              <span>Total:</span>
              <span>₹{billData.totals.netAmount.toFixed(2)}</span>
            </div>
          </div>
          
          <div className="bill-footer">
            <p>Thank You! Visit Again</p>
          </div>
        </div>
        
        <div className="print-preview-actions">
          <button onClick={handlePrint} className="print-btn">Print</button>
          <button onClick={onClose} className="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default PrintPreview;