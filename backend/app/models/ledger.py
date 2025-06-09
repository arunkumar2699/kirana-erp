# backend/app/models/ledger.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TransactionType(enum.Enum):
    debit = "debit"
    credit = "credit"

class Ledger(Base):
    __tablename__ = "ledgers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    type = Column(String(50))  # customer, supplier, expense, income
    opening_balance = Column(Float(precision=2), default=0)
    current_balance = Column(Float(precision=2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    entries = relationship("LedgerEntry", back_populates="ledger")

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True, index=True)
    ledger_id = Column(Integer, ForeignKey("ledgers.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float(precision=2), nullable=False)
    description = Column(String(500))
    reference_type = Column(String(50))  # bill, payment, etc.
    reference_id = Column(Integer)
    balance = Column(Float(precision=2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    ledger = relationship("Ledger", back_populates="entries")