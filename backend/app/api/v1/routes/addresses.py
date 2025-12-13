from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_current_user
from app.db.session import get_db
from app.schemas.address import AddressCreate, AddressResponse
from app.services.address_service import (
    create_address, list_addresses, delete_address
)
from typing import List

router = APIRouter()

@router.post("/", response_model=AddressResponse)
def add_address(
    payload: AddressCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_address(user.id, payload, db)

@router.get("/", response_model=List[AddressResponse])
def get_addresses(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return list_addresses(user.id, db)

@router.delete("/{address_id}")
def remove_address(
    address_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not delete_address(user.id, address_id, db):
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted"}
