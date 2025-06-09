# backend/app/services/billing_service.py
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime

from app.models import Bill, BillItem, Item, Customer, Supplier
from app.schemas import BillCreate, BillItemCreate, BillResponse, BillItemResponse
from app.services.inventory_service import InventoryService

class BillingService:
    def __init__(self, db: Session):
        self.db = db
        self.inventory_service = InventoryService(db)
    
    def generate_bill_number(self, bill_type: str) -> str:
        """Generate unique bill number based on type and sequence"""
        prefix_map = {
            "sale_challan": "SC",
            "gst_invoice": "INV",
            "quotation": "QT",
            "purchase": "PUR"
        }
        
        prefix = prefix_map.get(bill_type, "BILL")
        year = datetime.now().strftime("%y")
        
        # Get the last bill number for this type
        last_bill = self.db.query(Bill).filter(
            Bill.bill_type == bill_type,
            Bill.bill_number.like(f"{prefix}{year}%")
        ).order_by(Bill.id.desc()).first()
        
        if last_bill:
            # Extract sequence number and increment
            last_sequence = int(last_bill.bill_number[len(prefix) + 2:])
            sequence = last_sequence + 1
        else:
            sequence = 1
        
        return f"{prefix}{year}{sequence:05d}"
    
    def create_bill(self, bill_data: BillCreate, user_id: int) -> Bill:
        """Create a new bill with items"""
        # Generate bill number
        bill_number = self.generate_bill_number(bill_data.bill_type.value)
        
        # Create bill
        bill = Bill(
            bill_number=bill_number,
            bill_type=bill_data.bill_type,
            customer_id=bill_data.customer_id,
            supplier_id=bill_data.supplier_id,
            discount_amount=bill_data.discount_amount,
            payment_method=bill_data.payment_method,
            payment_status=bill_data.payment_status,
            created_by=user_id
        )
        
        # Process bill items
        total_amount = 0
        total_gst = 0
        
        for item_data in bill_data.items:
            # Get item details
            item = self.db.query(Item).filter(Item.item_code == item_data.item_code).first()
            if not item:
                raise ValueError(f"Item not found: {item_data.item_code}")
            
            # Calculate amounts
            rate = item_data.rate if item_data.rate else item.selling_price
            mrp = item_data.mrp if item_data.mrp else item.mrp
            item_total = item_data.quantity * rate
            gst_amount = (item_total * item.gst_percentage) / 100
            
            # Create bill item
            bill_item = BillItem(
                item_id=item.id,
                quantity=item_data.quantity,
                rate=rate,
                mrp=mrp,
                gst_percentage=item.gst_percentage,
                gst_amount=gst_amount,
                total_amount=item_total + gst_amount
            )
            
            bill.items.append(bill_item)
            total_amount += item_total
            total_gst += gst_amount
            
            # Update inventory for sales
            if bill_data.bill_type in ["sale_challan", "gst_invoice"]:
                self.inventory_service.update_stock(item.id, -item_data.quantity, f"Sale: {bill_number}")
            elif bill_data.bill_type == "purchase":
                self.inventory_service.update_stock(item.id, item_data.quantity, f"Purchase: {bill_number}")
        
        # Set bill totals
        bill.total_amount = total_amount
        bill.gst_amount = total_gst
        bill.net_amount = total_amount + total_gst - bill.discount_amount
        
        # Save bill
        self.db.add(bill)
        self.db.commit()
        self.db.refresh(bill)
        
        return bill
    
    def get_bill_response(self, bill: Bill) -> BillResponse:
        """Convert bill model to response schema"""
        # Load related data
        bill = self.db.query(Bill).options(
            joinedload(Bill.items).joinedload(BillItem.item),
            joinedload(Bill.customer),
            joinedload(Bill.supplier)
        ).filter(Bill.id == bill.id).first()
        
        # Prepare items response
        items = []
        for bill_item in bill.items:
            item_response = BillItemResponse(
                id=bill_item.id,
                item_id=bill_item.item_id,
                item_code=bill_item.item.item_code,
                item_name=bill_item.item.name,
                size=bill_item.item.size,
                quantity=bill_item.quantity,
                rate=bill_item.rate,
                mrp=bill_item.mrp,
                gst_percentage=bill_item.gst_percentage,
                gst_amount=bill_item.gst_amount,
                total_amount=bill_item.total_amount
            )
            items.append(item_response)
        
        # Create response
        return BillResponse(
            id=bill.id,
            bill_number=bill.bill_number,
            bill_type=bill.bill_type,
            customer_id=bill.customer_id,
            customer_name=bill.customer.name if bill.customer else None,
            supplier_id=bill.supplier_id,
            supplier_name=bill.supplier.name if bill.supplier else None,
            total_amount=bill.total_amount,
            gst_amount=bill.gst_amount,
            discount_amount=bill.discount_amount,
            net_amount=bill.net_amount,
            payment_method=bill.payment_method,
            payment_status=bill.payment_status,
            created_by=bill.created_by,
            created_at=bill.created_at,
            updated_at=bill.updated_at,
            items=items
        )