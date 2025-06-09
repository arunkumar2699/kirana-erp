# backend/app/utils/validators.py
"""
Validation utility functions for various fields
"""
import re
from typing import Optional

def validate_phone(phone: str) -> bool:
    """
    Validate Indian phone number
    Accepts 10 digit numbers with optional +91 prefix
    """
    if not phone:
        return True  # Phone is optional
    
    # Remove spaces and hyphens
    phone = phone.replace(" ", "").replace("-", "")
    
    # Indian phone number pattern
    pattern = r'^(\+91)?[6-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_gst(gst_number: str) -> bool:
    """
    Validate Indian GST number
    Format: 2 digits state code + 10 char PAN + 1 digit entity + 1 char Z + 1 check digit
    Total: 15 characters
    """
    if not gst_number:
        return True  # GST is optional
    
    # GST pattern
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return bool(re.match(pattern, gst_number.upper()))

def validate_email(email: str) -> bool:
    """
    Validate email address
    """
    if not email:
        return True  # Email is optional
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_item_code(code: str) -> bool:
    """
    Validate item code
    Alphanumeric, 3-50 characters
    """
    if not code:
        return False
    
    pattern = r'^[A-Z0-9]{3,50}$'
    return bool(re.match(pattern, code.upper()))

def validate_barcode(barcode: str) -> bool:
    """
    Validate barcode (EAN-13 or custom format)
    """
    if not barcode:
        return True  # Barcode is optional
    
    # Check if it's numeric and reasonable length
    if barcode.isdigit() and 8 <= len(barcode) <= 13:
        return True
    
    # Allow alphanumeric barcodes up to 50 chars
    pattern = r'^[A-Za-z0-9]{1,50}$'
    return bool(re.match(pattern, barcode))

def validate_quantity(quantity: float, allow_negative: bool = False) -> bool:
    """
    Validate quantity
    """
    if allow_negative:
        return True
    return quantity > 0

def validate_price(price: float) -> bool:
    """
    Validate price (must be non-negative)
    """
    return price >= 0

def validate_percentage(percentage: float) -> bool:
    """
    Validate percentage (0-100)
    """
    return 0 <= percentage <= 100
