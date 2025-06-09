# backend/app/schemas/ledger.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    debit = "debit"
    credit = "credit"

class LedgerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    type: str = Field(..., min_length=1, max_length=50)
    opening_balance: float = Field(0, precision=2)

class LedgerEntryCreate(BaseModel):
    ledger_id: int
    transaction_type: TransactionType
    amount: float = Field(..., gt=0)
    description: str
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None

class LedgerEntryResponse(BaseModel):
    id: int
    transaction_type: TransactionType
    amount: float
    description: str
    reference_type: Optional[str]
    reference_id: Optional[int]
    balance: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class LedgerResponse(BaseModel):
    id: int
    name: str
    type: str
    opening_balance: float
    current_balance: float
    created_at: datetime
    entries: List[LedgerEntryResponse] = []
    
    class Config:
        from_attributes = True