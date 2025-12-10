from pydantic import BaseModel
from typing import List
from app.schemas.products import ProductResponse


class OrderItemResponse(BaseModel):
    id: int
    product: ProductResponse
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
