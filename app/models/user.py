from sqlalchemy import Column, String
from app.models.base import Base, TimestampMixin

class User(Base, TimestampMixin):
  __tablename__ = "users"
    
  id = Column(String, primary_key=True)
  name = Column(String, nullable=True)
  email = Column(String, unique=True, nullable=False)
