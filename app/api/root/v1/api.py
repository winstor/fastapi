from fastapi import APIRouter, Depends
from .endpoints import users, login, sites
from app.api.root import common

api_router = APIRouter()

# endpoints 登录
api_router.include_router(
    login.router,
    tags=["登录管理"],
)
# 用户
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["用户管理"],
    dependencies=[Depends(common.get_current_root)]
)

# 站点
api_router.include_router(
    sites.router,
    prefix="/sites",
    tags=["站点管理"],
    dependencies=[Depends(common.get_current_root)]
)
