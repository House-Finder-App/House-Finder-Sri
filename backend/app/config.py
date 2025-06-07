from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/housefinder"
    )
    
    # API keys
    ZILLOW_API_KEY: str = os.getenv("ZILLOW_API_KEY", "")
    
    # AWS settings
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET_NAME: Optional[str] = os.getenv("S3_BUCKET_NAME")
    
    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # React development server
        "http://localhost:19006",  # Expo development server
        "exp://localhost:19000",  # Expo Go app
    ]
    
    class Config:
        case_sensitive = True
        env_file = ".env" 