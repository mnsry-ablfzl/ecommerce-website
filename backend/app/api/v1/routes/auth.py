from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import LoginSchema, TokenResponse
from app.services.auth_service import login_user
from app.services.user_service import create_user
from app.core.deps import get_current_user
from app.core.jwt import create_access_token
from app.services.auth_service import store_refresh_token
from app.services.auth_service import authenticate_user
from app.db.models.refresh_token import RefreshToken



router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(payload, db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@router.post("/login", response_model=TokenResponse)
def login_user(email: str, password: str, db: Session):
    user = authenticate_user(email, password, db)
    if not user:
        return None

    access_token = create_access_token(user.id)
    refresh_token = store_refresh_token(user.id, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(token: str, db: Session = Depends(get_db)):
    refresh = db.query(RefreshToken).filter(
        RefreshToken.token == token,
        RefreshToken.expires_at > datetime.utcnow()
    ).first()

    if not refresh:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(refresh.user_id)
    return {"access_token": access_token}




@router.post("/logout")
def logout(token: str, db: Session = Depends(get_db)):
    db.query(RefreshToken).filter(RefreshToken.token == token).delete()
    db.commit()
    return {"message": "Logged out successfully"}



@router.get("/me")
def get_profile(user = Depends(get_current_user)):
    return user