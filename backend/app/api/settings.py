# backend/app/api/settings.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.models import User
from app.utils.security import get_current_active_user, check_permission
from app.config import settings

router = APIRouter()

@router.get("/company-info")
async def get_company_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get company information"""
    return {
        "company_name": settings.COMPANY_NAME,
        "financial_year": settings.FINANCIAL_YEAR,
        # Add more company info as needed
    }

@router.put("/company-info")
async def update_company_info(
    company_data: Dict[str, Any],
    current_user: User = Depends(check_permission("admin"))
):
    """Update company information (Admin only)"""
    # In a real app, you'd save this to database or config file
    return {"message": "Company info updated", "data": company_data}

@router.get("/print-formats")
async def get_print_formats(
    current_user: User = Depends(get_current_active_user)
):
    """Get available print formats"""
    return {
        "formats": [
            {
                "id": "thermal_58mm",
                "name": "Thermal 58mm",
                "width": 58,
                "type": "thermal"
            },
            {
                "id": "thermal_80mm",
                "name": "Thermal 80mm",
                "width": 80,
                "type": "thermal"
            },
            {
                "id": "a4",
                "name": "A4 Size",
                "width": 210,
                "type": "standard"
            },
            {
                "id": "a5",
                "name": "A5 Size",
                "width": 148,
                "type": "standard"
            }
        ]
    }

@router.get("/bill-series")
async def get_bill_series(
    current_user: User = Depends(get_current_active_user)
):
    """Get bill number series configuration"""
    return {
        "series": {
            "sale_challan": {"prefix": "SC", "next_number": 1},
            "gst_invoice": {"prefix": "INV", "next_number": 1},
            "quotation": {"prefix": "QT", "next_number": 1},
            "purchase": {"prefix": "PUR", "next_number": 1}
        }
    }

@router.put("/bill-series")
async def update_bill_series(
    series_data: Dict[str, Any],
    current_user: User = Depends(check_permission("admin"))
):
    """Update bill number series (Admin only)"""
    return {"message": "Bill series updated", "data": series_data}

@router.get("/remote-access")
async def get_remote_access_settings(
    current_user: User = Depends(check_permission("admin"))
):
    """Get remote access configuration (Admin only)"""
    return {
        "enable_lan": settings.ENABLE_LAN,
        "enable_internet": settings.ENABLE_INTERNET,
        "port": settings.PORT,
        "authentication_required": settings.AUTHENTICATION_REQUIRED
    }

@router.put("/remote-access")
async def update_remote_access_settings(
    access_settings: Dict[str, Any],
    current_user: User = Depends(check_permission("admin"))
):
    """Update remote access settings (Admin only)"""
    return {"message": "Remote access settings updated", "data": access_settings}