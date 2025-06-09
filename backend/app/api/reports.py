# backend/app/api/reports.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional
from datetime import date, datetime, timedelta

from app.database import get_db
from app.models import Bill, BillItem, Item, Customer, User
from app.utils.security import get_current_active_user
from app.services.report_service import ReportService

router = APIRouter()

@router.get("/daily-sales")
async def get_daily_sales_report(
    report_date: Optional[date] = Query(None, description="Date for report (default: today)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get daily sales summary"""
    report_service = ReportService(db)
    if not report_date:
        report_date = date.today()
    
    return report_service.get_daily_sales_report(report_date)

@router.get("/item-wise")
async def get_item_wise_report(
    from_date: date,
    to_date: date,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get item-wise sales report"""
    report_service = ReportService(db)
    return report_service.get_item_wise_report(from_date, to_date, category)

@router.get("/customer-wise")
async def get_customer_wise_report(
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get customer-wise sales report"""
    report_service = ReportService(db)
    return report_service.get_customer_wise_report(from_date, to_date)

@router.get("/gst-summary")
async def get_gst_summary(
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get GST summary report"""
    report_service = ReportService(db)
    return report_service.get_gst_summary(from_date, to_date)

@router.get("/profit-loss")
async def get_profit_loss_report(
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get profit and loss statement"""
    report_service = ReportService(db)
    return report_service.get_profit_loss_report(from_date, to_date)

@router.get("/stock-report")
async def get_stock_report(
    category: Optional[str] = None,
    low_stock_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current stock report"""
    report_service = ReportService(db)
    return report_service.get_stock_report(category, low_stock_only)