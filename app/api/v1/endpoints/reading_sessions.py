from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.reading_session import ReadingSession, ReadingSessionCreate, IntervalType
from app.services.reading_session import reading_session_service
from app.models.user import User
from app.api.deps import CurrentUser

router = APIRouter()

@router.post("/", response_model=ReadingSession)
async def create_reading_session(
	*,
	current_user: CurrentUser,
	db: Session = Depends(deps.get_db),
	session_in: ReadingSessionCreate,
) -> Any:
	"""
	Create new reading session for a book.
	"""
	return reading_session_service.create_session(
		db=db,
		user_id=current_user.id,
		book_id=session_in.book_id,
		chapter_data=session_in.chapter_data  # Chapter data comes from client
	)

@router.get("/active", response_model=List[ReadingSession])
def get_active_sessions(
	current_user: CurrentUser,
	db: Session = Depends(deps.get_db),
):
	"""
	Get all active reading sessions for current user.
	"""
	return reading_session_service.get_active_sessions(db=db, user_id=current_user.id)

@router.post("/{session_id}/intervals")
def create_interval(
	*,
	current_user: CurrentUser,
	db: Session = Depends(deps.get_db),
	session_id: int,
	interval_type: IntervalType
):
	"""Start a new interval in the reading session"""
	return reading_session_service.start_new_interval(
		db=db, 
		session_id=session_id,
		interval_type=interval_type
	)

@router.post("/intervals/{interval_id}/pause")
def pause_interval(
	*,
	current_user: CurrentUser,
	db: Session = Depends(deps.get_db),
	interval_id: int,
	remaining_time: int
):
	"""Pause an active interval"""
	return reading_session_service.pause_interval(
		db=db,
		interval_id=interval_id,
		remaining_time=remaining_time
	)

@router.post("/intervals/{interval_id}/resume")
def resume_interval(
	*,
	current_user: CurrentUser,
	db: Session = Depends(deps.get_db),
	interval_id: int,
):
	"""Resume an interval"""
	return reading_session_service.resume_interval(
		db=db,
		interval_id=interval_id
	)

@router.post("/intervals/{interval_id}/complete")
def complete_interval(
	*,
	current_user: CurrentUser,
	db: Session = Depends(deps.get_db),
	interval_id: int,
):
	"""Complete an interval"""
	return reading_session_service.complete_interval(
		db=db,
		interval_id=interval_id
	)

@router.post("/{session_id}/complete", response_model=ReadingSession)
async def complete_session(
	*,
	current_user: CurrentUser,
	db: Session = Depends(deps.get_db),
	session_id: int,
):
	"""Complete a reading session"""
	return await reading_session_service.complete_session(
		db=db,
		session_id=session_id,
		user_id=current_user.id
	) 