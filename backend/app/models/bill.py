# backend/app/models/bill.py
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class BillType(enum.Enum):
    sale_challan = "sale_challan"
    gst_invoice = "gst_invoice"
    quotation = "quotation"
    purchase = "purchase"

class PaymentStatus(enum.Enum):
    paid = "paid"
    pending = "pending"
    partial = "partial"

class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    bill_number = Column(String(20), nullable=False, index=True)
    bill_type = Column(Enum(BillType), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    total_amount = Column(Float(precision=2))
    gst_amount = Column(Float(precision=2))
    discount_amount = Column(Float(precision=2))
    net_amount = Column(Float(precision=2))
    payment_method = Column(String(50))
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.paid)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="bills")
    supplier = relationship("Supplier", back_populates="bills")
    items = relationship("BillItem", back_populates="bill", cascade="all, delete-orphan")
    created_by_user = relationship("User")

class BillItem(Base):
    __tablename__ = "bill_items"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Float(precision=3))
    rate = Column(Float(precision=2))
    mrp = Column(Float(precision=2))
    gst_percentage = Column(Float(precision=2))
    gst_amount = Column(Float(precision=2))
    total_amount = Column(Float(precision=2))
    
    # Relationships
    bill = relationship("Bill", back_populates="items")
    item = relationship("Item")
