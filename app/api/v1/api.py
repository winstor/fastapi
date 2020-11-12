from fastapi import APIRouter

from .endpoints import wechat, user, login, site

# from .auth import token

api_router = APIRouter()

# endpoints 登录

api_router.include_router(login.router,  tags=["login"])
api_router.include_router(wechat.router, prefix="/wechat", tags=["wechat"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(site.router, prefix="/sites", tags=["sites"])


# user 信息
# router.include_router(users.router, prefix="/users", tags=["users"])
