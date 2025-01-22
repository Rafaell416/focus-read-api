from pydantic import BaseModel, Field
from typing import List

class QuizQuestion(BaseModel):
	question: str
	options: List[str]
	correct_answer: int = Field(ge=0, le=2)  # Ensures value is between 0 and 2

class QuizRequest(BaseModel):
	book_name: str
	chapter_name: str
	author_name: str

class QuizResponse(BaseModel):
  questions: List[QuizQuestion] 