from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models.email_verification import EmailVerificationToken
from app.db.models.user import User
from app.core.tokens import generate_secure_token
from app.core.config import settings
from app.services.email_service import send_email

def send_verification_email(user: User, db: Session):
    token = generate_secure_token()
    expires = datetime.utcnow() + timedelta(
        hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS
    )

    record = EmailVerificationToken(
        user_id=user.id,
        token=token,
        expires_at=expires
    )

    db.add(record)
    db.commit()

    verify_link = f"{settings.FRONTEND_VERIFY_EMAIL_URL}?token={token}"

    send_email(
        to_email=user.email,
        subject="Verify your email address",
        content=f"Click the link to verify your account:\n{verify_link}"
    )


def verify_email(token: str, db: Session):
    record = db.query(EmailVerificationToken).filter(
        EmailVerificationToken.token == token,
        EmailVerificationToken.used == 0,
        EmailVerificationToken.expires_at > datetime.utcnow()
    ).first()

    if not record:
        return False

    user = db.query(User).filter(User.id == record.user_id).first()
    user.is_verified = True

    record.used = 1
    db.commit()
    return True