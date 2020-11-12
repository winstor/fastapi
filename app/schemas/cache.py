from pydantic import BaseModel


# Shared properties
class CacheBase(BaseModel):
    id: str
    data: str
    expire_at: str


class CacheCreate(CacheBase):
    id: str
    data: str
    expire_at: int


class Cache(CacheBase):

    class Config:
        orm_mode = True

