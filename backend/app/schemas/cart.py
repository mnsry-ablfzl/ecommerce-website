from pydantic import BaseModel
from typing import List
from app.schemas.products import ProductResponse


class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(BaseModel):
    id: int
    quantity: int
    product: ProductResponse

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    items: List[CartItemResponse]

    class Config:
        from_attributes = True
