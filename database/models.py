from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, ForeignKey, 
    Date, String,
    Text, Column, Float
)
from sqlalchemy.orm import relationship

Base = declarative_base()

def generate_date() -> object:
    from datetime import date
    return date.today()


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    user_email = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    user_phone = Column(String, nullable=False)
    profile_pic_url = Column(String, nullable=True)
    date_created = Column(Date, default=generate_date)

    products = relationship("Product", back_populates="user")


class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    product_name = Column(String, nullable=False)
    product_category = Column(String, nullable=False)
    product_description = Column(Text, nullable=False)
    product_price = Column(Float, default=0.0)
    date_created = Column(Date, default=generate_date)

    images = relationship("ProductImage", back_populates="product")
    user = relationship("User", back_populates="products")


class ProductImage(Base):
    __tablename__ = "product_images"
    image_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    image_url = Column(String, nullable=False)
    date_created = Column(Date, default=generate_date)

    product = relationship("Product", back_populates="images")
