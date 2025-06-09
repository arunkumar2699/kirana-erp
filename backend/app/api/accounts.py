# backend/app/api/accounts.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.models import Customer, Supplier, Ledger, LedgerEntry, User
from app.schemas import (
    CustomerCreate, CustomerUpdate, CustomerResponse,
    SupplierCreate, SupplierUpdate, SupplierResponse,
    LedgerCreate, LedgerResponse
)
from app.utils.security import get_current_active_user

router = APIRouter()

# Customer endpoints
@router.get("/customers", response_model=List[CustomerResponse])
async def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all customers"""
    query = db.query(Customer)
    if search:
        query = query.filter(Customer.name.ilike(f"%{search}%"))
    
    customers = query.offset(skip).limit(limit).all()
    return customers

@router.post("/customers", response_model=CustomerResponse)
async def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new customer"""
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    
    # Create ledger for customer
    ledger = Ledger(
        name=f"Customer - {db_customer.name}",
        type="customer",
        opening_balance=0
    )
    db.add(ledger)
    db.commit()
    
    return db_customer

@router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific customer"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/customers/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a customer"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    for field, value in customer_update.dict(exclude_unset=True).items():
        setattr(customer, field, value)
    
    db.commit()
    db.refresh(customer)
    return customer

# Supplier endpoints (similar structure)
@router.get("/suppliers", response_model=List[SupplierResponse])
async def get_suppliers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all suppliers"""
    query = db.query(Supplier)
    if search:
        query = query.filter(Supplier.name.ilike(f"%{search}%"))
    
    suppliers = query.offset(skip).limit(limit).all()
    return suppliers

@router.post("/suppliers", response_model=SupplierResponse)
async def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new supplier"""
    db_supplier = Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    
    # Create ledger for supplier
    ledger = Ledger(
        name=f"Supplier - {db_supplier.name}",
        type="supplier",
        opening_balance=0
    )
    db.add(ledger)
    db.commit()
    
    return db_supplier

# Ledger endpoints
@router.get("/ledgers", response_model=List[LedgerResponse])
async def get_ledgers(
    ledger_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all ledgers"""
    query = db.query(Ledger)
    if ledger_type:
        query = query.filter(Ledger.type == ledger_type)
    
    ledgers = query.all()
    return ledgers

@router.get("/ledgers/{ledger_id}", response_model=LedgerResponse)
async def get_ledger_details(
    ledger_id: int,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get ledger with entries"""
    ledger = db.query(Ledger).filter(Ledger.id == ledger_id).first()
    if not ledger:
        raise HTTPException(status_code=404, detail="Ledger not found")
    
    # Filter entries by date if provided
    entries_query = db.query(LedgerEntry).filter(LedgerEntry.ledger_id == ledger_id)
    if from_date:
        entries_query = entries_query.filter(LedgerEntry.created_at >= from_date)
    if to_date:
        entries_query = entries_query.filter(LedgerEntry.created_at <= to_date)
    
    ledger.entries = entries_query.order_by(LedgerEntry.created_at.desc()).all()
    return ledger