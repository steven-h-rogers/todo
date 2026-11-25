from sqlalchemy import create_engine, text
from core.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from collections.abc import Generator
from typing import Annotated
from fastapi import Depends

admin_engine = create_engine(config.prod_admin_uri, echo=True, pool_pre_ping=True, pool_size=3)
readwrite_engine = create_engine(config.prod_read_write_uri, echo=True, pool_pre_ping=True, pool_size=3)
readonly_engine = create_engine(config.prod_read_only_uri, echo=True, pool_pre_ping=True, pool_size=3)

AdminSessionLocal = sessionmaker(bind=admin_engine, autoflush=False, expire_on_commit=False)
ReadWriteSessionLocal = sessionmaker(bind=readwrite_engine, autoflush=False, expire_on_commit=False)
ReadOnlySessionLocal = sessionmaker(bind=readonly_engine, autoflush=False, expire_on_commit=False)

def get_admin_db() -> Generator[Session, None, None]:
    with AdminSessionLocal() as session:
        yield session

def get_readwrite_db() -> Generator[Session, None, None]:
    with ReadWriteSessionLocal() as session:
        yield session

def get_readonly_db() -> Generator[Session, None, None]:
    with ReadOnlySessionLocal as session:
        yield session

AdminDB = Annotated[Session, Depends(get_admin_db)]
ReadWriteDB = Annotated[Session, Depends(get_readwrite_db)]
ReadOnlyDB = Annotated[Session, Depends(get_readonly_db)]






