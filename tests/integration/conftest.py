import pytest
import psycopg
from core.config import config
from sqlalchemy import create_engine


test_readonly_engine = create_engine(config.test_read_only_uri, echo=True, pool_pre_ping=True, pool_size=3)
test_readwrite_engine = create_engine(config.test_read_write_uri, echo=True, pool_pre_ping=True, pool_size=3)




@pytest.fixture(scope="session")
def admin_test_engine():
    admin_test_engine = create_engine(config.test_admin_uri, echo=True, pool_pre_ping=True, pool_size=3)
    yield admin_test_engine

@pytest.fixture(scope="session")
def readonly_test_engine():
    readonly_test_engine = create_engine(config.test_read_only_uri, echo=True, pool_pre_ping=True, pool_size=3)
    yield readonly_test_engine

@pytest.fixture(scope="session")
def readwrite_test_engine():
    readwrite_test_engine = create_engine(config.test_read_write_uri, echo=True, pool_pre_ping=True, pool_size=3)
    yield readwrite_test_engine

@pytest.fixture
def admin_db_connection():
    with psycopg.connect(config.test_admin_uri) as conn:
        try:
            yield conn
        finally:
            conn.rollback()

@pytest.fixture
def read_only_db_connection():
    with psycopg.connect(config.test_read_only_uri) as conn:
        try:
            yield conn
        finally:
            conn.rollback()

@pytest.fixture
def read_write_db_connection():
    with psycopg.connect(config.test_read_write_uri) as conn:
        try:
            yield conn
        finally:
            conn.rollback()