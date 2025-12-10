from pydantic import BaseModel
from typing import List
from app.schemas.product import ProductResponse


class OrderItemResponse(BaseModel):
    id: int
    product: ProductResponse
    quantity: int
    price: float

    class Config:
        orm_mode = True


class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True
