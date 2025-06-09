# backend/app/schemas/supplier.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    phone: Optional[str] = Field(None, max_length=15)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    gst_number: Optional[str] = Field(None, max_length=20)

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    gst_number: Optional[str] = None

class SupplierResponse(SupplierBase):
    id: int
    outstanding_balance: float
    created_at: datetime
    
    class Config:
        from_attributes = True