from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

from app.models.user import Base

class SessionStatus(str, Enum):
  IN_PROGRESS = "in_progress"
  COMPLETED = "completed"

class IntervalType(str, Enum):
  WORK = "work"
  SHORT_BREAK = "short_break"
  LONG_BREAK = "long_break"

class IntervalStatus(str, Enum):
  ACTIVE = "active"
  PAUSED = "paused"
  COMPLETED = "completed"

class Interval(Base):
  __tablename__ = "intervals"

  id = Column(Integer, primary_key=True, index=True)
  session_id = Column(Integer, ForeignKey("reading_sessions.id"))
  type = Column(SQLEnum(IntervalType))
  status = Column(SQLEnum(IntervalStatus))
  remaining_time = Column(Integer)  # in seconds
  started_at = Column(DateTime, nullable=True)
  completed_at = Column(DateTime, nullable=True)

  session = relationship("ReadingSession", back_populates="intervals")

class ReadingSession(Base):
  __tablename__ = "reading_sessions"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  book_id = Column(String, index=True)
  chapter_number = Column(Integer)
  chapter_title = Column(String)
  chapter_type = Column(String)
  status = Column(SQLEnum(SessionStatus), default=SessionStatus.IN_PROGRESS)
  started_at = Column(DateTime, default=datetime.now)
  completed_at = Column(DateTime, nullable=True)
  intervals_count = Column(Integer, default=0)

  intervals = relationship("Interval", back_populates="session")
  user = relationship("User", back_populates="reading_sessions") 