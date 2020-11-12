import time
import json
from app.db.database import session
from app.models.cache import CacheModel


class Cache:
    @staticmethod
    def get(key: str):
        res = session.query(CacheModel).filter(CacheModel.id == key).first()
        if res:
            now = int(time.time())
            if now < res.expire_at:
                return json.loads(res.data)
            else:
                session.query(CacheModel).filter(CacheModel.expire_at < now).delete()
        return False

    @staticmethod
    def put(key: str, value, minute: int):
        session.query(CacheModel).filter(CacheModel.id == key).delete()
        if value:
            expire_at = int(time.time()) + int(minute) * 60
            data = json.dumps(value)
            db_cache = CacheModel(id=key, data=data, expire_at=expire_at)
            session.add(db_cache)
            session.commit()
            session.refresh(db_cache)
            session.close()
