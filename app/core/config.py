from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Focus Read API"
    VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str | None = None  # Make it optional if needed
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # OpenAi
    OPENAI_API_KEY: str | None = None  # Make it optional if needed

    # Google Books
    GOOGLE_BOOKS_API_KEY: str | None = None  # Make it optional if needed

    # Apple Sign In
    APPLE_BUNDLE_ID: str | None = None
    APPLE_PUBLIC_KEYS_URL: str = "https://appleid.apple.com/auth/keys"

    # Database settings    
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_DB: str = "focus_read_db"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Check if we're running on Heroku (DATABASE_URL will be set)
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            # Handle Heroku's postgres:// URLs
            if database_url.startswith("postgres://"):
                return database_url.replace("postgres://", "postgresql://", 1)
            return database_url
            
        # Use local database settings if no DATABASE_URL is set
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()