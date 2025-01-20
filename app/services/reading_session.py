from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.reading_session import ReadingSession, Interval
from app.schemas.reading_session import (
  ReadingSessionCreate, 
  IntervalType, 
  IntervalStatus,
  SessionStatus,
  ChapterData,
)
from app.crud.base import CRUDBase
from app.services.book_progress import BookProgressService

WORK_INTERVAL = 25 * 60      # 25 minutes in seconds
SHORT_BREAK = 5 * 60         # 5 minutes in seconds
LONG_BREAK = 15 * 60         # 15 minutes in seconds

class ReadingSessionService(CRUDBase[ReadingSession, ReadingSessionCreate, ReadingSessionCreate]):
	def create_session(
		self, 
		db: Session, 
		*, 
		user_id: int, 
		book_id: str,
		chapter_data: ChapterData
	) -> ReadingSession:
		db_obj = ReadingSession(
			book_id=book_id,
			user_id=user_id,
			chapter_number=chapter_data.number,
			chapter_type=chapter_data.type,
			chapter_title=chapter_data.title,
			status=SessionStatus.IN_PROGRESS,
			started_at=datetime.now(),
			intervals_count=0,
		)
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj

	def start_new_interval(self, db: Session, *, session_id: int, interval_type: IntervalType) -> Interval:
		duration = {
			IntervalType.WORK: WORK_INTERVAL,
			IntervalType.SHORT_BREAK: SHORT_BREAK,
			IntervalType.LONG_BREAK: LONG_BREAK
		}[interval_type]

		interval = Interval(
			session_id=session_id,
			type=interval_type,
			status=IntervalStatus.ACTIVE,
			remaining_time=duration,
			started_at=datetime.now()
		)
			
		session = db.query(ReadingSession).filter(ReadingSession.id == session_id).first()
		session.intervals_count += 1
		
		db.add(interval)
		db.commit()
		db.refresh(interval)
		return interval

	def pause_interval(self, db: Session, *, interval_id: int, remaining_time: int) -> Interval:
		interval = db.query(Interval).filter(Interval.id == interval_id).first()
		if interval:
			interval.status = IntervalStatus.PAUSED
			interval.remaining_time = remaining_time
			db.commit()
			db.refresh(interval)
		return interval
	
	def resume_interval(self, db: Session, *, interval_id: int) -> Interval:
		interval = db.query(Interval).filter(Interval.id == interval_id).first()
		if interval:
			interval.status = IntervalStatus.ACTIVE
			db.commit()
			db.refresh(interval)
		return interval
	
	def complete_interval(self, db: Session, *, interval_id: int) -> Interval:
		interval = db.query(Interval).filter(Interval.id == interval_id).first()
		if interval:
			interval.status = IntervalStatus.COMPLETED
			interval.completed_at = datetime.now()
			interval.remaining_time = 0
			db.commit()
			db.refresh(interval)
		return interval

	@staticmethod
	async def complete_session(db: Session, session_id: int, user_id: int) -> ReadingSession:
		session = db.query(ReadingSession).filter(
			ReadingSession.id == session_id,
			ReadingSession.user_id == user_id
		).first()
		
		if not session:
			raise HTTPException(status_code=404, detail="Reading session not found")
			
		session.status = SessionStatus.COMPLETED
		session.completed_at = datetime.now()
		
		# Update book progress
		await BookProgressService.update_progress(
			db=db,
			user_id=user_id,
			book_id=session.book_id,
			chapter_number=session.chapter_number
		)
		
		db.commit()
		db.refresh(session)
		return session

	def get_active_sessions(self, db: Session, user_id: int) -> List[ReadingSession]:
		return db.query(ReadingSession).filter(
			ReadingSession.user_id == user_id,
			ReadingSession.status == SessionStatus.IN_PROGRESS
		).all()

reading_session_service = ReadingSessionService(ReadingSession) 