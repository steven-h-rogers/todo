import pytest
import psycopg
from core.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.users import Users
from models.task import Task
from models.task_group import TaskGroup
# from models.db import Base

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

# SEEDS FOR TESTING PRIVILEGE

# Use when pre-existing data is needed
@pytest.fixture(scope="function")
def seeded_user(readwrite_session):
    user = Users(usr_name="seeded_username", pwd_hash="seeded_hash123!@#", email="seed@test.com")
    readwrite_session.add(user)
    readwrite_session.commit()
    readwrite_session.refresh(user)

    yield user

    readwrite_session.delete(user)
    readwrite_session.commit()




# PSYCOPG

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