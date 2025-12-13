from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.schemas.products import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import (
    create_product, update_product,
    delete_product, get_product,
    list_products, search_products
)

from typing import List

router = APIRouter()


@router.post("/", response_model=ProductResponse)
def create(payload: ProductCreate, db: Session = Depends(get_db)):
    return create_product(payload, db)

@router.get("/", response_model=list[ProductResponse])
def list_all(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return list_products(db, skip, limit)

@router.put("/{product_id}", response_model=ProductResponse)
def update(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product(product_id, payload, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return product

@router.delete("/{product_id}", response_model=ProductResponse)
def delete(product_id: int, db: Session = Depends(get_db)):
    if not delete_product(product_id, db):
        raise HTTPException(status_code=404, detail="Product Not Found")
    return {"message": "Product deleted"}


@router.get("/search", response_model=List[ProductResponse])
def search(
    q: Optional[str] = Query(None, description="Search keyword"),
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = False,
    sort: Optional[str] = Query(
        None,
        regex="^(price_asc|price_desc)$"
    ),
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return search_products(
        db=db,
        q=q,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        sort=sort,
        page=page,
        limit=limit,
    )