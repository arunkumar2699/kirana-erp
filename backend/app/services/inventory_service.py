# backend/app/services/inventory_service.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime

from app.models import Item

class InventoryService:
    def __init__(self, db: Session):
        self.db = db
    
    def search_items(
        self,
        query: str,
        category: Optional[str] = None,
        in_stock_only: bool = False,
        limit: int = 10
    ) -> List[Item]:
        """Search items by code, name, or barcode"""
        search_query = self.db.query(Item).filter(Item.is_active == True)
        
        # Search in multiple fields
        if query:
            search_filter = or_(
                Item.item_code.ilike(f"%{query}%"),
                Item.name.ilike(f"%{query}%"),
                Item.barcode.ilike(f"%{query}%")
            )
            search_query = search_query.filter(search_filter)
        
        # Apply filters
        if category:
            search_query = search_query.filter(Item.category == category)
        if in_stock_only:
            search_query = search_query.filter(Item.current_stock > 0)
        
        # Order by relevance (exact matches first)
        search_query = search_query.order_by(
            Item.item_code == query,
            Item.barcode == query,
            Item.name
        )
        
        return search_query.limit(limit).all()
    
    def update_stock(self, item_id: int, quantity_change: float, reason: str) -> Item:
        """Update item stock with validation"""
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError("Item not found")
        
        new_stock = item.current_stock + quantity_change
        if new_stock < 0:
            raise ValueError(f"Insufficient stock. Available: {item.current_stock}")
        
        item.current_stock = new_stock
        item.updated_at = datetime.utcnow()
        
        # TODO: Add stock movement logging here
        
        self.db.commit()
        self.db.refresh(item)
        
        return item
    
    def get_stock_value(self) -> dict:
        """Calculate total stock value"""
        items = self.db.query(Item).filter(Item.is_active == True).all()
        
        total_purchase_value = sum(
            item.current_stock * (item.purchase_price or 0) for item in items
        )
        total_selling_value = sum(
            item.current_stock * item.selling_price for item in items
        )
        
        return {
            "total_items": len(items),
            "total_purchase_value": total_purchase_value,
            "total_selling_value": total_selling_value,
            "potential_profit": total_selling_value - total_purchase_value
        }
    
    def check_expiry_alerts(self, days_ahead: int = 30) -> List[Item]:
        """Get items expiring within specified days"""
        from datetime import date, timedelta
        
        expiry_date = date.today() + timedelta(days=days_ahead)
        
        items = self.db.query(Item).filter(
            Item.expiry_date <= expiry_date,
            Item.expiry_date >= date.today(),
            Item.is_active == True
        ).all()
        
        return items
    
