from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.order import Order
from app.core.deps import get_admin_user
from app.db.session import get_db
from typing import List
from app.schemas.order import OrderResponse

router = APIRouter()


@router.get("/", response_model=List[OrderResponse])
def list_all_orders(db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    return db.query(Order).all()


@router.put("/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")

    order.status = status
    db.commit()
    return {"message": "Order status updated"}
