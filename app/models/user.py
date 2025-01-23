from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True)
  username = Column(String, unique=True, index=True)
  is_active = Column(Boolean, default=True)
  
  book_progresses = relationship("BookProgress", back_populates="user")
  reading_sessions = relationship("ReadingSession", back_populates="user")
  notes = relationship("Notes", back_populates="user")
