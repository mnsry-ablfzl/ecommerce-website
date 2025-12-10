from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from app.services.payment_service import create_payment_session, confirm_payment
from app.core.config import settings
import stripe

router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/create-session/{order_id}")
def create_session(order_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    session = create_payment_session(order_id, db)
    if not session:
        raise HTTPException(status_code=404, detail="Order not found")
    return session


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    signature = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    if event["type"] == "payment_intent.succeeded":
        payment_intent_id = event["data"]["object"]["id"]
        confirm_payment(payment_intent_id, db)

    return {"status": "success"}
