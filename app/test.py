from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

SQLALCHEMY_DATABASE_URL = "sqlite:///./app/db/sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# connect_args={"check_same_thread": False} ...仅适用于SQLite。其他数据库不需要它。

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session: Session = SessionLocal()

session.query()
session.refresh()
session.close()