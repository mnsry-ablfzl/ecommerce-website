from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    total_price = Column(Float, default=0)
    status = Column(String, default="pending")  # pending, paid, shipped, delivered, cancelled

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
