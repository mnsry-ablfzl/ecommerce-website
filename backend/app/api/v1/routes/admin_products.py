from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.products import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import (
    create_product,
    update_product,
    delete_product,
    get_product
)
from app.core.deps import get_admin_user
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=ProductResponse)
def admin_create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_admin_user)
):
    return create_product(payload, db)


@router.put("/{product_id}", response_model=ProductResponse)
def admin_update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_admin_user)
):
    updated = update_product(product_id, payload, db)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.delete("/{product_id}")
def admin_delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_admin_user)
):
    if not delete_product(product_id, db):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
