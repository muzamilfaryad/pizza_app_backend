import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/pizza_db"
    )
    
    # JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # App
    APP_NAME = "Pizza App API"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "True") == "True"

settings = Settings()
