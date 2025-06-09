# backend/app/schemas/item.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, date

class ItemBase(BaseModel):
    item_code: str = Field(..., min_length=1, max_length=50)
    barcode: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=200)
    category: Optional[str] = None
    size: Optional[str] = None
    unit: Optional[str] = None
    purchase_price: Optional[float] = Field(None, ge=0)
    selling_price: float = Field(..., ge=0)
    mrp: float = Field(..., ge=0)
    gst_percentage: float = Field(0, ge=0, le=100)
    current_stock: float = Field(0, ge=0)
    min_stock_alert: Optional[float] = Field(None, ge=0)
    expiry_date: Optional[date] = None
    is_active: bool = True

    @validator('selling_price')
    def selling_price_less_than_mrp(cls, v, values):
        if 'mrp' in values and v > values['mrp']:
            raise ValueError('Selling price cannot be greater than MRP')
        return v

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    barcode: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    size: Optional[str] = None
    unit: Optional[str] = None
    purchase_price: Optional[float] = None
    selling_price: Optional[float] = None
    mrp: Optional[float] = None
    gst_percentage: Optional[float] = None
    current_stock: Optional[float] = None
    min_stock_alert: Optional[float] = None
    expiry_date: Optional[date] = None
    is_active: Optional[bool] = None

class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ItemSearch(BaseModel):
    query: str
    category: Optional[str] = None
    in_stock_only: bool = False
    limit: int = Field(10, ge=1, le=50)
