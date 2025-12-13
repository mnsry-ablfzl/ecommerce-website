from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.services.email_verification_service import send_verification_email

def create_user(payload: UserCreate, db: Session):
    user = db.query(User).filter(User.email == payload.email).first()
    if user:
        raise ValueError("Email already registered")
    
    new_user = User(
        email=payload.email,
        hash_passwor=hash_password(payload.password),
        full_name=payload.full_name,
        is_verified = False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_verification_email(user, db)

    return new_user


def update_profile(user, payload, db):
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user