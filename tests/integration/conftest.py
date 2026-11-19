import pytest
import psycopg
from core.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
# from models.db import Base


test_readonly_engine = create_engine(config.test_read_only_uri, echo=True, pool_pre_ping=True, pool_size=3)
test_readwrite_engine = create_engine(config.test_read_write_uri, echo=True, pool_pre_ping=True, pool_size=3)



# ENGINES
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

# SESSIONS
@pytest.fixture(scope="function")
def admin_session(admin_test_engine):
    with Session(admin_test_engine) as session:
        yield session
        session.rollback()

@pytest.fixture(scope="function")
def readonly_session(readonly_test_engine):
    with Session(readonly_test_engine) as session:
        yield session
        session.rollback()

@pytest.fixture(scope="function")
def readwrite_session(readwrite_test_engine):
    with Session(readwrite_test_engine) as session:
        yield session
        session.rollback()






# psycopg fixtures

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