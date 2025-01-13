from fastapi import APIRouter
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import books

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(books.router, prefix="/books", tags=["books"])