from sqlalchemy.orm import Session
from app.models.user import User

def find_or_create_user(user_id: str, email: str, db: Session):
  user = db.query(User).filter(User.id == user_id).first()
    
  if not user:
    user = User(
      id=user_id,
      email=email
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
  return user 