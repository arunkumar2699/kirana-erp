// frontend/src/services/printService.js
export const printService = {
  formatBillForPrint: (bill, format = 'thermal_58mm') => {
    // Format bill data for printing based on selected format
    const formats = {
      thermal_58mm: formatThermal58mm,
      thermal_80mm: formatThermal80mm,
      a4: formatA4,
      a5: formatA5
    };

    const formatter = formats[format] || formats.thermal_58mm;
    return formatter(bill);
  },

  printBill: (billContent) => {
    // Create a new window for printing
    const printWindow = window.open('', 'Print Bill', 'width=800,height=600');
    
    printWindow.document.write(`
      <html>
        <head>
          <title>Print Bill</title>
          <style>
            body { font-family: monospace; margin: 20px; }
            .bill-content { white-space: pre-wrap; }
            @media print {
              body { margin: 0; }
            }
          </style>
        </head>
        <body>
          <div class="bill-content">${billContent}</div>
        </body>
      </html>
    `);
    
    printWindow.document.close();
    printWindow.focus();
    
    setTimeout(() => {
      printWindow.print();
      printWindow.close();
    }, 250);
  }
};

// Helper functions for different formats
function formatThermal58mm(bill) {
  const width = 32;
  let content = '';
  
  // Header
  content += centerText('KIRANA STORE', width) + '\n';
  content += centerText('Ph: 9876543210', width) + '\n';
  content += '-'.repeat(width) + '\n';
  
  // Bill details
  content += `Bill: ${bill.billNumber}\n`;
  content += `Date: ${new Date(bill.date).toLocaleDateString()}\n`;
  content += '-'.repeat(width) + '\n';
  
  // Items
  bill.items.forEach(item => {
    const name = item.name.substring(0, 16).padEnd(16);
    const qty = item.quantity.toString().padStart(3);
    const rate = item.rate.toFixed(0).padStart(4);
    const amt = item.amount.toFixed(0).padStart(5);
    content += `${name} ${qty} ${rate} ${amt}\n`;
  });
  
  content += '-'.repeat(width) + '\n';
  
  // Total
  content += `TOTAL:`.padEnd(26) + bill.totals.netAmount.toFixed(0).padStart(6) + '\n';
  content += '-'.repeat(width) + '\n';
  content += centerText('Thank You!', width) + '\n';
  
  return content;
}

function formatThermal80mm(bill) {
  // Similar to 58mm but with more width
  const width = 48;
  // Implementation similar to above with adjusted width
  return formatThermal58mm(bill); // Placeholder
}

function formatA4(bill) {
  // Return HTML formatted content for A4
  return `<div>A4 Format - To be implemented</div>`;
}

function formatA5(bill) {
  // Return HTML formatted content for A5
  return `<div>A5 Format - To be implemented</div>`;
}

function centerText(text, width) {
  const padding = Math.floor((width - text.length) / 2);
  return ' '.repeat(padding) + text;
}