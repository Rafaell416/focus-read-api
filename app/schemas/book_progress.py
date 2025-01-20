from pydantic import BaseModel
from enum import Enum
from typing import Optional, Dict, Any

class BookProgressStatus(str, Enum):
  IN_PROGRESS = "in_progress"
  COMPLETED = "completed"

class BookProgressBase(BaseModel):
  book_id: str
  title: str
  author: Optional[str] = None
  cover_image: Optional[str] = None
  current_chapter: int
  total_chapters: int
  progress_percentage: float
  status: BookProgressStatus
  book_metadata: Optional[Dict[str, Any]] = None

class BookProgressCreate(BookProgressBase):
  user_id: int

class BookProgress(BookProgressBase):
  id: int

  class Config:
    from_attributes = True 

class BookProgressRequest(BaseModel):
    book_data: dict
    total_chapters: int

    class Config:
        json_schema_extra = {
            "example": {
                "book_data": {
                    "book_id": "abc123",
                    "title": "The Great Book",
                    "author": "John Doe",
                    "cover_image": "https://example.com/cover.jpg",
                    "metadata": {
                        "publisher": "Publisher Name",
                        "publishedDate": "2023"
                    }
                },
                "total_chapters": 12
            }
        } 