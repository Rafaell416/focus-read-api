from typing import Generator, Annotated
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from fastapi import Depends

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user() -> User:
    """
    Mock dependency for development/testing before implementing real authentication.
    Returns a hardcoded mock user.
    """
    mock_user = User(
        id=1,
        email="test@example.com",
        username="test_user",
        is_active=True
    )
    return mock_user

# Use this in your endpoints
CurrentUser = Annotated[User, Depends(get_current_user)]