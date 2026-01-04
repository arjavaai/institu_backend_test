import os
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List
import json

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Institute Management API"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # Razorpay
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    RAZORPAY_WEBHOOK_SECRET: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Parse ALLOWED_ORIGINS if it's a string (env file issue)
if isinstance(settings.ALLOWED_ORIGINS, str):
    try:
        settings.ALLOWED_ORIGINS = json.loads(settings.ALLOWED_ORIGINS)
    except json.JSONDecodeError:
        settings.ALLOWED_ORIGINS = ["http://localhost:3000"]
