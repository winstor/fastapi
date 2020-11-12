from typing import Optional
from fastapi import Depends, APIRouter, Depends, HTTPException, status
from app.db import database
from pydantic import BaseModel
from app.api import deps
from app.models import UserModel
from app import crud, schemas
from sqlalchemy.orm import Session
from app.core import http_exception

database.Base.metadata.create_all(bind=database.engine)

router = APIRouter()


class Site(BaseModel):
    id: int
    name: Optional[str] = None
    secret: Optional[str] = None


@router.get("/")
async def get_user(
        db: Session = Depends(database.get_db),
        current_user: UserModel = Depends(deps.get_current_active_superuser)
):
    obj = crud.site.get_multi(db)
    return obj


@router.post("/add")
async def add(
        *,
        db: Session = Depends(database.get_db),
        site_in: schemas.SiteCreate,
        current_user: UserModel = Depends(deps.get_current_active_superuser)
):
    site = crud.site.get_by_name(db, name=site_in.name)
    if site:
        raise http_exception.repeat()
    site = crud.site.create(db, obj_in=site_in)
    return site
