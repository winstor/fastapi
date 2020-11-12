from sqlalchemy import Boolean, Column, Integer, String
from app.db.database import Base


# 用户表
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment='主键')
    username = Column(String, unique=True, nullable=True, index=True, comment='用户名')
    name = Column(String(50), nullable=True, comment='姓名')
    avatar = Column(String, nullable=True, comment='头像')
    mobile = Column(String(11), nullable=True, comment='电话')
    email = Column(String, nullable=True, comment='邮箱')
    disabled = Column(Boolean, default=False, comment='是否禁用')
    hashed_password = Column(String, nullable=True, comment='hash密码')
    wx_openid = Column(String(64), unique=True, index=True, nullable=True, comment='微信openid')
    site_id = Column(Integer, default=0, index=True, comment='应用ID')
    is_superuser = Column(Boolean, default=False, comment='超级用户')

