from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
  email: EmailStr
  full_name: Optional[str] = None
  is_active: bool = True
  is_superuser: bool = False


class UserCreate(UserBase):
    apple_id: str
    email: EmailStr


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class AppleAuthData(BaseModel):
    apple_id: str
    email: EmailStr
    full_name: Optional[str] = None
    identity_token: str


class UserInDBBase(UserBase):
    id: int
    apple_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserInDBBase):
    """
    Return model for general use, without sensitive data
    """
    pass


class UserInDB(UserInDBBase):
    """
    Additional fields for database storage
    Add any sensitive fields here that shouldn't be returned to the client
    """
    hashed_refresh_token: Optional[str] = None 