from fastapi import FastAPI
from app.api.v1.routes import auth, products, cart

app = FastAPI(title="Ecommerce API")


app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(cart.router, prefix="/api/v1/cart", tags=["Cart"])



@app.get("/")
def root():
    return {"message": "Ecommerce backend is running!"}