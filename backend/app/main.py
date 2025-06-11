# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.api import auth, billing, inventory, accounts, reports, settings
from app.config import settings as app_settings

# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        Base.metadata.create_all(bind=engine)
        # Create default admin user if not exists
        from scripts.create_admin import create_admin_user
        create_admin_user()
    except Exception as e:
        print(f"Startup error: {e}")
    yield
    # Shutdown

app = FastAPI(
    title="Kirana ERP API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(billing.router, prefix="/api/v1/billing", tags=["Billing"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["Inventory"])
app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["Accounts"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(settings.router, prefix="/api/v1/settings", tags=["Settings"])

@app.get("/")
def read_root():
    return {"message": "Kirana ERP API", "version": "1.0.0"}