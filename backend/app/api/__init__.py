# backend/app/api/__init__.py
# Don't import the modules here to avoid circular imports
# Just make this an empty package file

__all__ = [
    'auth',
    'billing',
    'inventory',
    'accounts',
    'reports',
    'settings'
]