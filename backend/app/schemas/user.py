from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    phone: Optional[str]

    class Config:
        orm_mode = True


class UserProfileUpdate(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]