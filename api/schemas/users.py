from pydantic import BaseModel, EmailStr
from typing import Optional

class UserIn(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: str
    user_phone: str
    profile_pic_url: Optional[str] = None

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    user_phone: str
    profile_pic_url: Optional[str] = None

    class Config:
        orm_mode = True
    
class UserLogin(BaseModel):
    user_name: str
    user_password: str
