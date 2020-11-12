from typing import Optional

from pydantic import BaseModel


# Shared properties
class SiteBase(BaseModel):
    name: str


class SiteCreate(SiteBase):
    pass


class SiteUpdate(SiteBase):
    pass


# Properties shared by models stored in DB
class SiteInDBBase(SiteBase):
    id: int

    class Config:
        orm_mode = True


class Site(SiteInDBBase):
    pass


