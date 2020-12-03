from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.api.root import common
from app.core import security
from app import crud
from app.db import database
from app.models import UserModel

router = APIRouter()


def response_token(access_token: str):
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# # 生成root用户
# @router.post("/register", response_model=Token)
# async def register(
#         db_user=Depends(common.add_root_user),
# ):
#     access_token = security.create_access_token({"sub": db_user.id})
#     return response_token(access_token)


@router.post("/login/access-token")
async def login_access_token(
        db: Session = Depends(database.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    db_user = crud.user.authenticate(
        db, site_id=0, username=form_data.username, password=form_data.password
    )
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif crud.user.disabled(db_user):
        # 已禁用
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not crud.user.is_root(db_user):
        # 不是root超级账号
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")
    data = {"sub": str(db_user.id), "site_id": 0, "scopes": 'root'}
    access_token = security.create_access_token(data)
    return response_token(access_token)


# 刷新token
@router.get("/refresh", response_model=Token)
async def refresh_token(
        current_user: UserModel = Depends(common.get_current_root),
        token: str = Depends(common.oauth2_scheme)
):
    access_token = security.create_access_token({"sub": current_user.id})
    return response_token(access_token)
