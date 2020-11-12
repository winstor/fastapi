from datetime import datetime, timedelta
from typing import List, Optional, Any, Union

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from app.db.database import session
from app.models.user import User
from sqlalchemy import or_
import json

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)


class JwtAuth:
    # 获取用户信息
    @staticmethod
    def user(token: str = Depends(oauth2_scheme)) -> User:
        authenticate_value = f"Bearer"
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
        try:
            user_id: int = JwtAuth.token_decode(token)
            if user_id is None:
                raise credentials_exception
        except (JWTError, ValidationError):
            raise credentials_exception
        user = session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user

    # 解码token
    @staticmethod
    def decode(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            sub: str = payload.get("sub")
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        return json.loads(sub)

    # 生成token
    @staticmethod
    def encode(sub: str, expires_delta: Optional[timedelta] = None):
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": sub, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    # user_id 创建token
    @staticmethod
    def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None):
        encoded_jwt = JwtAuth.token_encode(subject, expires_delta)
        return encoded_jwt

    # user 创建token
    @staticmethod
    def from_user(user: User, scopes: list = [], expires_delta: Optional[timedelta] = None):
        encoded_jwt = JwtAuth.token_encode(user.id, scopes, expires_delta)
        return encoded_jwt

    # 刷新token
    @staticmethod
    def refresh_token(token: str = Depends(oauth2_scheme)):
        authenticate_value = f"Bearer"
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
        try:
            user: User = JwtAuth.user(token)
            if user is None:
                raise credentials_exception
        except (JWTError, ValidationError):
            raise credentials_exception
        encoded_jwt = JwtAuth.from_user(user)
        return encoded_jwt
