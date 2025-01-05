from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
  PROJECT_NAME: str = "Focus Read API"
  API_V1_STR: str = "/api/v1"
  API_VERSION: str = "1.0.0"

  # Security
  SECRET_KEY: str
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

  # Database
  POSTGRES_SERVER: str
  POSTGRES_USER: str
  POSTGRES_PASSWORD: str
  POSTGRES_DB: str

  # OpenAi
  OPENAI_API_KEY: str

  # Apple Sign In
  APPLE_BUNDLE_ID: str
  APPLE_PUBLIC_KEYS_URL: str = "https://appleid.apple.com/auth/keys"

  class Config:
    env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()