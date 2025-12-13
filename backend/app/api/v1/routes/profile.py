from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_user
from app.db.session import get_db
from app.schemas.user import UserProfileResponse, UserProfileUpdate
from app.services.user_service import update_profile

router = APIRouter()

@router.get("/me", response_model=UserProfileResponse)
def get_profile(user=Depends(get_current_user)):
    return user

@router.put("/me", response_model=UserProfileResponse)
def update_me(
    payload: UserProfileUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_profile(user, payload, db)
