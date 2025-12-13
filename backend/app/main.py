from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.routes import (
    auth, products, cart, order, 
    payments, admin_products, 
    admin_categories, admin_orders
)
from app.api.v1.routes import password_reset
from app.api.v1.routes import email_verification

app = FastAPI(title="Ecommerce API")




app.include_router(
    email_verification.router,
    prefix="/api/v1/email-verification",
    tags=["Email Verification"]
)
app.include_router(
    password_reset.router,
    prefix="/api/v1/password-reset",
    tags=["Password Reset"]
)
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(cart.router, prefix="/api/v1/cart", tags=["Cart"])
app.include_router(order.router, prefix="/api/v1/order", tags=["Orders"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])
app.include_router(admin_products.router, prefix="/api/v1/admin/products", tags=["Admin Products"])
app.include_router(admin_categories.router, prefix="/api/v1/admin/categories", tags=["Admin Categories"])
app.include_router(admin_orders.router, prefix="/api/v1/admin/orders", tags=["Admin Orders"])




app.mount("/static", StaticFiles(directory="uploads"), name="static")


@app.get("/")
def root():
    return {"message": "Ecommerce backend is running!"}