from fastapi import APIRouter
from app.api.v1.endpoints import books, reading_sessions, auth, quiz

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(reading_sessions.router, prefix="/reading-sessions", tags=["reading-sessions"])
api_router.include_router(quiz.router, prefix="/quiz", tags=["quiz"])