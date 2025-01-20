from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
  PROJECT_NAME: str = "Focus Read API"
  VERSION: str = "0.0.1"
  API_V1_STR: str = "/api/v1"

    # Security
  SECRET_KEY: str
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

  # OpenAi
  OPENAI_API_KEY: str

  # Google Books
  GOOGLE_BOOKS_API_KEY: str

  # Apple Sign In
  APPLE_BUNDLE_ID: str
  APPLE_PUBLIC_KEYS_URL: str = "https://appleid.apple.com/auth/keys"

  # Database settings    
  POSTGRES_USER: str
  POSTGRES_PASSWORD: str
  POSTGRES_SERVER: str = "localhost"
  POSTGRES_DB: str = "focus_read_db"
  
  @property
  def SQLALCHEMY_DATABASE_URI(self) -> str:
    return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
  
  class Config:
    env_file = ".env"
    case_sensitive = True

@lru_cache
def get_settings() -> Settings:
  return Settings()