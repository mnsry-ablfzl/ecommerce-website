from sqlalchemy.orm import Session
from app.db.models.product import Product
from app.schemas.products import ProductCreate, ProductUpdate


def create_product(payload: ProductCreate, db: Session):
    product = Product(**payload.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product(product_id: int, db: Session):
    return db.query(Product).filter(Product.id == product_id).first()

def list_products(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Product).offset(skip).limit(limit).all()

def update_product(product_id: int, payload: ProductUpdate, db: Session):
    product = get_product(product_id, db)
    if not product:
        return None
    
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

def delete_product(product_id: int, db: Session):
    product = get_product(product_id, db)
    if not product:
        return None
    
    db.delete(product)
    db.commit()
    return True
