from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
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


def search_products(
    db: Session,
    q: str | None = None,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    in_stock: bool | None = None,
    sort: str | None = None,
    page: int = 1,
    limit: int = 20,
):
    query = db.query(Product)

    if q:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{q}%"),
                Product.description.ilike(f"%{q}%")
            )
        )


    if category_id:
        query = query.filter(Product.category_id == category_id)


    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)


    if in_stock:
        query = query.filter(Product.stock > 0)


    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.id.desc())  


    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()
