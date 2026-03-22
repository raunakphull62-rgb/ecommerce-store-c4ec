from sqlalchemy import Column, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from typing import List

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)

    orders = relationship("OrderProduct", back_populates="product")

    def __init__(self, id: str, name: str, price: float, description: str = None):
        self.id = id
        self.name = name
        self.price = price
        self.description = description

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price}, description={self.description})"


class OrderProduct(Base):
    __tablename__ = "orders_products"

    order_id = Column(String, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), primary_key=True)

    order = relationship("Order", back_populates="products")
    product = relationship("Product", back_populates="orders")

    def __init__(self, order_id: str, product_id: str):
        self.order_id = order_id
        self.product_id = product_id

    def __repr__(self):
        return f"OrderProduct(order_id={self.order_id}, product_id={self.product_id})"