# backend/app/api/billing.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from app.database import get_db
from app.models import Bill, BillItem, Item, Customer, Supplier, User
from app.schemas import BillCreate, BillUpdate, BillResponse, BillItemResponse
from app.utils.security import get_current_active_user
from app.services.billing_service import BillingService
from app.services.inventory_service import InventoryService

router = APIRouter()

@router.post("/create", response_model=BillResponse)
async def create_bill(
    bill_data: BillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new bill"""
    billing_service = BillingService(db)
    try:
        bill = billing_service.create_bill(bill_data, current_user.id)
        return billing_service.get_bill_response(bill)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/retrieve/{bill_number}", response_model=BillResponse)
async def retrieve_bill(
    bill_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieve a bill by bill number"""
    bill = db.query(Bill).filter(Bill.bill_number == bill_number).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    billing_service = BillingService(db)
    return billing_service.get_bill_response(bill)

@router.put("/update/{bill_id}", response_model=BillResponse)
async def update_bill(
    bill_id: int,
    bill_update: BillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an existing bill"""
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Update bill fields
    for field, value in bill_update.dict(exclude_unset=True).items():
        setattr(bill, field, value)
    
    bill.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(bill)
    
    billing_service = BillingService(db)
    return billing_service.get_bill_response(bill)

@router.post("/hold/{bill_id}")
async def hold_bill(
    bill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Hold a bill for later retrieval"""
    # In a real implementation, you might want to add a 'status' field to bills
    # For now, we'll just mark it as pending
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    bill.payment_status = "pending"
    db.commit()
    
    return {"message": "Bill held successfully", "bill_id": bill_id}

@router.get("/formats")
async def get_bill_formats(current_user: User = Depends(get_current_active_user)):
    """Get available bill formats"""
    return {
        "formats": [
            {"value": "sale_challan", "label": "Sale Challan"},
            {"value": "gst_invoice", "label": "GST Invoice"},
            {"value": "quotation", "label": "Quotation"},
            {"value": "purchase", "label": "Purchase Bill"}
        ]
    }

@router.get("/pending", response_model=List[BillResponse])
async def get_pending_bills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all pending/held bills"""
    bills = db.query(Bill).filter(Bill.payment_status == "pending").all()
    billing_service = BillingService(db)
    return [billing_service.get_bill_response(bill) for bill in bills]

@router.get("/search", response_model=List[BillResponse])
async def search_bills(
    q: Optional[str] = Query(None, description="Search query"),
    bill_type: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    customer_id: Optional[int] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Search bills with filters"""
    query = db.query(Bill)
    
    if q:
        query = query.filter(Bill.bill_number.contains(q))
    if bill_type:
        query = query.filter(Bill.bill_type == bill_type)
    if from_date:
        query = query.filter(Bill.created_at >= from_date)
    if to_date:
        query = query.filter(Bill.created_at <= to_date)
    if customer_id:
        query = query.filter(Bill.customer_id == customer_id)
    
    bills = query.offset(offset).limit(limit).all()
    billing_service = BillingService(db)
    return [billing_service.get_bill_response(bill) for bill in bills]