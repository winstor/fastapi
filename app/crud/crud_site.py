from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models import SiteModel
from app.schemas import SiteCreate, SiteUpdate
import uuid


class CRUDSite(CRUDBase[SiteModel, SiteCreate, SiteUpdate]):

    def get_by_name(self, db: Session, *, name: str) -> Optional[SiteModel]:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_by_secret(self, db: Session, *, secret: str) -> Optional[SiteModel]:
        return db.query(self.model).filter(self.model.secret == secret).first()

    def create(self, db: Session, *, obj_in: SiteCreate) -> SiteModel:
        db_site = SiteModel(
            name=obj_in.name,
            secret=str(uuid.uuid1())
        )
        db.add(db_site)
        db.commit()
        db.refresh(db_site)
        return db_site

    def update(
            self, db: Session, *, db_obj: SiteModel, obj_in: Union[SiteUpdate, Dict[str, Any]]
    ) -> SiteModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


site = CRUDSite(SiteModel)
