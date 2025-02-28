# app/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Portfolio API"
    DEBUG: bool = False
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    SESSION_COOKIE_NAME: str = "session_id"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/portfolio_db")
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:5173"]  # Vite React app default port
    
    class Config:
        env_file = ".env"

settings = Settings()

# app/__init__.py
# Initialize the app package