from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models import UserModel
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[UserModel]:
        return db.query(self.model).filter(self.model.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[UserModel]:
        return db.query(self.model).filter(self.model.username == username).first()

    def get_by_wx_openid(self, db: Session, wx_openid: str) -> Optional[UserModel]:
        return db.query(self.model).filter(self.model.wx_openid == wx_openid).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> UserModel:
        db_user = UserModel(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def create_by_wechat(self, db: Session, wx_openid: str, name: str = None, avatar: str = None):
        db_user = self.model(wx_openid=wx_openid, name=name, avatar=avatar)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(
            self, db: Session, *, db_obj: UserModel, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[UserModel]:
        db_user = self.get_by_username(db, username=username)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user

    @staticmethod
    def disabled(db_user: UserModel) -> bool:
        return db_user.disabled

    @staticmethod
    def is_superuser(db_user: UserModel):
        return db_user.is_superuser


user = CRUDUser(UserModel)
