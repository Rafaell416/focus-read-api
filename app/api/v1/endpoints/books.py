from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
from app.services.book import search_books, get_book_details, scrape_toc_from_bn, parse_toc_to_json
from app.schemas.book import BookSearchResponse, BookDetailResponse, ToCResponse
from sqlalchemy.orm import Session
from app.api import deps
from app.models.table_of_contents import TableOfContents
from app.services.book_progress import BookProgressService
from app.schemas.book_progress import BookProgress
from app.models.book_progress import BookProgressStatus
from app.schemas.book_progress import BookProgressRequest

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

@router.get("/currently-reading", response_model=List[BookProgress])
async def get_currently_reading(
	db: Session = Depends(deps.get_db),
	current_user = Depends(deps.get_current_user)
):
	"""
	Get all books currently being read by the user
	"""
	return await BookProgressService.get_user_reading_books(
		db=db,
		user_id=current_user.id,
		status=BookProgressStatus.IN_PROGRESS
	)

@router.get("/completed-books", response_model=List[BookProgress])
async def get_completed_books(
	db: Session = Depends(deps.get_db),
	current_user = Depends(deps.get_current_user)
):
	"""
	Get all completed books for the user
	"""
	return await BookProgressService.get_user_reading_books(
		db=db,
		user_id=current_user.id,
		status=BookProgressStatus.COMPLETED
	)

@router.post("/progress", response_model=BookProgress)
async def create_book_progress(
	request: BookProgressRequest,
	db: Session = Depends(deps.get_db),
	current_user = Depends(deps.get_current_user)
):
	"""
	Create a new book progress entry for a user
	"""
	return await BookProgressService.get_or_create_progress(
		db=db,
		user_id=current_user.id,
		book_data=request.book_data,
		total_chapters=request.total_chapters
	)

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
async def get_table_of_contents_endpoint(
	book_id: str,
	db: Session = Depends(deps.get_db)
):
	"""
	Get table of contents for a book. 
	First checks database, if not found scrapes from Barnes & Noble.
	"""
	# Try to get from database first
	toc = db.query(TableOfContents).filter(
		TableOfContents.book_id == book_id
	).first()

	if toc:
		return {"toc": toc.content}

	# If not in database, scrape from B&N
	book_details = get_book_details(book_id)
	toc_text = scrape_toc_from_bn(
		book_title=book_details["volumeInfo"]["title"],
		author_name=book_details["volumeInfo"]["authors"][0]
	)	
	# Parse the scraped text to JSON format with chapter numbers
	toc_data = parse_toc_to_json(toc_text)
	
	# Save to database
	new_toc = TableOfContents(
		book_id=book_id,
		content=toc_data["toc"]  # Save the formatted data with chapter numbers
	)
	db.add(new_toc)
	db.commit()
	db.refresh(new_toc)

	return {"toc": new_toc.content}  # Return the saved content instead of raw toc_data 