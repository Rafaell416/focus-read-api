from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.models.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reading_session_id = Column(Integer, ForeignKey("reading_sessions.id"), nullable=False)
    content = Column(String, nullable=False) 
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="notes")
    reading_session = relationship("ReadingSession", back_populates="notes") 