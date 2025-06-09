# scripts/load_sample_data.py
"""
Script to load sample data for testing
"""
import os
import sys
from pathlib import Path
from datetime import datetime, date

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

# Create Base
Base = declarative_base()

# Define models directly
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

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    phone = Column(String(15), index=True)
    email = Column(String(100))
    address = Column(Text)
    gst_number = Column(String(20))
    outstanding_balance = Column(Float(precision=2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

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

def load_sample_data():
    # Database URL
    db_path = backend_path / "kirana_erp.db"
    DATABASE_URL = f"sqlite:///{db_path}"
    
    # Create engine and session
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Sample items
        items_data = [
            {"code": "MLK001", "name": "Amul Milk 500ml", "category": "Dairy", "price": 25, "mrp": 27, "gst": 5, "stock": 100},
            {"code": "MLK002", "name": "Amul Milk 1L", "category": "Dairy", "price": 48, "mrp": 52, "gst": 5, "stock": 80},
            {"code": "BRD001", "name": "Bread White", "category": "Bakery", "price": 35, "mrp": 40, "gst": 5, "stock": 50},
            {"code": "BRD002", "name": "Bread Brown", "category": "Bakery", "price": 40, "mrp": 45, "gst": 5, "stock": 40},
            {"code": "SUG001", "name": "Sugar 1kg", "category": "Grocery", "price": 45, "mrp": 50, "gst": 5, "stock": 200},
            {"code": "SUG002", "name": "Sugar 5kg", "category": "Grocery", "price": 220, "mrp": 240, "gst": 5, "stock": 100},
            {"code": "TEA001", "name": "Red Label Tea 100g", "category": "Beverages", "price": 40, "mrp": 45, "gst": 5, "stock": 150},
            {"code": "TEA002", "name": "Taj Mahal Tea 100g", "category": "Beverages", "price": 50, "mrp": 55, "gst": 5, "stock": 120},
            {"code": "RIC001", "name": "Basmati Rice 1kg", "category": "Grocery", "price": 90, "mrp": 100, "gst": 0, "stock": 150},
            {"code": "RIC002", "name": "Basmati Rice 5kg", "category": "Grocery", "price": 425, "mrp": 475, "gst": 0, "stock": 80},
            {"code": "OIL001", "name": "Sunflower Oil 1L", "category": "Grocery", "price": 140, "mrp": 155, "gst": 5, "stock": 100},
            {"code": "OIL002", "name": "Mustard Oil 1L", "category": "Grocery", "price": 130, "mrp": 145, "gst": 5, "stock": 90},
            {"code": "SOP001", "name": "Lifebuoy Soap", "category": "Personal Care", "price": 25, "mrp": 28, "gst": 18, "stock": 200},
            {"code": "SOP002", "name": "Dove Soap", "category": "Personal Care", "price": 45, "mrp": 50, "gst": 18, "stock": 150},
            {"code": "SMP001", "name": "Head & Shoulders 180ml", "category": "Personal Care", "price": 140, "mrp": 160, "gst": 18, "stock": 80},
            {"code": "BIS001", "name": "Parle-G Biscuits", "category": "Snacks", "price": 10, "mrp": 10, "gst": 18, "stock": 300},
            {"code": "BIS002", "name": "Marie Gold Biscuits", "category": "Snacks", "price": 30, "mrp": 35, "gst": 18, "stock": 200},
            {"code": "CHI001", "name": "Lays Classic 52g", "category": "Snacks", "price": 20, "mrp": 20, "gst": 18, "stock": 150},
            {"code": "CHO001", "name": "Dairy Milk 50g", "category": "Confectionery", "price": 40, "mrp": 40, "gst": 28, "stock": 100},
            {"code": "NOO001", "name": "Maggi Noodles Pack", "category": "Instant Food", "price": 14, "mrp": 14, "gst": 18, "stock": 250},
        ]
        
        # Add items
        items_added = 0
        for item_data in items_data:
            existing_item = db.query(Item).filter(Item.item_code == item_data["code"]).first()
            if not existing_item:
                item = Item(
                    item_code=item_data["code"],
                    name=item_data["name"],
                    category=item_data["category"],
                    selling_price=item_data["price"],
                    mrp=item_data["mrp"],
                    purchase_price=item_data["price"] * 0.8,  # 20% margin
                    gst_percentage=item_data["gst"],
                    current_stock=item_data["stock"],
                    min_stock_alert=20,
                    unit="pcs",
                    is_active=True
                )
                db.add(item)
                items_added += 1
        
        # Sample customers
        customers_data = [
            {"name": "Rajesh Kumar", "phone": "9876543210", "address": "123, MG Road"},
            {"name": "Priya Sharma", "phone": "9876543211", "address": "456, Station Road"},
            {"name": "Amit Patel", "phone": "9876543212", "address": "789, Market Street"},
            {"name": "Sunita Verma", "phone": "9876543213", "address": "321, Park Avenue"},
            {"name": "Walk-in Customer", "phone": "", "address": ""},
        ]
        
        customers_added = 0
        for cust_data in customers_data:
            existing_customer = db.query(Customer).filter(Customer.name == cust_data["name"]).first()
            if not existing_customer:
                customer = Customer(
                    name=cust_data["name"],
                    phone=cust_data["phone"],
                    address=cust_data["address"]
                )
                db.add(customer)
                customers_added += 1
        
        # Sample suppliers
        suppliers_data = [
            {"name": "Metro Cash & Carry", "phone": "1800123456", "gst": "27AAAAA0000A1Z5"},
            {"name": "Reliance Wholesale", "phone": "1800123457", "gst": "27BBBBB0000B1Z5"},
            {"name": "Local Distributor", "phone": "9898989898", "gst": "27CCCCC0000C1Z5"},
        ]
        
        suppliers_added = 0
        for supp_data in suppliers_data:
            existing_supplier = db.query(Supplier).filter(Supplier.name == supp_data["name"]).first()
            if not existing_supplier:
                supplier = Supplier(
                    name=supp_data["name"],
                    phone=supp_data["phone"],
                    gst_number=supp_data["gst"]
                )
                db.add(supplier)
                suppliers_added += 1
        
        db.commit()
        
        print("Sample data loaded successfully!")
        print(f"Items added: {items_added}")
        print(f"Customers added: {customers_added}")
        print(f"Suppliers added: {suppliers_added}")
        
        # Print summary
        total_items = db.query(Item).count()
        total_customers = db.query(Customer).count()
        total_suppliers = db.query(Supplier).count()
        
        print(f"\nDatabase Summary:")
        print(f"- Total Items: {total_items}")
        print(f"- Total Customers: {total_customers}")
        print(f"- Total Suppliers: {total_suppliers}")
        
    except Exception as e:
        print(f"Error loading sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_sample_data()