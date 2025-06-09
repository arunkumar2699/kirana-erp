# backend/app/api/inventory.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Item, User
from app.schemas import ItemCreate, ItemUpdate, ItemResponse, ItemSearch
from app.utils.security import get_current_active_user, check_permission
from app.services.inventory_service import InventoryService

router = APIRouter()

@router.get("/items", response_model=List[ItemResponse])
async def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    category: Optional[str] = None,
    in_stock: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all items with optional filters"""
    query = db.query(Item)
    
    if category:
        query = query.filter(Item.category == category)
    if in_stock:
        query = query.filter(Item.current_stock > 0)
    
    items = query.offset(skip).limit(limit).all()
    return items

@router.post("/items", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("admin"))
):
    """Create a new item (Admin only)"""
    # Check if item code already exists
    existing_item = db.query(Item).filter(Item.item_code == item.item_code).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Item code already exists")
    
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific item by ID"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("admin"))
):
    """Update an item (Admin only)"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for field, value in item_update.dict(exclude_unset=True).items():
        setattr(item, field, value)
    
    item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(item)
    return item

@router.delete("/items/{item_id}")
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("admin"))
):
    """Delete an item (Admin only)"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Soft delete
    item.is_active = False
    db.commit()
    
    return {"message": "Item deleted successfully"}

@router.post("/items/search", response_model=List[ItemResponse])
async def search_items(
    search: ItemSearch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Search items by code, name, or barcode"""
    inventory_service = InventoryService(db)
    items = inventory_service.search_items(
        search.query,
        search.category,
        search.in_stock_only,
        search.limit
    )
    return items

@router.put("/stock/update")
async def update_stock(
    item_id: int,
    quantity_change: float,
    reason: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("manager"))
):
    """Update stock levels (Manager/Admin only)"""
    inventory_service = InventoryService(db)
    try:
        item = inventory_service.update_stock(item_id, quantity_change, reason)
        return {"message": "Stock updated successfully", "new_stock": item.current_stock}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/low-stock-alerts", response_model=List[ItemResponse])
async def get_low_stock_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get items with low stock"""
    items = db.query(Item).filter(
        Item.current_stock <= Item.min_stock_alert,
        Item.is_active == True
    ).all()
    return items

@router.get("/categories")
async def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all unique categories"""
    categories = db.query(Item.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]