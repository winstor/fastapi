from sqlalchemy import Column, Integer, String
from app.db.database import Base


# 用户表
class WechatTicketModel(Base):
    __tablename__ = "wechat_tickets"

    wx_openid = Column(String, comment='wx_openid')
    ticket = Column(String, unique=True, index=True, comment='ticket')
    create_time = Column(Integer, default=0, comment='添加时间')




