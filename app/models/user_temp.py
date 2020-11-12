from sqlalchemy import Boolean, Column, Integer, String, Text, Enum
from app.db.database import Base
import uuid


def gen_id():
    return uuid.uuid4().hex


# 作用域 临时权限
# 指派类型 1，地址指派，2地址+密码指派，3，地址+关联账号指派，4
class UserTempModel(Base):
    __tablename__ = "user_temps"

    id = Column(String, default=gen_id, primary_key=True, index=True, comment='主键')
    user_id = Column(Integer, index=True, comment='指派人ID')
    title = Column(String, nullable=True, comment='标题')
    scopes = Column(Text, comment='作用域,权限')
    hashed_password = Column(String, nullable=True, comment='hash密码')
    secret = Column(String, nullable=True, comment='密钥,被指派人提供')
    type = Column(Enum('password', 'secret', 3), nullable=True, comment='指派类型')
    token = Column(String, nullable=True, comment='登录生成token')
    expire = Column(Integer, comment='到期时间')
    disabled = Column(Boolean, default=False, comment='是否禁用')
