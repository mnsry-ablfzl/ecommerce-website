from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.models.password_reset import PasswordResetToken
from app.core.tokens import generate_secure_token
from app.core.config import settings
from app.services.email_service import send_email
from app.core.security import hash_password

def request_password_reset(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return  # silent fail for security

    token = generate_secure_token()
    expires = datetime.utcnow() + timedelta(
        minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
    )

    reset = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expires
    )

    db.add(reset)
    db.commit()

    reset_link = f"{settings.FRONTEND_RESET_PASSWORD_URL}?token={token}"

    send_email(
        to_email=user.email,
        subject="Reset your password",
        content=f"Click the link to reset your password:\n{reset_link}"
    )


def reset_password(token: str, new_password: str, db: Session):
    reset = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token,
        PasswordResetToken.used == 0,
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()

    if not reset:
        return False

    user = db.query(User).filter(User.id == reset.user_id).first()
    user.hashed_password = hash_password(new_password)

    reset.used = 1
    db.commit()
    return True