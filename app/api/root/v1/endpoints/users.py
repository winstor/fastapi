from typing import Optional, List, Any
from fastapi import Depends, APIRouter, Depends, HTTPException
from app.db import database
from sqlalchemy.orm import Session
from app.api.root import common
from app.models import UserModel
from app.api.root import crud
from app.api.root import schemas

router = APIRouter()


# from app.api.middleware.check_token import CheckTokenHandler
# router.route_class = CheckTokenHandler


class UserOut(schemas.UserOut):
    is_root: bool


# @router.get("/", response_model=List[UserOut])
@router.get("/", response_model=List[UserOut])
async def read_users(
        db: Session = Depends(database.get_db),
        skip: int = 0,
        limit: int = 100
):
    users = crud.userCrud.get_multi(db=db, skip=skip, limit=limit)
    return users


@router.post("/")
async def create_user(
        *,
        db: Session = Depends(database.get_db),
        obj_in: schemas.UserCreate
):
    site = crud.userCrud.create(db, obj_in=obj_in)
    return site


@router.get("/{id}", response_model=UserOut)
async def read_users(
        *,
        db: Session = Depends(database.get_db),
        id: int
):
    users = crud.userCrud.get(db=db, id=id)
    return users


# 我的信息
@router.get("/user_info", response_model=UserOut)
async def get_user_detail(current_user: UserModel = Depends(common.get_current_user)):
    return current_user
