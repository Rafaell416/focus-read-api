from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.user import User
from app.models.notes import Notes
from app.models.reading_session import ReadingSession
from app.models.book_progress import BookProgress
from app.schemas.notes import NotesCreate, NotesList, Notes as NotesSchema
from sqlalchemy import desc

router = APIRouter()

@router.post("/", response_model=NotesSchema)
def create_note(
    note: NotesCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Create a new note for a reading session.
    """
    # Verify reading session exists and belongs to user
    reading_session = db.query(ReadingSession).filter(
        ReadingSession.id == note.reading_session_id,
        ReadingSession.user_id == current_user.id
    ).first()
    
    if not reading_session:
        raise HTTPException(
            status_code=404,
            detail="Reading session not found or doesn't belong to user"
        )

    db_note = Notes(
        content=note.content,
        user_id=current_user.id,
        reading_session_id=note.reading_session_id
    )
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/reading-session/{reading_session_id}", response_model=NotesList)
def get_reading_session_notes(
    reading_session_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get all notes for a specific reading session.
    """
    notes = db.query(Notes).filter(
        Notes.reading_session_id == reading_session_id,
        Notes.user_id == current_user.id
    ).order_by(desc(Notes.created_at)).all()
    
    return NotesList(notes=notes, total=len(notes))

@router.get("/book/{book_id}", response_model=NotesList)
def get_book_notes(
    book_id: str,  # Google Books ID
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get all notes for a specific book across all reading sessions.
    First verifies if user has a book progress for this book.
    Returns notes ordered by chapter number and creation date.
    """
    # Verify user has access to this book through book progress
    book_progress = db.query(BookProgress).filter(
        BookProgress.book_id == book_id,
        BookProgress.user_id == current_user.id
    ).first()
    
    if not book_progress:
        raise HTTPException(
            status_code=404,
            detail="Book progress not found"
        )

    # Get all notes from reading sessions for this book
    notes = db.query(Notes).join(
        ReadingSession, Notes.reading_session_id == ReadingSession.id
    ).filter(
        ReadingSession.book_id == book_id,
        Notes.user_id == current_user.id
    ).order_by(
        ReadingSession.chapter_number,  # Order by chapter number
        desc(Notes.created_at)  # Then by creation date (newest first)
    ).all()
    
    return NotesList(notes=notes, total=len(notes))



