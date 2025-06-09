# backend/app/services/print_service.py
from typing import Dict, Any, List
from datetime import datetime
import json

class PrintService:
    """Service for generating print formats for bills"""
    
    PRINT_FORMATS = {
        'thermal_58mm': {
            'width': 58,
            'font_size': 8,
            'columns': ['item', 'qty', 'rate', 'amount'],
            'char_per_line': 32
        },
        'thermal_80mm': {
            'width': 80,
            'font_size': 9,
            'columns': ['item', 'qty', 'rate', 'amount'],
            'char_per_line': 48
        },
        'a4': {
            'width': 210,
            'font_size': 10,
            'columns': ['sr', 'code', 'item', 'size', 'qty', 'rate', 'mrp', 'gst', 'amount'],
            'char_per_line': 80
        },
        'a5': {
            'width': 148,
            'font_size': 9,
            'columns': ['sr', 'item', 'qty', 'rate', 'amount'],
            'char_per_line': 60
        }
    }
    
    def __init__(self, company_info: Dict[str, Any]):
        self.company_info = company_info
    
    def generate_bill_print(self, bill: Dict[str, Any], format_type: str = 'thermal_58mm') -> Dict[str, Any]:
        """Generate print data for a bill in specified format"""
        format_config = self.PRINT_FORMATS.get(format_type, self.PRINT_FORMATS['thermal_58mm'])
        
        if format_type.startswith('thermal'):
            return self._generate_thermal_format(bill, format_config)
        else:
            return self._generate_standard_format(bill, format_config)
    
    def _generate_thermal_format(self, bill: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate thermal printer format"""
        char_width = config['char_per_line']
        
        lines = []
        
        # Header
        lines.append(self._center_text(self.company_info.get('name', 'KIRANA STORE'), char_width))
        if self.company_info.get('address'):
            lines.append(self._center_text(self.company_info['address'], char_width))
        if self.company_info.get('phone'):
            lines.append(self._center_text(f"Ph: {self.company_info['phone']}", char_width))
        
        lines.append("-" * char_width)
        
        # Bill info
        bill_type_display = {
            'sale_challan': 'SALE CHALLAN',
            'gst_invoice': 'TAX INVOICE',
            'quotation': 'QUOTATION',
            'purchase': 'PURCHASE BILL'
        }
        
        lines.append(self._center_text(bill_type_display.get(bill['bill_type'], 'BILL'), char_width))
        lines.append("-" * char_width)
        
        # Bill details
        lines.append(f"Bill No: {bill['bill_number']}")
        lines.append(f"Date: {datetime.fromisoformat(bill['created_at']).strftime('%d/%m/%Y %I:%M %p')}")
        
        if bill.get('customer_name'):
            lines.append(f"Customer: {bill['customer_name']}")
        
        lines.append("-" * char_width)
        
        # Items header
        if char_width == 32:  # 58mm
            lines.append("Item              Qty Rate  Amt")
        else:  # 80mm
            lines.append("Item                        Qty   Rate    Amount")
        lines.append("-" * char_width)
        
        # Items
        for item in bill['items']:
            if char_width == 32:  # 58mm
                name = item['item_name'][:16].ljust(16)
                qty = str(item['quantity']).rjust(3)
                rate = str(int(item['rate'])).rjust(4)
                amt = str(int(item['total_amount'])).rjust(5)
                lines.append(f"{name} {qty} {rate} {amt}")
            else:  # 80mm
                name = item['item_name'][:27].ljust(27)
                qty = str(item['quantity']).rjust(5)
                rate = str(item['rate']).rjust(7)
                amt = str(item['total_amount']).rjust(8)
                lines.append(f"{name} {qty} {rate} {amt}")
        
        lines.append("-" * char_width)
        
        # Totals
        if char_width == 32:
            lines.append(f"Subtotal:".ljust(26) + str(int(bill['total_amount'])).rjust(6))
            if bill['gst_amount'] > 0:
                lines.append(f"GST:".ljust(26) + str(int(bill['gst_amount'])).rjust(6))
            if bill['discount_amount'] > 0:
                lines.append(f"Discount:".ljust(26) + str(int(bill['discount_amount'])).rjust(6))
            lines.append("=" * char_width)
            lines.append(f"TOTAL:".ljust(26) + str(int(bill['net_amount'])).rjust(6))
        else:
            lines.append(f"Subtotal:".ljust(40) + str(bill['total_amount']).rjust(8))
            if bill['gst_amount'] > 0:
                lines.append(f"GST:".ljust(40) + str(bill['gst_amount']).rjust(8))
            if bill['discount_amount'] > 0:
                lines.append(f"Discount:".ljust(40) + str(bill['discount_amount']).rjust(8))
            lines.append("=" * char_width)
            lines.append(f"TOTAL:".ljust(40) + str(bill['net_amount']).rjust(8))
        
        lines.append("-" * char_width)
        
        # Footer
        lines.append(self._center_text("Thank You! Visit Again", char_width))
        
        return {
            'format': 'text',
            'content': '\n'.join(lines),
            'config': config
        }
    
    def _generate_standard_format(self, bill: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate standard printer format (A4/A5)"""
        # This would generate HTML or PDF format
        # For now, returning a structured format that can be rendered by frontend
        
        return {
            'format': 'html',
            'config': config,
            'data': {
                'company': self.company_info,
                'bill': bill,
                'print_date': datetime.now().isoformat()
            }
        }
    
    def _center_text(self, text: str, width: int) -> str:
        """Center text within given width"""
        return text.center(width)
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap text to fit within width"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
