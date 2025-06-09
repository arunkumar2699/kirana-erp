# backend/app/services/report_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, case
from typing import Optional, List, Dict, Any
from datetime import date, datetime, timedelta

from app.models import Bill, BillItem, Item, Customer, Supplier

class ReportService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_daily_sales_report(self, report_date: date) -> Dict[str, Any]:
        """Generate daily sales summary"""
        start_datetime = datetime.combine(report_date, datetime.min.time())
        end_datetime = datetime.combine(report_date, datetime.max.time())
        
        # Get sales bills for the day
        sales_bills = self.db.query(Bill).filter(
            and_(
                Bill.bill_type.in_(["sale_challan", "gst_invoice"]),
                Bill.created_at >= start_datetime,
                Bill.created_at <= end_datetime
            )
        ).all()
        
        # Calculate totals
        total_bills = len(sales_bills)
        total_amount = sum(bill.total_amount for bill in sales_bills)
        total_gst = sum(bill.gst_amount for bill in sales_bills)
        total_discount = sum(bill.discount_amount for bill in sales_bills)
        net_amount = sum(bill.net_amount for bill in sales_bills)
        
        # Payment method breakdown
        payment_methods = {}
        for bill in sales_bills:
            method = bill.payment_method or "cash"
            if method not in payment_methods:
                payment_methods[method] = {"count": 0, "amount": 0}
            payment_methods[method]["count"] += 1
            payment_methods[method]["amount"] += bill.net_amount
        
        # Top selling items
        top_items = self.db.query(
            Item.name,
            Item.item_code,
            func.sum(BillItem.quantity).label("total_quantity"),
            func.sum(BillItem.total_amount).label("total_amount")
        ).join(
            BillItem, Item.id == BillItem.item_id
        ).join(
            Bill, BillItem.bill_id == Bill.id
        ).filter(
            and_(
                Bill.bill_type.in_(["sale_challan", "gst_invoice"]),
                Bill.created_at >= start_datetime,
                Bill.created_at <= end_datetime
            )
        ).group_by(Item.id).order_by(func.sum(BillItem.total_amount).desc()).limit(10).all()
        
        return {
            "date": report_date.isoformat(),
            "summary": {
                "total_bills": total_bills,
                "total_amount": float(total_amount),
                "total_gst": float(total_gst),
                "total_discount": float(total_discount),
                "net_amount": float(net_amount)
            },
            "payment_methods": payment_methods,
            "top_selling_items": [
                {
                    "name": item.name,
                    "code": item.item_code,
                    "quantity": float(item.total_quantity),
                    "amount": float(item.total_amount)
                }
                for item in top_items
            ]
        }
    
    def get_item_wise_report(self, from_date: date, to_date: date, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Generate item-wise sales report"""
        query = self.db.query(
            Item.id,
            Item.item_code,
            Item.name,
            Item.category,
            func.sum(BillItem.quantity).label("total_quantity"),
            func.sum(BillItem.total_amount - BillItem.gst_amount).label("total_amount"),
            func.sum(BillItem.gst_amount).label("total_gst"),
            func.count(BillItem.id).label("transaction_count")
        ).join(
            BillItem, Item.id == BillItem.item_id
        ).join(
            Bill, BillItem.bill_id == Bill.id
        ).filter(
            and_(
                Bill.bill_type.in_(["sale_challan", "gst_invoice"]),
                Bill.created_at >= from_date,
                Bill.created_at <= to_date
            )
        )
        
        if category:
            query = query.filter(Item.category == category)
        
        results = query.group_by(Item.id).order_by(func.sum(BillItem.total_amount).desc()).all()
        
        return [
            {
                "item_code": result.item_code,
                "name": result.name,
                "category": result.category,
                "quantity_sold": float(result.total_quantity),
                "total_amount": float(result.total_amount),
                "gst_amount": float(result.total_gst),
                "transaction_count": result.transaction_count,
                "average_per_transaction": float(result.total_amount / result.transaction_count) if result.transaction_count > 0 else 0
            }
            for result in results
        ]
    
    def get_customer_wise_report(self, from_date: date, to_date: date) -> List[Dict[str, Any]]:
        """Generate customer-wise sales report"""
        results = self.db.query(
            Customer.id,
            Customer.name,
            Customer.phone,
            func.count(Bill.id).label("bill_count"),
            func.sum(Bill.net_amount).label("total_amount"),
            func.avg(Bill.net_amount).label("average_bill")
        ).join(
            Bill, Customer.id == Bill.customer_id
        ).filter(
            and_(
                Bill.bill_type.in_(["sale_challan", "gst_invoice"]),
                Bill.created_at >= from_date,
                Bill.created_at <= to_date
            )
        ).group_by(Customer.id).order_by(func.sum(Bill.net_amount).desc()).all()
        
        return [
            {
                "customer_id": result.id,
                "name": result.name,
                "phone": result.phone,
                "bill_count": result.bill_count,
                "total_amount": float(result.total_amount),
                "average_bill_value": float(result.average_bill)
            }
            for result in results
        ]
    
    def get_gst_summary(self, from_date: date, to_date: date) -> Dict[str, Any]:
        """Generate GST summary report"""
        # Sales GST
        sales_gst = self.db.query(
            func.sum(Bill.gst_amount).label("total_gst"),
            func.sum(Bill.total_amount).label("taxable_amount")
        ).filter(
            and_(
                Bill.bill_type.in_(["gst_invoice"]),
                Bill.created_at >= from_date,
                Bill.created_at <= to_date
            )
        ).first()
        
        # Purchase GST
        purchase_gst = self.db.query(
            func.sum(Bill.gst_amount).label("total_gst"),
            func.sum(Bill.total_amount).label("taxable_amount")
        ).filter(
            and_(
                Bill.bill_type == "purchase",
                Bill.created_at >= from_date,
                Bill.created_at <= to_date
            )
        ).first()
        
        # GST rate wise breakup
        gst_breakup = self.db.query(
            BillItem.gst_percentage,
            func.sum(BillItem.total_amount - BillItem.gst_amount).label("taxable_amount"),
            func.sum(BillItem.gst_amount).label("gst_amount")
        ).join(
            Bill, BillItem.bill_id == Bill.id
        ).filter(
            and_(
                Bill.bill_type.in_(["gst_invoice"]),
                Bill.created_at >= from_date,
                Bill.created_at <= to_date
            )
        ).group_by(BillItem.gst_percentage).all()
        
        return {
            "period": {
                "from": from_date.isoformat(),
                "to": to_date.isoformat()
            },
            "sales_gst": {
                "taxable_amount": float(sales_gst.taxable_amount or 0),
                "gst_amount": float(sales_gst.total_gst or 0)
            },
            "purchase_gst": {
                "taxable_amount": float(purchase_gst.taxable_amount or 0),
                "gst_amount": float(purchase_gst.total_gst or 0)
            },
            "net_gst_payable": float((sales_gst.total_gst or 0) - (purchase_gst.total_gst or 0)),
            "gst_rate_breakup": [
                {
                    "rate": float(item.gst_percentage),
                    "taxable_amount": float(item.taxable_amount),
                    "gst_amount": float(item.gst_amount)
                }
                for item in gst_breakup
            ]
        }
    
    def get_profit_loss_report(self, from_date: date, to_date: date) -> Dict[str, Any]:
        """Generate profit and loss statement"""
        # Sales data
        sales_data = self.db.query(
            func.sum(BillItem.quantity * BillItem.rate).label("sales_amount"),
            func.sum(BillItem.quantity * Item.purchase_price).label("cost_amount")
        ).join(
            Item, BillItem.item_id == Item.id
        ).join(
            Bill, BillItem.bill_id == Bill.id
        ).filter(
            and_(
                Bill.bill_type.in_(["sale_challan", "gst_invoice"]),
                Bill.created_at >= from_date,
                Bill.created_at <= to_date
            )
        ).first()
        
        # Purchase data
        purchase_data = self.db.query(
            func.sum(Bill.net_amount).label("total_purchases")
        ).filter(
            and_(
                Bill.bill_type == "purchase",
                Bill.created_at >= from_date,
                Bill.created_at <= to_date
            )
        ).first()
        
        sales_amount = float(sales_data.sales_amount or 0)
        cost_of_goods = float(sales_data.cost_amount or 0)
        gross_profit = sales_amount - cost_of_goods
        gross_profit_margin = (gross_profit / sales_amount * 100) if sales_amount > 0 else 0
        
        return {
            "period": {
                "from": from_date.isoformat(),
                "to": to_date.isoformat()
            },
            "revenue": {
                "total_sales": sales_amount,
                "cost_of_goods_sold": cost_of_goods,
                "gross_profit": gross_profit,
                "gross_profit_margin": gross_profit_margin
            },
            "expenses": {
                "purchases": float(purchase_data.total_purchases or 0)
            },
            "net_profit": gross_profit  # Simplified - add more expense categories as needed
        }
    
    def get_stock_report(self, category: Optional[str] = None, low_stock_only: bool = False) -> List[Dict[str, Any]]:
        """Generate current stock report"""
        query = self.db.query(Item).filter(Item.is_active == True)
        
        if category:
            query = query.filter(Item.category == category)
        
        if low_stock_only:
            query = query.filter(Item.current_stock <= Item.min_stock_alert)
        
        items = query.order_by(Item.category, Item.name).all()
        
        total_value_purchase = sum(item.current_stock * (item.purchase_price or 0) for item in items)
        total_value_selling = sum(item.current_stock * item.selling_price for item in items)
        
        return {
            "summary": {
                "total_items": len(items),
                "total_stock_value_purchase": total_value_purchase,
                "total_stock_value_selling": total_value_selling,
                "potential_profit": total_value_selling - total_value_purchase
            },
            "items": [
                {
                    "item_code": item.item_code,
                    "name": item.name,
                    "category": item.category,
                    "current_stock": float(item.current_stock),
                    "min_stock_alert": float(item.min_stock_alert or 0),
                    "stock_value_purchase": float(item.current_stock * (item.purchase_price or 0)),
                    "stock_value_selling": float(item.current_stock * item.selling_price),
                    "is_low_stock": item.current_stock <= (item.min_stock_alert or 0)
                }
                for item in items
            ]
        }