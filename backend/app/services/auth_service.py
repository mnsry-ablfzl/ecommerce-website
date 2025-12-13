from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.jwt import create_refresh_token
from app.db.models.refresh_token import RefreshToken
from datetime import datetime, timedelta


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_verified:
        raise ValueError("Email not verified")
    
    return user

def login_user(email: str, password: str, db: Session):
    user = authenticate_user(email, password, db)
    if not user:
        return None
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


def store_refresh_token(user_id: int, db: Session):
    token = create_refresh_token()
    expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    refresh = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires
    )

    db.add(refresh)
    db.commit()
    return token