from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.security import verify_password
from app.core.jwt import create_access_token


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    return user

def login_user(email: str, password: str, db: Session):
    user = authenticate_user(email, password, db)
    if not user:
        return None
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}