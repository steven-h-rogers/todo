# TODO: initialize database related things and don't add database logic here

from sqlalchemy import create_engine
from core.config import config

engine = create_engine(config.prod_read_only_uri, echo=True, pool_pre_ping=True)