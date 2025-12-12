from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.password_reset import (
    PasswordResetRequest,
    PasswordResetConfirm
)
from app.services.password_reset_service import (
    request_password_reset,
    reset_password
)

router = APIRouter()

@router.post("/request")
def request_reset(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    request_password_reset(payload.email, db)
    return {"message": "If the email exists, a reset link was sent"}

@router.post("/confirm")
def confirm_reset(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    success = reset_password(payload.token, payload.new_password, db)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"message": "Password updated successfully"}
