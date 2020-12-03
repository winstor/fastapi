from app.api.deps import *


# 添加超级管理员
def add_root_user(db: Session = Depends(database.get_db)):
    hashed_password = security.get_password_hash("root")
    data = {
        "id": 1,
        "site_id": 0,
        "username": "root",
        "hashed_password": hashed_password,
        "name": "root",
        "is_root": True,
    }
    db_user = crud.user.get(db, 1)
    if not db_user:
        db_user = UserModel(**data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user
