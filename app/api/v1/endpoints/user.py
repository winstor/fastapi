from typing import Optional
from fastapi import Depends, APIRouter, Depends, HTTPException
from app.db import database
from pydantic import BaseModel
from app.api import deps
from app.models import UserModel

database.Base.metadata.create_all(bind=database.engine)

router = APIRouter()


class User(BaseModel):
    id: int
    username: Optional[str] = None
    name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None


# 长连接 监测scan扫码情况是否
@router.get("/", response_model=User)
async def get_user(current_user: UserModel = Depends(deps.get_current_active_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "name": current_user.name,
        "mobile": current_user.mobile,
        "email": current_user.email,
        "avatar": current_user.avatar,
        "disabled": current_user.disabled
    }
