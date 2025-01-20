from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class IntervalType(str, Enum):
  WORK = "work"  # 25 minutes
  SHORT_BREAK = "short_break"  # 5 minutes
  LONG_BREAK = "long_break"  # 15 minutes

class IntervalStatus(str, Enum):
  ACTIVE = "active"
  PAUSED = "paused"
  COMPLETED = "completed"

class SessionStatus(str, Enum):
  IN_PROGRESS = "in_progress"
  COMPLETED = "completed"

class ChapterType(str, Enum):
  INTRO = "intro"
  CHAPTER = "chapter"

class IntervalBase(BaseModel):
  type: IntervalType
  status: IntervalStatus
  remaining_time: int  # in seconds
  started_at: Optional[datetime] = None
  completed_at: Optional[datetime] = None

class IntervalCreate(IntervalBase):
  pass

class Interval(IntervalBase):
  id: int
  session_id: int
    
  class Config:
    from_attributes = True

class ReadingSessionBase(BaseModel):
    book_id: str  # Changed from int to str to match Google Books IDs
    chapter_number: int
    chapter_type: ChapterType
    chapter_title: str
    intervals_count: int = 0

class ChapterData(BaseModel):
    number: int = Field(..., description="Chapter number", example=1)
    type: ChapterType = Field(..., description="Type of chapter", example=ChapterType.CHAPTER)
    title: str = Field(..., description="Chapter title", example="The Beginning")

class ReadingSessionCreate(BaseModel):
    book_id: str = Field(
        ..., 
        description="The ID of the book being read",
        example="abc123xyz"
    )
    chapter_data: ChapterData = Field(
        ...,
        description="Data about the chapter being read"
    )

    def to_base(self) -> ReadingSessionBase:
        """Convert create model to base model"""
        return ReadingSessionBase(
            book_id=self.book_id,
            chapter_number=self.chapter_data.number,
            chapter_type=self.chapter_data.type,
            chapter_title=self.chapter_data.title,
            intervals_count=0
        )

class ReadingSession(ReadingSessionBase):
  id: int
  user_id: int
  status: SessionStatus
  intervals: List[Interval]
  started_at: datetime
  completed_at: Optional[datetime] = None

class Config:
  from_attributes = True

class ChapterData(BaseModel):
  number: int
  type: str
  title: str 