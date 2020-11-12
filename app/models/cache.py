from sqlalchemy import Boolean, Column, Integer, String, Text
from app.db.database import Base


# 用户表
class CacheModel(Base):
    __tablename__ = "caches"

    id = Column(String(100), primary_key=True, index=True, comment='主键')
    expire_at = Column(Integer, comment='到期时间')
    data = Column(Text, default='', comment='缓存数据')
