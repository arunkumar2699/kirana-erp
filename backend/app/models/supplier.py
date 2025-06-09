# backend/app/models/supplier.py
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    phone = Column(String(15))
    email = Column(String(100))
    address = Column(Text)
    gst_number = Column(String(20))
    outstanding_balance = Column(Float(precision=2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    bills = relationship("Bill", back_populates="supplier")