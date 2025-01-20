from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.book_progress import BookProgress, BookProgressStatus

class BookProgressService:
	@staticmethod
	async def get_or_create_progress(
		db: Session, 
		user_id: int,
		book_data: dict,
		total_chapters: int
	) -> BookProgress:
			progress = db.query(BookProgress).filter(
					BookProgress.user_id == user_id,
					BookProgress.book_id == book_data["book_id"]
			).first()
			
			if not progress:
					progress = BookProgress(
							user_id=user_id,
							book_id=book_data["book_id"],
							title=book_data["title"],
							author=book_data.get("author"),
							cover_image=book_data.get("cover_image"),
							total_chapters=total_chapters,
							current_chapter=0,
							book_metadata=book_data.get("metadata")
					)
					db.add(progress)
					db.commit()
					db.refresh(progress)
			
			return progress

	@staticmethod
	async def update_progress(db: Session, user_id: int, book_id: str, chapter_number: int) -> BookProgress:
		# Get existing progress or create new
		progress = db.query(BookProgress).filter(
			BookProgress.user_id == user_id,
			BookProgress.book_id == book_id
		).first()

		if progress:
			progress.current_chapter = max(progress.current_chapter, chapter_number)
			progress.update_progress()
			db.commit()
			db.refresh(progress)
		
		return progress

	@staticmethod
	async def get_user_reading_books(db: Session, user_id: int, status: BookProgressStatus) -> List[BookProgress]:
		"""
		Get all books with the specified status for a user
		"""
		return db.query(BookProgress).filter(
			BookProgress.user_id == user_id,
			BookProgress.status == status
		).all() 