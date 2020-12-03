from typing import Optional

from pydantic import BaseModel, EmailStr, validator
from datetime import datetime


class UserBase(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None
    site_id: Optional[int] = 0
    disabled: Optional[bool] = False
    is_mgmt: Optional[bool] = False
    is_root: Optional[bool] = False


class UserUpdate(UserBase):
    password: str
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None
    site_id: Optional[int] = 0
    disabled: Optional[bool] = False
    is_mgmt: Optional[bool] = False
    is_root: Optional[bool] = False


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    disabled: bool

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserOut(UserInDBBase):
    site_id: int
    is_root: bool
    is_mgmt: bool
    name: Optional[str] = None
    username: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    wx_openid: Optional[str] = None
    created_at: Optional[datetime] = None
    avatar: Optional[str] = None

    @validator('created_at')
    def create_time_format(cls, v: Optional[datetime] = None):
        if v:
            return v.strftime("%Y-%m-%d %H:%M:%S")
        return ''
