# backend/app/schemas/bill.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class BillType(str, Enum):
    sale_challan = "sale_challan"
    gst_invoice = "gst_invoice"
    quotation = "quotation"
    purchase = "purchase"

class PaymentStatus(str, Enum):
    paid = "paid"
    pending = "pending"
    partial = "partial"

class BillItemCreate(BaseModel):
    item_code: str
    quantity: float = Field(..., gt=0)
    rate: float = Field(..., ge=0)
    mrp: Optional[float] = None
    
    @validator('quantity')
    def validate_quantity(cls, v):
        return round(v, 3)

class BillItemResponse(BaseModel):
    id: int
    item_id: int
    item_code: str
    item_name: str
    size: Optional[str]
    quantity: float
    rate: float
    mrp: float
    gst_percentage: float
    gst_amount: float
    total_amount: float
    
    class Config:
        from_attributes = True

class BillCreate(BaseModel):
    bill_type: BillType
    customer_id: Optional[int] = None
    supplier_id: Optional[int] = None
    items: List[BillItemCreate]
    discount_amount: float = Field(0, ge=0)
    payment_method: Optional[str] = "cash"
    payment_status: PaymentStatus = PaymentStatus.paid

    @validator('customer_id', 'supplier_id')
    def validate_party(cls, v, values):
        if values.get('bill_type') == BillType.purchase:
            if not values.get('supplier_id') and not v:
                raise ValueError('Supplier is required for purchase bills')
        return v

class BillUpdate(BaseModel):
    customer_id: Optional[int] = None
    supplier_id: Optional[int] = None
    discount_amount: Optional[float] = None
    payment_method: Optional[str] = None
    payment_status: Optional[PaymentStatus] = None

class BillResponse(BaseModel):
    id: int
    bill_number: str
    bill_type: BillType
    customer_id: Optional[int]
    customer_name: Optional[str]
    supplier_id: Optional[int]
    supplier_name: Optional[str]
    total_amount: float
    gst_amount: float
    discount_amount: float
    net_amount: float
    payment_method: str
    payment_status: PaymentStatus
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[BillItemResponse] = []
    
    class Config:
        from_attributes = True