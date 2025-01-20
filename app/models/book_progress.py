from sqlalchemy import Column, Integer, Float, ForeignKey, String, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from enum import Enum

from app.models.base import Base

class BookProgressStatus(str, Enum):
  IN_PROGRESS = "in_progress"
  COMPLETED = "completed"

class BookProgress(Base):
  __tablename__ = "book_progress"

  id = Column(Integer, primary_key=True, index=True)
  book_id = Column(String, index=True, nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  title = Column(String, nullable=False)
  author = Column(String)
  cover_image = Column(String)
  current_chapter = Column(Integer, default=0)
  total_chapters = Column(Integer, nullable=False)
  status = Column(SQLEnum(BookProgressStatus), default=BookProgressStatus.IN_PROGRESS)
  progress_percentage = Column(Float, default=0.0)
  book_metadata = Column(JSON, nullable=True)  # For any additional book info you want to store

    # Relationship
  user = relationship("User", back_populates="book_progresses")

  def update_progress(self) -> None:
    """Update progress percentage and status based on current chapter"""
    if self.total_chapters > 0:
      self.progress_percentage = (self.current_chapter / self.total_chapters) * 100
      if self.current_chapter >= self.total_chapters:
        self.status = BookProgressStatus.COMPLETED
      else:
        self.status = BookProgressStatus.IN_PROGRESS 