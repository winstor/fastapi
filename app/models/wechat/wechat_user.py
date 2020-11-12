from sqlalchemy import Boolean, Column, Integer, String
from app.db.database import Base


# 用户表
class WechatUserModel(Base):
    __tablename__ = "wechat_users"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    app_id = Column(String(100), index=True, comment='用户公众平台唯一标识')
    wechat_id = Column(Integer,  default=0, comment='')
    subscribe = Column(Boolean, default=False, nullable=False, comment='用户是否订阅该公众号标识')
    openid = Column(String(100), index=True, comment='用户公众平台唯一标识')
    nickname = Column(String, nullable=True, comment='用户昵称')
    sex = Column(Integer, default=0, comment='性别')
    city = Column(String, nullable=True, default='', comment='用户所在城市')
    country = Column(String, nullable=True, comment='用户所在国家')
    province = Column(String, nullable=True, comment='用户所在省份')
    language = Column(String, nullable=True, comment='用户的语言')
    headimgurl = Column(String, nullable=True, comment='用户头像')
    subscribe_time = Column(Integer, default=0, comment='用户关注时间')
    ticket = Column(String, nullable=True, default='', comment='注册登录的时候使用')



