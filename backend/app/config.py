from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./kirana_erp.db"
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Remote Access
    ENABLE_LAN: bool = True
    ENABLE_INTERNET: bool = False
    PORT: int = 8000
    NGROK_AUTH_TOKEN: Optional[str] = None
    AUTHENTICATION_REQUIRED: bool = True
    
    # Application Settings
    COMPANY_NAME: str = "Kirana Store"
    FINANCIAL_YEAR: str = "2024-2025"
    
    class Config:
        env_file = ".env"

settings = Settings()