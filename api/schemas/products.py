from pydantic import BaseModel, EmailStr
from typing import Optional

class ProductIn(BaseModel):
    product_name: str
    product_category: str
    product_description: str
    product_price: float

    class Config:
        orm_mode = True

class ProductOut(BaseModel):
    product_id: int
    user_id: Optional[int]
    product_name: str
    product_category: str
    product_description: str
    product_price: float
    class Config:
        orm_mode = True