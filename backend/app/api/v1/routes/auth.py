from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import LoginSchema, TokenResponse
from app.services.auth_service import login_user
from app.services.user_service import create_user
from app.core.deps import get_current_user
router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(payload, db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    token = login_user(payload.email, payload.password, db)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    return token


@router.get("/me")
def get_profile(user = Depends(get_current_user)):
    return user