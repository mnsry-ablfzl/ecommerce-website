from fastapi import FastAPI
from app.api.v1.routes import auth

app = FastAPI(title="Ecommerce API")


app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])



@app.get("/")
def root():
    return {"message": "Ecommerce backend is running!"}