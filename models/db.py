"""This file is so that each mapping has context of the other tables in the database"""
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass