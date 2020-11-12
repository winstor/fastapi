from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None


class UserCreate(UserBase):
    username: str
    mobile: str
    password: str


class UserUpdate(UserBase):
    username: str
    name: str
    mobile: str
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    disabled: int

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


