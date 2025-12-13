from pydantic import BaseModel
from typing import Optional

class AddressCreate(BaseModel):
    full_name: str
    phone: str
    country: str
    city: str
    street: str
    postal_code: str
    is_default: bool = False
    address_type: str = "shipping"


class AddressResponse(AddressCreate):
    id: int

    class Config:
        orm_mode = True
