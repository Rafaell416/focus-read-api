from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict

class IndustryIdentifier(BaseModel):
    type: str
    identifier: str

class ImageLinks(BaseModel):
    smallThumbnail: Optional[HttpUrl] = None
    thumbnail: Optional[HttpUrl] = None
    small: Optional[HttpUrl] = None
    medium: Optional[HttpUrl] = None
    large: Optional[HttpUrl] = None
    extraLarge: Optional[HttpUrl] = None

class VolumeInfo(BaseModel):
    title: str
    subtitle: Optional[str] = None
    authors: Optional[List[str]] = None
    publisher: Optional[str] = None
    publishedDate: Optional[str] = None
    description: Optional[str] = None
    industryIdentifiers: Optional[List[IndustryIdentifier]] = None
    pageCount: Optional[int] = None
    categories: Optional[List[str]] = None
    averageRating: Optional[float] = None
    ratingsCount: Optional[int] = None
    imageLinks: Optional[ImageLinks] = None
    language: Optional[str] = None
    previewLink: Optional[HttpUrl] = None
    infoLink: Optional[HttpUrl] = None

class BookBase(BaseModel):
    id: str
    volumeInfo: VolumeInfo

class BookSearchResponse(BaseModel):
    books: List[BookBase]
    totalItems: int

class BookDetailResponse(BookBase):
    pass

class ToCEntry(BaseModel):
    type: str  # "section", "chapter", "intro", or "other"
    title: str
    page: Optional[int] = None

class ToCResponse(BaseModel):
    toc: List[ToCEntry] 