from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.utils.main import verify_apple_token
from app.services.user import find_or_create_user
from app.api.deps import get_db

router = APIRouter()

class AppleAuthRequest(BaseModel):
  id_token: str

@router.post("/apple")
async def apple_auth(
    auth_request: AppleAuthRequest,
    db: Session = Depends(get_db)
):
    # Verify Apple JWT
    user_data = verify_apple_token(auth_request.id_token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Handle user creation or retrieval
    user_id = user_data.get("sub")
    email = user_data.get("email")
    
    user = find_or_create_user(user_id=user_id, email=email, db=db)
    
    return {
        "message": "Authentication successful",
        "user_id": user.id,
        "email": user.email
    } 