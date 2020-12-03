from typing import List
from fastapi import Depends, APIRouter, Depends, HTTPException
from app.db import database
from app.api.middleware.check_token import CheckTokenHandler
from app import crud
from sqlalchemy.orm import Session
from app import schemas

#
router = APIRouter()
# router.route_class = CheckTokenHandler


@router.get("/", response_model=List[schemas.Site])
async def read_sites(
        db: Session = Depends(database.get_db),
        skip: int = 0,
        limit: int = 100,
):
    sites = crud.site.get_multi(db, skip=skip, limit=limit)
    return sites


@router.get("/{id}", response_model=schemas.Site)
async def read_site(
        *,
        db: Session = Depends(database.get_db),
        id: int
):
    site = crud.site.get(db=db, id=id)
    return site


# @router.post("/", response_model=schemas.Site)
@router.post("/")
async def create_site(
        *,
        db: Session = Depends(database.get_db),
        obj_in: schemas.SiteCreate
):
    site = crud.site.create(db, obj_in=obj_in)
    return site


@router.put("/{id}", response_model=schemas.Site)
async def update_site(
        *,
        db: Session = Depends(database.get_db),
        id: int,
        obj_in: schemas.SiteUpdate
):
    site = crud.site.get(db=db, id=id)
    if not site:
        raise HTTPException(status_code=400, detail="not Found")
    site = crud.site.update(db=db, db_obj=site, obj_in=obj_in)
    return site


@router.delete("/{id}", response_model=schemas.Site)
async def delete_site(
        *,
        db: Session = Depends(database.get_db),
        id: int
):
    site = crud.site.remove(db=db, id=id)
    return site
