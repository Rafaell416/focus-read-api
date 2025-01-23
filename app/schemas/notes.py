from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# Base Note Schema with common attributes
class NotesBase(BaseModel):
	content: str = Field(..., description="The content of the note")
	created_at: datetime = Field(default_factory=datetime.now)

# Schema for creating a new note
class NotesCreate(BaseModel):
  content: str = Field(..., description="The content of the note")
  reading_session_id: int = Field(..., description="ID of the reading session")

# Schema for reading note from database
class Notes(NotesBase):
	id: int
	user_id: int
	reading_session_id: int
	
	class Config:
		from_attributes = True

# Schema for returning multiple notes
class NotesList(BaseModel):
	notes: List[Notes]
	total: int = Field(..., description="Total number of notes") 