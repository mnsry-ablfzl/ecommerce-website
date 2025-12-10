import stripe
from app.core.config import settings
from sqlalchemy.orm import Session
from app.db.models.payment import Payment
from app.db.models.order import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_session(order_id: int, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None

    # Save payment in DB
    payment = Payment(
        order_id=order_id,
        amount=order.total_price,
        status="pending"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    # Create Stripe Payment Intent
    intent = stripe.PaymentIntent.create(
        amount=int(order.total_price * 100),  # Stripe uses cents
        currency="usd",
        metadata={"order_id": order_id}
    )

    payment.stripe_payment_intent = intent["id"]
    db.commit()

    return {
        "client_secret": intent["client_secret"],
        "payment_id": payment.id
    }


def confirm_payment(payment_intent_id: str, db: Session):
    payment = db.query(Payment).filter(
        Payment.stripe_payment_intent == payment_intent_id
    ).first()

    if not payment:
        return None

    payment.status = "paid"
    payment.order.status = "paid"

    db.commit()
    return payment
