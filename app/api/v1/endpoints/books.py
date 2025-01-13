from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.book import search_books, get_book_details, scrape_toc_from_bn, parse_toc_to_json
from app.schemas.book import BookSearchResponse, BookDetailResponse, ToCResponse

router = APIRouter()

@router.get("/search", response_model=BookSearchResponse)
async def search_books_endpoint(
    q: str = Query(..., description="Search query"),
    lang: Optional[str] = Query(None, description="Filter by language"),
    max_results: int = Query(10, le=40, description="Maximum number of results to return")
):
    """
    Search for books using the Google Books API.
    
    - **q**: Search query (e.g., "python programming", "title:dune", "author:asimov")
    - **lang**: Filter by language (e.g., "en", "es", "fr")
    - **max_results**: Maximum number of results to return (default: 10, max: 40)
    """
    try:
        result = search_books(q, lang, max_results)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{book_id}", response_model=BookDetailResponse)
async def get_book_details_endpoint(book_id: str):
    """
    Get detailed information about a specific book by its ID.
    """
    try:
        book = get_book_details(book_id)
        return book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{book_id}/toc", response_model=ToCResponse)
async def get_toc_endpoint(book_id: str):
    """
    Get a table of contents for a book from Barnes & Noble.
    """
    try:
        book = get_book_details(book_id)
        toc_text = scrape_toc_from_bn(
            book["volumeInfo"]["title"],
            book["volumeInfo"].get("authors", [])[0]
        )
        if "Error" not in toc_text:
            toc_data = parse_toc_to_json(toc_text)
            return ToCResponse(toc=toc_data["toc"])
        else:
            return ToCResponse(toc=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 