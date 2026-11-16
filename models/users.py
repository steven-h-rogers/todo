# TODO: use sqlalchemy to model the users table

import uuid
from sqlalchemy import Table, Column, Integer, String, UUID, Uuid, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"
    usr_id : Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.uuidv7(monotonoic=True))
    usr_name : Mapped[str] = mapped_column(Text, nullable=False)
    pwd_hash : Mapped[str] = mapped_column(Text, nullable=False)
    email : Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    created_at : Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now()) 

    __table_args__ = (None) # TODO: add table constraints here and add constraint names in the database