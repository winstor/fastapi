from fastapi import FastAPI
from app.wechat import wechat_router
from app.api.v1.api import api_router as v1_api_router

app = FastAPI()


@app.get("/")
async def root():
    return "郑州芝麻知识产权代理有限公司欢迎您！"


# 微信服务端
app.include_router(wechat_router)
# api版本v1
app.include_router(v1_api_router, prefix='/api/v1')

'''
运行 命令
uvicorn app.main:app --reload

'''
