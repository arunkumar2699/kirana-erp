# backend/app/utils/formatters.py
"""
Formatting utility functions for display
"""
from datetime import datetime, date
from typing import Optional, Union
from decimal import Decimal, ROUND_HALF_UP

def format_currency(amount: Union[float, Decimal], symbol: str = "₹") -> str:
    """
    Format amount as currency
    Example: 1234.5 -> "₹ 1,234.50"
    """
    if amount is None:
        return f"{symbol} 0.00"
    
    # Convert to Decimal for precise handling
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount))
    
    # Round to 2 decimal places
    amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Format with Indian numbering system
    amount_str = f"{amount:,.2f}"
    
    # Indian numbering: Add commas after every 2 digits from right (except last 3)
    if abs(amount) >= 1000:
        parts = amount_str.split('.')
        whole = parts[0].replace(',', '')
        decimal = parts[1] if len(parts) > 1 else '00'
        
        # Indian format
        if len(whole) > 3:
            last_three = whole[-3:]
            rest = whole[:-3]
            new_rest = ''
            for i, digit in enumerate(reversed(rest)):
                if i > 0 and i % 2 == 0:
                    new_rest = ',' + new_rest
                new_rest = digit + new_rest
            amount_str = new_rest + ',' + last_three + '.' + decimal
        else:
            amount_str = whole + '.' + decimal
    
    return f"{symbol} {amount_str}"

def format_date(date_obj: Union[datetime, date, str], format_str: str = "%d/%m/%Y") -> str:
    """
    Format date object to string
    Default format: DD/MM/YYYY
    """
    if isinstance(date_obj, str):
        # If it's already a string, try to parse it
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except:
            return date_obj
    
    if isinstance(date_obj, datetime):
        return date_obj.strftime(format_str)
    elif isinstance(date_obj, date):
        return date_obj.strftime(format_str)
    else:
        return str(date_obj)

def format_datetime(dt_obj: Union[datetime, str], format_str: str = "%d/%m/%Y %I:%M %p") -> str:
    """
    Format datetime object to string with time
    Default format: DD/MM/YYYY HH:MM AM/PM
    """
    if isinstance(dt_obj, str):
        try:
            dt_obj = datetime.fromisoformat(dt_obj.replace('Z', '+00:00'))
        except:
            return dt_obj
    
    if isinstance(dt_obj, datetime):
        return dt_obj.strftime(format_str)
    else:
        return str(dt_obj)

def format_bill_number(bill_type: str, sequence: int, year: Optional[str] = None) -> str:
    """
    Format bill number based on type
    Example: INV2400001 for invoice
    """
    prefix_map = {
        "sale_challan": "SC",
        "gst_invoice": "INV",
        "quotation": "QT",
        "purchase": "PUR"
    }
    
    prefix = prefix_map.get(bill_type, "BILL")
    
    if not year:
        year = datetime.now().strftime("%y")
    
    return f"{prefix}{year}{sequence:05d}"

def format_phone(phone: str) -> str:
    """
    Format phone number for display
    Example: 9876543210 -> "+91 98765 43210"
    """
    if not phone:
        return ""
    
    # Remove all non-digits
    phone = re.sub(r'\D', '', phone)
    
    # Add +91 if 10 digits
    if len(phone) == 10:
        phone = "91" + phone
    
    # Format as +91 XXXXX XXXXX
    if len(phone) == 12 and phone.startswith("91"):
        return f"+91 {phone[2:7]} {phone[7:]}"
    
    return phone

def format_quantity(quantity: Union[float, Decimal], unit: Optional[str] = None) -> str:
    """
    Format quantity with optional unit
    Example: 2.5, "kg" -> "2.500 kg"
    """
    if quantity is None:
        return "0"
    
    # Convert to Decimal
    if not isinstance(quantity, Decimal):
        quantity = Decimal(str(quantity))
    
    # Format to 3 decimal places, removing trailing zeros
    formatted = f"{quantity:.3f}".rstrip('0').rstrip('.')
    
    if unit:
        return f"{formatted} {unit}"
    return formatted

def format_percentage(value: float) -> str:
    """
    Format percentage
    Example: 5.5 -> "5.5%"
    """
    return f"{value:.1f}%".rstrip('0').rstrip('.')

def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to specified length
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

# Import re for regex operations
import re