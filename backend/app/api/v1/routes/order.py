from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from app.services.order_service import create_order, list_user_orders
from app.schemas.order import OrderResponse
from typing import List

router = APIRouter()


@router.post("/checkout", response_model=OrderResponse)
def checkout(user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        order = create_order(user.id, db)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[OrderResponse])
def orders(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return list_user_orders(user.id, db)
