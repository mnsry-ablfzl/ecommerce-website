from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.cart import CartItemCreate, CartResponse
from app.services.cart_service import (
    get_cart,
    add_item_to_cart,
    remove_item_from_cart
)
from app.core.deps import get_current_user


router = APIRouter()

@router.get("/", response_model=CartResponse)
def view_cart(user = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_cart(user.id, db)

@router.post("/", response_model=CartResponse)
def add_item(payload: CartItemCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return add_item_to_cart(user.id, payload, db)

@router.delete("/{product_id}")
def remove_item(product_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    success = remove_item_from_cart(user.id, product_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Item not in cart")
    return {"message": "Item Remove"}