from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

def create_user(payload: UserCreate, db: Session):
    user = db.query(User).filter(User.email == payload.email).first()
    if user:
        raise ValueError("Email already registered")
    
    new_user = User(
        email=payload.email,
        hash_passwor=hash_password(payload.password),
        full_name=payload.full_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user