from fastapi import Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from app import crud
from app.db import database
from app.models import UserModel
from app.core import security
from fastapi.security import OAuth2PasswordBearer
from app.core import http_exception

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/token"
)


def get_current_user(
        db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)
) -> UserModel:
    sub = security.jwt_decode(token)
    current_user = crud.user.get(db=db, id=sub)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    if crud.user.disabled(current_user):
        raise HTTPException(status_code=404, detail="User not found")
    return current_user


def get_current_active_user(
        current_user: UserModel = Depends(get_current_user)
) -> UserModel:
    if crud.user.disabled(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
        current_user: UserModel = Depends(get_current_user)
) -> UserModel:
    if not crud.user.is_superuser(current_user):
        raise http_exception.unauthorized()
    return current_user


def refresh_access_token(
        current_user: UserModel = Depends(get_current_user)
) -> str:
    token = security.create_access_token(current_user.id)
    return token
