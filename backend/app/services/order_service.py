from sqlalchemy.orm import Session
from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.models.product import Product
from app.services.cart_service import get_cart


def create_order(user_id: int, db: Session):
    cart = get_cart(user_id, db)

    if not cart.items:
        raise ValueError("Cart is empty")

    order = Order(user_id=user_id, total_price=0)
    db.add(order)
    db.commit()
    db.refresh(order)

    total_price = 0

    for item in cart.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        # Deduct stock
        if product.stock < item.quantity:
            raise ValueError(f"Not enough stock for product {product.name}")

        product.stock -= item.quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)

        total_price += product.price * item.quantity

    order.total_price = total_price

    # Clear cart after order created
    db.query(type(cart)).filter_by(id=cart.id).delete()
    db.commit()

    db.refresh(order)

    return order


def list_user_orders(user_id: int, db: Session):
    return db.query(Order).filter(Order.user_id == user_id).all()
