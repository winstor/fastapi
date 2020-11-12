import json
from fastapi import Depends, APIRouter, Body, Depends, HTTPException
from app.db import database
from wechatpy import WeChatClient
from app.config import wechat
from pydantic import BaseModel

database.Base.metadata.create_all(bind=database.engine)

router = APIRouter()


class Qrcode(BaseModel):
    url: str
    expire_at: int


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 获取微信公众号临时二维码 用于登录、注册
@router.get("/qrcode", response_model=Qrcode)
async def get_qrcode():
    client = WeChatClient(wechat.app_id, wechat.secret)
    expire_seconds = 1800
    res = client.qrcode.create({
        # 有效时间秒
        'expire_seconds': expire_seconds,
        'action_name': 'QR_LIMIT_STR_SCENE',
        'action_info': {
            'scene': {'scene_str': "register_or_login"},
        }
    })
    #  数值需测试
    res = json.loads(res)
    url = client.qrcode.get_url(res['ticket'])
    return {"url": url, "expire_at": expire_seconds}
