from sqlalchemy.orm import Session
from app.db.models.cart import Cart
from app.db.models.cart_item import CartItem
from app.schemas.cart import CartItemCreate

def get_to_create_cart(user_id: int, db: Session):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        cart = Cart(user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart

def add_item_to_cart(user_id: int, payload: CartItemCreate, db: Session):
    cart = get_to_create_cart(user_id, db)

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == payload.product_id
    ).first()

    if item:
        item.quantity += payload.quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=payload.product_id,
            quantity=payload.quantity
        )
        db.add(item)

    db.commit()
    db.refresh(cart)
    return cart

def remove_item_from_cart(user_id: int, product_id: int, db: Session):
    cart = get_to_create_cart(user_id, db)

    item = db.query(CartItem).filter(
        CartItem.user_id == cart.id,
        CartItem.product_id == product_id
    ).first()

    if not item:
        return None
    
    db.delete(item)
    db.commit()
    return True

def get_cart(user_id: int, db: Session):
    return get_to_create_cart(user_id, db)


