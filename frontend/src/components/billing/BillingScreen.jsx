// frontend/src/components/billing/BillingScreen.jsx
import React, { useState, useEffect, useRef } from 'react';
import ItemSearchModal from './ItemSearchModal';
import BillFormatSelector from './BillFormatSelector';
import PrintPreview from './PrintPreview';
import { billingService } from '../../services/billingService';
import { inventoryService } from '../../services/inventoryService';
import './BillingScreen.css';

const BillingScreen = () => {
  const [billType, setBillType] = useState('gst_invoice');
  const [customer, setCustomer] = useState({ phone: '', name: '' });
  const [items, setItems] = useState([]);
  const [currentItemInput, setCurrentItemInput] = useState('');
  const [showItemSearch, setShowItemSearch] = useState(false);
  const [showPrintPreview, setShowPrintPreview] = useState(false);
  const [searchResults, setSearchResults] = useState([]);
  const [totals, setTotals] = useState({
    subtotal: 0,
    gstAmount: 0,
    discount: 0,
    netAmount: 0
  });
  
  const itemInputRef = useRef(null);
  const [billNumber, setBillNumber] = useState('');

// At the top of the component, update the useEffect:
useEffect(() => {
  generateBillNumber();
}, [billType]); // Re-generate when bill type changes

useEffect(() => {
  const handleKeyPress = (e) => {
    // Function key shortcuts
    if (e.key === 'F2') {
      e.preventDefault();
      saveBill();
    } else if (e.key === 'F3') {
      e.preventDefault();
      printBill();
    } else if (e.key === 'F4') {
      e.preventDefault();
      holdBill();
    } else if (e.key === 'F5') {
      e.preventDefault();
      retrieveBill();
    }
  };

  document.addEventListener('keydown', handleKeyPress);
  
  return () => {
    document.removeEventListener('keydown', handleKeyPress);
  };
}, [items, totals]); // Add dependencies that are used in the functions


  const generateBillNumber = () => {
    // In real app, this would be generated from backend
    const date = new Date();
    const prefix = billType === 'gst_invoice' ? 'INV' : 'SC';
    setBillNumber(`${prefix}${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}001`);
  };

  const setupKeyboardShortcuts = () => {
    document.addEventListener('keydown', handleKeyPress);
  };

  const handleKeyPress = (e) => {
    // Function key shortcuts
    if (e.key === 'F2') {
      e.preventDefault();
      saveBill();
    } else if (e.key === 'F3') {
      e.preventDefault();
      printBill();
    } else if (e.key === 'F4') {
      e.preventDefault();
      holdBill();
    } else if (e.key === 'F5') {
      e.preventDefault();
      retrieveBill();
    }
  };

  const handleItemInputChange = async (value) => {
    setCurrentItemInput(value);
    
    if (value === '0') {
      saveBill();
      return;
    }
    
    if (value.length > 2) {
      try {
        const results = await inventoryService.searchItems({
          query: value,
          limit: 10,
          in_stock_only: true
        });
        setSearchResults(results);
        if (results.length > 0) {
          setShowItemSearch(true);
        }
      } catch (error) {
        console.error('Failed to search items:', error);
      }
    } else {
      setShowItemSearch(false);
    }
  };

  const handleItemSelect = (item) => {
    const existingItem = items.find(i => i.id === item.id);
    
    if (existingItem) {
      updateQuantity(item.id, existingItem.quantity + 1);
    } else {
      setItems([...items, {
        ...item,
        quantity: 1,
        rate: item.selling_price,
        amount: item.selling_price
      }]);
    }
    
    setCurrentItemInput('');
    setShowItemSearch(false);
    itemInputRef.current?.focus();
  };

  const updateQuantity = (itemId, newQuantity) => {
    if (newQuantity <= 0) {
      setItems(items.filter(i => i.id !== itemId));
    } else {
      setItems(items.map(item => {
        if (item.id === itemId) {
          const amount = newQuantity * item.rate;
          return { ...item, quantity: newQuantity, amount };
        }
        return item;
      }));
    }
  };

  const updateRate = (itemId, newRate) => {
    setItems(items.map(item => {
      if (item.id === itemId) {
        const amount = item.quantity * newRate;
        return { ...item, rate: newRate, amount };
      }
      return item;
    }));
  };

  const calculateTotals = () => {
    let subtotal = 0;
    let gstAmount = 0;
    
    items.forEach(item => {
      const itemAmount = item.quantity * item.rate;
      const itemGst = (itemAmount * item.gst_percentage) / 100;
      subtotal += itemAmount;
      gstAmount += itemGst;
    });
    
    const netAmount = subtotal + gstAmount - totals.discount;
    
    setTotals({
      ...totals,
      subtotal,
      gstAmount,
      netAmount
    });
  };

  const saveBill = async () => {
    if (items.length === 0) {
      alert('Please add items to the bill');
      return;
    }
    
    try {
      const billData = {
        bill_type: billType,
        customer_id: null, // In real app, would lookup customer
        items: items.map(item => ({
          item_code: item.item_code,
          quantity: item.quantity,
          rate: item.rate,
          mrp: item.mrp
        })),
        discount_amount: totals.discount,
        payment_method: 'cash',
        payment_status: 'paid'
      };
      
      const response = await billingService.createBill(billData);
      console.log('Bill saved:', response);
      
      // Reset form
      setItems([]);
      setCustomer({ phone: '', name: '' });
      generateBillNumber();
      itemInputRef.current?.focus();
      
      alert('Bill saved successfully!');
    } catch (error) {
      console.error('Failed to save bill:', error);
      alert('Failed to save bill');
    }
  };

  const printBill = () => {
    if (items.length === 0) {
      alert('Please add items to the bill');
      return;
    }
    setShowPrintPreview(true);
  };

  const holdBill = () => {
    // Implement hold bill functionality
    console.log('Hold bill');
  };

  const retrieveBill = () => {
    // Implement retrieve bill functionality
    console.log('Retrieve bill');
  };

  return (
    <div className="billing-screen">
      <div className="billing-header">
        <div className="bill-info">
          <BillFormatSelector value={billType} onChange={setBillType} />
          <div className="bill-number">
            <label>Bill No:</label>
            <input type="text" value={billNumber} readOnly />
          </div>
          <div className="bill-date">
            <label>Date:</label>
            <input type="date" defaultValue={new Date().toISOString().split('T')[0]} />
          </div>
        </div>
        
        <div className="customer-info">
          <input
            type="text"
            placeholder="Customer Phone"
            value={customer.phone}
            onChange={(e) => setCustomer({ ...customer, phone: e.target.value })}
          />
          <input
            type="text"
            placeholder="Customer Name"
            value={customer.name}
            onChange={(e) => setCustomer({ ...customer, name: e.target.value })}
          />
        </div>
      </div>

      <div className="item-entry">
        <input
          ref={itemInputRef}
          type="text"
          placeholder="Enter item code/name or press 0 to save..."
          value={currentItemInput}
          onChange={(e) => handleItemInputChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Escape') {
              setShowItemSearch(false);
              setCurrentItemInput('');
            }
          }}
          className="item-input"
          autoFocus
        />
        
        {showItemSearch && (
          <ItemSearchModal
            searchResults={searchResults}
            onSelect={handleItemSelect}
            onClose={() => setShowItemSearch(false)}
          />
        )}
      </div>

      <div className="items-table-container">
        <table className="items-table">
          <thead>
            <tr>
              <th width="10%">Code</th>
              <th width="30%">Item Name</th>
              <th width="10%">Qty</th>
              <th width="10%">Rate</th>
              <th width="10%">MRP</th>
              <th width="10%">GST%</th>
              <th width="15%">Amount</th>
              <th width="5%"></th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{item.item_code}</td>
                <td>{item.name}</td>
                <td>
                  <input
                    type="number"
                    value={item.quantity}
                    onChange={(e) => updateQuantity(item.id, parseFloat(e.target.value) || 0)}
                    className="qty-input"
                  />
                </td>
                <td>
                  <input
                    type="number"
                    value={item.rate}
                    onChange={(e) => updateRate(item.id, parseFloat(e.target.value) || 0)}
                    className="rate-input"
                  />
                </td>
                <td>₹{item.mrp}</td>
                <td>{item.gst_percentage}%</td>
                <td>₹{item.amount.toFixed(2)}</td>
                <td>
                  <button
                    onClick={() => updateQuantity(item.id, 0)}
                    className="remove-btn"
                  >
                    ✕
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="billing-footer">
        <div className="shortcuts">
          <button onClick={saveBill} className="shortcut-btn save">
            F2 - Save
          </button>
          <button onClick={printBill} className="shortcut-btn print">
            F3 - Print
          </button>
          <button onClick={holdBill} className="shortcut-btn hold">
            F4 - Hold
          </button>
          <button onClick={retrieveBill} className="shortcut-btn retrieve">
            F5 - Retrieve
          </button>
        </div>
        
        <div className="totals">
          <div className="total-row">
            <span>Subtotal:</span>
            <span>₹{totals.subtotal.toFixed(2)}</span>
          </div>
          <div className="total-row">
            <span>GST:</span>
            <span>₹{totals.gstAmount.toFixed(2)}</span>
          </div>
          <div className="total-row">
            <span>Discount:</span>
            <input
              type="number"
              value={totals.discount}
              onChange={(e) => setTotals({ ...totals, discount: parseFloat(e.target.value) || 0 })}
              className="discount-input"
            />
          </div>
          <div className="total-row net">
            <span>Net Amount:</span>
            <span>₹{totals.netAmount.toFixed(2)}</span>
          </div>
        </div>
      </div>

      {showPrintPreview && (
        <PrintPreview
          billData={{
            billNumber,
            billType,
            customer,
            items,
            totals,
            date: new Date()
          }}
          onClose={() => setShowPrintPreview(false)}
        />
      )}
    </div>
  );
};

export default BillingScreen;