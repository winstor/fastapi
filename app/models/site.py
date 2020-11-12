from sqlalchemy import Boolean, Column, Integer, String
from app.db.database import Base


# 站点 比如 郑州芝麻、郑州大学、中原大学
class SiteModel(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    name = Column(String, unique=True, index=True, comment='名称')
    secret = Column(String, unique=True, index=True, comment='密钥')
