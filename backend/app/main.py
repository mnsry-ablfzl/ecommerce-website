from fastapi import FastAPI
from app.api.v1.routes import auth, products, cart, order, payments

app = FastAPI(title="Ecommerce API")


app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(cart.router, prefix="/api/v1/cart", tags=["Cart"])
app.include_router(order.router, prefix="/api/v1/order", tags=["Orders"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])



@app.get("/")
def root():
    return {"message": "Ecommerce backend is running!"}