# backend/app/models/item.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date
from sqlalchemy.sql import func
from app.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_code = Column(String(50), unique=True, nullable=False, index=True)
    barcode = Column(String(100), index=True)
    name = Column(String(200), nullable=False, index=True)
    category = Column(String(100), index=True)
    size = Column(String(50))
    unit = Column(String(20))
    purchase_price = Column(Float(precision=2))
    selling_price = Column(Float(precision=2))
    mrp = Column(Float(precision=2))
    gst_percentage = Column(Float(precision=2), default=0)
    current_stock = Column(Float(precision=3), default=0)
    min_stock_alert = Column(Float(precision=3))
    expiry_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())