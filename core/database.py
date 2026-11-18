# TODO: initialize database related things and don't add database logic here

from sqlalchemy import create_engine, text
from core.config import config

admin_engine = create_engine(config.prod_admin_uri, echo=True, pool_pre_ping=True, pool_size=3)
readonly_engine = create_engine(config.prod_read_only_uri, echo=True, pool_pre_ping=True, pool_size=3)
readwrite_engine = create_engine(config.prod_read_write_uri, echo=True, pool_pre_ping=True, pool_size=3)
