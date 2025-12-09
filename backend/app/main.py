from fastapi import FastAPI
from app.api.v1.routes import auth, products

app = FastAPI(title="Ecommerce API")


app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])



@app.get("/")
def root():
    return {"message": "Ecommerce backend is running!"}