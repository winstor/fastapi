import asyncio
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.api import deps
from app.core import security
from app import crud
from app.db import database
from app.core.cache import Cache

database.Base.metadata.create_all(bind=database.engine)

router = APIRouter()


# 长连接 监测scan扫码情况是否
@router.post("/token", response_model=Token)
async def get_token(
        db: Session = Depends(database.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    db_user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif crud.user.disabled(db_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return {
        "access_token": security.create_access_token(db_user.id),
        "token_type": "bearer",
    }


# 长连接 监测scan扫码情况是否
@router.get("/wechat_scan", response_model=Token)
async def get_token_by_scan(db: Session = Depends(database.get_db), scan: str = None):
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not Found scan",
        )
    for i in range(60):
        wx_openid = Cache.get(key=scan)
        if wx_openid:
            db_user = crud.user.get_by_wx_openid(db, wx_openid)
            if db_user:
                return {
                    "access_token": security.create_access_token(db_user.id),
                    "token_type": "bearer"
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Could not Found scan",
                )
        else:
            print("sleep" + str(i))
            await asyncio.sleep(1)
    raise HTTPException(
        status_code=status.HTTP_408_REQUEST_TIMEOUT,
        detail="request timeout",
    )


# 长连接 监测scan扫码情况是否
@router.get("/refresh", response_model=Token)
async def refresh_token(access_token: str = Depends(deps.refresh_access_token)):
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
