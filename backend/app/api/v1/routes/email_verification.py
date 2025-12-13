from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.email_verification import EmailVerificationConfirm
from app.services.email_verification_service import verify_email

router = APIRouter()

@router.post("/confirm")
def confirm_email(payload: EmailVerificationConfirm, db: Session = Depends(get_db)):
    success = verify_email(payload.token, db)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"message": "Email verified successfully"}
