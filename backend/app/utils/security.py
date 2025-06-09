# backend/app/utils/security.py
"""
Security utility functions
Note: The main security functions are in app/api/auth.py
This file imports and re-exports them for convenience
"""
from app.api.auth import get_current_active_user, check_permission

# Re-export the security functions
__all__ = ['get_current_active_user', 'check_permission']